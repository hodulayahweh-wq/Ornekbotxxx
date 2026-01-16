-- coding: utf-8 --

""" LORD SYSTEM 2026 – ANDROID FIXED VERSION

sorunu yok, GitHub/Android uyumlu

Tek dosya | Flask | Pydroid 3 + Render uyumlu """

from flask import Flask, request, jsonify, render_template_string import requests, os, json

app = Flask(name)

AYARLAR

PANEL_PASSWORD = os.environ.get("PANEL_PASSWORD", "atar6367lord") ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "atar6367lord") PORT = int(os.environ.get("PORT", 5000)) DATA_FILE = "apis.json"

DEFAULT_APIS = { "adrespro": "https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc={v}", "adsoyadpro": "https://sorgum.2026tr.xyz/nabi/api/v1/adsoyad?ad={a}&soyad={s}&q={q}", "ailepro": "https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc={v}", "gsmpro": "https://sorgum.2026tr.xyz/nabi/api/v1/gsm?q={v}" }

YARDIMCILAR

def load_apis(): if not os.path.exists(DATA_FILE): with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(DEFAULT_APIS, f, ensure_ascii=False, indent=2) return dict(DEFAULT_APIS) with open(DATA_FILE, "r", encoding="utf-8") as f: data = json.load(f) for k, v in DEFAULT_APIS.items(): data.setdefault(k, v) return data

def save_apis(data): with open(DATA_FILE, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

def call_api(url): r = requests.get(url, timeout=20) r.raise_for_status() try: j = r.json() except Exception: return {"raw": r.text} if isinstance(j, dict) and "veri" in j: return j["veri"] return j

AUTH

@app.post("/login") def login(): if request.json and request.json.get("password") == PANEL_PASSWORD: return {"ok": True} return {"ok": False}, 401

@app.post("/admin/login") def admin_login(): if request.json and request.json.get("password") == ADMIN_PASSWORD: return {"ok": True} return {"ok": False}, 401

API

@app.post("/api/<name>") def api_proxy(name): data = load_apis() if name not in data: return {"error": "Geçersiz"}, 404 body = request.json or {} url = data[name].format( v=body.get("value", ""), a=body.get("ad", ""), s=body.get("soyad", ""), q=body.get("q", "") ) return jsonify(call_api(url))

ADMIN

@app.get("/admin/apis") def admin_apis(): return load_apis()

@app.post("/admin/add") def admin_add(): body = request.json or {} if not body.get("name") or not body.get("url"): return {"error": "Eksik"}, 400 data = load_apis() data[body["name"].lower()] = body["url"] save_apis(data) return {"ok": True}

UI

@app.get("/") def index(): apis = load_apis() return render_template_string("""

<!DOCTYPE html><html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LORD SYSTEM 2026</title>
<style>
body{background:#050814;color:white;font-family:sans-serif;margin:0}
.box{max-width:420px;margin:40px auto;background:#0b1230;padding:20px;border-radius:16px}
button,input{width:100%;padding:14px;margin-top:10px;border-radius:12px;border:0}
button{background:#1D9BF0;color:white;font-weight:700}
pre{white-space:pre-wrap;word-break:break-word}
</style>
</head>
<body>
<div class="box" id="login">
<h3>Kullanıcı Giriş</h3>
<input id="pass" type="password" placeholder="Panel Şifresi">
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
fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:pass.value})})
.then(r=>{if(!r.ok)throw 0;login.style.display='none';app.style.display='block'})
.catch(()=>alert('Şifre yanlış'))}
function run(q){
let v=prompt('Değer');
fetch('/api/'+q,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({value:v})})
.then(r=>r.json()).then(j=>out.textContent=JSON.stringify(j,null,2))}
</script>
</body>
</html>
""", apis=apis)RUN

if name == 'main': app.run(host='0.0.0.0', port=PORT)
