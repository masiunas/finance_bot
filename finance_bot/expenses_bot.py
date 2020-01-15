# === Standard library imports ===
import logging

# === Third party imports ========
import telebot

# === Local application imports ==
from settings import api_token

bot = telebot.TeleBot(api_token)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'i am help')


if __name__ == '__main__':
    bot.polling()
