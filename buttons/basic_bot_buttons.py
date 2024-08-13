from telegram import Update
from handlers.basic_bot_handlers import start_command, help_command

async def help_command_button_handler(update, context):
    query = update.callback_query

    if 'blocked_by_questions' in context.user_data:
        if context.user_data['blocked_by_questions']:
            await query.message.reply_text(f'Command not available until you complete receiving the question')
            await query.answer()
            return

    command = query.data

    fake_update = Update(update.update_id, message=query.message)

    if command == 'start':
        await start_command(fake_update, context)
    elif command == 'categories':
        context.user_data['just_show_categories'] = True
        from handlers.categories_handlers import categories_fetch_command
        await categories_fetch_command(fake_update, context)
    elif command == 'random question':
        from handlers.questions_handlers import random_question
        await random_question(fake_update, context)
    elif command == 'filter question':
        from handlers.questions_handlers import filter_question
        await filter_question(fake_update, context)
    elif command == 'help':
        await help_command(fake_update, context)

    await query.answer()
