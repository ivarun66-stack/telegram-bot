
import telebot
import threading
from flask import Flask
import os
import time
import requests
import feedparser

TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

# ===== КОМАНДА START =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "Привет! 👋\n\n"
        "Команды:\n"
        "/news — последние космические новости 🚀"
    )

# ===== НОВОСТИ =====
@bot.message_handler(commands=['tech'])
def tech_news(message):
    bot.reply_to(message, "Загружаю новости технологий... 💻")

    rss_url = "https://habr.com/ru/rss/articles/"
    feed = feedparser.parse(rss_url)

    if not feed.entries:
        bot.send_message(message.chat.id, "Новости не найдены.")
        return

    text = "💻 Последние новости технологий:\n\n"

    for entry in feed.entries[:5]:
        text += f"• {entry.title}\n{entry.link}\n\n"

    bot.send_message(message.chat.id, text)

# ===== Flask для Render =====
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

# ===== Устойчивый polling =====
def run_bot():
    while True:
        try:
            bot.delete_webhook()
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(e)
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
