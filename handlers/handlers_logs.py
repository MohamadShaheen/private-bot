import logging
from datetime import datetime

def naive_logs(update, command):
    query = update.effective_chat
    username = f'@{query.username}'
    user_id = query.id

    logging.info(f'\'/{command}\' command was used by {username} of id {user_id} - [{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}]')
