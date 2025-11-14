from dataclasses import dataclass, field
from typing import List
from models.venda_mensal import VendaMensal

@dataclass
class Produto:
    ean: str
    descricao: str | None = None
    estoque: int = 0
    vendas: List[VendaMensal] = field(default_factory=list)

    def __post_init__(self):
        
        if not isinstance(self.ean, str):
            raise TypeError("EAN deve ser uma string")

        if not self.ean.isdigit():
            raise ValueError("EAN deve conter apenas numeros")

        if len(self.ean) != 13:
            raise ValueError("EAN deve ter exatamente 13 digitos")

        if self.estoque < 0:
            raise ValueError("Estoque nao pode ser negativo")


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
