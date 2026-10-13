import aesMath
import aesTools
import math

def _first_run(data_in, data_key):
    dataFile = aesTools._organize_data_in(data_in)
    key = aesTools._organize_round_key(data_key)
    state = aesMath._xor_string(dataFile, key)

def _cipher_text(data_in, data_key, main_rounds):
    # Zmiana kolejności znaków tekstu zgodnych z macierzą
    dataFile = [aesTools._organize_data_in(data_in[0])]
    # Zmiana kolejności znaków klucza zgodnych z macierzą
    key = aesTools._organize_round_key(data_key)
    # Dodawanie klucza do zmiennej state
    state = [aesMath._xor_string(dataFile[0], key)]
    round = 1

    while round < len(data_in):
        dataFile.append(aesMath._xor_string(state[round - 1], aesTools._organize_data_in(data_in[round])))
    
    return dataFile