import telebot
import time
import threading
import os
from flask import Flask

from telebot import types

# ===== AYARLAR =====
API_TOKEN = "8498288720:AAF4hUTWn6b3Z3rQmaJWaAXwYvfFzU3GVOc"
ADMIN_ID = 7461081198
ADMIN_KANAL_ID = -1001234567890  # KENDİ KANAL ID'İN

bot = telebot.TeleBot(API_TOKEN)

BOT_AKTIF = True
REKLAM_SURE = 4 * 24 * 60 * 60  # 4 gün

SABIT_REKLAM = """LORD SİSTEME AİT BOTLAR 
@LordDestekHat

LORDA AİT BOTLAR 

İP SORGU AKTİF 👇
@revoipsorgubot 

SMS BOMBER BOT 👇
@smsbombexr2026bot

Kamera hack botu aktif 👇
@sizacamsanahareketbot

🧪📱 Sorgu botu aktif 👇  
@BenbirsmsBot

REKLAM BOT aktif 👇
@lordkanalduyurubot
"""

# ===== FLASK (SADECE KEEP ALIVE) =====
app = Flask(__name__)

@app.route("/")
def home():
    return "BOT ONLINE", 200

# ===== OTOMATİK REKLAM =====
def reklam_loop():
    while True:
        try:
            bot.send_message(ADMIN_KANAL_ID, SABIT_REKLAM)
        except Exception as e:
            print("Reklam hata:", e)
        time.sleep(REKLAM_SURE)

# ===== /START =====
@bot.message_handler(commands=["start"])
def start(message):
    if not BOT_AKTIF:
        return

    uid = message.from_user.id
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    if uid == ADMIN_ID:
        kb.add("⚙️ Admin Komutları", "📢 Reklam At")
        bot.send_message(uid, "👑 Admin menü aktif", reply_markup=kb)
    else:
        kb.add("📢 Botlar", "📞 Destek")
        bot.send_message(uid, "🤖 Bot aktif", reply_markup=kb)

# ===== KULLANICI BUTONLARI =====
@bot.message_handler(func=lambda m: m.text == "📢 Botlar")
def botlar(m):
    bot.send_message(m.chat.id, SABIT_REKLAM)

@bot.message_handler(func=lambda m: m.text == "📞 Destek")
def destek(m):
    bot.send_message(m.chat.id, "@LordDestekHat")

# ===== ADMIN BUTON =====
@bot.message_handler(func=lambda m: m.text == "📢 Reklam At")
def reklam_at(m):
    if m.from_user.id == ADMIN_ID:
        bot.send_message(ADMIN_KANAL_ID, SABIT_REKLAM)
        bot.send_message(m.chat.id, "✅ Reklam gönderildi")

# ===== ÇALIŞTIR =====
if __name__ == "__main__":
    threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 5000))
        ),
        daemon=True
    ).start()

    threading.Thread(target=reklam_loop, daemon=True).start()

    print("BOT BAŞLADI")
    bot.infinity_polling(skip_pending=True, none_stop=True)
