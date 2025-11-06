import argparse
import pandas as pd
from produto import Produto


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

def get_column(df: pd.DataFrame, dictionary):
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
    for prod in lista_prods:
        try:
            if int(prod.ean) == int(ean):
                return False
        except (ValueError, TypeError):
            continue

    return True


def extract_products(file, sheet, produtos):
    df = pd.read_excel(file, sheet_name=sheet, header=None)
    df = df.ffill()

    header_index = get_header_index(df)
    df.columns = df.iloc[header_index]
    drop_header = header_index + 1
    df = df[drop_header:].reset_index(drop=True)

    ean_column = get_column(df, variacoes_codigo_barras)
    description_column = get_column(df, variacoes_descricao)
    estoque_column = get_column(df, variacoes_estoque)

    if not df.empty:
        for index, row in df.iterrows():
            if not pd.isna(row[ean_column]) and ean_valido(row[ean_column]) and produto_unico(row[ean_column], produtos):
                produtos.append(Produto(row[ean_column], row[description_column], row[estoque_column]))
    else:
        print(f"nao foi encontrado o EAN da sheet {sheet}")


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
