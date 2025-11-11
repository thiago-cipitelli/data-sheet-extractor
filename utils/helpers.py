import pandas as pd
from models.produto import Produto

def find_product(ean: str, lista_prods: list[Produto]):
    for prod in lista_prods:
        if int(prod.ean) == int(ean):
            return prod

def ean_valido(ean: str) -> bool:
    return str(ean).isdigit() and len(str(ean)) > 12

def produto_unico(ean: str, lista_prods: list[Produto]) -> bool:
    return find_product(ean, lista_prods) is None

def valida_coluna_estoque(column_index: int, sheet: str) -> bool:
    if column_index == -1:
        print(f"Coluna Estoque faltando na planilha {sheet}")
        return False
    return True
