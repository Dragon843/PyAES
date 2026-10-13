import sys
import aesTools
import cipherAES
import cipherCBC
from PySide6.QtCore import (
    Qt,
    QFileInfo
)
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (
    #main 
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog, 
    QDialogButtonBox, 
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton, 
    QTextEdit,
    QVBoxLayout, 
    QWidget
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.__keyPath = ""

        # Sztywne ustawienie wielkości aplikacji
        self.setFixedSize(1000, 600)
        self.setWindowTitle("Widgets App")

        # Kontenery zawierające widżety
        layout_main = QVBoxLayout()

        layout_file_box_search = QHBoxLayout()
        layout_file_box_save = QHBoxLayout()
        layout_lenght_key_box = QHBoxLayout()
        layout_buttons_box_key = QHBoxLayout()
        layout_checks_box_modes = QGridLayout()
        layout_buttons_box_controll = QHBoxLayout()

        #
        label_file_search = QLabel("Plik tekstowy")

        # Pole ze ścieżką do pliku tekstowego
        self._line_path_fsearch = QLineEdit("")
        layout_file_box_search.addWidget(self._line_path_fsearch)

        # przycisk do wywołania eksploratora plików potrzebnego do wskazania pliku tekstowego
        # i zapisania jego ścieżki w line_path_fsearch
        self.button_path_fsearch = QPushButton("...")
        self.button_path_fsearch.setCheckable(True)
        self.button_path_fsearch.clicked.connect(self._brows_file)
        layout_file_box_search.addWidget(self.button_path_fsearch)

        #
        label_file_save = QLabel("Ścieżka zapisu")

        # Pole ze ścieżką do miejsca zapisu pliku
        self._line_path_fsave = QLineEdit("")
        layout_file_box_save.addWidget(self._line_path_fsave)

        # przycisk do wywołania eksploratora plików potrzebnego do wskazania ścieżki
        # i zapisania w line_path_fsave
        self.button_path_fsave = QPushButton("...")
        self.button_path_fsave.setCheckable(True)
        self.button_path_fsave.clicked.connect(self._brows_file)
        layout_file_box_save.addWidget(self.button_path_fsave)

        # rozwijana lista wyboru długości klucza
        label_combo_lenght = QLabel("Długość klucza")
        self.combo_lenght_key = QComboBox()
        self.combo_lenght_key.addItems(["256", "192", "128"])
        layout_lenght_key_box.addWidget(label_combo_lenght)
        layout_lenght_key_box.addWidget(self.combo_lenght_key)

        #
        label_options_key = QLabel("Opcje wyboru klucza")

        # przyciski do wywołania eksploratora plików potrzebnego do stworzenia
        # lub wskazania istniejącego pliku z kluczem
        # szyfrującym i zapisania jego ścieżki w line_path_fkeys 
        self.button_create_fkey = QPushButton("Wygeneruj plik z kluczem")
        self.button_create_fkey.setCheckable(True)
        self.button_create_fkey.clicked.connect(self._brows_file)
        layout_buttons_box_key.addWidget(self.button_create_fkey)

        self.button_select_fkey = QPushButton("Wybierz plik z kluczem ")
        self.button_select_fkey.setCheckable(True)
        self.button_select_fkey.clicked.connect(self._brows_file)
        layout_buttons_box_key.addWidget(self.button_select_fkey)

        self.button_check_lenght_key = QPushButton("Sprawdź klucz")
        self.button_check_lenght_key.setCheckable(True)
        self.button_check_lenght_key.clicked.connect(self._check_lenght_key)
        
        #
        label_mode = QLabel("Tryb")

        # Pola do wybrania trybu pracy aplikacji
        self.check_cipher = QCheckBox("Szyfrowania")
        self.check_cipher.stateChanged.connect(self._change_check_cipher)
        layout_checks_box_modes.addWidget(self.check_cipher,0,0)
        
        self.check_decipher = QCheckBox("Deszyfrowania")
        self.check_decipher.stateChanged.connect(self._change_check_decipher)
        layout_checks_box_modes.addWidget(self.check_decipher,0,1)

        self.check_test = QCheckBox("Testowania")
        self.check_test.stateChanged.connect(self._change_check_test)
        layout_checks_box_modes.addWidget(self.check_test,0,2)

        #
        label_extra = QCheckBox("Dodatkowe ustawienia")

        # Pola do zaznaczenia dodatkowych ustawień wyświetlania aplikacji
        self.value_lenght_test = ""
        self.vector_lenght_test = ""
        self.combo_vector_test = QComboBox()
        self.combo_vector_test.addItems(["Aes-128 Vektor 1", "Aes-128 Vektor 2", "Aes-128 Vektor 3", "Aes-128 Vektor 4", "Aes-192 Vektor 1", "Aes-192 Vektor 2", "Aes-192 Vektor 3", "Aes-192 Vektor 4", "Aes-256 Vektor 1", "Aes-256 Vektor 2", "Aes-256 Vektor 3", "Aes-256 Vektor 4"])

        # Przycisk startu programu
        self.button_start = QPushButton("Start")
        self.button_start.clicked.connect(self._check_program_files)
        layout_buttons_box_controll.addWidget(self.button_start)

        #
        self._window_log = QTextEdit()
        self._window_log.setReadOnly(True)
        

        # Dostosowywanie rozmieszczenia widżetów
        #layout_main.setSpacing(5)
        layout_main.addWidget(label_file_search)
        layout_main.addLayout(layout_file_box_search)
        layout_main.addWidget(label_file_save)
        layout_main.addLayout(layout_file_box_save)
        layout_main.addLayout(layout_lenght_key_box)
        layout_main.addWidget(label_options_key)
        layout_main.addLayout(layout_buttons_box_key)
        layout_main.addWidget(self.button_check_lenght_key)
        layout_main.addWidget(label_mode)
        layout_main.addLayout(layout_checks_box_modes)
        layout_main.addWidget(self.combo_vector_test)
        layout_main.addLayout(layout_buttons_box_controll)
        layout_main.addWidget(self._window_log)

        #tworzenie main_widget
        widget_main = QWidget()
        #ustawianie układu main_widget
        widget_main.setLayout(layout_main)
        #wyświetlanie main_widget na głównym ekranie
        self.setCentralWidget(widget_main)

    # Funkcja wywołująca menadżer plików
    def _brows_file(self):
        # extNames = "Microsoft office: .docx(*.docx);;Dokument otwarto-źródłowy: .odt(*.odt);;Notatnik: .txt(*.txt)"
        fileKeyName = ""

        # Sprawdza który konkretny przycis został przyciśnięty
        if self.button_path_fsearch.isChecked() == True:
            # Wywołanie menadżera plików
            file_manager = QFileDialog(self, "Open File", "~/", "Notatnik: .txt(*.txt)")
            file_manager.exec()

            # Zapisanie w etykiecie line_path_fsearch 
            # ścieżki do wybranego pliku w menadżerze
            filePath = file_manager.selectedFiles()
            self._line_path_fsearch.setText(filePath[0])

            # Wyświetlenie zakończenie procesu
            # w _widow_log
            self._window_log.setReadOnly(False)
            self._window_log.append("Pomyślnie wybrano plik: " + self._line_path_fsearch.text())
            self._window_log.setReadOnly(True)

            # Zmiana stanu przyciku
            self.button_path_fsearch.setChecked(False)
            self.button_path_fsearch.setFlat(False)

        elif self.button_select_fkey.isChecked() == True:
            # Wywołanie menadżera plików
            file_manager = QFileDialog(self, "Open File", "~/", "Notatnik: .txt(*.txt)")
            file_manager.exec()
            
            # Wczytanie ścieżki do wybranego pliku w menadżerze
            # z etykiety line_path_fsearch
            self.__keyPath = ""
            self.__keyPath = file_manager.selectedFiles()
            self.__keyPath = str(self.__keyPath[0])

            # Wyświetlenie zakończenie procesu
            # w _widow_log
            self._window_log.setReadOnly(False)
            self._window_log.append("Pomyślnie wybrano klucz: " + self.__keyPath)
            self._window_log.setReadOnly(True)

            self.button_select_fkey.setChecked(False)
            self.button_select_fkey.setFlat(False)

        elif self.button_create_fkey.isChecked() == True:
            file_manager = QFileDialog(self, "Save file", "~/", "Notatnik: .txt(*.txt)")
            file_manager.exec()

            fileKeyName = file_manager.selectedFiles()
            fileKeyName = str(fileKeyName[0])
            self._create_file_key(fileKeyName)

            self._window_log.setReadOnly(False)
            self._window_log.append("Pomyślnie utworzono plik: " + fileKeyName)
            self._window_log.setReadOnly(True)

            self.button_create_fkey.setChecked(False)
            self.button_create_fkey.setFlat(False)
        
        elif self.button_path_fsave.isChecked() == True:
            file_manager = QFileDialog(self, "Open File", "~/")
            file_manager.exec()

            filePath = file_manager.selectedFiles()
            self._line_path_fsave.setText(filePath[0])

            self._window_log.setReadOnly(False)
            self._window_log.append("Pomyślnie wybrano ścieżkę: " + self._line_path_fsearch.text())
            self._window_log.setReadOnly(True)

            self.button_path_fsave.setChecked(False)
            self.button_path_fsave.setFlat(False)
            

    def _change_check_cipher(self):
        self.check_decipher.setChecked(False)
        self.check_test.setChecked(False)

    def _change_check_decipher(self):
        self.check_cipher.setChecked(False)
        self.check_test.setChecked(False)

    def _change_check_test(self):
        self.check_cipher.setChecked(False)
        self.check_decipher.setChecked(False)

    def _check_program_files(self):
        if self.__keyPath != "" or self.check_test.isChecked() == True:
            self._start_program()
        else:
            self._window_log.setReadOnly(False)
            self._window_log.append("Błąd!")
            self._window_log.append("Nie podano ścieżki do pliku tekstowego i/lub pliku z kluczem!")
            self._window_log.setReadOnly(True)

    def _create_file_key(self, path):
        text = aesTools._create_main_key(int(self.combo_lenght_key.currentText()))
        # text += aesTools._create_main_key(128)
        keyFileCreated = open(path, "w")
        keyFileCreated.write(text)
        keyFileCreated.close()

    def _check_lenght_key(self):
        fileOpened = open(self.__keyPath, "r")
        textFile = fileOpened.read()
        self._window_log.setReadOnly(False)

        self._window_log.append("klucz główny")
        text = textFile[:int((len(textFile) - 32))]
        self._window_log.append("")
        self._window_log.append(self.combo_lenght_key.currentText())
        self._window_log.append(("klucz: " + text))
        self._window_log.append("Długość w hexach: " + str(len(text)))

        # self._window_log.append("")
        # self._window_log.append("klucz CBC")
        # text = textFile[int((len(textFile) - 32)):]
        # self._window_log.append(text)
        # self._window_log.append(str(len(text)))

        self._window_log.setReadOnly(True)
        fileOpened.close()

    def _vectors_test(self):
        
        if(self.combo_vector_test.currentText() == "Aes-128 Vektor 1"):
            self.vector_lenght_test = "2b7e151628aed2a6abf7158809cf4f3c"
            self.value_lenght_test = "6bc1bee22e409f96e93d7e117393172a"
            self.result = "3ad77bb40d7a3660a89ecaf32466ef97"
        elif(self.combo_vector_test.currentText() == "Aes-128 Vektor 2"):
            self.vector_lenght_test = "2b7e151628aed2a6abf7158809cf4f3c"
            self.value_lenght_test = "ae2d8a571e03ac9c9eb76fac45af8e51"
            self.result = "f5d3d58503b9699de785895a96fdbaaf"
        elif(self.combo_vector_test.currentText() == "Aes-128 Vektor 3"):
            self.vector_lenght_test = "2b7e151628aed2a6abf7158809cf4f3c"
            self.value_lenght_test = "30c81c46a35ce411e5fbc1191a0a52ef"
            self.result = "43b1cd7f598ece23881b00e3ed030688"
        elif(self.combo_vector_test.currentText() == "Aes-128 Vektor 4"):
            self.vector_lenght_test = "2b7e151628aed2a6abf7158809cf4f3c"
            self.value_lenght_test = "f69f2445df4f9b17ad2b417be66c3710"
            self.result = "7b0c785e27e8ad3f8223207104725dd4"
        elif(self.combo_vector_test.currentText() == "Aes-192 Vektor 1"):
            self.vector_lenght_test = "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b"
            self.value_lenght_test = "6bc1bee22e409f96e93d7e117393172a"
            self.result = "bd334f1d6e45f25ff712a214571fa5cc"
        elif(self.combo_vector_test.currentText() == "Aes-192 Vektor 2"):
            self.vector_lenght_test = "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b"
            self.value_lenght_test = "ae2d8a571e03ac9c9eb76fac45af8e51"
            self.result = "974104846d0ad3ad7734ecb3ecee4eef"
        elif(self.combo_vector_test.currentText() == "Aes-192 Vektor 3"):
            self.vector_lenght_test = "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b"
            self.value_lenght_test = "30c81c46a35ce411e5fbc1191a0a52ef"
            self.result = "ef7afd2270e2e60adce0ba2face6444e"
        elif(self.combo_vector_test.currentText() == "Aes-192 Vektor 4"):
            self.vector_lenght_test = "8e73b0f7da0e6452c810f32b809079e562f8ead2522c6b7b"
            self.value_lenght_test = "f69f2445df4f9b17ad2b417be66c3710"
            self.result = "9a4b41ba738d6c72fb16691603c18e0e"
        elif(self.combo_vector_test.currentText() == "Aes-256 Vektor 1"):
            self.vector_lenght_test = "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4"
            self.value_lenght_test = "6bc1bee22e409f96e93d7e117393172a"
            self.result = "f3eed1bdb5d2a03c064b5a7e3db181f8"
        elif(self.combo_vector_test.currentText() == "Aes-256 Vektor 2"):
            self.vector_lenght_test = "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4"
            self.value_lenght_test = "ae2d8a571e03ac9c9eb76fac45af8e51"
            self.result = "591ccb10d410ed26dc5ba74a31362870"
        elif(self.combo_vector_test.currentText() == "Aes-256 Vektor 3"):
            self.vector_lenght_test = "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4"
            self.value_lenght_test = "30c81c46a35ce411e5fbc1191a0a52ef"
            self.result = "b6ed21b99ca6f4f9f153e7b1beafed1d"
        elif(self.combo_vector_test.currentText() == "Aes-256 Vektor 4"):
            self.vector_lenght_test = "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4"
            self.value_lenght_test = "f69f2445df4f9b17ad2b417be66c3710"
            self.result = "23304b7a39f9f3ff067d8d8f9e24ecc7"

    def _start_program(self):
        self._window_log.setReadOnly(False)
        self._window_log.setText("Rozpoczynam proces!")

        fileOpened = ""
        fileConverted = ""
        roundKeys = ""
        rounds = 0

        if(self.check_test.isChecked() == False):
            self._window_log.append("Sczytywanie danych z pliku tekstowego")
            fileOpened = open(self._line_path_fsearch.text())
            fileConverted = fileOpened.read()
            fileTest = ""
            fileOpened.close()
            self._window_log.append("Zakończono sczytywanie danych.")

            self._window_log.append("Sczytywanie danych z pliku, z kluczami")
            fileOpened = open(self.__keyPath)
            roundKeys = fileOpened.read()
            # cbcKey = roundKeys[(len(roundKeys) - 32):]
            # print(cbcKey + " " + str(len(cbcKey)))
            # roundKeys = roundKeys[:(len(roundKeys) - 32)]
            rounds = int((len(roundKeys) / 8) + 6)
            fileOpened.close()
            self._window_log.append("Zakończono sczytywanie danych")

            self._window_log.append("Tworzenie kluczy rundy")
            roundKeys = aesTools._create_rounds_keys(roundKeys, rounds)
            self._window_log.append("Zakończono tworzenie kluczy rundy")
        else:
            self._window_log.append("Aktualizowanie danych testowych")
            self._vectors_test()
            fileOpened = self.value_lenght_test
            rounds = int((len(self.vector_lenght_test) / 8) + 6)
            roundKeys = aesTools._create_rounds_keys(self.vector_lenght_test, rounds)
            self._window_log.append("Zakończono aktualizacje danych testowych")
            

        self._window_log.append("Sortowanie danych")
        if(self.check_cipher.isChecked() == True):
            fileFinal = []
            point = 0

            fileConverted = aesTools._convert_input(fileConverted, "hex")
            self._window_log.append("Zakończono sortowanie")
            
            # self._window_log.append("Szyfrowanie pliku trybem CBC")
            # while point < len(fileConverted):
            #     if point == 0:
            #         fileCBC = [cipherCBC._first_run(fileConverted[point], cbcKey)]
            #     else:
            #         fileCBC = cipherCBC._cipher_text(fileConverted[(point - 1): point], cbcKey, rounds)
            #     self._window_log.append(fileCBC[point])
            # self._window_log.append("Zakończono proces szyfrowania trybem CBC")

            self._window_log.append("Szyfrowanie pliku standardem AES")
            # for text in fileCBC:
            #     fileFinal.append(cipherAES._cipher_text(text, roundKeys, rounds))
            fileFinal = cipherAES._cipher_text(fileConverted[0], roundKeys, rounds)
            self._window_log.append("Zakończono proces szyfrowania!")

            self._window_log.append("Zapisywanie wyniku")
            fileOpened = open(self._line_path_fsave.text())
            fileOpened.write(fileFinal)
            self._window_log.append("Zakończono operacje!")

        elif(self.check_decipher.isChecked() == True):
            fileConverted = aesTools._convert_input(fileConverted, "str")
            self._window_log.append("Zakończono sortowanie.")

            self._window_log.append("Deszyfracja pliku standardem AES.")
            fileFinal = cipherAES._inv_cipher_text(fileConverted, roundKeys, rounds)
            self._window_log.append("Zakończono proces deszyfracji!")

            self._window_log.append("Zapisywanie wyniku")
            fileOpened = open(self._line_path_fsave.text())
            fileOpened.write(fileFinal)
            self._window_log.append("Zakończono operacje!")

        elif(self.check_test.isChecked() == True):
            fileConverted = aesTools._convert_input(fileOpened, "hex")
            self._window_log.append("Zakończono sortowanie.")

            self._window_log.append("Szyfrowanie pliku standardem AES.")
            fileFinal = cipherAES._cipher_text(fileConverted[0], roundKeys, rounds)
            self._window_log.append("Zakończono szyfrowanie.")

            self._window_log.append("Deszyfracja pliku standardem AES.")
            fileTest = cipherAES._inv_cipher_text(fileFinal, roundKeys, rounds)
            self._window_log.append("Zakończono deszyfracje.")

            fileTest = aesTools._convert_input(fileTest, "str")
            self._window_log.append("Zakończono sortowanie.")

            self._window_log.append("Wyświetlanie wyników. \n")
            self._window_log.append("klucz testowy: " + self.vector_lenght_test)
            self._window_log.append("długość klucza: " + str(int(len(fileOpened))))
            self._window_log.append("ilość rund: " + str(rounds) + "\n")
            self._window_log.append("tekst testowy: " + fileOpened)
            self._window_log.append("oczekiwany wynik szyfrowania: " + self.result + "\n")

            self._window_log.append("klucze rundy: ")
            for i in range(int(len(roundKeys))):
                self._window_log.moveCursor(QTextCursor.End)
                self._window_log.insertPlainText(roundKeys[i] + ", ")

            self._window_log.append("tekst po przekształceniu: ")
            for i in range(int(len(fileConverted))):
                self._window_log.moveCursor(QTextCursor.End)
                self._window_log.insertPlainText(fileConverted[i] + ", ")
            
            self._window_log.append("tekst po zaszyfrowaniu: ")
            for i in range(int(len(fileFinal))):
                self._window_log.moveCursor(QTextCursor.End)
                self._window_log.insertPlainText(fileFinal[i] + ", ")

            self._window_log.append("tekst po odszyfrowaniu: ")
            for i in range(int(len(fileTest))):
                self._window_log.moveCursor(QTextCursor.End)
                self._window_log.insertPlainText(fileTest[i] + ", ")

            self._window_log.append("Zakończono proces testowania!")

        self._window_log.setReadOnly(True)


# funkcja potrzebna do startu aplikacji i wyświetlenia okna
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# dodatkowe ustawienie gdy program nie jest w stanie otworzyć okna
# i kończy proces samoistnie
if __name__ == "__main__":
    main()