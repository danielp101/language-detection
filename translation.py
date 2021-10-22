class Translation:

    def __init__(self, text, source_lang, source_lang_code, dest_lang, dest_lang_code, translated_text):
        self._text = text
        self._source_lang = source_lang
        self._source_lang_code = source_lang_code
        self._dest_lang = dest_lang
        self._dest_lang_code = dest_lang_code
        self._translated_text = translated_text

    def __str__(self):
        return "\nSource text:%s\nSource lang:%s\nSource lang code:%s\nDestination lang:%s\n" \
               "Destination lang code:%s\nTranslated text:%s" % (self._text, self._source_lang, self._source_lang_code, self._dest_lang,
                                       self._dest_lang_code, self._translated_text)

    def get_text(self):
        return self._text

    def get_source_lang(self):
        return self._source_lang

    def get_source_lang_code(self):
        return self._source_lang_code

    def get_dest_lang(self):
        return self._dest_lang

    def get_dest_lang_code(self):
        return self._dest_lang_code

    def get_translated_text(self):
        return self._translated_text

    def set_text(self, value):
        self._text = value

    def set_source_lang(self, value):
        self._source_lang = value

    def set_source_lang_code(self, value):
        self._source_lang_code = value

    def set_dest_lang(self, value):
        self._dest_lang = value

    def set_dest_lang_code(self, value):
        self._dest_lang_code = value

    def set_translated_text(self, value):
        self._translated_text = value

    def clear_values(self):
        self._text = ""
        self._source_lang = ""
        self._source_lang_code = ""
        self._dest_lang = ""
        self._dest_lang_code = ""
        self._translated_text = ""
