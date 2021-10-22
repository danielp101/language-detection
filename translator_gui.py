"""
Moduler som krävs: PyQt5 detectlanguage googletrans
Funktionalitet som hämtas utifrån: 
- Språkdetektering från detectlanguage.com (API) 
- Översättning genom Google Translate, med modulen googletrans

Detta är ett översättningsprogram med följande funktionalitet:
- Öppna filer från hårddisken och hämta innehållet, eller skriv in egen text
- Detektera språk
- Översätt text som en helhet med bevarad grammatik
- Skapa ordlista: Översätter valda ord, ord för ord, utan bevarad grammatik och skapar en liten ordlista bestående 
av max 10 ord med orden på originalspråk + översättning. Ett gränsvärde är satt för att inte överstiga begränsning 
i mängd data för googletrans. Finns fler än tio ord i användarens text så slumpas 10 ord från texten.
- Spara fil, låter användaren spara sin skapta ordlista som en textfil på hårddisken

Användning:
1) Är ingen databas skapad måste användaren först skapa och fylla databasen genom att köra filen fa_db_functionality.py
2) Finns en databas redan så hoppas steg 1 över
3) Sedan ska alla andra moduler fungera
4) Skriv in text i den översta textrutan eller tryck på 'hämta textfil' för att navigera till en fil att öppna hårddisken
5) Justera vilken typ av frekvensanalys du vill använda med reglaget.  Antingen egen frekvensanalys (mer inexakt)
eller användning av frekvensanalys via detectlanguage.com (hämtas via API och har en databegränsning)
6) Använd rullgardinsmenyn för att välja ett språk att översätta till
7) Klicka på översätt för att översätta hela texten med bevarad grammatik
8) Klicka på skapa ordlista för att skapa en ordlista av tio ord (slumpmässigt om din text består av mer än tio ord)
9) Klicka på spara ordlista som textfil för att spara din ordlista som en textfil på hårddisken
10) Klicka på rensa för att nollställa det du skrivit in och eventuella ordlistor och översättningar som skapats
"""

from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTextEdit, QComboBox, QTableWidget, QTableWidgetItem, QDialog, QFormLayout, \
    QLabel, QPushButton, QVBoxLayout, QFileDialog, QRadioButton, QHBoxLayout, QGridLayout, QSlider, QMessageBox
from language_manager import languages

import sys

import translation_manager as tm
from language_manager import languages
from freq_analysis import return_detected_lang
import fa_db_functionality

global own_analysis
own_analysis = True


