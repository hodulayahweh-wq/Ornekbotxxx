# ============================================================
# LORD ULTRA SEVİYE BOT + WEB PANEL
# Android (Pydroid 3 / Termux) + Render uyumlu
# Tek dosya: main.py
# ============================================================

import os
import json
import threading
from flask import Flask, request, redirect, session, render_template_string
import telebot

# ==================== AYARLAR ====================
BOT_NAME = "LORD"
ADMIN_PASSWORD = "316363"
DATA_FILE = "commands.json"

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN bulunamadı")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

# ==================== KOMUTLAR ====================
USER_COMMANDS = {
    "/start": "Botu başlatır",
    "/help": "Komutları gösterir",
    "/menu": "Ana menü",
    "/profil": "Profil",
    "/dil": "Dil seçimi",
    "/istatistik": "İstatistik",
    "/destek": "@LordDestekHat",
    "/ping": "Bot durumu",
    "/zaman": "Saat",
    "/kurallar": "Kurallar",
    "/duyuru": "Duyurular",
    "/linkler": "Linkler",
    "/paketler": "Paketler",
    "/limit": "Limit",
    "/referans": "Referans",
    "/puan": "Puan",
    "/bildir": "Sorun bildir",
    "/versiyon": "Versiyon",
    "/iletisim": "İletişim",
    "/sss": "SSS"
}

ADMIN_COMMANDS = {
    "/admin": "Admin panel",
    "/broadcast": "Duyuru",
    "/users": "Kullanıcılar",
    "/ban": "Ban",
    "/unban": "Unban",
    "/stats": "Stats",
    "/logs": "Loglar",
    "/restart": "Restart",
    "/addcmd": "Komut ekle",
    "/delcmd": "Komut sil",
    "/editcmd": "Komut düzenle"
}

ALL_COMMANDS = {**USER_COMMANDS, **ADMIN_COMMANDS}

# ==================== KOMUT DOSYASI ====================
def default_commands():
    cmds = []
    i = 1
    for k, v in ALL_COMMANDS.items():
        cmds.append({
            "id": i,
            "name": k,
            "desc": v,
            "active": True
        })
        i += 1
    return cmds

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(default_commands(), f, ensure_ascii=False, indent=2)

# ==================== TELEGRAM BOT ====================
@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(
        m,
        f"⚡ <b>{BOT_NAME}</b> aktif!\n\n/help ile komutları gör"
    )

@bot.message_handler(commands=["help"])
def help_cmd(m):
    text = "<b>📜 KOMUTLAR</b>\n\n"
    for k, v in USER_COMMANDS.items():
        text += f"{k} - {v}\n"
    bot.reply_to(m, text)

# ==================== FLASK PANEL ====================
app = Flask(__name__)
app.secret_key = "lord-secret"

PANEL_HTML = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>LORD PANEL</title>
<style>
body{margin:0;font-family:Arial;background:#0f0f1a;color:white}
header{padding:20px;text-align:center;font-size:28px;font-weight:bold;animation:glow 2s infinite}
@keyframes glow{0%{color:#fff}50%{color:#00f7ff}100%{color:#fff}}
.container{padding:20px}
.card{background:#1a1a2e;border-radius:12px;padding:15px;margin:10px 0}
</style>
</head>
<body>
<header>⚡ LORD WEB PANEL ⚡</header>
<div class="container">
{% for c in commands %}
<div class="card">
<b>{{c.name}}</b> - {{c.desc}}
</div>
{% endfor %}
</div>
</body>
</html>
"""

LOGIN_HTML = """
<html>
<body style="background:#0f0f1a;color:white;text-align:center;padding-top:100px">
<h2>LORD PANEL GİRİŞ</h2>
<form method="post">
<input type="password" name="password" placeholder="Şifre">
<br><br>
<button>Giriş</button>
</form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/panel")
    return render_template_string(LOGIN_HTML)

@app.route("/panel")
def panel():
    if not session.get("admin"):
        return redirect("/")
    with open(DATA_FILE, encoding="utf-8") as f:
        commands = json.load(f)
    return render_template_string(PANEL_HTML, commands=commands)

# ==================== ÇALIŞTIR ====================
def run_bot():
    bot.infinity_polling(skip_pending=True)

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()