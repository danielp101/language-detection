"""
Class that handles, modifies and connetcs to data related to language objects
"""

from language import *

language_names_eng = {"Arabic": "ar", "Danish": "da", "English": "en", "Estonian": "et", "Finish": "fi",
                      "French": "fr", "Greek": "el", "Hebrew": "iw", "Hindi": "hi", "Irish": "ga",
                      "Italian": "it", "Japanese": "ja", "Korean": "ko", "Norwegian": "no", "Persian": "fa",
                      "Polish": "pl", "Portugiese": "pt", "Russian": "ru", "Swedish": "sv", "Spanish": "es",
                      "German": "de", "Welsh": "cy"}

language_codes_sv = {"ar": "Arabiska", "cy": "Walesiska", "da": "Danska", "de": "Tyska",
                     "en": "Engelska", "et": "Estniska", "el": "Grekiska", "es": "Spanska", "fi": "Finska",
                     "fr": "Franska", "fa": "Persiska", "ga": "Irländska", "hi": "Hindi", "iw": "Hebreiska",
                     "it": "Italienska", "ja": "Japanska", "ko": "Koreanska", "no": "Norska", "pl": "Polska",
                     "pt": "Portugisiska", "ru": "Ryska", "sv": "Svenska"}

languages = []
for key, value in language_names_eng.items():
    lang = Language(key, language_codes_sv[language_names_eng[key]], language_names_eng[key], [])
    languages.append(lang)


# print languages for testing or clarification purposes (program work without it)
def print_available_languages():
    for language in languages:
        print(language.get_eng_name())
