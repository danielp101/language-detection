import random
from translation import *
import translator_functionality as tf
import language_manager as lm

my_trans = Translation("", "", "", "", "", "")


# detects language and returns language name
def detect_language(text):
    language = tf.detect_language(text)
    my_trans.set_source_lang(language)
    for language in lm.languages:
        if language.get_sv_name() == language:
            my_trans.set_source_lang_code(language.get_code())

    return my_trans.get_source_lang()


# translate a complete text by detecting source language (with detectlanguage API)
def translate(text, translate_to):
    my_trans.set_text(text)
    my_trans.set_dest_lang(translate_to.title())

    for language in lm.languages:
        if language.get_sv_name() == translate_to:
            my_trans.set_dest_lang_code(language.get_code())

    my_trans.set_translated_text(tf.translate(text, translate_to.title()))
    return my_trans.get_translated_text()


# divide a text into words and translate them separately (max 10 words)
# if more than 10 words in text, choses 10 words randomly as to not overstep the datalimit of googletrans
# return a list of words in orginal language as well as a list of translated words
# at the same time detects language by using the text as a whole
# sending the complete text as a parameter with a call to the detect_language_code method
# this is done to limit language detection errors, which are more common when no frequency can be calculated
# (due to few words)
def translate_list(text, translate_to):
    translated_list = []
    filtered_words_as_list = []

    # split the whole text to words to translate them seperately
    words_as_list = text.split(" ")

    # remove unwanted chars:
    unwanted_chars = [",", ".", "'", "´", "`", '"', ":", ";", "-", "–", ""]
    for word in words_as_list:
        for char in unwanted_chars:
            word = word.replace(char, "")

    # filter words that do not only contain strings as well as words that are three letters or shorter:
    for word in words_as_list:
        if word.isalpha() and len(word) > 3:
            filtered_words_as_list.append(word)

    # if more words than 10 words in text, chose 10 random words out of all words
    if len(words_as_list) > 10:
        filtered_words_as_list = random.sample(filtered_words_as_list, 10)

    # if not own_analysis:
    detected_lang_code = tf.detect_language_code(text)
    """ else:
        detected_source_language_name_eng = detection.return_deteced_lang(text)
        detected_lang_code = tf.language_names_eng[detected_source_language_name_eng]"""

    # translate the 10 words
    for word in filtered_words_as_list:
        translated_list.append(tf.translate_without_detection(word, translate_to, detected_lang_code))

    return filtered_words_as_list, translated_list


# Clear values of translation object
def clear_translation():
    my_trans.clear_values()


# Print str representation of object
def print_values():
    print(my_trans)


# Translates text "without" detection, because detection is done by own language analysis
def translate_without_detection(text, translate_to, source_language):
    source_language_code = ""
    for language in lm.languages:
        if language.get_eng_name() == source_language:
            source_language_code = language.get_code()
            source_language = language.get_sv_name()

    my_trans.set_text(text)
    my_trans.set_source_lang_code(source_language_code)
    my_trans.set_dest_lang(translate_to.title())

    for language in lm.languages:
        if language.get_sv_name() == translate_to.title():
            my_trans.set_dest_lang_code(language.get_code())

    my_trans.set_translated_text(tf.translate_without_detection(text, translate_to, source_language_code))

    return my_trans.get_translated_text()


def translate_list_wihtout_detection(text, translate_to, source_lang):
    translated_list = []
    filtered_words_as_list = []

    # split the whole text to words to translate them seperately
    words_as_list = text.split(" ")

    # remove unwanted chars:
    unwanted_chars = [",", ".", "'", "´", "`", '"', ":", ";", "-", "–", ""]
    for word in words_as_list:
        for char in unwanted_chars:
            word = word.replace(char, "")

    # filter words that do not only contain strings as well as words that are three letters or shorter:
    for word in words_as_list:
        if word.isalpha() and len(word) > 3:
            filtered_words_as_list.append(word)

    # if more words than 10 words in text, chose 10 random words out of all words
    if len(words_as_list) > 10:
        filtered_words_as_list = random.sample(filtered_words_as_list, 10)

    detected_lang_code = ""
    for language in lm.languages:
        if language.get_eng_name() == source_lang:
            detected_lang_code = language.get_code()
    #detected_lang_code = tf.language_names_eng[source_lang]

    # translate the 10 words
    for word in filtered_words_as_list:
        translated_list.append(tf.translate_without_detection(word, translate_to, detected_lang_code))

    return filtered_words_as_list, translated_list
