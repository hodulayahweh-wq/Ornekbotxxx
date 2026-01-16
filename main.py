import os, json, time, threading, secrets, datetime, requests
from flask import Flask, request, session, redirect, render_template_string
import telebot

# ================= AYAR =================
BOT_TOKEN = os.getenv("BOT_TOKEN","")
ADMIN_ID  = int(os.getenv("ADMIN_ID","0"))
PORT      = int(os.getenv("PORT","5000"))

ADMIN_PASSWORD = "2026xlord"
USER_PASSWORD  = "2026lordcheck"

API_FILE   = "apis.json"
LOG_FILE   = "logs.json"
TOKENS     = "tg_tokens.json"
IPS        = "ips.json"

# ================= DEFAULT API =================
DEFAULT_APIS = {
 "gsmtc": {"url":"https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm=","on":1},
 "adsoyad":{"url":"https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad={ad}&soyad={soyad}","on":1},
 "tcgsm": {"url":"https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc=","on":1},
 "recete":{"url":"https://nabisorguapis.onrender.com/api/v1/eczane/recete-gecmisi?tc=","on":1},
 "istanbulkart":{"url":"https://nabisorguapis.onrender.com/api/v1/ulasim/istanbulkart-bakiye?tc=","on":1},
 "vergi":{"url":"https://nabisorguapis.onrender.com/api/v1/vergi/borc-sorgu?tc=","on":1},
 "su":{"url":"https://nabisorguapis.onrender.com/api/v1/ibb/su-fatura?tc=","on":1}
}

