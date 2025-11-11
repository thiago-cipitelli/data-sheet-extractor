import pandas as pd
from utils.helpers import (
    find_product, ean_valido, produto_unico, valida_coluna_estoque
)
from models.produto import Produto

variacoes_descricao = ["prod", "descrição", "desc"]
variacoes_estoque = ["disp", "dsp", "estoque", "total", "saldo"]
variacoes_codigo_barras = [
    "Codigo_Barra", "Código_Barra", "cod_barra", "cód barra", "cod barra",
    "codigo de barra", "código de barra", "cod. barra", "codbarra",
    "codigo_barra", "codigo_bar", "codbar", "EAN"
]

def get_column_name(df: pd.DataFrame, dictionary):
    colunas_lower = [col.lower() for col in dictionary]
    for col in df.columns:
        for possivel_col in colunas_lower:
            if possivel_col in str(col).lower():
                return col

def get_column_index(df: pd.DataFrame, dictionary):
    pattern = '|'.join([v.replace('.', r'\.') for v in dictionary])
    mask = df.apply(lambda col: col.astype(str).str.contains(pattern, case=False, na=False, regex=True))
    any_match = mask.any(axis=0)
    if not any_match.any():
        return -1
    column_index = mask.any(axis=0)[::-1].idxmax()
    return df.columns.get_loc(column_index)

def get_header_index(df: pd.DataFrame) -> int:
    pattern = '|'.join([v.replace('.', r'\.') for v in variacoes_codigo_barras])
    mask = df.apply(lambda col: col.astype(str).str.contains(pattern, case=False, na=False, regex=True))
    header_index = mask.any(axis=1)[::-1].idxmax()
    return header_index

def extract_products(file, sheet, produtos):
    errors = []
    df = pd.read_excel(file, sheet_name=sheet, header=None)
    df = df.ffill()

    header_index = get_header_index(df)
    df.columns = df.iloc[header_index]

    ean_column_name = get_column_name(df, variacoes_codigo_barras)
    if ean_column_name is None:
        return [f"não foi encontrado o EAN"]

    description_column_name = get_column_name(df, variacoes_descricao)
    estoque_column_name = get_column_name(df, variacoes_estoque)

    description_column_index = get_column_index(df, variacoes_descricao)
    estoque_column_index = get_column_index(df, variacoes_estoque)

    estoque_valido = valida_coluna_estoque(estoque_column_index, sheet)

    drop_header = header_index + 1
    df = df[drop_header:].reset_index(drop=True)

    for _, row in df.iterrows():
        ean = row.get(ean_column_name)
        if pd.notna(ean) and ean_valido(ean):
            if produto_unico(ean, produtos):
                produtos.append(Produto(ean, row[description_column_name], row[estoque_column_name]))
            else:
                if estoque_valido:
                    try:
                        prod = find_product(ean, produtos)
                        prod.estoque += int(row[estoque_column_name])
                    except Exception:
                        errors.append(f"Erro ao inserir estoque no produto {prod.descricao}")
                else:
                    errors.append(f"estoque inválido")

    return errors
