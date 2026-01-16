# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template_string
import requests
import os
import json

app = Flask(__name__)

# SABİT ŞİFRELER (DEĞİŞMEZ)
PANEL_PASSWORD = "lord2026freepanel"
ADMIN_PASSWORD = "lordatar6367"

PORT = 5000
DATA_FILE = "apis.json"

DEFAULT_APIS = {
    "adrespro": "https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc={v}",
    "adsoyadpro": "https://sorgum.2026tr.xyz/nabi/api/v1/adsoyad?ad={a}&soyad={s}&q={q}",
    "ailepro": "https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc={v}",
    "gsmpro": "https://sorgum.2026tr.xyz/nabi/api/v1/gsm?q={v}",
    "babapro": "https://sorgum.2026tr.xyz/nabi/api/v1/baba?tc={v}",
    "annepro": "https://sorgum.2026tr.xyz/nabi/api/v1/anne?tc={v}",
    "tcpro": "https://sorgum.2026tr.xyz/nabi/api/v1/tcpro?tc={v}"
}

def load_apis():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_APIS, f, ensure_ascii=False, indent=2)
        return dict(DEFAULT_APIS)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for k, v in DEFAULT_APIS.items():
        data.setdefault(k, v)

    return data

def save_apis(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def call_api(url):
    r = requests.get(url, timeout=20)
    try:
        j = r.json()
    except Exception:
        return {"raw": r.text}

    if isinstance(j, dict) and "veri" in j:
        return j["veri"]
    return j

@app.route("/login", methods=["POST"])
def login():
    if request.json and request.json.get("password") == PANEL_PASSWORD:
        return {"ok": True}
    return {"ok": False}, 401

@app.route("/admin/login", methods=["POST"])
def admin_login():
    if request.json and request.json.get("password") == ADMIN_PASSWORD:
        return {"ok": True}
    return {"ok": False}, 401

@app.route("/api/<name>", methods=["POST"])
def api_proxy(name):
    apis = load_apis()
    if name not in apis:
        return {"error": "Geçersiz API"}, 404

    body = request.json or {}
    url = apis[name].format(
        v=body.get("value", ""),
        a=body.get("ad", ""),
        s=body.get("soyad", ""),
        q=body.get("q", "")
    )
    return jsonify(call_api(url))

@app.route("/admin/apis")
def admin_apis():
    return load_apis()

@app.route("/admin/add", methods=["POST"])
def admin_add():
    body = request.json or {}
    name = body.get("name", "").lower().strip()
    url = body.get("url", "").strip()

    if not name or not url:
        return {"error": "Eksik"}, 400

    data = load_apis()
    data[name] = url
    save_apis(data)
    return {"ok": True}

@app.route("/")
def index():
    apis = load_apis()
    return render_template_string("""
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LORD SYSTEM 2026</title>
<style>
body{background:#050814;color:#fff;font-family:sans-serif;margin:0}
.box{max-width:420px;margin:24px auto;background:#0b1230;padding:18px;border-radius:16px}
input,button{width:100%;padding:14px;margin-top:10px;border-radius:12px;border:0}
button{background:#1D9BF0;color:white;font-weight:700}
pre{white-space:pre-wrap}
</style>
</head>
<body>

<div class="box" id="login">
<h3>Kullanıcı Giriş</h3>
<input id="pass" type="password">
<button onclick="login()">Giriş</button>
</div>

<div class="box" id="app" style="display:none">
<h3>Sorgular</h3>
{% for k in apis %}
<button onclick="run('{{k}}')">{{k}}</button>
{% endfor %}
<pre id="out"></pre>
</div>

<script>
function login(){
fetch('/login',{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({password:pass.value})
}).then(r=>{
if(!r.ok) throw 0;
login.style.display='none';
app.style.display='block';
}).catch(()=>alert('Şifre yanlış'));
}

function run(q){
let v=prompt('Değer');
fetch('/api/'+q,{
method:'POST',
headers:{'Content-Type':'application/json'},
body:JSON.stringify({value:v})
}).then(r=>r.json()).then(j=>{
out.textContent=JSON.stringify(j,null,2);
});
}
</script>

</body>
</html>
""", apis=apis)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
