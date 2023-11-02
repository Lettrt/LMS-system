import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
ACCOUNT_ID = os.environ.get('ACCOUNT_ID')