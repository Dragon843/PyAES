import operator
import lookUps
import math


# Funkcja zmieniająca miejscami znaki hexowe w kluczu
def _rotation_word(text_in, mode):
    # Inicjalizacja zmiennej string dla przesuniętych znaków hexowych w kluczu
    text_new = "" 

    # Warunek if oznaczający tryb działania dla cipher lub invers cipher
    if mode == "left": # Dla Cipher
        text_new = str(text_in[2:8]) + str(text_in[:2]) # Przesunięcie dwóch pierwszych znaków na koniec stringa
    elif mode == "right": # Dla Invers Cipher
        text_new = str(text_in[6:8]) + str(text_in[:6]) # Przesunięcie dwóch ostatnich znaków na początek stringa

    return text_new

# Funkcja zmieniająca miejscami znaki hexowe w tekście
def _shift_rows(text_in, mode):
    # Inicjalizacja zmiennej string dla przesuniętych znaków hexowych w tekście i dodanie pierwszej części niezmienionego tekstu
    text_new = ""
    t = 0

    # Pętla przechodząca przez każdy wiersz
    while t < 4:
        # Przesuniecie bajtu o jedno, drugie i trzecie miejsce
        ## Rozbite dla lepszej czytelności
        if mode == "left" and t != 0: # Dla Cipher
            text_new += str(text_in[(t * 8) + (t * 2):(t * 8) + 8])
            text_new += str(text_in[(t * 8):(t * 8) + (t * 2)])
        elif mode == "right" and t != 0: # Dla Invers Cipher
            text_new += str(text_in[(t * 8) + (8 - (t * 2)):(t * 8) + 8])
            text_new += str(text_in[(t * 8):(t * 8) + (8 - (t * 2))])
        elif t == 0:
            text_new = str(text_in[:8])

        t += 1
    
    return text_new    


# Funkcja wykonująca działanie xor
def _xor_string(to_convert, variable):
    # Wykonanie dodawania pierścienia
    converted = to_convert

    try:
        converted = operator.xor(converted, variable)
    except:
        converted = int(converted, 16)
    else:
        print("good")
    
    try:
        converted = operator.xor(converted, variable)
    except:
        variable = int(variable, 16)
    else:
        print("good")

    converted = operator.xor(converted, variable)
    # Zmiana z liczb całkowitych na liczby heksowe
    converted = hex(converted)
    # Usuwanie znaku heksowego '0x'
    converted = converted[2:]
    #print(to_convert, variable, converted)

    ## Warunek porawiający wyjątek przy 0x0m gdzie m to dowolna liczba w systemie szesnastkowym
    ## Wynika to ze sposobu zapisu liczb, gdzie 0 nie jest zapisywane jako miejsce na dalszy ciąg liczbowy

    for i in range(2):
        # Dodawanie miejsca 0 dla wartości o długości 32-heksowej
        if(len(converted) < 32 and len(converted) > 8):
            converted = "0" + converted
        # Dodawanie miejsca 0 dla wartości o długości 8-heksowej
        elif(len(converted) < 8 and len(converted) > 2):
            converted = "0" + converted
        # Dodawanie miejsca 0 dla wartości o długości 2-heksowej
        elif(len(converted) < 2 and len(converted) > 0):
            converted = "0" + converted

    return converted


# Funkcja zmieniająca bajt w kluczu na wartość z tablicy Sbox 
def _sub_word(key_in):
    # Inicjalizacja zmiennej przechowującej klucz po transformacji
    key_new = "" 

    ## Bierze wartość liczbową bajta i podmienia nową wartością z tablicy
    ## jedno wymiarowej, gdzie wartość liczbowa bajta wskazuje na miejsce
    ## w tablicy Sbox 
    for key_round in range(4):
        # Zmiana liczb heksowych na liczby całkowite, wskazujące miejsce
        # w tablicy Sbox
        try:
            tmp = (int(key_in[(key_round * 2)],16) * 16) + int(key_in[(key_round * 2) + 1],16)
        except:
            tmp = 0
        # Zapisanie wartości z tablicy Sbox do zmiennej tmp
        tmp = lookUps.Sbox[tmp]
        # Zmienna przechowująca nowe wartości z tablicy Sbox
        key_new += tmp

    return key_new


# Funkcja zmieniająca bajty tekstu na wartości z tablicy Sbox
def _sub_byte(text_in, mode):
    table = [] # Lista do przechowywania wartości cipher_ax lub cipher_inv_ax
    text_new = "" # Zmienna do przechowywania tekstu wejściowego po transformacji
    t = 0

    # Przypisanie wartości z listy Sbox lub Sbox_inv
    if(mode == "normal"):
        table.extend(lookUps.Sbox)
    elif(mode == "invers"):
        table.extend(lookUps.Sbox_inv)

    ## Bierze wartość liczbową bajta i podmienia nową wartością z tablicy
    ## jedno wymiarowej, gdzie wartość liczbowa bajta wskazuje na miejsce
    ## w tablicy Sbox, dla każdego bajta tekstu
    while t < 16:
        # Zmiana liczb heksowych na liczby całkowite, wskazujące miejsce
        # w tablicy Sbox
        try:
            tmp = (int(text_in[t * 2],16)*16) + int(text_in[(t *2 )+1],16)
        except:
            tmp = 0
        # Zapisanie wartości z tablicy Sbox do zmiennej tmp
        tmp = table[tmp]
        # Zmienna przechowująca nowe wartości z tablicy Sbox
        text_new += tmp

        t += 1

    return text_new