# ================= DOSYA =================
def ensure(f,d):
    if not os.path.exists(f):
        json.dump(d,open(f,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

ensure(API_FILE,DEFAULT_APIS)
ensure(LOG_FILE,[])
ensure(TOKENS,{})
ensure(IPS,[])

def load(f): return json.load(open(f,encoding="utf-8"))
def save(f,d): json.dump(d,open(f,"w",encoding="utf-8"),ensure_ascii=False,indent=2)

# ================= LOG =================
def log_event(who,act,det):
    logs = load(LOG_FILE)
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logs.insert(0,{"time":t,"who":who,"action":act,"detail":det})
    save(LOG_FILE,logs[:500])
    if bot and ADMIN_ID:
        bot.send_message(ADMIN_ID,f"📌 {act}\n👤 {who}\n🕒 {t}\n📝 {det}")

# ================= API CALL =================
def call_api(url):
    try:
        r=requests.get(url,timeout=15)
        if "json" in r.headers.get("content-type",""):
            return r.json()
        return {"raw":r.text}
    except Exception as e:
        return {"error":str(e)}

# ================= BOT =================
bot = telebot.TeleBot(BOT_TOKEN,parse_mode="HTML") if BOT_TOKEN else None

if bot:
    @bot.message_handler(commands=["login"])
    def tg_login(m):
        token=secrets.token_hex(16)
        t=load(TOKENS)
        t[token]={"id":m.from_user.id,"time":time.time()}
        save(TOKENS,t)
        bot.reply_to(m,f"🔐 Web giriş linkin:\nhttps://YOUR-RENDER.onrender.com/tg/{token}")

# ================= WEB =================
app=Flask(__name__)
app.secret_key="lord-ultra"

USER_HTML = """
<!doctype html><html><head>
<meta name=viewport content="width=device-width,initial-scale=1">
<style>
body{margin:0;font-family:Arial;background:#020617;color:#fff}
.menu{position:fixed;left:0;top:0;width:260px;height:100%;
background:#020617;border-right:1px solid #1e293b;transform:translateX(-100%);
transition:.3s;padding:15px}
.menu a{display:block;padding:10px;color:#fff;text-decoration:none}
.menu a:hover{background:#1e293b}
.open{transform:translateX(0)}
.top{padding:10px;background:#020617;border-bottom:1px solid #1e293b}
button{padding:10px;border-radius:10px;border:0}
input,select{width:100%;padding:10px;margin:5px 0;border-radius:10px;border:0}
pre{white-space:pre-wrap;font-size:12px}
</style>
<script>
function toggle(){document.getElementById('menu').classList.toggle('open')}
</script>
</head>
<body>

<div class="top">
<button onclick="toggle()">☰</button> LORD ULTRA
</div>

<div id="menu" class="menu">
{% for k,v in apis.items() if v.on %}
<a href="/user?api={{k}}">{{k}}</a>
{% endfor %}
<a href="/logout">Çıkış</a>
</div>

<div style="padding:15px">
{% if api %}
<form method=post action=/query>
<input name=v1 placeholder="tc / gsm / ad">
<input name=v2 placeholder="soyad (gerekirse)">
<input type=hidden name=api value="{{api}}">
<button>Sorgula</button>
</form>
{% endif %}

{% if result %}
<pre>{{result}}</pre>
{% endif %}
</div>
</body></html>
"""

ADMIN_HTML = """
<h2>🛡 ADMIN PANEL</h2>

<h3>➕ API EKLE</h3>
<form method=post action=/admin/add>
<input name=name placeholder=isim>
<input name=url placeholder="api url">
<button>Ekle</button>
</form>

<h3>📜 API LİSTESİ</h3>
{% for k,v in apis.items() %}
<p>
<b>{{k}}</b> | {{v.url}} |
<a href="/admin/toggle/{{k}}">Aç/Kapat</a> |
<a href="/admin/del/{{k}}">Sil</a>
</p>
{% endfor %}

<h3>📊 LOG</h3>
{% for l in logs %}
<p>[{{l.time}}] {{l.who}} - {{l.action}} - {{l.detail}}</p>
{% endfor %}
"""

@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form["pass"]==USER_PASSWORD:
            session["user"]=1
            ip=request.remote_addr
            ips=load(IPS)
            if ip not in ips: ips.append(ip); save(IPS,ips)
            return redirect("/user")
        if request.form["pass"]==ADMIN_PASSWORD:
            session["admin"]=1
            return redirect("/admin")
    return '<form method=post><input type=password name=pass><button>Giriş</button></form>'

@app.route("/tg/<t>")
def tg(t):
    data=load(TOKENS)
    if t in data:
        session["user"]=1
        ip=request.remote_addr
        ips=load(IPS)
        if ip not in ips: ips.append(ip); save(IPS,ips)
        del data[t]; save(TOKENS,data)
        log_event("TG","Telegram Login",ip)
        return redirect("/user")
    return "Geçersiz"

@app.route("/user")
def user():
    if not session.get("user"): return redirect("/")
    api=request.args.get("api")
    return render_template_string(USER_HTML,apis=load(API_FILE),api=api)

@app.route("/query",methods=["POST"])
def query():
    if not session.get("user"): return redirect("/")
    api=request.form["api"]
    apis=load(API_FILE)
    base=apis[api]["url"]
    v1=request.form.get("v1","")
    v2=request.form.get("v2","")
    if "{ad}" in base:
        url=base.format(ad=v1,soyad=v2)
    else:
        url=base+v1
    res=call_api(url)
    log_event("WEB","Sorgu",api)
    return render_template_string(USER_HTML,apis=apis,api=api,
        result=json.dumps(res,indent=2,ensure_ascii=False))

@app.route("/admin")
def admin():
    if not session.get("admin"): return redirect("/")
    return render_template_string(ADMIN_HTML,apis=load(API_FILE),logs=load(LOG_FILE))

@app.route("/admin/add",methods=["POST"])
def add_api():
    if not session.get("admin"): return redirect("/")
    apis=load(API_FILE)
    apis[request.form["name"]]={"url":request.form["url"],"on":1}
    save(API_FILE,apis)
    log_event("ADMIN","API EKLE",request.form["name"])
    return redirect("/admin")

@app.route("/admin/del/<k>")
def del_api(k):
    if not session.get("admin"): return redirect("/")
    apis=load(API_FILE)
    if k in apis: del apis[k]
    save(API_FILE,apis)
    log_event("ADMIN","API SİL",k)
    return redirect("/admin")

@app.route("/admin/toggle/<k>")
def tog(k):
    if not session.get("admin"): return redirect("/")
    apis=load(API_FILE)
    apis[k]["on"]=0 if apis[k]["on"] else 1
    save(API_FILE,apis)
    log_event("ADMIN","API DURUM",k)
    return redirect("/admin")

@app.route("/logout")
def logout():
    session.clear(); return redirect("/")

# ================= RUN =================
if __name__=="__main__":
    if bot:
        threading.Thread(target=lambda:bot.infinity_polling(skip_pending=True),
                         daemon=True).start()
    app.run("0.0.0.0",PORT)
