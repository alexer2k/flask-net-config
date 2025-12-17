import re
from netmiko import ConnectHandler

class CiscoVGDriver:
    def __init__(self, device_db_obj):
        self.device = {
            'device_type': 'cisco_ios_telnet',
            'host': device_db_obj.ip_address,
            'username': device_db_obj.username,
            'password': device_db_obj.password,
            'secret': device_db_obj.enable_password, 
            'port': device_db_obj.port,
            'fast_cli': False, # Uncomment if older router is too slow/glitchy
        }

    def get_diversions(self):
        """
        Robustly parses configuration to find ONLY 'voice translation-rule 2'.
        It ignores 'voice translation-rule 255' or others.
        """
        try:
            with ConnectHandler(**self.device) as net_connect:
                net_connect.enable()
                # We fetch a slightly broader section to ensure we get context,
                # but we will filter it strictly in Python.
                output = net_connect.send_command("show run | section voice translation-rule")
                
            rules = []
            
            # --- State Machine Parsing ---
            in_target_block = False
            
            # Regex to parse the specific rule line:
            # rule 1 /^677250412/ /970202/ plan any unknown
            rule_pattern = re.compile(r"rule\s+(\d+)\s+/(.*?)/\s+/(.*?)/")

            for line in output.splitlines():
                line = line.strip()

                # 1. Check if we are entering the specific block we want
                if line == "voice translation-rule 2":
                    in_target_block = True
                    continue # Move to next line

                # 2. Check if we are hitting a different block (e.g., rule 255)
                # If we see any other "voice translation-rule X", stop capturing
                if line.startswith("voice translation-rule") and line != "voice translation-rule 2":
                    in_target_block = False
                    continue

                # 3. Check for the end of a section (usually '!' or a global command)
                if line.startswith("!"):
                    in_target_block = False
                    continue

                # 4. If we are inside the correct block, parse the rules
                if in_target_block and line.startswith("rule"):
                    match = rule_pattern.search(line)
                    if match:
                        rules.append({
                            'id': match.group(1),
                            'source': match.group(2).replace('^', ''), 
                            'destination': match.group(3),
                            'raw_source': match.group(2) 
                        })
            
            return rules

        except Exception as e:
            # Log the error to console for debugging
            print(f"Driver Error: {e}")
            raise Exception(f"Connection Error: {str(e)}")

    def update_diversion(self, rule_id, raw_source, new_destination):
        """
        Executes the config change sequence.
        """
        # Security safety: Ensure raw_source doesn't contain newlines/config injection
        if "\n" in raw_source or "\r" in raw_source:
            raise Exception("Invalid characters in source pattern")

        command_line = f"rule {rule_id} /{raw_source}/ /{new_destination}/ plan any unknown"
        
        config_set = [
            "voice translation-rule 2",
            command_line,
            "exit",
            "exit"
        ]
        
        try:
            with ConnectHandler(**self.device) as net_connect:
                net_connect.enable()
                output = net_connect.send_config_set(config_set)
                net_connect.save_config()
            return output
        except Exception as e:
            raise Exception(f"Configuration Error: {str(e)}")