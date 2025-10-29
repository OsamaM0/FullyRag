import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

display_texts_json_path = os.getenv("DISPLAY_TEXTS_JSON_PATH", "display_texts.json")


class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = DotDict(v)
            elif isinstance(v, list):
                self[k] = [DotDict(i) if isinstance(i, dict) else i for i in v]


class MultiLanguageTexts:
    """Multi-language support for display texts"""

    AVAILABLE_LANGUAGES = {"en": "English", "ar": "العربية"}

    # Language code mapping from .env LANGUAGE variable to ISO codes
    LANGUAGE_CODE_MAPPING = {"english": "en", "arabic": "ar", "en": "en", "ar": "ar"}

    def __init__(self, base_path: str, default_language: str = "en"):
        self.base_path = Path(base_path)

        # Check .env for default language
        env_language = os.getenv("LANGUAGE", "english").lower()
        mapped_language = self.LANGUAGE_CODE_MAPPING.get(env_language, "en")

        self.default_language = mapped_language
        self.current_language = mapped_language
        self.texts = {}

        # Load all available language files
        self._load_languages()

    def _load_languages(self):
        """Load all available language files"""
        # Load default language (English)
        try:
            with open(self.base_path, encoding="utf-8") as f:
                self.texts["en"] = json.load(f)
        except FileNotFoundError:
            raise Exception(
                f"FATAL: Display texts JSON file not found at '{self.base_path}'. The application cannot start without it."
            )
        except json.JSONDecodeError as e:
            raise Exception(
                f"FATAL: Error decoding display texts JSON file at '{self.base_path}': {e}. The application cannot start."
            )

        # Load other language files (e.g., display_texts.ar.json)
        base_dir = self.base_path.parent
        base_name = self.base_path.stem  # 'display_texts'

        for lang_code in self.AVAILABLE_LANGUAGES.keys():
            if lang_code == "en":
                continue  # Already loaded

            lang_file = base_dir / f"{base_name}.{lang_code}.json"
            if lang_file.exists():
                try:
                    with open(lang_file, encoding="utf-8") as f:
                        self.texts[lang_code] = json.load(f)
                except Exception as e:
                    print(f"Warning: Could not load language file '{lang_file}': {e}")

    def set_language(self, language_code: str):
        """Set the current language"""
        if language_code in self.texts:
            self.current_language = language_code
        else:
            print(f"Warning: Language '{language_code}' not available. Using default.")
            self.current_language = self.default_language

    def get_texts(self) -> DotDict:
        """Get texts for current language"""
        return DotDict(self.texts.get(self.current_language, self.texts[self.default_language]))

    def get_available_languages(self) -> dict:
        """Get list of available languages"""
        return {k: v for k, v in self.AVAILABLE_LANGUAGES.items() if k in self.texts}


# Initialize multi-language support
_ml_texts = None
dt = None

try:
    _ml_texts = MultiLanguageTexts(display_texts_json_path)
    dt = _ml_texts.get_texts()
except Exception as e:
    raise Exception(
        f"FATAL: An unexpected error occurred while loading display texts: {e}. The application cannot start."
    )


def get_language_manager():
    """Get the language manager instance"""
    return _ml_texts


def set_language(language_code: str):
    """Set the current language and return updated texts"""
    global dt
    if _ml_texts:
        _ml_texts.set_language(language_code)
        dt = _ml_texts.get_texts()
    return dt


def get_current_language() -> str:
    """Get current language code"""
    return _ml_texts.current_language if _ml_texts else "en"


def get_available_languages() -> dict:
    """Get available languages"""
    return _ml_texts.get_available_languages() if _ml_texts else {"en": "English"}
