from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = "6332933342:AAEMo5e0MEpgYpt8O7hEtWj3Ii9-OSmSlro"


async def start_handler(update, context):
    await update.message.reply_text(text="Hello")


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler(["start", "help"], start_handler))

    application.run_polling()


if __name__ == '__main__':
    main()
