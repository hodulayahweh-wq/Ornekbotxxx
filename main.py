import os import json import time import threading from flask import Flask, request, redirect, session, render_template_string import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN") if not BOT_TOKEN: raise RuntimeError("BOT_TOKEN bulunamadi")

ADMIN_PASSWORD = "316363" ADMIN_IDS = [123456789] DATA_FILE = "commands.json" LANG_FILE = "langs.json"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML") app = Flask(name) app.secret_key = "lord-secret"

DEFAULT_LANGS = { "tr": { "start": "Komutlar", "noauth": "Yetkin yok", "updated": "Guncellendi, /start yaz" }, "en": { "start": "Commands", "noauth": "No permission", "updated": "Updated, type /start" } }

if not os.path.exists(LANG_FILE): with open(LANG_FILE, "w", encoding="utf-8") as f: json.dump(DEFAULT_LANGS, f, ensure_ascii=False, indent=2)

def default_commands(): data = [] for i in range(1, 21): data.append({"name": f"/user{i}", "desc": f"User command {i}", "type": "user", "active": True}) for i in range(1, 26): data.append({"name": f"/admin{i}", "desc": f"Admin command {i}", "type": "admin", "active": True}) return data

if not os.path.exists(DATA_FILE): with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(default_commands(), f, ensure_ascii=False, indent=2)

def load_cmds(): return json.load(open(DATA_FILE, encoding="utf-8"))

def save_cmds(c): json.dump(c, open(DATA_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def notify_admins(msg): for a in ADMIN_IDS: try: bot.send_message(a, msg) except: pass

@bot.message_handler(commands=["start"]) def start_cmd(m): cmds = load_cmds() msg = "<b>LORD KOMUTLAR</b>\n\n" for c in cmds: if not c["active"]: continue if c["type"] == "admin" and m.from_user.id not in ADMIN_IDS: continue msg += f"{c['name']} - {c['desc']}\n" bot.send_message(m.chat.id, msg)

@bot.message_handler(func=lambda m: True) def any_cmd(m): for c in load_cmds(): if c["active"] and m.text == c["name"]: if c["type"] == "admin" and m.from_user.id not in ADMIN_IDS: bot.reply_to(m, "Yetkin yok") return bot.reply_to(m, "Komut calisti") return

LOGIN_HTML = """ <!doctype html>

<html><head><meta name=viewport content="width=device-width, initial-scale=1">
<style>
body{background:#0f0f1a;color:white;font-family:sans-serif;text-align:center}
input,button,select{padding:12px;border-radius:12px;border:none;width:80%;margin:10px}
button{background:#00f7ff;animation:pulse 2s infinite}
@keyframes pulse{0%{box-shadow:0 0 5px #00f7ff}50%{box-shadow:0 0 20px #00f7ff}100%{box-shadow:0 0 5px #00f7ff}}
</style></head>
<body><h2>LORD PANEL</h2>
<form method=post>
<input type=password name=password placeholder=Şifre>
<button>Giriş</button>
</form></body></html>
"""PANEL_HTML = """ <!doctype html>

<html><head><meta name=viewport content="width=device-width, initial-scale=1">
<style>
body{background:#0f0f1a;color:white;font-family:sans-serif}
.card{background:#1a1a2e;margin:10px;padding:15px;border-radius:15px;animation:slide 0.6s}
@keyframes slide{from{transform:translateY(20px);opacity:0}to{transform:none;opacity:1}}
button{padding:8px;border:none;border-radius:8px;background:#00f7ff}
</style></head>
<body>
<h2 style=text-align:center>LORD WEB PANEL</h2>
{% for c in cmds %}
<div class=card>
<b>{{c.name}}</b> ({{c.type}})<br>{{c.desc}}<br>
Durum: {{"Açık" if c.active else "Kapalı"}}
<form method=post action=/toggle>
<input type=hidden name=name value="{{c.name}}">
<button>Durum</button>
</form>
</div>
{% endfor %}
<form method=post action=/add class=card>
<input name=name placeholder=/yenikomut>
<input name=desc placeholder=Açıklama>
<select name=type><option value=user>User</option><option value=admin>Admin</option></select>
<button>Ekle</button>
</form>
</body></html>
"""@app.route('/', methods=['GET','POST']) def login(): if request.method == 'POST' and request.form.get('password') == ADMIN_PASSWORD: session['admin'] = True return redirect('/panel') return render_template_string(LOGIN_HTML)

@app.route('/panel') def panel(): if not session.get('admin'): return redirect('/') return render_template_string(PANEL_HTML, cmds=load_cmds())

@app.route('/add', methods=['POST']) def add(): if not session.get('admin'): return redirect('/') c = load_cmds() c.append({"name":request.form['name'],"desc":request.form['desc'],"type":request.form['type'],"active":True}) save_cmds(c) notify_admins("Yeni komut eklendi, /start yaz") return redirect('/panel')

@app.route('/toggle', methods=['POST']) def toggle(): if not session.get('admin'): return redirect('/') c = load_cmds() for x in c: if x['name'] == request.form['name']: x['active'] = not x['active'] save_cmds(c) notify_admins("Komut guncellendi, /start yaz") return redirect('/panel')

def run_bot(): bot.infinity_polling()

threading.Thread(target=run_bot).start() port = int(os.environ.get('PORT', 10000)) app.run(host='0.0.0.0', port=port)