class Dialog(QDialog):
    global own_analysis

    def __init__(self, parent=None):

        def detect():
            if 0 < len(self.your_text.toPlainText()) <= 12000:
                try:
                    if own_analysis:
                        all_detected_langs, detected_lang = return_detected_lang(self.your_text.toPlainText())
                        if len(all_detected_langs) > 1:
                            show_dialog(all_detected_langs)
                        else:
                            for language in languages:
                                if language.get_eng_name() == detected_lang:
                                    self.detected.setText(language.get_sv_name())
                    else:
                        detected_lang = tm.detect_language(self.your_text.toPlainText())
                        self.detected.setText(detected_lang)
                except TypeError:
                    self.detected.setText("Error, detection failed, try using other detection method")


        def translate():
            """Translates text and shows output of translation and detected language"""
            self.translation.clear()
            if len(self.your_text.toPlainText()) <= 12000:
                try:
                    # translate through call language detection API through translator_functionality
                    if not own_analysis:
                        self.translation.insertPlainText(
                            tm.translate(self.your_text.toPlainText(), self.your_lang.currentText()))  #
                        self.detected.setText(tm.detect_language(self.your_text.toPlainText()))

                    # if own analysis send to own language detection in detection class,
                    # then translate using that detection
                    else:
                        if len(self.your_text.toPlainText()) > 0:
                            all_detected_langs, detected_source_lang = return_detected_lang(self.your_text.toPlainText())
                            if len(all_detected_langs) > 1:
                                show_dialog(all_detected_langs)

                            else:
                                try:
                                    self.translation.insertPlainText(
                                        tm.translate_without_detection(self.your_text.toPlainText(),
                                                                       self.your_lang.currentText(),
                                                                       detected_source_lang))

                                    for language in languages:
                                        if language.get_eng_name() == detected_source_lang:
                                            self.detected.setText(language.get_sv_name())

                            # check for occurencies when no output language should be displayed,
                            # for example empty strings
                                except TypeError:
                                    self.detected.setText("")
                        else:
                            self.detected.setText("")

                except ZeroDivisionError:
                    lang_found = False
                    for language in languages:
                        if self.your_lang.currentText() == language.get_sv_name():
                            lang_found = True
                    if lang_found or len(self.your_lang.text()) == 0:
                        self.detected.setText("Du måste skriva in en text och ange ett språk att översätta till")
                    else:
                        self.detected.setText(
                            "Du måste ange ett språk som appen stöder och ange det språkets svenska namn")
            else:
                self.detected.setText(
                    "Kan inte översätta texter som består av över 12000 tecken")
            tm.print_values()

        # Clears all text and sets values to defualt (starting values)
        def clear():
            self.your_text.clear()
            self.detected.setText("")
            self.translation.clear()
            self.dictionary.clear()
            tm.clear_translation()
            self.btn_save.setEnabled(False)

        # create a 'dictionary' by making a list of 10 words with their translations
        def translate_list():
            detected_lang = ""
            words_list = []
            try:
                # translate through call language detection API through translator_functionality
                if not own_analysis:
                    your_text_as_words, words_list = tm.translate_list(self.your_text.toPlainText(),
                                                                       self.your_lang.currentText())
                    detected_lang = tm.detect_language(self.your_text.toPlainText())

                # if own analysis send to own language detection in detection class, then translate using that detection
                else:
                    if len(self.your_text.toPlainText()) > 0:
                        all_detected_langs, detected_lang = return_detected_lang(self.your_text.toPlainText())
                        if len(all_detected_langs) > 1:
                            show_dialog(all_detected_langs)
                        else:

                            your_text_as_words, words_list = tm.translate_list_wihtout_detection(
                                self.your_text.toPlainText(),
                                self.your_lang.currentText(),
                                detected_lang)

                            # set detected language
                            for language in languages:
                                if language.get_eng_name() == detected_lang:
                                    self.detected.setText(language.get_sv_name())

                    else:
                        self.detected.setText("")

                # name the headers of the 'dictionary' table
                list_of_headers_vertical = [detected_lang, self.your_lang.currentText()]
                self.dictionary.setHorizontalHeaderLabels(list_of_headers_vertical)

                # add the values to the 'dictionary' table, word in: original language / translated language
                i = 0
                for word in words_list:
                    self.dictionary.setItem(i, 0, QTableWidgetItem(your_text_as_words[i]))
                    self.dictionary.setItem(i, 1, QTableWidgetItem(word))
                    i += 1
                self.btn_save.setEnabled(True)

            # If unsupported, incorrect or no data found
            except KeyError:
                lang_found = False
                for language in languages:
                    if self.your_lang.currentText() == language.get_sv_name():
                        lang_found = True
                if lang_found or len(self.your_lang.text()) == 0:
                    self.detected.setText("Du måste skriva in en text och ange ett språk att översätta till")
                else:
                    self.detected.setText("Du måste ange ett språk som appen stöder och ange det språkets svenska namn")
            tm.print_values()

        def open_file():
            # opens FileDialog and lets user chose a folder and a filename, filters to show only .txt-files
            fname, _filter = QFileDialog.getOpenFileName(None, "Open " + " Data File", '.', "(*.txt)")
            text = ""
            lines = 0

            mf = None
            try:
                mf = open(fname, encoding="UTF-8")
            except FileNotFoundError:  # if no file, do nothing
                pass

            totallines = []
            try:
                totallines = mf.readlines()
            except AttributeError:  # if nothing to read, do nothing
                pass

            # check totallines to know when to stop iteration
            for line in totallines:
                if lines > 225:
                    break
                lines += 1

            # at most, read the 225 first lines, add them to one text and insert it to the GUI
            try:
                with open(fname, encoding="UTF-8") as myfile:
                    limit = [next(myfile) for x in range(lines)]

                for line in limit:
                    text += line

                self.your_text.clear()
                self.your_text.insertPlainText(text)
            except FileNotFoundError:  # if no file, do nothing
                pass

        # Save file as text file in an archive on computer
        def save_file():
            i = 0
            thestring = ""

            # loops thorugh the 'dictionary' table and extracts data
            for i in range(0, 10):
                item = self.dictionary.item(i, 0)
                try:
                    thestring += str(item.text()) + " "
                except AttributeError:
                    pass

                item = self.dictionary.item(i, 1)
                try:
                    thestring += str(item.text()) + "\n"
                except AttributeError:
                    pass

            # opens FileDialog and lets user chose a folder and a filename, writes data to file
            name, filter = QFileDialog.getSaveFileName(None, "Open " + " Data File", '.', "(*.txt)")

            file = None
            try:
                file = open(name, 'w')
            except FileNotFoundError:  # if no file do nothing
                pass

            try:
                file.write(thestring)
                file.close()
            except AttributeError:  # if not able to write do nothing
                pass

        # Functionality of slider. If changed, set to either own analysis or analysis through API
        def toggle_analysis():
            global own_analysis
            if self.slider_analysis.value() == 1:
                own_analysis = False
                self.slider_label.setText("Frekvensanalys från detectlanguage.com")
            else:
                own_analysis = True
                self.slider_label.setText("Egen frekvensanalys")

        def show_dialog(all_langs):
            self.msg.setText("This is a message box")
            text = ""
            for item in all_langs:
                text += str(item) + "\n"

            self.msg.setInformativeText("Can't determine language")
            self.msg.setWindowTitle("Language detection failed")
            self.msg.setDetailedText("The following languages recieved the same score:\n" + text)
            self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            self.msg.buttonClicked.connect(accept)
            returnValue = self.msg.exec()

        def accept():
            pass

        # Initializer
        super().__init__(parent)
        self.setWindowTitle('Translator PyQt5')

        # Add layouts to be used
        self.dlgLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.formLayoutR = QFormLayout()
        self.formLayoutU = QFormLayout()
        self.gridLayout = QGridLayout()

        # Add elements
        self.your_text = QTextEdit()
        self.your_lang = QComboBox()
        self.detected = QLabel()
        self.translation = QTextEdit()
        self.dictionary = QTableWidget()
        self.btn_open = QPushButton('Hämta textfil')
        self.rbtn_analysis = QPushButton("Använder egen frekvensanalys")
        self.btn_translate = QPushButton('Översätt')
        self.btn_clear = QPushButton('Rensa')
        self.btn_translate_list = QPushButton('Skapa ordlista')
        self.btn_save = QPushButton('Spara ordlista som textfil')
        self.empty_label = QLabel(" ")
        self.btn_detect = QPushButton("Detektera språk")
        self.slider_analysis = QSlider(Qt.Horizontal)
        self.slider_label = QLabel("Egen frekvensanalys")
        self.msg = QMessageBox()
        self.google_label = QLabel("Translations powered by Google Translate")

        # Set interval of slider
        self.slider_analysis.setMinimum(0)
        self.slider_analysis.setMaximum(1)

        # Behavior of toggle-button
        self.rbtn_analysis.setCheckable(True)

        # Button functionality
        self.slider_analysis.valueChanged.connect(toggle_analysis)
        self.btn_open.clicked.connect(open_file)
        self.btn_translate.clicked.connect(translate)
        self.btn_clear.clicked.connect(clear)
        self.btn_translate_list.clicked.connect(translate_list)
        self.btn_save.clicked.connect(save_file)
        self.btn_detect.clicked.connect(detect)

        # Sets columns and rows of gridlayout
        self.gridLayout.addItem(self.formLayoutU, 0, 0, 1, 2)
        self.gridLayout.addItem(self.formLayout, 1, 0)
        self.gridLayout.addItem(self.formLayoutR, 1, 1)
        self.gridLayout.addWidget(self.google_label, 2, 0, 1, 2, alignment=Qt.AlignCenter)

        # Add the components to the upper layaut
        self.formLayoutU.addRow('Din text:  ', self.your_text)
        self.formLayoutU.addRow("", self.empty_label)
        self.formLayoutU.addRow(self.btn_open)
        self.formLayoutU.addRow(self.btn_detect)
        self.formLayoutU.addRow("", self.empty_label)
        self.formLayoutU.addRow(self.slider_label)
        self.formLayoutU.addRow(self.slider_analysis)
        self.formLayoutU.addRow("", self.empty_label)
        self.formLayoutU.addRow('Detekterat språk:  ', self.detected)

        # Adds the components to the lower left layout
        self.formLayout.addRow('Översätt till:  ', self.your_lang)
        self.formLayout.addRow("", self.empty_label)
        self.formLayout.addRow(self.btn_translate, self.btn_clear)
        self.formLayout.addRow("", self.empty_label)
        self.formLayout.addRow('Översättning:  ', self.translation)

        # Adds the components to lower right layout
        self.formLayoutR.addRow(self.btn_translate_list, self.btn_save)
        self.formLayoutR.addRow("", self.empty_label)
        self.formLayoutR.addRow(self.dictionary)

        # Disbales save file-button before any list is made
        self.btn_save.setEnabled(False)

        # Center adjustment of buttons and labels
        self.formLayoutU.setAlignment(self.slider_analysis, Qt.AlignCenter)
        self.formLayoutU.setAlignment(self.slider_label, Qt.AlignCenter)
        self.formLayoutU.setAlignment(self.btn_open, Qt.AlignCenter)
        self.formLayoutU.setAlignment(self.btn_detect, Qt.AlignCenter)

        # Set stylesheets
        self.setStyleSheet("font: 12pt Verdana")
        self.setStyleSheet("font-weight: bold; color: white")
        self.rbtn_analysis.setStyleSheet("color: black; background-color: white")
        self.your_text.setStyleSheet("font-weight: Normal; color: black")
        self.your_lang.setStyleSheet("font-weight: Normal; color: black")
        self.translation.setStyleSheet("font-weight: Normal; color: black")
        self.btn_translate.setStyleSheet("color: black")
        self.btn_clear.setStyleSheet("color: black")
        self.btn_translate_list.setStyleSheet("color: black")
        self.dictionary.setStyleSheet("color: black")
        self.btn_save.setStyleSheet("color: black")
        self.btn_open.setStyleSheet("color: black")
        self.btn_detect.setStyleSheet("color: black")

        # Set connection between layouts
        self.dlgLayout.addLayout(self.gridLayout)
        self.setLayout(self.dlgLayout)

        # fills combobox with values from dictionary in translator-class
        for language in languages:
            self.your_lang.addItem(language.get_sv_name())

        # sets start value for combobox to 'english'
        self.your_lang.setCurrentIndex(2)

        # sets columns and rows of tablebox
        self.dictionary.setColumnCount(2)
        self.dictionary.setRowCount(100)

        # sets min/max sizes
        self.btn_open.setMinimumWidth(350)
        self.btn_open.setMaximumWidth(450)
        self.btn_detect.setMinimumWidth(350)
        self.btn_detect.setMaximumWidth(450)
        self.your_text.setMaximumHeight(180)
        self.your_text.setMinimumWidth(550)
        self.translation.setMinimumHeight(90)
        self.dictionary.setMinimumHeight(150)
        self.slider_analysis.setMinimumWidth(200)
        self.slider_analysis.setMaximumWidth(300)


# Run
if __name__ == '__main__':
    fa_db_functionality.create_complete_db()

    app = QApplication(sys.argv)
    dlg = Dialog()

    # Set size of main window and visibility
    dlg.resize(800, 550)
    dlg.show()

    # Set background color
    p = dlg.palette()
    color = QColor('#303030')
    p.setColor(dlg.backgroundRole(), color)
    dlg.setPalette(p)

    sys.exit(app.exec_())
