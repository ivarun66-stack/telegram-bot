import telebot

TOKEN = "8788093402:AAHDbaKmBvHsT1RNcElMNVxbr1MjE8OmirE"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Бот работает 🚀")

bot.polling()
