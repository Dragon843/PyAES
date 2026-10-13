import os
import binascii
import aesMath
import lookUps
import math

# Funkcja generująca klucz główny przy użyciu biblioteki os
def _create_main_key(key_len):
    gen_key = os.urandom(int(key_len/8))
    gen_key = gen_key.hex()
    return gen_key


# Funkcja tworząca podklucze
def _create_rounds_keys(key,rounds):
    # Inicjalizacja tablicy podkluczy
    rounds_keys = []
    # Zmienna licząca ilość rund z klucza głównego
    # Licznik rund
    ext_list_count = 0
    print(len(key))

    # Pętla zapisująca główny klucz jako części podkluczy
    while ext_list_count < (len(key) / 8):
        rounds_keys.append(key[ext_list_count*8 : (ext_list_count*8)+8])
        ext_list_count += 1

    # Pętla tworząca nowe podklucze na bazie poprzednich podkluczy 
    while ext_list_count <= 4 * (rounds + 1) - 1:
        # Inicjalizacja klucza tymczasowego potrzebnego do przeprowadzania transformacji podklucza
        tmp_keys = rounds_keys[ext_list_count - 1]

        # Gdy licznik ext_list_count modulo z Nk jest równy 0 to:
        # Dwa pierwsze heksy ustawiamy na samym końcu
        # Szukamy wartości dla pary heksów odpowiadających wierszowi i kolumnie w tablicy S-box,
        # i zastępujemy wskazaną wartością
        # Przeprowadzamy operacji xor miedzy kluczem, a tablicą Rcon
        if ext_list_count % (rounds - 6) == 0:
            tmp_keys = aesMath._rotation_word(tmp_keys, 'left')
            tmp_keys = aesMath._sub_word(tmp_keys) 
            tmp_keys = aesMath._xor_string(tmp_keys[0:2], lookUps.Rcon[int(ext_list_count/rounds)]) + tmp_keys[2:]
            
        # Gdy klucz Nk jest dłuższy bądź równy 6 i licznik mod runda jest równa 4 to
        # szukane są wartości dla pary hexów odpowiadających wierszowi i kolumnie w tablicy S-box,
        # a później zstępowane wskazaną wartością
        elif (len(key) / 8) >= 6 and ext_list_count % rounds == 4: 
            tmp_keys = aesMath._sub_word(tmp_keys)

        # Działanie xor między pierwszym podkluczem rundy, a ostatnim podkluczem rundy
        rounds_keys.append(aesMath._xor_string(rounds_keys[ext_list_count - 4], tmp_keys))
        ext_list_count += 1

    return rounds_keys


# dzielenie tekstu na 16-bytowe części
def _convert_input(text_input, mode):
    converted_text = [] # Lista przechowująca podzielony tekst w częściach
    char_counter = 0 # Zmienna licząca który z kolei znak będzie w ciągu znaków
    char_line = "" # Zmienna do zapisywania ciągów znaków

    if mode == "hex":
        ## Pętla przechodząca przez całą długość tekstu
        ## potrzebna do podziału tekstu na części
        for text in text_input:
            # Zmiana znaku char na wartości heksową
            tmp = hex(ord(text))
            # Usuwania przedrostka 0x
            char_line += tmp[2:]
            # Dodanie wartości 1 do licznika
            char_counter += 1

            ## Warunek wykonywany gdy mamy ciąg bytów o długości 16
            # Podmienić stałą liczbę bloku n na zmienną odpowiadającą wybranej długości bloku przez użytkownika
            if(char_counter == 16):
                # Dodawanie ciągu znaków do tablicy
                converted_text.append(char_line)
                # czyszczenie zmiennej ze śmieci
                char_line = ""
                # zerowanie licznika
                char_counter = 0

        ## Wyjątek dla ciągów znaków które nie da się
        ## podzielić na równe części
        if(char_counter != 0):
            # Zapisywanie ilości potrzebnych bytów do równego podzielenia tekstu
            char_counter = 16 - char_counter
            # Dodanie bytu wskazującego koniec tekstu
            char_line += "2D"
            char_counter -= 1
            # Pętla powtarzana przez ilość potrzebnych bytów
            while char_counter != 0:
                # Dodawanie brakujących bytów
                tmp = os.urandom(1)
                tmp = tmp.hex()
                tmp = tmp[2:]
                if(tmp != "2D"):
                    char_line += tmp
                    char_counter -= 1
            # Dodawanie ciągu znaków do listy
            converted_text.append(char_line)

    elif mode == "str":
        while char_counter < (len(text_input) / 2):
            if text_input[char_counter * 2:(char_counter * 2) + 2] != "00":
                tmp = (int(text_input[char_counter * 2], 16) * 16) + int(text_input[(char_counter * 2) + 1], 16)
                
                char_tmp = chr(tmp)

                char_line += char_tmp
                char_counter += 1
            
            elif text_input[char_counter * 2:(char_counter * 2) + 2] == "00":
                char_counter = len(text_input)
        
        converted_text = char_line

        # tmp = False
        # char_line = -1
        # while tmp != True:
        #     if(converted_text[char_line] == "-"):
        #         converted_text = converted_text[:(len(converted_text) + char_line)]
        #         if(len(converted_text) + char_line == 0):
        #             tmp = True
        #     else:
        #         char_line -= 1

    return converted_text


def _organize_round_key(key_slice):
    resoult = ""

    for i in range(4):
        resoult += key_slice[i * 2:(i * 2) + 2]
        resoult += key_slice[(i * 2) + 8:(i * 2) + 10]
        resoult += key_slice[(i * 2) + 16:(i * 2) + 18]
        resoult += key_slice[(i * 2) + 24:(i * 2) + 26]
    
    return resoult


def _organize_data_in(data_in):
    resoult = ""

    for i in range(4):
        resoult += data_in[i * 2:(i * 2) + 2]
        resoult += data_in[(i * 2) + 8:(i * 2) + 10]
        resoult += data_in[(i * 2) + 16:(i * 2) + 18]
        resoult += data_in[(i * 2) + 24:(i * 2) + 26]
    
    return resoult
    

# stworzyć funkcję do otwierania tekstu orginalnego lub zaszyfrowanego, i zapisania konwersji