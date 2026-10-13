import aesMath
import aesTools
import lookUps
import math


def _cipher_text(data_in, data_key, main_rounds):
    # Zmiana kolejności znaków tekstu zgodnych z macierzą
    state = aesTools._organize_data_in(data_in)
    # Łaczenie fragmentów klucza rundy w jedną całość
    key = data_key[0] + data_key[1] + data_key[2] + data_key[3]
    # Zmiana kolejności znaków klucza zgodnych z macierzą
    key = aesTools._organize_round_key(key)
    # Dodawanie klucza do zmiennej state
    state = aesMath._xor_string(state, key)
    round = 1

    while round < main_rounds:
        # Zmiana stringa na intiger w zmiennej key
        key = data_key[round * 4] + data_key[(round * 4) + 1] + data_key[(round * 4) + 2] + data_key[(round * 4) + 3]
        key = aesTools._organize_round_key(key)
        state = aesMath._sub_byte(state, "normal")
        state = aesMath._shift_rows(state, "left")
        state = aesMath._mix_columns(state, "normal")
        state = aesMath._xor_string(state, key)
        round += 1

    # Fragment kodu wykonujący ostatnią rundę szyfrowania
    state = aesMath._sub_byte(state, "normal")
    state = aesMath._shift_rows(state, "left")
    # Zmiana stringa na intiger w zmiennej key
    key = data_key[-4] + data_key[-3] + data_key[-2] + data_key[-1]
    key = aesTools._organize_round_key(key)
    state = aesMath._xor_string(state, key)
    
    return state

def _inv_cipher_text(data_in, data_key, main_rounds):
    # Zmiana stringa na integer w zmiennej state
    state = data_in
    # Łaczenie fragmentów klucza rundy w jedną całość
    key = data_key[-4] + data_key[-3] + data_key[-2] + data_key[-1]
    # Zmiana kolejności znaków klucza zgodnych z macierzą
    key = aesTools._organize_round_key(key)

    # Dodawanie klucza do zmiennej state
    state = aesMath._xor_string(state, key)
    state = aesMath._shift_rows(state,"right")
    state = aesMath._sub_byte(state, "invers")

    round = main_rounds - 1

    while round > 0:
        # Zmiana stringa na intiger w zmiennej key
        key = data_key[round * 4] + data_key[(round * 4) + 1] + data_key[(round * 4) + 2] + data_key[(round * 4) + 3]
        key = aesTools._organize_round_key(key)

        state = aesMath._xor_string(state, key)
        state = aesMath._mix_columns(state, "invers")
        state = aesMath._shift_rows(state, "right")
        state = aesMath._sub_byte(state, "invers")
        
        round -= 1

    # Zmiana stringa na intiger w zmiennej key
    key = data_key[0] + data_key[1] + data_key[2] + data_key[3]
    key = aesTools._organize_round_key(key)
    state = aesMath._xor_string(state, key)

    state = aesTools._organize_data_in(state)
    
    return state