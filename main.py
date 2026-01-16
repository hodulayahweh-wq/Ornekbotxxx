#================= ULTRA UST SEVIYE LORD PANEL + BOT =================

#Render Uyumlu | Web Admin Panel | Animasyon | Login | Yetki | Stabil

import os, time, threading, platform, psutil, socket, json from datetime import datetime from flask import Flask, request, render_template_string, session, redirect import telebot

#================= AYARLAR =================

TOKEN = "8474819821:AAFc2uafIfJGmks469JxlsbjVTIjF8YH6Wc" ADMIN_ID = 7461081198 ADMIN_KANAL_ID = -1001234567890 PANEL_SIFRE = "316363" PORT = int(os.environ.get("PORT", 10000))

START_TIME = time.time() reklam_aktif = True reklam_sure = 606024*4

REKLAM_METNI = """LORD SİSTEME AİT BOTLAR @LordDestekHat

İP SORGU AKTİF 👇 @revoipsorgubot

SMS BOMBER BOT 👇 @smsbombexr2026bot

Kamera hack botu AKTİF 👇 @sizacamsanahareketbot

🧪📱 Sorgu botu AKTİF 👇 @BenbirsmsBot

REKLAM BOT AKTİF 👇 @lordkanalduyurubot"""

#================= BOT =================

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

#================= FLASK =================

app = Flask(name) app.secret_key = "lord_ultra_secret"

#================= HTML =================

HTML = """

<!DOCTYPE html><html><head><title>LORD ULTRA PANEL</title><style>
body{margin:0;background:#020617;color:#e5e7eb;font-family:Arial}
.sidebar{width:220px;position:fixed;height:100%;background:#020617;border-right:1px solid #22d3ee}
.sidebar h2{color:#22d3ee;text-align:center}
.sidebar a{display:block;padding:10px;color:#e5e7eb;text-decoration:none}
.sidebar a:hover{background:#22d3ee;color:#020617}
.main{margin-left:220px;padding:20px;animation:fade 1s}
.card{background:#020617;padding:15px;border-radius:14px;margin-bottom:15px;box-shadow:0 0 25px rgba(34,211,238,.3)}
button{padding:10px;border:none;border-radius:10px;background:#22d3ee;color:#020617;font-weight:bold;cursor:pointer}
textarea{width:100%;height:140px;background:#020617;color:#e5e7eb;border:1px solid #22d3ee;border-radius:10px}
@keyframes fade{from{opacity:0}to{opacity:1}}
</style></head><body><div class='sidebar'>
<h2>👑 LORD</h2>
<a href='/'>📊 Dashboard</a>
<a href='/reklam'>📢 Reklam</a>
<a href='/system'>⚙️ Sistem</a>
<a href='/logout'>🚪 Çıkış</a>
</div>
<div class='main'>{{content}}</div>
</body></html>
"""LOGIN = """

<form method='post' style='display:flex;justify-content:center;align-items:center;height:100vh'>
<div class='card'>
<h2>🔐 PANEL GİRİŞ</h2>
<input type='password' name='password' placeholder='Şifre' style='padding:10px'><br><br>
<button>Giriş</button>
</div></form>
"""================= ROUTES =================

@app.route('/', methods=['GET','POST']) def dashboard(): if not session.get('auth'): return redirect('/login') up = int(time.time()-START_TIME) content = f""" <div class='card'>⏱ Uptime: {up//60} dk</div> <div class='card'>🧠 CPU: {psutil.cpu_percent()}%</div> <div class='card'>💾 RAM: {psutil.virtual_memory().percent}%</div> <div class='card'>🖥 OS: {platform.system()}</div> <div class='card'>🐍 Python: {platform.python_version()}</div> <div class='card'>📢 Reklam Durumu: {'AKTİF' if reklam_aktif else 'KAPALI'}</div> """ return render_template_string(HTML, content=content)

@app.route('/reklam', methods=['GET','POST']) def reklam(): global REKLAM_METNI, reklam_aktif if not session.get('auth'): return redirect('/login') if request.method=='POST': if 'save' in request.form: REKLAM_METNI=request.form['msg'] if 'send' in request.form: try: bot.send_message(ADMIN_KANAL_ID, REKLAM_METNI) except: pass if 'on' in request.form: reklam_aktif=True if 'off' in request.form: reklam_aktif=False content = f""" <div class='card'> <form method='post'> <textarea name='msg'>{REKLAM_METNI}</textarea><br><br> <button name='save'>💾 Kaydet</button> <button name='send'>📢 Hemen At</button> <button name='on'>▶️ Aç</button> <button name='off'>⏸️ Kapat</button> </form></div> """ return render_template_string(HTML, content=content)

@app.route('/system') def system(): if not session.get('auth'): return redirect('/login') content=f""" <div class='card'>IP: {socket.gethostbyname(socket.gethostname())}</div> <div class='card'>Saat: {datetime.now()}</div> <div class='card'><a href='/restart'>🔄 Bot Restart</a></div> """ return render_template_string(HTML, content=content)

@app.route('/restart') def restart(): os._exit(0)

@app.route('/login', methods=['GET','POST']) def login(): if request.method=='POST' and request.form.get('password')==PANEL_SIFRE: session['auth']=True; return redirect('/') return LOGIN

@app.route('/logout') def logout(): session.clear(); return redirect('/login')

#================= BOT =================

@bot.message_handler(commands=['start']) def start(m): bot.send_message(m.chat.id, "🤖 LORD BOT AKTİF")

@bot.message_handler(commands=['admin']) def admin(m): if m.from_user.id==ADMIN_ID: bot.send_message(m.chat.id, "👑 Admin yetkili. Web panelden yönet.")

#================= LOOP =================

def reklam_loop(): while True: if reklam_aktif: try: bot.send_message(ADMIN_KANAL_ID, REKLAM_METNI) except: pass time.sleep(reklam_sure)

#================= RUN =================

def run_web(): app.run(host='0.0.0.0', port=PORT)

if name=='main': threading.Thread(target=run_web).start() threading.Thread(target=reklam_loop, daemon=True).start() bot.infinity_polling(skip_pending=True)
