# ================== IMPORTS ==================
import os, json, threading, random, requests, datetime
from flask import Flask, request, redirect, session, render_template_string
import telebot

# ================== AYARLAR ==================
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

ADMIN_PASSWORD = "2026xlord"
USER_PASSWORD = "2026lordcheck"

PORT = int(os.getenv("PORT", "5000"))
DATA_CMDS = "commands.json"
DATA_LOGS = "logs.json"

# ================== DOSYA OLUŞTUR ==================
def ensure_files():
    if not os.path.exists(DATA_CMDS):
        json.dump({}, open(DATA_CMDS,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    if not os.path.exists(DATA_LOGS):
        json.dump([], open(DATA_LOGS,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

ensure_files()

# ================== BOT ==================
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML") if BOT_TOKEN else None

def load_cmds(): return json.load(open(DATA_CMDS,encoding="utf-8"))
def save_cmds(d): json.dump(d, open(DATA_CMDS,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

def load_logs(): return json.load(open(DATA_LOGS,encoding="utf-8"))
def save_logs(l): json.dump(l, open(DATA_LOGS,"w",encoding="utf-8"), ensure_ascii=False, indent=2)

def log_event(who, action, detail):
    logs = load_logs()
    entry = {
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "who": who,
        "action": action,
        "detail": detail
    }
    logs.insert(0, entry)
    save_logs(logs[:200])

    if bot and ADMIN_ID:
        bot.send_message(ADMIN_ID,
            f"📌 <b>{action}</b>\n👤 {who}\n🕒 {entry['time']}\n📝 {detail}"
        )

# ================== API ==================
def adapter_call(url, args):
    try:
        r = requests.get(url, params={"q": args[0]} if args else {}, timeout=10)
        r.raise_for_status()
        return r.json() if "json" in r.headers.get("content-type","") else {"raw":r.text}
    except Exception as e:
        return {"error": str(e)}

# ================== BOT ==================
if bot:

    @bot.message_handler(commands=["start"])
    def start(m):
        bot.reply_to(m, "👑 LORD ULTRA AKTİF")

    @bot.message_handler(commands=["ekle"])
    def add_cmd(m):
        if m.from_user.id != ADMIN_ID:
            return bot.reply_to(m,"Yetkin yok")
        _, name, url = m.text.split(maxsplit=2)
        d = load_cmds()
        d[name] = {"url":url,"enabled":True,"desc":"Admin ekledi"}
        save_cmds(d)
        log_event("ADMIN","Komut Eklendi",f"/{name}")
        bot.reply_to(m,f"/{name} eklendi")

    @bot.message_handler(func=lambda m:m.text.startswith("/"))
    def dynamic(m):
        cmd = m.text.split()[0][1:]
        args = m.text.split()[1:]
        d = load_cmds()
        if cmd in d and d[cmd]["enabled"]:
            res = adapter_call(d[cmd]["url"], args)
            log_event(f"TG:{m.from_user.id}", "API Sorgu", f"/{cmd} {args}")
            bot.reply_to(m,f"<pre>{json.dumps(res,indent=2,ensure_ascii=False)}</pre>")
        else:
            bot.reply_to(m,"Komut yok")

# ================== WEB ==================
app = Flask(__name__)
app.secret_key = "lord-secret"

LOGIN_HTML = """
<h3>Giriş</h3>
<form method=post>
<input name=user placeholder="user/admin"><br>
<input name=pass type=password placeholder="şifre"><br>
{{a}}+{{b}}=?<br>
<input name=captcha><br>
<button>Giriş</button>
</form>
"""

ADMIN_HTML = """
<h3>ADMIN PANEL</h3>
<a href="/logout">Çıkış</a>
<h4>LOGS</h4>
{% for l in logs %}
<p>[{{l.time}}] <b>{{l.action}}</b> - {{l.who}} : {{l.detail}}</p>
{% endfor %}
"""

USER_HTML = """
<h3>KULLANICI PANEL</h3>
<a href="/logout">Çıkış</a>
<h4>Sorgularım</h4>
{% for l in logs %}
<p>[{{l.time}}] {{l.detail}}</p>
{% endfor %}
"""

@app.route("/", methods=["GET","POST"])
def login():
    if "a" not in session:
        session["a"]=random.randint(1,9)
        session["b"]=random.randint(1,9)
    if request.method=="POST":
        if int(request.form["captcha"])!=session["a"]+session["b"]:
            session.clear(); return redirect("/")
        u,p=request.form["user"],request.form["pass"]
        session.clear()
        if u=="admin" and p==ADMIN_PASSWORD:
            session["admin"]=1; log_event("ADMIN","Web Giriş",""); return redirect("/admin")
        if u=="user" and p==USER_PASSWORD:
            session["user"]=1; log_event("USER","Web Giriş",""); return redirect("/user")
    return render_template_string(LOGIN_HTML,a=session["a"],b=session["b"])

@app.route("/admin")
def admin():
    if not session.get("admin"): return redirect("/")
    return render_template_string(ADMIN_HTML, logs=load_logs())

@app.route("/user")
def user():
    if not session.get("user"): return redirect("/")
    user_logs=[l for l in load_logs() if l["who"].startswith("TG") or l["who"]=="USER"]
    return render_template_string(USER_HTML, logs=user_logs)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================== RUN ==================
if __name__=="__main__":
    if bot:
        threading.Thread(target=lambda:bot.infinity_polling(skip_pending=True),daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
