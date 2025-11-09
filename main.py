import argparse
import pandas as pd
from produto import Produto


# refatorar codigo para pegar o estoque
# lembrar de procurar sempre o ultima aparicao na linha (ultima cedula)
#TODO:  integrar com API para buscar o nome certo do produto pelo EAN (https://www.ean-search.org/)
#ATENCAO: nem todos os produtos aparecem no ean


variacoes_descricao = [
    "prod",
    "descrição",
    "desc"
]

variacoes_estoque = [
    "disp",
    "dsp",
    "estoque",
    "total",
    "saldo"
]

variacoes_codigo_barras = [
    "Codigo_Barra",
    "Código_Barra",
    "cod_barra",
    "cód barra",
    "cod barra",
    "codigo de barra",
    "código de barra",
    "cod. barra",
    "codbarra",
    "codigo_barra",
    "codigo_bar",
    "codbarra",
    "codbar",
    "EAN"
]

def find_product(ean: str, lista_prods: list[Produto]):
    for prod in lista_prods:
        if int(prod.ean) == int(ean):
            return prod


def get_column_index(df: pd.DataFrame, dictionary):
    pattern = '|'.join([v.replace('.', r'\.') for v in dictionary])
    mask = df.apply(lambda col: col.astype(str).str.contains(pattern, case=False, na=False, regex=True))
    column_index = mask.any(axis=0)[::-1].idxmax()
    
    any_match = mask.any(axis=0)
    if not any_match.any():
        return -1

    return df.columns.get_loc(column_index)


def get_column_name(df: pd.DataFrame, dictionary):
    colunas_lower = [col.lower() for col in dictionary]

    for col in df.columns:
        for possivel_col in colunas_lower:
            if possivel_col in str(col).lower():
                return col


def get_header_index(df: pd.DataFrame) -> int:
    pattern = '|'.join([v.replace('.', r'\.') for v in variacoes_codigo_barras])
    mask = df.apply(lambda col: col.astype(str).str.contains(pattern, case=False, na=False, regex=True))
    header_index = mask.any(axis=1)[::-1].idxmax()

    return header_index


def ean_valido(ean: str) -> bool:
    if str(ean).isdigit() and len(str(ean)) > 12:
        return True

    return False


def produto_unico(ean: str, lista_prods: list[Produto]) -> bool:
    if find_product(ean, lista_prods):
        return False

    return True

def valida_coluna_estoque(column_index: int, sheet: str) -> bool:
    if column_index == -1:
        print(f"coluna Estoque faltando na planilha {sheet}")
        return False

    return True


def extract_products(file, sheet, produtos):
    df = pd.read_excel(file, sheet_name=sheet, header=None)
    df = df.ffill()

    header_index = get_header_index(df)
    df.columns = df.iloc[header_index]

    ean_column_name = get_column_name(df, variacoes_codigo_barras)

    if ean_column_name is None:
        print(f"nao foi encontrado o EAN da planilha {sheet}")
        return

    description_column_name = get_column_name(df, variacoes_descricao)
    estoque_column_name = get_column_name(df, variacoes_estoque)

    description_column_index = get_column_index(df, variacoes_descricao)
    estoque_column_index = get_column_index(df, variacoes_estoque)

    estoque_valido = valida_coluna_estoque(estoque_column_index, sheet)

    cols = df.columns.tolist()
    cols[estoque_column_index] = estoque_column_name
    cols[description_column_index] = description_column_name
    df.columns = cols

    drop_header = header_index + 1
    df = df[drop_header:].reset_index(drop=True)

    print(sheet)
    for index, row in df.iterrows():
        if not pd.isna(row[ean_column_name]) and ean_valido(row[ean_column_name]):
            if produto_unico(row[ean_column_name], produtos):
                produtos.append(Produto(row[ean_column_name], row[description_column_name], row[estoque_column_name]))
            else:
                if estoque_valido:
                    try:
                        prod = find_product(row[ean_column_name], produtos)
                        prod.estoque += int(row[estoque_column_name])
                    except Exception as e:
                        print(f"Erro ao inserir estoque no produto {prod.descricao} na planilha {sheet}")
                else:
                    print("estoque invalido")


def main():
    parser = argparse.ArgumentParser(description="Extrai produtos de um arquivo Excel")
    parser.add_argument("arquivo", help="caminho do arquivo Excel")
    args = parser.parse_args()

    excel_file = pd.ExcelFile(args.arquivo)
    sheets = excel_file.sheet_names
    produtos = []

    for sheet in sheets:
        extract_products("mapa.xlsx", sheet, produtos)

    print(f"{len(produtos)} produtos encontrados")
    for p in produtos:
        print(p)


if __name__ == "__main__":
    main()
