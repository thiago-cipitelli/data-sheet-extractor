import pytest
from src.models.produto import Produto
from src.models.venda_mensal import VendaMensal



def test_produto_criacao_valida():
    p = Produto("1234567890123", "Produto X", 10)

    assert p.ean == "1234567890123"
    assert p.descricao == "Produto X"
    assert p.estoque == 10
    assert p.vendas == []



def test_produto_ean_nao_string():
    with pytest.raises(TypeError):
        Produto(1234567890123, "Produto X", 10)


def test_produto_ean_com_caracteres_invalidos():
    with pytest.raises(ValueError):
        Produto("12345678901A3", "Produto X", 10)


def test_produto_ean_tamanho_errado():
    with pytest.raises(ValueError):
        Produto("1234", "Produto X", 10)



def test_produto_estoque_nao_numerico():
    with pytest.raises(TypeError):
        Produto("1234567890123", "Produto X", "dez")


def test_produto_estoque_negativo():
    with pytest.raises(ValueError):
        Produto("1234567890123", "Produto X", -5)


def test_produto_adiciona_venda():
    p = Produto("1234567890123", "Produto X", 10)
    v1 = VendaMensal(p, 2024, 5, 30)

    p.adiciona_venda(v1)

    assert len(p.vendas) == 1
    assert p.vendas[0].quantidade == 30


def test_produto_vendas_total():
    p = Produto("1234567890123", "Produto X", 10)

    v1 = VendaMensal(p, 2024, 5, 30)
    v2 = VendaMensal(p, 2024, 6, 20)

    p.adiciona_venda(v1)
    p.adiciona_venda(v2)

    assert p.vendas_total() == 50


def test_produto_str():
    p = Produto("1234567890123", "Produto X", 10)

    v1 = VendaMensal(p, 2024, 5, 30)
    p.adiciona_venda(v1)

    texto = str(p)

    assert "1234567890123" in texto
    assert "Produto X" in texto
    assert "Estoque=10" in texto
    assert "Vendas=30" in texto
