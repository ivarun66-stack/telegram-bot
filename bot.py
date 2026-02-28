import telebot
import threading
from flask import Flask
import os
import time

# Вставь сюда свой токен
TOKEN = "8788093402:AAHDbaKmBvHsT1RNcElMNVxbr1MjE8OmirE"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Бот работает 🚀")

# --- Flask сервер для Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

# --- Устойчивый polling ---
def run_bot():
    while True:
        try:
            print("Bot started polling...")
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
