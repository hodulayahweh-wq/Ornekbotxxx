#==================== LORD FULL BOT + WEB PANEL ====================

#Telegram Bot + Animasyonlu Çok Dilli Web Admin Panel (Render uyumlu)

#Dil Seçimi: TR, EN, DE, FR, ES, AR (kolayca genişletilebilir)

#================================================================

import os import time import threading from datetime import datetime

import telebot from flask import Flask, request, redirect, url_for, render_template_string, session

#==================== AYARLAR ====================

TOKEN = os.getenv("BOT_TOKEN", "BOT_TOKEN bulunamadı") ADMIN_IDS = {7461081198} ADMIN_CHANNEL_ID = -1001234567890 WEB_PANEL_PASSWORD = "316363" BASE_URL = "https://ornekbotxxxx.onrender.com"

REKLAM_SURESI = 4 * 24 * 60 * 60  # 4 gün

REKLAM_METNI = """ 📢 LORD SİSTEME AİT BOTLAR

@LordDestekHat

LORDA AİT BOTLAR

İP SORGU AKTİF 👇 @revoipsorgubot

SMS BOMBER BOT 👇 @smsbombexr2026bot

Kamera botu AKTİF 👇 @sizacamsanahareketbot

🧪📱 Sorgu botu AKTİF 👇 @BenbirsmsBot

REKLAM BOT AKTİF 👇 @lordkanalduyurubot """

#==================== DİLLER ====================

LANGS = { "tr": { "title": "LORD Admin Panel", "login": "Giriş", "password": "Şifre", "logout": "Çıkış", "welcome": "Hoş geldiniz", "stats": "İstatistikler", "uptime": "Çalışma Süresi", "users": "Kullanıcı Sayısı", "admins": "Adminler", "language": "Dil Seçimi" }, "en": { "title": "LORD Admin Panel", "login": "Login", "password": "Password", "logout": "Logout", "welcome": "Welcome", "stats": "Statistics", "uptime": "Uptime", "users": "Users", "admins": "Admins", "language": "Language" }, "de": {"title": "LORD Admin", "login": "Anmelden", "password": "Passwort", "logout": "Abmelden", "welcome": "Willkommen", "stats": "Statistiken", "uptime": "Laufzeit", "users": "Benutzer", "admins": "Admins", "language": "Sprache"}, "fr": {"title": "LORD Admin", "login": "Connexion", "password": "Mot de passe", "logout": "Déconnexion", "welcome": "Bienvenue", "stats": "Statistiques", "uptime": "Temps de fonctionnement", "users": "Utilisateurs", "admins": "Admins", "language": "Langue"}, "es": {"title": "LORD Admin", "login": "Iniciar", "password": "Contraseña", "logout": "Salir", "welcome": "Bienvenido", "stats": "Estadísticas", "uptime": "Tiempo activo", "users": "Usuarios", "admins": "Admins", "language": "Idioma"}, "ar": {"title": "لوحة LORD", "login": "تسجيل", "password": "كلمة المرور", "logout": "خروج", "welcome": "مرحبا", "stats": "إحصائيات", "uptime": "مدة التشغيل", "users": "المستخدمون", "admins": "المدراء", "language": "اللغة"} }

#==================== BOT ====================

bot = telebot.TeleBot(TOKEN, parse_mode="HTML") START_TIME = time.time() USERS = set()

@bot.message_handler(commands=['start']) def start_cmd(m): USERS.add(m.from_user.id) bot.reply_to(m, "🤖 <b>LORD REKLAM Bot Aktif</b> Komutlar: /help")

@bot.message_handler(commands=['help']) def help_cmd(m): bot.reply_to(m, "/start /help")

@bot.message_handler(commands=['admin']) def admin_cmd(m): if m.from_user.id in ADMIN_IDS: bot.reply_to(m, "Admin panel: " + BASE_URL) else: bot.reply_to(m, "Yetkin yok")

#==================== REKLAM ====================

def reklam_loop(): last = 0 while True: if time.time() - last > REKLAM_SURESI: try: bot.send_message(ADMIN_CHANNEL_ID, REKLAM_METNI) last = time.time() except: pass time.sleep(60)

#==================== WEB PANEL ====================

app = Flask(name) app.secret_key = "lord-secret"

PANEL_HTML = """ <!doctype html>

<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<title>{{t['title']}}</title>
<style>
body{font-family:Arial;background:linear-gradient(120deg,#0f2027,#203a43,#2c5364);color:#fff;animation:bg 10s infinite alternate}
@keyframes bg{0%{filter:hue-rotate(0deg)}100%{filter:hue-rotate(360deg)}}
.card{background:rgba(0,0,0,.5);padding:20px;border-radius:12px;max-width:420px;margin:60px auto;box-shadow:0 0 20px #000}
select,input,button{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:0}
button{background:#00c6ff;color:#000;font-weight:bold;cursor:pointer}
.stat{margin:8px 0}
</style>
</head>
<body>
<div class=card>
<form method=post>
<label>{{t['language']}}</label>
<select name=lang onchange="this.form.submit()">
{% for k in langs %}<option value="{{k}}" {% if k==lang %}selected{% endif %}>{{k}}</option>{% endfor %}
</select>
</form>
{% if not logged %}
<h3>{{t['login']}}</h3>
<form method=post>
<input type=password name=password placeholder="{{t['password']}}">
<button>{{t['login']}}</button>
</form>
{% else %}
<h3>{{t['welcome']}}</h3>
<div class=stat>{{t['users']}}: {{users}}</div>
<div class=stat>{{t['admins']}}: {{admins}}</div>
<div class=stat>{{t['uptime']}}: {{uptime}}</div>
<a href=/logout><button>{{t['logout']}}</button></a>
{% endif %}
</div>
</body>
</html>
"""@app.route('/', methods=['GET','POST']) def panel(): lang = request.form.get('lang') or session.get('lang') or 'tr' session['lang'] = lang t = LANGS.get(lang, LANGS['tr'])

if 'password' in request.form:
    if request.form['password'] == WEB_PANEL_PASSWORD:
        session['logged'] = True

logged = session.get('logged', False)
uptime = int(time.time() - START_TIME)
return render_template_string(PANEL_HTML,
    t=t, langs=LANGS.keys(), lang=lang, logged=logged,
    users=len(USERS), admins=len(ADMIN_IDS), uptime=uptime)

@app.route('/logout') def logout(): session.clear() return redirect('/')

#==================== ÇALIŞTIR ====================

def run(): threading.Thread(target=reklam_loop, daemon=True).start() threading.Thread(target=lambda: bot.infinity_polling(skip_pending=True), daemon=True).start() app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

if name == 'main': run()
