class Produto:
    def __init__(self, ean, descricao=None, estoque=0):
        self.ean = ean
        self.descricao = descricao
        self.estoque = estoque
        self.vendas = []

    def adicionar_venda(self, venda):
        self.vendas.append(venda)

    def __str__(self):
        return f"Produto(EAN={self.ean}, Desc={self.descricao}, Estoque={self.estoque})"

    def __repr__(self):
        return self.__str__()
