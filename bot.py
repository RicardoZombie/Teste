import telebot

CHAVE_API = "botapi"

bot = telebot.TeleBot(CHAVE_API)

@bot.message_handler(commands=["iniciar"])
def iniciar(mensagem):
    bot.send_message(mensagem.chat.id, "🚀 **Bem-vindo ao Bot de Precificação da Amazon!**\nPara começar, use /calcular_preco")

@bot.message_handler(commands=["calcular_preco"])
def calcular_preco(mensagem):
    bot.send_message(mensagem.chat.id, "📦 **Calculando Preço de Venda:**\n\nEnvie o valor que você paga no site do fornecedor:")
    bot.register_next_step_handler(mensagem, obter_custo_fornecedor)

def obter_custo_fornecedor(mensagem):
    try:
        custo_fornecedor = float(mensagem.text)
        tarifa_amazon = 5.50

        preco_venda = custo_fornecedor
        comissao_amazon = 0
        lucro_venda = 0

        roi_desejado = float(input("Qual é o ROI desejado (%)? "))
        
        calculo_roi = 0.00
        while calculo_roi < roi_desejado:
            preco_venda += 0.01
            comissao_amazon = preco_venda * 0.12
            lucro_venda = preco_venda - custo_fornecedor - comissao_amazon
            calculo_roi = lucro_venda / preco_venda * 100

        resposta = f"""
        🚀 **Resultado do Cálculo:**
        Valor sugerido: R${preco_venda:.2f}
        Comissão da Amazon: R${comissao_amazon:.2f}
        Lucro por venda: R${lucro_venda:.2f}
        ROI Recomendado: {calculo_roi:.2f}%
        Custo total: R${custo_fornecedor + tarifa_amazon:.2f}

        /iniciar para começar novamente
        """
        bot.send_message(mensagem.chat.id, resposta)

    except ValueError:
        bot.send_message(mensagem.chat.id, "Formato incorreto. Por favor, insira um valor numérico.")
        bot.register_next_step_handler(mensagem, obter_custo_fornecedor)

bot.polling()
