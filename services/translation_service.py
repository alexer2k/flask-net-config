"""
Translation Service for multi-language support
Handles language detection, translation lookup, and caching
"""

from flask import request, session, g
from models import Language, Translation
from functools import lru_cache
import logging

class TranslationService:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the translation service with Flask app"""
        self.app = app
        self.logger = logging.getLogger(__name__)

        # Set up request processing
        app.before_request(self._before_request)
        app.context_processor(self._context_processor)

    def _before_request(self):
        """Set up translation context before each request"""
        # Get language from session, cookie, or default
        language_code = session.get('language', 'en-US')
        g.current_language = language_code

    def _context_processor(self):
        """Make translation functions available in templates"""
        return {
            'get_translation': self.get_translation,
            'current_language': self.get_current_language,
            'available_languages': self.get_available_languages
        }

    def get_current_language(self):
        """Get the current language code"""
        return getattr(g, 'current_language', 'en-US')

    def get_available_languages(self):
        """Get all available languages"""
        return Language.query.filter_by(is_active=True).all()

    @lru_cache(maxsize=1000)
    def get_translation(self, key, language_code=None):
        """
        Get translation for a given key
        Uses caching for better performance
        """
        if language_code is None:
            language_code = self.get_current_language()

        # Try to get from database
        translation = Translation.query.filter_by(
            key=key,
            language_code=language_code
        ).first()

        if translation:
            return translation.value

        # Fallback to English if not current language
        if language_code != 'en-US':
            return self.get_translation(key, 'en-US')

        # Return key as fallback if no translation found
        return key

    def set_language(self, language_code):
        """Set the user's preferred language"""
        # Validate language exists
        language = Language.query.filter_by(code=language_code, is_active=True).first()
        if not language:
            raise ValueError(f"Language {language_code} not available")

        session['language'] = language_code
        return True

# Create instance
translation_service = TranslationService()
