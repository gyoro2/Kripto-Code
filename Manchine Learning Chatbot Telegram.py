import spacy 
from telegram.ext import Updater
from telegram import Update 
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Inisialisasi model bahasa spaCy
nlp = spacy.load("en_core_web_sm")

# Contoh data makanan (nama, deskripsi, harga)
food_data = {
    'nasi goreng': {'description': 'Nasi goreng spesial dengan telur, ayam, dan sayuran.', 'price': 'Rp 20.000'},
    'sop ayam': {'description': 'Sop ayam hangat dengan potongan daging ayam dan sayuran.', 'price': 'Rp 15.000'},
    'salad': {'description': 'Salad segar dengan campuran sayuran dan dressing pilihan.', 'price': 'Rp 25.000'}
}

# Fungsi untuk memberikan rekomendasi makanan
def recommend_food():
    # Di sini Anda dapat mengimplementasikan logika untuk memberikan rekomendasi makanan
    # Misalnya, Anda bisa menggunakan model rekomendasi berdasarkan preferensi pengguna sebelumnya atau popularitas makanan
    return ['nasi goreng', 'sop ayam', 'salad']

# Fungsi untuk memproses pesan pengguna dan memberikan respons
def handle_message(update: Update, context):
    user_input = update.message.text.lower()  # Ambil input pengguna dan ubah ke huruf kecil

    # Proses input pengguna menggunakan spaCy
    doc = nlp(user_input)

    # Cek apakah input mengandung kata kunci untuk rekomendasi makanan
    if any(token.text in ['rekomendasi', 'makan'] for token in doc):
        recommended_food = recommend_food()
        response = "Berikut rekomendasi makanan untuk Anda:\n"
        for food in recommended_food:
            response += f"- {food}: {food_data[food]['description']}, Harga: {food_data[food]['price']}\n"
    else:
        response = "Maaf, saya tidak bisa memahami permintaan Anda. Silakan coba lagi."

    update.message.reply_text(response)  # Kirim respons ke pengguna

def main():
    # Inisialisasi Updater dengan token bot Anda
    updater = Updater("6482038147:AAHZ88iF4BS8a8D8pTZbT-1BEyp6GhvEd_0", use_context=True)

    # Dapatkan dispatcher untuk mendaftarkan handler
    dp = updater.dispatcher

    # Tambahkan handler untuk perintah /start
    dp.add_handler(CommandHandler("start", start))

    # Mulai polling agar bot dapat menerima pesan
    updater.start_polling()

    # Jalankan bot sampai Anda menekan Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
