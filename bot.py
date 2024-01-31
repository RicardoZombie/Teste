import telebot

# Chave API do bot
CHAVE_API = "5564553228:AAFZlf_ubLFKHFgWTejgAj23JKaxAW-3Rc0"

# Inicializar o bot do Telegram
bot = telebot.TeleBot(CHAVE_API)

# Função para calcular a tarifa com base no peso e região
def calcular_tarifa(peso):
    # Tabela de tarifas para outras regiões
    tarifas_outras_regioes = {"0-249g": 17.45, "250g-500g": 18.45, "500g-1kg": 19.45, "1kg-2kg": 19.95,
                              "2kg-3kg": 23.45, "3kg-4kg": 24.95, "4kg-5kg": 27.95, "5kg-6kg": 33.95,
                              "6kg-7kg": 35.95, "7kg-8kg": 36.95, "8kg-9kg": 46.95, "9kg-10kg": 57.45,
                              "kg-adicional": 3.50}

    # Obter a faixa de peso correspondente
    faixa_peso = next((key for key in tarifas_outras_regioes if key.startswith(str(peso))), None)

    if faixa_peso is not None:
        # Calcular a tarifa com base no peso
        tarifa = tarifas_outras_regioes[faixa_peso]
        return tarifa
    else:
        # Caso o peso não esteja em nenhuma faixa conhecida
        return 0.0

@bot.message_handler(commands=["start"])
def iniciar(mensagem):
    bot.send_message(mensagem.chat.id, "🚀 **Bem-vindo ao Bot de Precificação da Amazon!**\nEste bot foi desenvolvido por Ricardo Barbosa.\n\nPara começar, use /calcular_preco")

@bot.message_handler(commands=["calcular_preco"])
def calcular_preco(mensagem):
    bot.send_message(mensagem.chat.id, "📦 **Calculando Preço de Venda:**\n\nEnvie o valor que você paga no site do fornecedor:")
    bot.register_next_step_handler(mensagem, obter_custo_fornecedor)

def obter_custo_fornecedor(mensagem):
    try:
        # Substituído ',' por '.' e convertido para float
        custo_fornecedor = float(mensagem.text.replace(',', '.'))
        tarifa_fixa_amazon = 5.50
        tarifa_personalizada_amazon = 0

        preco_venda = custo_fornecedor
        comissao_amazon = 0
        lucro_venda = 0

        bot.send_message(mensagem.chat.id, "🚀 **Informe o ROI desejado (%):**")
        bot.register_next_step_handler(mensagem, lambda msg: obter_roi(msg, custo_fornecedor, tarifa_fixa_amazon, tarifa_personalizada_amazon, preco_venda, comissao_amazon, lucro_venda))

    except ValueError:
        bot.send_message(mensagem.chat.id, "Formato incorreto. Por favor, insira um valor numérico.")
        bot.register_next_step_handler(mensagem, obter_custo_fornecedor)

def obter_roi(mensagem, custo_fornecedor, tarifa_fixa_amazon, tarifa_personalizada_amazon, preco_venda, comissao_amazon, lucro_venda):
    try:
        roi_desejado = float(mensagem.text.replace(',', '.'))

        calculo_roi = 0.00
        while calculo_roi < roi_desejado:
            preco_venda += 0.01
            comissao_amazon = preco_venda * 0.12

            # Lógica de precificação diferenciada
            if preco_venda <= 78:
                # Apenas a tarifa fixa para produtos até R$78
                tarifa = tarifa_fixa_amazon
            else:
                # Calcular a tarifa personalizada para produtos acima de R$78
                tarifa = calcular_tarifa(preco_venda, "Sul e Sudeste")

            # Adicionar tarifa ao preço de venda
            preco_venda += tarifa

            lucro_venda = preco_venda - custo_fornecedor - comissao_amazon
            calculo_roi = lucro_venda / preco_venda * 100

        resposta = f"""
        🚀 **Resultado do Cálculo:**
        Valor sugerido: R${preco_venda:.2f}
        Comissão da Amazon: R${comissao_amazon:.2f}
        Tarifa fixa da Amazon (até R$78): R${tarifa_fixa_amazon:.2f}
        Tarifa personalizada da Amazon (acima de R$78): R${tarifa:.2f}
        Lucro por venda: R${lucro_venda:.2f}
        ROI Recomendado: {calculo_roi:.2f}%
        Custo total: R${custo_fornecedor + tarifa_fixa_amazon:.2f}

        /start para começar novamente
        """
        bot.send_message(mensagem.chat.id, resposta)

    except ValueError:
        bot.send_message(mensagem.chat.id, "Formato incorreto. Por favor, insira um valor numérico.")
        bot.register_next_step_handler(mensagem, lambda msg: obter_roi(msg, custo_fornecedor, tarifa_fixa_amazon, tarifa_personalizada_amazon, preco_venda, comissao_amazon, lucro_venda))

@bot.message_handler(func=lambda message: True)
def responder_pergunta(message):
    bot.send_message(message.chat.id, "Comando desconhecido. Use /start ou /calcular_preco para interagir com o bot.")

bot.polling()
