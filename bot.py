import telebot
import threading
from flask import Flask
import os
import time
import tempfile
from ebooklib import epub

TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Бот работает 🚀")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_name = message.document.file_name

    if file_name and file_name.lower().endswith(".fb2"):
        try:
            bot.reply_to(message, "Получил файл, конвертирую...")

            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".fb2") as fb2_file:
                fb2_file.write(downloaded_file)
                fb2_path = fb2_file.name

            book = epub.EpubBook()
            book.set_title("Converted Book")
            book.set_language("ru")

            chapter = epub.EpubHtml(title='Chapter', file_name='chap_01.xhtml')
            chapter.content = downloaded_file.decode("utf-8", errors="ignore")

            book.add_item(chapter)
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())
            book.spine = ['nav', chapter]

            epub_path = fb2_path.replace(".fb2", ".epub")
            epub.write_epub(epub_path, book)

            with open(epub_path, "rb") as f:
                bot.send_document(message.chat.id, f)

            os.remove(fb2_path)
            os.remove(epub_path)

        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")
    else:
        bot.reply_to(message, "Отправьте файл формата .fb2")

# --- Flask сервер для Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run_bot():
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(e)
            time.sleep(5)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
