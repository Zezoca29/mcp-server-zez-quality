from datetime import datetime

def processar_pedido(cliente, itens, metodo_pagamento, cupom=None, endereco_entrega=None):
    """
    Função grande de exemplo para processar um pedido.
    Possui múltiplas variáveis intermediárias e vários retornos possíveis.
    """

    # Variáveis iniciais
    total_itens = sum(item["quantidade"] for item in itens)
    subtotal = sum(item["quantidade"] * item["preco"] for item in itens)
    desconto = 0.0
    status_pagamento = "pendente"
    data_criacao = datetime.now()
    mensagem = ""
    taxa_frete = 0.0

    # Validações iniciais
    if not cliente.get("ativo", False):
        return {
            "status": "erro",
            "mensagem": "Cliente inativo. Não é possível processar pedido.",
            "data": data_criacao
        }

    if total_itens == 0:
        return {
            "status": "erro",
            "mensagem": "Nenhum item no pedido.",
            "data": data_criacao
        }

    # Regras de frete
    if endereco_entrega:
        if endereco_entrega.get("cidade") == "São Paulo":
            taxa_frete = 15.0
        else:
            taxa_frete = 25.0
    else:
        return {
            "status": "erro",
            "mensagem": "Endereço de entrega obrigatório.",
            "data": data_criacao
        }

    # Aplicar cupom de desconto
    if cupom:
        if cupom == "DESCONTO10":
            desconto = subtotal * 0.10
        elif cupom == "FRETEGRATIS":
            taxa_frete = 0.0
        elif cupom == "VIP50" and cliente.get("vip", False):
            desconto = subtotal * 0.50
        else:
            mensagem = "Cupom inválido ou não aplicável."

    # Total final
    total = subtotal - desconto + taxa_frete

    # Processar pagamento
    if metodo_pagamento == "cartao":
        if total > 0 and cliente.get("limite_credito", 0) >= total:
            status_pagamento = "aprovado"
            cliente["limite_credito"] -= total
        else:
            return {
                "status": "erro",
                "mensagem": "Pagamento não autorizado no cartão.",
                "total": total,
                "data": data_criacao
            }
    elif metodo_pagamento == "boleto":
        status_pagamento = "aguardando pagamento"
    elif metodo_pagamento == "pix":
        status_pagamento = "aprovado"
    else:
        return {
            "status": "erro",
            "mensagem": f"Método de pagamento '{metodo_pagamento}' não aceito.",
            "data": data_criacao
        }

    # Retorno final do pedido
    return {
        "status": "sucesso",
        "cliente": cliente["nome"],
        "total_itens": total_itens,
        "subtotal": subtotal,
        "desconto": desconto,
        "frete": taxa_frete,
        "total_final": total,
        "status_pagamento": status_pagamento,
        "mensagem": mensagem,
        "data": data_criacao
    }
