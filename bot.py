from handlers.questions_handlers import *
from handlers.basic_bot_handlers import *
from handlers.categories_handlers import *
from buttons.categories_buttons import categories_button_handler
from buttons.basic_bot_buttons import help_command_button_handler
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from buttons.questions_buttons import questions_button_handler, type_button_handler, difficulty_button_handler

logging.basicConfig(filename=f'logs/bot.log', level=logging.INFO, force=True)
logging.getLogger('httpx').disabled = True
logging.getLogger('telegram.ext.Application').disabled = True
bot_token = os.getenv('BOT_TOKEN')

def main():
    if bot_token is None:
        print('Bot token not found. Please save your bot token in .env file under the name BOT_TOKEN')
        return

    try:
        categories = get_cached_categories()
        categories = '|'.join(categories)
    except Exception as e:
        logging.error(f'{e} - [{datetime.now().strftime('%d-%m-%Y %H:%M:%S')}]')
        exit(1)

    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CallbackQueryHandler(help_command_button_handler, pattern='^(start|categories|random question|filter question|help)$'))
    application.add_handler(CallbackQueryHandler(questions_button_handler, pattern='^(correct|incorrect1|incorrect2|incorrect3)$'))
    application.add_handler(CallbackQueryHandler(type_button_handler, pattern=f'^(boolean|multiple|None_type)$'))
    application.add_handler(CallbackQueryHandler(difficulty_button_handler, pattern='^(easy|medium|hard|None_difficulty)$'))
    application.add_handler(CallbackQueryHandler(categories_button_handler, pattern=f'^{categories}|None_category$'))

    application.run_polling()


if __name__ == '__main__':
    main()
