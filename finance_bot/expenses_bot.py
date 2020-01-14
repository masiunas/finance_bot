import logging

import telebot

from tokens import api

bot = telebot.TeleBot(api)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, 'i am help')


if __name__ == '__main__':
    bot.polling()
