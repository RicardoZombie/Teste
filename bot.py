from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Função para o comando /start
def start(update, context):
    update.message.reply_text('Olá! Bem-vindo ao seu bot.')

# Função para o comando /echo
def echo(update, context):
    # Responder à mensagem de texto com a mesma mensagem
    update.message.reply_text(update.message.text)

# Função principal
def main():
    # Substitua 'SEU_TOKEN' pelo token do seu bot Telegram
    updater = Updater('SEU_TOKEN', use_context=True)

    dp = updater.dispatcher

    # Adicione manipuladores de comando
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("echo", echo))

    # Adicione um manipulador para mensagens de texto
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Inicie o bot
    updater.start_polling()

    # Aguarde o bot ser encerrado com Ctrl+C
    updater.idle()

if __name__ == '__main__':
    main()