import detectlanguage
from googletrans import Translator
from language_manager import languages

detectlanguage.configuration.api_key = "619597bdafdfa5e7fa602f9d7a4b0620"
user_status = detectlanguage.user_status()

def detect_language(text):
    """detects language with API from detectlanguage.com, via python-module 
    detectlanguage, and returns language name"""
    results = detectlanguage.detect(text)
    language_name = ""
    for result in results:
        if result['isReliable']:
            found = False
            for language in languages:
                if result['language'] == language.get_code():
                    language_name = language.get_sv_name()
                    found = True
            if not found:
                language_name = result['language']
                return language_name
    return language_name

def detect_language_code(text):
    """detects language with API from detectlanguage.com, via python-module 
    detectlanguage, and returns language code"""
    results = detectlanguage.detect(text)
    language_code = ""
    for result in results:
        if result['isReliable']:
            found = False
            for language in languages:
                if result['language'] == language.get_code():
                    language_code = language.get_code()
                    found = True
            if not found:
                language_code = result['language']
                return language_code
    return language_code


# translate a complete text by detecting source language (with detectlanguage API)
def translate(text, translate_to):
    dest_lang = translate_to.title()
    dest_lang_code = ""
    for language in languages:
        if language.get_sv_name() == translate_to:
            dest_lang_code = language.get_code()

    translator = Translator()
    translated_text = ""
    try:
        translated_text = translator.translate(text, dest=dest_lang_code, src=detect_language_code(text))
    except ValueError:
        return
    translated_text = translated_text.text
    return translated_text


# translate wihout detection and instead chose own source language as parameter
def translate_without_detection(text, translate_to, source_language_code):
    language_name = translate_to
    language_name = language_name.title()
    language_code = ""
    for language in languages:
        if language.get_sv_name() == language_name:
            language_code = language.get_code()

    translator = Translator()
    translated_text = translator.translate(text, dest=language_code, src=source_language_code)
    return translated_text.text

