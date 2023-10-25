import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from typing import Dict
from aiogram.types import ParseMode
from tg_bot.config import TOKEN, CHAT_ID, ACCOUNT_ID

bot = Bot(token=TOKEN)
chat_id = CHAT_ID
account_id = ACCOUNT_ID


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
chat_id = CHAT_ID
account_id = ACCOUNT_ID
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def send_telegram_notification(contact_data: Dict[str, str]) -> None:
    '''
    Receiving a notification from the website about a new user request.
    contact_data - a dictionary with user data, obtained from the form on the website.
    '''
    message_text = f"Новый запрос от пользователя:\n\n"
    message_text += f"Имя: {contact_data['name']}\n"
    message_text += f"Email: {contact_data['email']}\n"
    message_text += f"Номер телефона: {contact_data['phone_number']}\n"
    message_text += f"Сообщение: {contact_data['message']}"
    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
