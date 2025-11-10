class VendaMensal:
    def __init__(self, produto, ano, mes, quantidade):
        self.produto = produto
        self.ano = ano
        self.mes = mes
        self.quantidade = quantidade

    def __str__(self):
        return f"VendaMensal({self.produto.ean}, {self.mes}/{self.ano}, qtd={self.quantidade})"

    def __repr__(self):
        return self.__str__()
