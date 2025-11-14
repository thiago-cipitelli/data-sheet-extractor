import pytest
from src.models.produto import Produto
from src.models.venda_mensal import VendaMensal


@pytest.fixture
def produto_mock():
    return Produto(ean="1234567890123")


def test_cria_venda_mensal_valida(produto_mock):
    venda = VendaMensal(produto=produto_mock, ano=2024, mes=5, quantidade=10)
    assert venda.produto.ean == "1234567890123"
    assert venda.ano == 2024
    assert venda.mes == 5
    assert venda.quantidade == 10


@pytest.mark.parametrize("mes", [0, 13, -1, 100])
def test_mes_invalido(produto_mock, mes):
    with pytest.raises(ValueError):
        VendaMensal(produto=produto_mock, ano=2024, mes=mes, quantidade=10)


@pytest.mark.parametrize("quantidade", [-1, -10])
def test_quantidade_negativa(produto_mock, quantidade):
    with pytest.raises(ValueError):
        VendaMensal(produto=produto_mock, ano=2024, mes=5, quantidade=quantidade)


def test_quantidade_tipo_invalido(produto_mock):
    with pytest.raises(ValueError):
        VendaMensal(produto=produto_mock, ano=2024, mes=5, quantidade="10")


def test_str_venda_mensal(produto_mock):
    venda = VendaMensal(produto=produto_mock, ano=2024, mes=8, quantidade=3)
    assert str(venda) == "VendaMensal(1234567890123, 8/2024, qtd=3)"
