import argparse
import pandas as pd
from produto import Produto


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

def get_column(df: pd.DataFrame):
    colunas_lower = [col.lower() for col in variacoes_codigo_barras]

    for col in df.columns:
        for possivel_col in colunas_lower:
            if possivel_col in str(col).lower():
                return col


def get_header_index(df: pd.DataFrame):
    pattern = '|'.join([v.replace('.', r'\.') for v in variacoes_codigo_barras])
    mask = df.apply(lambda col: col.astype(str).str.contains(pattern, case=False, na=False, regex=True))
    header_index = mask.any(axis=1)[::-1].idxmax()
    return header_index

def produto_unico(ean: str, lista_prods: list[Produto]) -> bool:
    for prod in lista_prods:
        if prod.ean == ean:
            return False

    return True


def extract_products(file, sheet, produtos):
    df = pd.read_excel(file, sheet_name=sheet, header=None)
    header_index = get_header_index(df)
    df = pd.read_excel(file, sheet_name=sheet, header=header_index)
    ean_column = get_column(df)
    print(sheet)
    if not df.empty:
        print(ean_column)
        for index, row in df.iterrows():
            if not pd.isna(row[ean_column]) and produto_unico(row[ean_column], produtos):
                produtos.append(Produto(row[ean_column]))
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
