import os
import json
import time
import threading

from flask import Flask, request, redirect, session, render_template_string
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_IDS = [7461081198]
ADMIN_PASSWORD = "316363"

DATA_FILE = "commands.json"

app = Flask(__name__)
app.secret_key = "lord_secret_key"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

def load_commands():
    if not os.path.exists(DATA_FILE):
        cmds = []
        for i in range(1, 46):
            cmds.append({
                "cmd": f"/komut{i}",
                "desc": f"LORD komut {i}",
                "type": "user" if i <= 20 else "admin",
                "active": True
            })
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(cmds, f, ensure_ascii=False, indent=2)
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)

def save_commands(cmds):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cmds, f, ensure_ascii=False, indent=2)

@bot.message_handler(commands=["start"])
def start(m):
    cmds = load_commands()
    text = "KOMUTLAR\n\n"
    for c in cmds:
        if c["active"] and c["type"] == "user":
            text += f'{c["cmd"]} - {c["desc"]}\n'
    bot.send_message(m.chat.id, text)

@bot.message_handler(func=lambda m: True)
def all_cmds(m):
    cmds = load_commands()
    for c in cmds:
        if m.text == c["cmd"] and c["active"]:
            if c["type"] == "admin" and m.from_user.id not in ADMIN_IDS:
                bot.send_message(m.chat.id, "Yetkin yok")
                return
            bot.send_message(m.chat.id, f'Calisti: {c["cmd"]}')
            return

LOGIN_HTML = """
<html>
<body style='background:#111;color:white;text-align:center;padding-top:120px'>
<h2>LORD PANEL</h2>
<form method='post'>
<input name='password' type='password' placeholder='Sifre'><br><br>
<button>Giris</button>
</form>
</body>
</html>
"""

PANEL_HTML = """
<html>
<body style='background:#0f0f1a;color:white;padding:20px'>
<h3>Komutlar</h3>
{% for c in commands %}
<div style='background:#1a1a2e;padding:10px;margin:6px;border-radius:8px'>
<b>{{c.cmd}}</b> - {{c.desc}} ({{c.type}})
</div>
{% endfor %}
<form method='post' action='/add'>
<input name='cmd' placeholder='/yenikomut'>
<input name='desc' placeholder='aciklama'>
<select name='type'>
<option value='user'>user</option>
<option value='admin'>admin</option>
</select>
<button>Ekle</button>
</form>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
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
    return render_template_string(PANEL_HTML, commands=load_commands())

@app.route("/add", methods=["POST"])
def add():
    cmds = load_commands()
    cmds.append({
        "cmd": request.form["cmd"],
        "desc": request.form["desc"],
        "type": request.form["type"],
        "active": True
    })
    save_commands(cmds)
    for aid in ADMIN_IDS:
        bot.send_message(aid, "Panelde yeni komut eklendi. /start ile guncelle")
    return redirect("/panel")

def run_bot():
    bot.infinity_polling()

threading.Thread(target=run_bot).start()

port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
