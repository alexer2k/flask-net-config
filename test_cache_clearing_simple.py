#!/usr/bin/env python3
"""
Simple test to verify that the translation cache is properly cleared when language changes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from services.translation_service import translation_service
from models import db, Language, Translation
from app import app

def test_cache_clearing():
    """Test that cache is cleared when language changes"""

    with app.app_context():
        # Set up test data
        db.create_all()

        # Add test languages
        if not Language.query.filter_by(code='en-US').first():
            en_lang = Language(code='en-US', name='English (US)', is_active=True)
            db.session.add(en_lang)

        if not Language.query.filter_by(code='it-IT').first():
            it_lang = Language(code='it-IT', name='Italian (IT)', is_active=True)
            db.session.add(it_lang)

        # Add test translations
        if not Translation.query.filter_by(key='test_key', language_code='en-US').first():
            en_trans = Translation(key='test_key', language_code='en-US', value='Hello World')
            db.session.add(en_trans)

        if not Translation.query.filter_by(key='test_key', language_code='it-IT').first():
            it_trans = Translation(key='test_key', language_code='it-IT', value='Ciao Mondo')
            db.session.add(it_trans)

        db.session.commit()

        print("Test data set up successfully")

        # Test the cache clearing functionality
        print("\nTesting cache clearing...")

        # Create a test client to get request context
        with app.test_request_context('/'):
            # Set language to English
            translation_service.set_language('en-US')
            translation1 = translation_service.get_translation('test_key')
            print(f"English translation: {translation1}")

            # Set language to Italian - this should clear the cache
            translation_service.set_language('it-IT')
            translation2 = translation_service.get_translation('test_key')
            print(f"Italian translation: {translation2}")

            # Set language back to English - this should clear the cache again
            translation_service.set_language('en-US')
            translation3 = translation_service.get_translation('test_key')
            print(f"English translation again: {translation3}")

        # Verify we get the correct translations
        assert translation1 == 'Hello World', f"Expected 'Hello World', got '{translation1}'"
        assert translation2 == 'Ciao Mondo', f"Expected 'Ciao Mondo', got '{translation2}'"
        assert translation3 == 'Hello World', f"Expected 'Hello World', got '{translation3}'"

        print("\n✅ All tests passed! Cache clearing is working correctly.")

if __name__ == '__main__':
    test_cache_clearing()