## Funkcja przeprowadzająca mnożenie przez macierze
def _mix_columns(text_in, mode):
    table = []
    multiplier = []
    result = "" # zmienna przechowująca szyfrowany tekst
    number = text_in # zmienna przechowująca ciąg znaków tekstu
    tmp_x = 0 # Zmienna tymczasowa do zapisywania obliczeń
    tmp_y = 0 # Zmienna tymczasowa do zapisywania obliczeń
    round = 0 # Zmienna zpisująca wartość aktualnej rundy

    # Przypisanie wartości z listy cipher_ax lub cipher_inv_ax
    if(mode == "normal"):
        multiplier.extend(lookUps.Cipher_ax)
    elif(mode == "invers"):
        multiplier.extend(lookUps.Cipher_inv_ax)

    # Obliczanie mnożenia macierzy bytowej tekstu z macierzą x^4 + 1
    ## Przechodzi przez każdy element listy i mnoży zgodznie z zasadą działań na macierzach
    for round in range(16):
        ## Przypisywanie wartości byta tekstu do tmp_x,
        ## wykonywanie mnożenia tmp_x z jedynm bajtem ciągu wielomianu a(x),
        ## gdzie a(x)={03}x^3 + {01}x^2 + {01}x + {02},
        ## dodawanie wartości tmp_y z tmp_x
        # mnożenie wartości bajtowej number[(round * 2) % 8:((round * 2) % 8) + 2] 
        # z multiplier(0 - (round) / 4)
        tmp_x = number[(round * 2) % 8:((round * 2) % 8) + 2]
        tmp_y = xTime(tmp_x, multiplier[int(0 - (round / 4))])
        tmp_x = ""

        # mnożenie wartości bajtowej number[((round * 2) % 8) + 8:((round * 2) % 8) + 10] 
        # z multiplier[int(0 - (round / 4)) + 1])
        tmp_x = number[((round * 2) % 8) + 8:((round * 2) % 8) + 10]
        tmp_x = xTime(tmp_x, multiplier[int(0 - (round / 4)) + 1])
        tmp_y = operator.xor(tmp_x, tmp_y)
        
        # mnożenie wartości bajtowej number[((round * 2) % 8) + 16:((round * 2) % 8) + 18] 
        # z multiplier[int(0 - (round / 4)) + 2])
        tmp_x = number[((round * 2) % 8) + 16:((round * 2) % 8) + 18]
        tmp_x = xTime(tmp_x, multiplier[int(0 - (round / 4)) + 2])
        tmp_y = operator.xor(tmp_x, tmp_y)

        # mnożenie wartości bajtowej number[((round * 2) % 8) + 24:((round * 2) % 8) + 26] 
        # z multiplier[int(0 - (round / 4)) + 3])
        tmp_x = number[((round * 2) % 8) + 24:((round * 2) % 8) + 26]
        tmp_x = xTime(tmp_x, multiplier[int(0 - (round / 4)) + 3])
        tmp_y = operator.xor(tmp_x, tmp_y)
        
        ## Działania usuwające przedrostek 0x i zapisujące wartość końcową do result
        if(tmp_y >= 16):
            tmp_y = hex(tmp_y)
            result += tmp_y[2:]
        elif(tmp_y < 16):
            tmp_y = hex(tmp_y)
            result += "0" + tmp_y[2:]

    return result


# Funkcja przeprowadzająca mnożenie w ciałach skończonych
def xTime(number, multiplier):
    # Wartość wejściowa multiplier
    x_time = multiplier
    # Licznik mnożenia wartości x1
    y_time = 1
    result = 0

    # Sprawdza czy wartość wejściowa jest różna od 0
    try:
        x1 = int(number, 16)
    # Zmień wartość x_time na 0
    except:
        x_time = 0

    # Pętla przeprowadzająca mnożenie w ciałach skończonych
    while(x_time != 0):
        # Ustawia x_time na 0 gdy dla mnożenia przez 0
        if(number == 0):
            result = 0
            x_time == 0
        # Jeżeli x_time jest nieparzysty, dodajemy tą nieparzystość do wyniku
        elif(x_time % 2 == 1 and x_time != 0):
            result = int(number,16)
            x_time -= 1
        # Jeżeli wartość y_time jest mniejszy/równy od x_time
        # i x_time jest różne od 0 to robimy przesunięcie bitowe
        # zmiennej x1
        elif(y_time * 2 <= x_time and x_time != 0):
            x1 = x1 * 2
            # Jeżeli x1 jest większy niż wielomian GF(8) to przeprowadzamy
            # XOR x^8 + x^4 + x^3 + x + 1
            if(x1 >= 256):
                x1 = operator.xor(x1, 283)
            y_time *= 2
        # Jeżeli wartość y_time jest większy/równy od x_time,
        # x_time jest różne od 0 i resoult != 0
        # to przeprowadzamy operacje XOR dla resoult i x1
        elif(y_time * 2 >= x_time and x_time != 0 and result != 0):
            result = operator.xor(result, x1)
            x1 = int(number,16)
            x_time -= y_time
            y_time = 1
        # Jeżeli wartość y_time jest większy/równy od x_time,
        # x_time jest różne od 0 i resoult == 0
        # to przeprowadzamy operacje XOR dla resoult i x1 i kończymy obliczenia
        elif(y_time * 2 >= x_time and x_time != 0 and result == 0):
            result += x1
            x1 = int(number,16)
            x_time -= y_time
            y_time = 1

    return result
