class Language:
    def __init__(self, eng_name, sv_name, code,language_fa):
        self._eng_name = eng_name
        self._sv_name = sv_name
        self._code = code
        self._language_fa = language_fa

    def __str__(self):
        return "language_name:%s\n code:%s\n language_fa:%s\n" % (self._eng_name,self._code,self._language_fa)

    def get_eng_name(self):
        return self._eng_name

    def get_sv_name(self):
        return self._sv_name

    def get_code(self):
        return self._code

    def get_language_fa(self):
        return self._language_fa

    def set_eng_name(self, value):
        self._eng_name = value

    def set_sv_name(self, value):
        self._sv_name = value

    def set_code(self, value):
        self._code = value

    def set_language_fa(self, value):
        self._language_fa = value