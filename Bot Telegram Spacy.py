from telegram.ext import Updater, CommandHandler
import random
from queue import Queue

# Daftar menu makanan di kantin BKL Itera
menu_makanan = [
    "Nasi Goreng",
    "Mie Goreng",
    "Ayam Goreng",
    "Nasi Padang",
    "Bakso",
    "Soto Ayam",
    "Gado-gado",
    "Martabak",
    "Pecel Lele",
    "Ikan Bakar"
]

class Bot:
    def __init__(self, token):
        self.updater = Updater(token, use_context=True, queue=Queue())
        self.dp = self.updater.dispatcher

    def start(self, update, context):
        update.message.reply_text("Halo! Selamat datang di Kantin BKL Itera. Untuk rekomendasi makanan, silakan gunakan perintah /makanan.")

    def recommend_food(self, update, context):
        recommended_food = random.choice(menu_makanan)
        update.message.reply_text(f"Saya merekomendasikan Anda mencoba {recommended_food} di Kantin BKL Itera.")

    def start_bot(self):
        self.dp.add_handler(CommandHandler("start", self.start))
        self.dp.add_handler(CommandHandler("makanan", self.recommend_food))
        self.updater.start_polling()
        self.updater.idle()

def main():
    bot = Bot("6482038147:AAHZ88iF4BS8a8D8pTZbT-1BEyp6GhvEd_0")
    bot.start_bot()

if __name__ == '__main__':
    main()
