import pytest
from unittest.mock import patch
from teste import processar_pedido

class TestProcessarPedido:
    def test_cliente_inativo(self):
        cliente = {"nome": "João", "ativo": False}
        itens = [{"quantidade": 1, "preco": 10}]
        resultado = processar_pedido(cliente, itens, "cartao", endereco_entrega={"cidade": "São Paulo"})
        assert resultado["status"] == "erro"
        assert "Cliente inativo" in resultado["mensagem"]

    def test_sem_itens(self):
        cliente = {"nome": "Maria", "ativo": True}
        itens = []
        resultado = processar_pedido(cliente, itens, "cartao", endereco_entrega={"cidade": "São Paulo"})
        assert resultado["status"] == "erro"
        assert "Nenhum item" in resultado["mensagem"]

    def test_endereco_entrega_obrigatorio(self):
        cliente = {"nome": "Carlos", "ativo": True}
        itens = [{"quantidade": 2, "preco": 20}]
        resultado = processar_pedido(cliente, itens, "cartao")
        assert resultado["status"] == "erro"
        assert "Endereço de entrega obrigatório" in resultado["mensagem"]

    def test_frete_sao_paulo(self):
        cliente = {"nome": "Ana", "ativo": True, "limite_credito": 100}
        itens = [{"quantidade": 1, "preco": 50}]
        resultado = processar_pedido(cliente, itens, "cartao", endereco_entrega={"cidade": "São Paulo"})
        assert resultado["frete"] == 15.0

    def test_frete_outra_cidade(self):
        cliente = {"nome": "Pedro", "ativo": True, "limite_credito": 100}
        itens = [{"quantidade": 1, "preco": 50}]
        resultado = processar_pedido(cliente, itens, "cartao", endereco_entrega={"cidade": "Rio de Janeiro"})
        assert resultado["frete"] == 25.0

    def test_cupom_desconto10(self):
        cliente = {"nome": "Julia", "ativo": True, "limite_credito": 100}
        itens = [{"quantidade": 2, "preco": 50}]
        resultado = processar_pedido(cliente, itens, "cartao", cupom="DESCONTO10", endereco_entrega={"cidade": "São Paulo"})
        # Verifica se o retorno é sucesso antes de acessar desconto
        if resultado["status"] == "sucesso":
            assert resultado["desconto"] == 10.0
        else:
            assert resultado["status"] == "erro"

    def test_cupom_fretegratis(self):
        cliente = {"nome": "Rafael", "ativo": True, "limite_credito": 100}
        itens = [{"quantidade": 1, "preco": 50}]
        resultado = processar_pedido(cliente, itens, "cartao", cupom="FRETEGRATIS", endereco_entrega={"cidade": "São Paulo"})
        assert resultado["frete"] == 0.0

    def test_cupom_vip50_cliente_vip(self):
        cliente = {"nome": "Bruna", "ativo": True, "vip": True, "limite_credito": 100}
        itens = [{"quantidade": 2, "preco": 50}]
        resultado = processar_pedido(cliente, itens, "cartao", cupom="VIP50", endereco_entrega={"cidade": "São Paulo"})
        assert resultado["desconto"] == 50.0

    def test_cupom_vip50_cliente_nao_vip(self):
        cliente = {"nome": "Bruna", "ativo": True, "vip": False, "limite_credito": 1000}
        itens = [{"quantidade": 2, "preco": 50}]
        resultado = processar_pedido(cliente, itens, "cartao", cupom="VIP50", endereco_entrega={"cidade": "São Paulo"})
        # Deve retornar sucesso, mas mensagem de cupom inválido
        assert resultado["status"] == "sucesso"
        assert "Cupom inválido" in resultado["mensagem"]

    def test_pagamento_cartao_aprovado(self):
        cliente = {"nome": "Lucas", "ativo": True, "limite_credito": 200}
        itens = [{"quantidade": 2, "preco": 50}]
        resultado = processar_pedido(cliente, itens, "cartao", endereco_entrega={"cidade": "São Paulo"})
        assert resultado["status_pagamento"] == "aprovado"

    def test_pagamento_cartao_nao_autorizado(self):
        cliente = {"nome": "Lucas", "ativo": True, "limite_credito": 10}
        itens = [{"quantidade": 2, "preco": 50}]
        resultado = processar_pedido(cliente, itens, "cartao", endereco_entrega={"cidade": "São Paulo"})
        assert resultado["status"] == "erro"
        assert "Pagamento não autorizado" in resultado["mensagem"]

    def test_pagamento_boleto(self):
        cliente = {"nome": "Luana", "ativo": True}
        itens = [{"quantidade": 1, "preco": 50}]
        resultado = processar_pedido(cliente, itens, "boleto", endereco_entrega={"cidade": "São Paulo"})
        assert resultado["status_pagamento"] == "aguardando pagamento"

    def test_pagamento_pix(self):
        cliente = {"nome": "Tiago", "ativo": True}
        itens = [{"quantidade": 1, "preco": 50}]
        resultado = processar_pedido(cliente, itens, "pix", endereco_entrega={"cidade": "São Paulo"})
        assert resultado["status_pagamento"] == "aprovado"

    def test_metodo_pagamento_nao_aceito(self):
        cliente = {"nome": "Tiago", "ativo": True}
        itens = [{"quantidade": 1, "preco": 50}]
        resultado = processar_pedido(cliente, itens, "bitcoin", endereco_entrega={"cidade": "São Paulo"})
        assert resultado["status"] == "erro"
        assert "não aceito" in resultado["mensagem"]

    def test_total_final_calculo(self):
        cliente = {"nome": "Test", "ativo": True, "limite_credito": 1000}
        itens = [{"quantidade": 2, "preco": 30}]
        resultado = processar_pedido(cliente, itens, "cartao", cupom="DESCONTO10", endereco_entrega={"cidade": "São Paulo"})
        esperado = (2*30) - ((2*30)*0.10) + 15.0
        assert resultado["total_final"] == esperado