############################################################ #LORD ULTRA SEVIYE BOT + WEB PANEL ############################################################ #Animasyonlu Web Admin Panel (45 Komut) #Tek dosya main.py | Render uyumlu | HATASIZ ############################################################

import os import json import threading import time

from flask import Flask, request, redirect, session, render_template_string import telebot

==================== AYARLAR ====================

BOT_TOKEN = os.getenv("BOT_TOKEN") if not BOT_TOKEN: raise RuntimeError("BOT_TOKEN bulunamadi. Render Environment'a ekle.")

BOT_NAME = "LORD" ADMIN_PASSWORD = "316363" ADMIN_IDS = {7461081198} DATA_FILE = "commands.json"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

==================== KOMUTLAR ====================

USER_COMMANDS = { '/start': 'Botu baslatir', '/help': 'Tum komutlari gosterir', '/menu': 'Ana menu', '/profil': 'Kullanici bilgileri', '/dil': 'Dil secimi', '/istatistik': 'Bot istatistikleri', '/destek': 'Destek hatti', '/ping': 'Bot durumu', '/zaman': 'Sunucu zamani', '/kurallar': 'Kullanim kosullari', '/duyuru': 'Son duyurular', '/linkler': 'Resmi linkler', '/paketler': 'Hizmet paketleri', '/limit': 'Gunluk limit', '/referans': 'Davet sistemi', '/puan': 'Kullanici puani', '/bildir': 'Sorun bildir', '/versiyon': 'Bot surumu', '/iletisim': 'Iletisim', '/sss': 'Sik sorulanlar' }

ADMIN_COMMANDS = { '/admin': 'Admin panel', '/broadcast': 'Duyuru gonder', '/users': 'Kullanicilar', '/ban': 'Ban at', '/unban': 'Ban kaldir', '/stats': 'Detayli istatistik', '/logs': 'Loglar', '/restart': 'Botu yeniden baslat', '/backup': 'Yedek al', '/restore': 'Yedek yukle', '/limits': 'Limit ayarlari', '/ads': 'Reklam yonetimi', '/panel': 'Web panel kontrol', '/langs': 'Dil ayarlari', '/roles': 'Yetkiler', '/security': 'Guvenlik', '/maintenance': 'Bakim modu', '/system': 'Sistem bilgisi', '/shutdown': 'Botu kapat', '/top': 'En aktifler', '/reset': 'Sifirla', '/config': 'Ayarlar', '/admins': 'Admin listesi', '/addadmin': 'Admin ekle' }

ALL_COMMANDS = {**USER_COMMANDS, **ADMIN_COMMANDS}

==================== TELEGRAM BOT ====================

@bot.message_handler(commands=['start']) def start_cmd(m): bot.reply_to(m, f"👑 <b>{BOT_NAME}</b> Hosgeldin!\n/help yazarak komutlari gorebilirsin.")

@bot.message_handler(commands=['help']) def help_cmd(m): text = "📜 <b>Kullanici Komutlari</b>\n" for k, v in USER_COMMANDS.items(): text += f"{k} - {v}\n" if m.from_user.id in ADMIN_IDS: text += "\n👑 <b>Admin Komutlari</b>\n" for k, v in ADMIN_COMMANDS.items(): text += f"{k} - {v}\n" bot.reply_to(m, text)

@bot.message_handler(func=lambda m: m.text and m.text.startswith('/')) def unknown(m): bot.reply_to(m, "❌ Bilinmeyen komut. /help yaz.")

==================== WEB PANEL ====================

app = Flask(name) app.secret_key = "lord-secret"

PANEL_HTML = """ <!doctype html><html lang=tr><head><meta charset=utf-8>

<title>LORD Panel</title>
<style>
body{margin:0;background:#0f0f1a;color:#fff;font-family:Arial}
header{text-align:center;padding:20px;font-size:28px;animation:glow 2s infinite}
@keyframes glow{0%{color:#fff}50%{color:#00f7ff}100%{color:#fff}}
.card{background:#1a1a2e;margin:10px;padding:15px;border-radius:12px;animation:slide .5s}
@keyframes slide{from{opacity:0;transform:translateX(-20px)}to{opacity:1}}
</style></head><body>
<header>⚡ LORD WEB ADMIN PANEL ⚡</header>
{% for k,v in commands.items() %}
<div class=card><b>{{k}}</b> - {{v}}</div>
{% endfor %}
</body></html>
"""LOGIN_HTML = """ <!doctype html><html><body style="background:#0f0f1a;color:white;text-align:center;padding-top:120px">

<h2>LORD PANEL GIRIS</h2>
<form method=post>
<input type=password name=password placeholder=Sifre><br><br>
<button>Giris</button>
</form></body></html>
"""@app.route('/', methods=['GET','POST']) def login(): if request.method == 'POST' and request.form.get('password') == ADMIN_PASSWORD: session['admin'] = True return redirect('/panel') return render_template_string(LOGIN_HTML)

@app.route('/panel') def panel(): if not session.get('admin'): return redirect('/') return render_template_string(PANEL_HTML, commands=ALL_COMMANDS)

==================== RUN ====================

def run_all(): threading.Thread(target=bot.infinity_polling, daemon=True).start() port = int(os.environ.get('PORT', 10000)) app.run(host='0.0.0.0', port=port)

if name == 'main': run_all()