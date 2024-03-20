import os

from telebot import TeleBot
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('URP_BOT_TOKEN')

bot = TeleBot(API_TOKEN)
