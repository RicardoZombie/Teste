import telebot

CHAVE_API = "botapi"

bot = telebot.TeleBot(CHAVE_API)

# Dados dos usuários (apenas para brincadeira, não use isso para dados reais!)
saldo_usuarios = {}

@bot.message_handler(commands=["saldo"])
def saldo(mensagem):
    user_id = mensagem.from_user.id
    if user_id in saldo_usuarios:
        bot.send_message(mensagem.chat.id, f"Seu saldo atual é: {saldo_usuarios[user_id]} reais")
    else:
        bot.send_message(mensagem.chat.id, "Você ainda não possui uma conta. Use /criar_conta para criar uma.")

@bot.message_handler(commands=["criar_conta"])
def criar_conta(mensagem):
    user_id = mensagem.from_user.id
    if user_id not in saldo_usuarios:
        saldo_usuarios[user_id] = 0
        bot.send_message(mensagem.chat.id, "Conta criada com sucesso!")
    else:
        bot.send_message(mensagem.chat.id, "Você já possui uma conta.")

@bot.message_handler(commands=["depositar"])
def depositar(mensagem):
    try:
        valor = float(mensagem.text.split()[1])
        user_id = mensagem.from_user.id

        if user_id in saldo_usuarios:
            saldo_usuarios[user_id] += valor
            bot.send_message(mensagem.chat.id, f"Depósito de {valor} reais realizado com sucesso. Seu saldo atual é: {saldo_usuarios[user_id]} reais")
        else:
            bot.send_message(mensagem.chat.id, "Você ainda não possui uma conta. Use /criar_conta para criar uma.")
    except (IndexError, ValueError):
        bot.send_message(mensagem.chat.id, "Formato incorreto. Use /depositar [valor] para realizar um depósito.")

@bot.message_handler(commands=["sacar"])
def sacar(mensagem):
    try:
        valor = float(mensagem.text.split()[1])
        user_id = mensagem.from_user.id

        if user_id in saldo_usuarios:
            if saldo_usuarios[user_id] >= valor:
                saldo_usuarios[user_id] -= valor
                bot.send_message(mensagem.chat.id, f"Saque de {valor} reais realizado com sucesso. Seu saldo atual é: {saldo_usuarios[user_id]} reais")
            else:
                bot.send_message(mensagem.chat.id, "Saldo insuficiente para realizar o saque.")
        else:
            bot.send_message(mensagem.chat.id, "Você ainda não possui uma conta. Use /criar_conta para criar uma.")
    except (IndexError, ValueError):
        bot.send_message(mensagem.chat.id, "Formato incorreto. Use /sacar [valor] para realizar um saque.")

@bot.message_handler(func=lambda mensagem: True)
def comando_desconhecido(mensagem):
    bot.send_message(mensagem.chat.id, "Comando desconhecido. Use /ajuda para ver os comandos disponíveis.")

bot.polling()
