import pytest
from utils.normalizacao import *


def test_remove_numeros_e_simbolos():
    assert remove_numeros_e_simbolos("123teste ./23@teste") == "teste teste"


def test_remove_letras():
    assert remove_letras("123teste ./23@teste") == "123 ./23@"

def test_extrai_data_mes_ano():
    assert extrai_data_mes_ano("Un. 11/25") == "11/25"

def test_normalizar_mes():
    assert normalizar_mes("Un. 11/25") == 11
    assert normalizar_mes("nov") == 11
    assert normalizar_mes("novembro") == 11
    assert normalizar_mes("nov/25") == 11
    assert normalizar_mes("teste nov-24") == 11
    assert normalizar_mes("teste novembrorogo") == None

