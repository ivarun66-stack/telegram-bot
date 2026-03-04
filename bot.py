import telebot
import threading
from flask import Flask
import os
import time
import feedparser
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.environ.get("BOT_TOKEN")

# ключ OpenWeather
API_KEY = "6f1e7bed7bca26223656b4f6aa03dbea"

bot = telebot.TeleBot(TOKEN)


# ===== КЛАВИАТУРА =====
def keyboard():

    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(
        KeyboardButton("💻 Технологии"),
        KeyboardButton("🧠 AI новости")
    )

    markup.add(
        KeyboardButton("📊 Крипто"),
        KeyboardButton("📈 BTC")
    )

    markup.add(
        KeyboardButton("🌤 Погода"),
        KeyboardButton("📅 Прогноз")
    )

    markup.add(
        KeyboardButton("🛰 Запуски")
    )

    return markup


# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(
        message.chat.id,
        "Выберите раздел:",
        reply_markup=keyboard()
    )


# ===== ТЕХНОЛОГИИ =====
@bot.message_handler(func=lambda m: m.text == "💻 Технологии")
def tech_news(message):

    rss = "https://habr.com/ru/rss/articles/"
    feed = feedparser.parse(rss)

    text = "💻 Новости технологий:\n\n"

    for entry in feed.entries[:5]:
        text += f"• {entry.title}\n{entry.link}\n\n"

    bot.send_message(message.chat.id, text)


# ===== AI =====
@bot.message_handler(func=lambda m: m.text == "🧠 AI новости")
def ai_news(message):

    rss = "https://habr.com/ru/hub/ai/rss/articles/"
    feed = feedparser.parse(rss)

    text = "🧠 Новости AI:\n\n"

    for entry in feed.entries[:5]:
        text += f"• {entry.title}\n{entry.link}\n\n"

    bot.send_message(message.chat.id, text)


# ===== КРИПТО =====
@bot.message_handler(func=lambda m: m.text == "📊 Крипто")
def crypto(message):

    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd"

    data = requests.get(url).json()

    text = (
        "📊 Курсы криптовалют:\n\n"
        f"BTC: ${data['bitcoin']['usd']}\n"
        f"ETH: ${data['ethereum']['usd']}\n"
        f"SOL: ${data['solana']['usd']}"
    )

    bot.send_message(message.chat.id, text)


# ===== BTC =====
@bot.message_handler(func=lambda m: m.text == "📈 BTC")
def btc(message):

    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    data = requests.get(url).json()

    bot.send_message(
        message.chat.id,
        f"📈 BTC цена:\n${data['bitcoin']['usd']}"
    )


# ===== ПОГОДА =====
@bot.message_handler(func=lambda m: m.text == "🌤 Погода")
def weather(message):

    city = "Omsk"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"

    data = requests.get(url).json()

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    bot.send_message(
        message.chat.id,
        f"🌤 Погода в {city}\n\n"
        f"{desc}\n"
        f"🌡 {temp}°C"
    )


# ===== ПРОГНОЗ =====
@bot.message_handler(func=lambda m: m.text == "📅 Прогноз")
def forecast(message):

    city = "Omsk"

    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ru"

    data = requests.get(url).json()

    text = f"📅 Прогноз для {city}:\n\n"

    for i in range(0, 40, 8):

        day = data["list"][i]

        date = day["dt_txt"].split(" ")[0]
        temp = day["main"]["temp"]
        desc = day["weather"][0]["description"]

        text += f"{date}\n{desc}\n🌡 {temp}°C\n\n"

    bot.send_message(message.chat.id, text)


# ===== КОСМИЧЕСКИЕ ЗАПУСКИ =====
@bot.message_handler(func=lambda m: m.text == "🛰 Запуски")
def launches(message):

    url = "https://ll.thespacedevs.com/2.2.0/launch/upcoming/"

    data = requests.get(url).json()

    launch = data["results"][0]

    name = launch["name"]
    date = launch["net"]

    bot.send_message(
        message.chat.id,
        f"🛰 Следующий запуск:\n\n{name}\n📅 {date}"
    )


# ===== Flask =====
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"


# ===== BOT =====
def run_bot():
    while True:
        try:
            bot.delete_webhook()
            bot.polling(none_stop=True)
        except:
            time.sleep(5)


if __name__ == "__main__":

    threading.Thread(target=run_bot).start()

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
