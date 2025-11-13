import argparse
import pandas as pd
from tqdm import tqdm
from extractor.produto_extractor import extract_products
from models.produto import Produto
from utils.normalizacao import normalizar_mes

def main():
    parser = argparse.ArgumentParser(description="Extrai produtos de um arquivo Excel")
    parser.add_argument("arquivo", help="Caminho do arquivo Excel")
    args = parser.parse_args()

    excel_file = pd.ExcelFile(args.arquivo)
    sheets = excel_file.sheet_names
    produtos = []
    vendas = []
    errors = {}

    for sheet in tqdm(sheets):
        sheet_errors = extract_products(args.arquivo, sheet, produtos, vendas)
        if sheet_errors:
            errors[sheet] = sheet_errors

    print(f"\n{len(errors)} erros encontrados:")
    for nome, erro_lista in errors.items():
        print(f"\n{nome}:")
        for e in erro_lista:
            print("  -", e)

    print(f"\n{len(produtos)} produtos encontrados:")
    for p in produtos:
        print(p)

if __name__ == "__main__":
    main()
