from handlers.buttons_handler import *
from handlers.questions_handlers import *
from handlers.basic_bot_handlers import *
from handlers.categories_handlers import *
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler

logging.basicConfig(filename=f'logs/bot.log', level=logging.INFO, force=True)
logging.getLogger('httpx').disabled = True
logging.getLogger('telegram.ext.Application').disabled = True
bot_token = os.getenv('BOT_TOKEN')

def main():
    if bot_token is None:
        print('Bot token not found. Please save your bot token in .env file under the name BOT_TOKEN')
        return

    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('categories', categories_fetch_command))
    application.add_handler(CommandHandler('question', random_question))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CallbackQueryHandler(help_command_button_handler))

    application.run_polling()


if __name__ == '__main__':
    main()
