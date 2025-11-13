class Produto:
    def __init__(self, ean, descricao=None, estoque=0):
        self.ean = ean
        self.descricao = descricao
        self.estoque = estoque
        self.vendas = []

    def adiciona_venda(self, venda):
        self.vendas.append(venda)

    def vendas_total(self):
        total = 0
        for venda in self.vendas:
            total += venda.quantidade

        return total

    def __str__(self):
        return f"Produto(EAN={self.ean}, Desc={self.descricao}, Estoque={self.estoque}, Vendas={self.vendas_total()})"

    def __repr__(self):
        return self.__str__()
