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
        self._translation_cache = None
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
            'get_translation_with_params': self.get_translation_with_params,
            'current_language': self.get_current_language,
            'available_languages': self.get_available_languages
        }

    def get_current_language(self):
        """Get the current language code"""
        return getattr(g, 'current_language', 'en-US')

    def get_available_languages(self):
        """Get all available languages"""
        return Language.query.filter_by(is_active=True).all()

    def get_translation(self, key, language_code=None):
        """
        Get translation for a given key
        Uses caching for better performance
        """
        # Initialize cache if not exists
        if self._translation_cache is None:
            self._translation_cache = lru_cache(maxsize=1000)(self._get_translation_uncached)

        return self._translation_cache(key, language_code)

    def _get_translation_uncached(self, key, language_code=None):
        """Uncached version of translation lookup"""
        if language_code is None:
            # Get language directly from session to avoid caching issues
            language_code = session.get('language', 'en-US')

        # Try to get from database
        translation = Translation.query.filter_by(
            key=key,
            language_code=language_code
        ).first()

        if translation:
            return translation.value

        # Fallback to English if not current language
        if language_code != 'en-US':
            return self._get_translation_uncached(key, 'en-US')

        # Return key as fallback if no translation found
        return key

    def set_language(self, language_code):
        """Set the user's preferred language"""
        # Validate language exists
        language = Language.query.filter_by(code=language_code, is_active=True).first()
        if not language:
            raise ValueError(f"Language {language_code} not available")

        session['language'] = language_code

        # Clear translation cache when language changes
        if self._translation_cache is not None:
            self._translation_cache.cache_clear()

        return True

    def get_translation_with_params(self, key, params=None, language_code=None):
        """
        Get translation for a given key with parameter replacement
        Supports dynamic values like {username}, {device_name}, etc.
        """
        if params is None:
            params = {}

        translation = self.get_translation(key, language_code)

        # Replace placeholders with actual values
        if params:
            for placeholder, value in params.items():
                translation = translation.replace('{' + placeholder + '}', str(value))

        return translation

# Create instance
translation_service = TranslationService()
