from dataclasses import dataclass, field
from typing import List

@dataclass
class VendaMensal:
    produto: "Produto"
    ano: int | None
    mes: int
    quantidade: int

    def __post_init__(self):
        if not (1 <= self.mes <= 12):
            raise ValueError("Mês precisa estar entre 1 e 12.")
            
        if not isinstance(self.quantidade, int) or self.quantidade < 0:
            raise ValueError("Quantidade deve ser inteiro >= 0")

    def __str__(self):
        return f"VendaMensal({self.produto.ean}, {self.mes}/{self.ano}, qtd={self.quantidade})"
