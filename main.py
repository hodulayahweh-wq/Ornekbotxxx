# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template_string
import requests
import os
import json

app = Flask(__name__)

# SABİT ŞİFRELER
USER_PASSWORD = "2026lordvipfree"
ADMIN_PASSWORD = "@lorddestekhatvip"

PORT = int(os.environ.get("PORT", 5000))
DATA_FILE = "apis.json"

DEFAULT_APIS = {
    "adrespro": "https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc={v}",
    "adsoyadpro": "https://sorgum.2026tr.xyz/nabi/api/v1/adsoyad?ad={a}&soyad={s}&q={q}",
    "ailepro": "https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc={v}",
    "gsmpro": "https://sorgum.2026tr.xyz/nabi/api/v1/gsm?q={v}"
}

# ------------------ API KAYIT ------------------

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

def call_api(url):
    r = requests.get(url, timeout=20)
    try:
        j = r.json()
    except Exception:
        return {"raw": r.text}
    return j.get("veri", j)

# ------------------ LOGIN ------------------

@app.route("/login", methods=["POST"])
def user_login():
    data = request.get_json(force=True)
    if data.get("password") == USER_PASSWORD:
        return {"ok": True}
    return {"ok": False}, 401


@app.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json(force=True)
    if data.get("password") == ADMIN_PASSWORD:
        return {"ok": True}
    return {"ok": False}, 401

# ------------------ API PROXY ------------------

@app.route("/api/<name>", methods=["POST"])
def api_proxy(name):
    apis = load_apis()
    if name not in apis:
        return {"error": "Geçersiz API"}, 404

    body = request.get_json(force=True)
    url = apis[name].format(
        v=body.get("value", ""),
        a=body.get("ad", ""),
        s=body.get("soyad", ""),
        q=body.get("q", "")
    )
    return jsonify(call_api(url))

# ------------------ UI ------------------

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

<div class="box" id="loginBox">
<h3>Kullanıcı Giriş</h3>
<input id="userpass" type="password" placeholder="Kullanıcı Şifresi">
<button onclick="userLogin()">Giriş</button>
</div>

<div class="box" id="adminBox">
<h3>Admin Giriş</h3>
<input id="adminpass" type="password" placeholder="Admin Şifresi">
<button onclick="adminLogin()">Admin Giriş</button>
</div>

<div class="box" id="app" style="display:none">
<h3>Sorgular</h3>
{% for k in apis %}
<button onclick="run('{{k}}')">{{k}}</button>
{% endfor %}
<pre id="out"></pre>
</div>

<script>
function userLogin(){
fetch('/login',{
  method:'POST',
  headers:{'Content-Type':'application/json'},
  body:JSON.stringify({password:document.getElementById('userpass').value})
})
.then(r=>r.json())
.then(d=>{
  if(d.ok){
    document.getElementById('loginBox').style.display='none';
    document.getElementById('adminBox').style.display='none';
    document.getElementById('app').style.display='block';
  }else{
    alert('Kullanıcı şifresi yanlış');
  }
});
}

function adminLogin(){
fetch('/admin/login',{
  method:'POST',
  headers:{'Content-Type':'application/json'},
  body:JSON.stringify({password:document.getElementById('adminpass').value})
})
.then(r=>r.json())
.then(d=>{
  if(d.ok){
    alert('Admin girişi başarılı');
  }else{
    alert('Admin şifresi yanlış');
  }
});
}

function run(q){
let v = prompt("Değer gir");
fetch('/api/'+q,{
  method:'POST',
  headers:{'Content-Type':'application/json'},
  body:JSON.stringify({value:v})
})
.then(r=>r.json())
.then(j=>{
  document.getElementById('out').textContent = JSON.stringify(j,null,2);
});
}
</script>

</body>
</html>
""", apis=apis)

# ------------------ RUN ------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
