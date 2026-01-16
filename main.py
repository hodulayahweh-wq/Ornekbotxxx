from flask import Flask, request, jsonify, render_template_string
import requests, os, json

app = Flask(__name__)

# Panel Şifresi
PANEL_PASSWORD = os.environ.get("PANEL_PASSWORD", "2026xlord")

# API'leri çağırma fonksiyonu
def fetch_api(url):
    r = requests.get(url, timeout=20)
    return r.json()

# Admin Paneli İçin Veri
commands = {}

# Giriş
@app.post("/login")
def login():
    if request.json.get("password") == PANEL_PASSWORD:
        return {"ok": True}
    return {"ok": False}, 401

# Admin Paneli İçin Sorgu Ekleme
@app.post("/admin/add_command")
def add_command():
    if request.json.get("password") == PANEL_PASSWORD:
        command_name = request.json.get("name")
        api_url = request.json.get("api_url")
        if command_name and api_url:
            commands[command_name] = {"url": api_url, "enabled": True}
            return {"status": "success", "message": f"Command {command_name} added!"}
        return {"status": "error", "message": "Name and API URL are required!"}, 400
    return {"status": "error", "message": "Unauthorized"}, 401

# Kullanıcı ve Admin API'leri
@app.post("/api/<name>")
def api(name):
    v = request.json.get("value", "")
    ad = request.json.get("ad", "")
    soyad = request.json.get("soyad", "")
    q = request.json.get("q", "")

    apis = {
        "gsmtc": f"https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm={v}",
        "adsoyad": f"https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad={ad}&soyad={soyad}",
        "tcgsm": f"https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc={v}",
        "recete": f"https://nabisorguapis.onrender.com/api/v1/eczane/recete-gecmisi?tc={v}",
        "istanbulkart": f"https://nabisorguapis.onrender.com/api/v1/ulasim/istanbulkart-bakiye?tc={v}",
        "vergi": f"https://nabisorguapis.onrender.com/api/v1/vergi/borc-sorgu?tc={v}",
        "su": f"https://nabisorguapis.onrender.com/api/v1/ibb/su-fatura?tc={v}",
        "adrespro": f"https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc={v}",
        "adsoyadpro": f"https://sorgum.2026tr.xyz/nabi/api/v1/adsoyad?ad={ad}&soyad={soyad}&q={q}",
        "ailepro": f"https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc={v}",
        "gsmpro": f"https://sorgum.2026tr.xyz/nabi/api/v1/gsm?q={v}",
        "babapro": f"https://sorgum.2026tr.xyz/nabi/api/v1/baba?tc={v}",
        "annepro": f"https://sorgum.2026tr.xyz/nabi/api/v1/anne?tc={v}",
        "tcpro": f"https://sorgum.2026tr.xyz/nabi/api/v1/tcpro?tc={v}",
    }

    if name not in apis:
        return {"error": "API bulunamadı"}, 404

    return jsonify(fetch_api(apis[name]))

# Anasayfa
@app.get("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>LORD SORGU</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;800&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Inter;background:#0b1020;color:#fff;overflow-x:hidden}
.bg-anim{position:fixed;inset:0;background:linear-gradient(120deg,rgba(29,155,240,.15),transparent);animation:move 6s infinite alternate;z-index:-1}
@keyframes move{to{transform:translateX(60px)}}

.glass{background:rgba(255,255,255,.08);backdrop-filter:blur(16px);border-radius:20px;padding:24px;box-shadow:0 20px 40px rgba(0,0,0,.4)}
.center{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.btn{background:#1D9BF0;border:0;color:#fff;padding:14px;border-radius:14px;width:100%;font-weight:800;cursor:pointer;transition:.3s}
.btn:hover{transform:scale(1.04)}
input{width:100%;padding:14px;border-radius:14px;border:0;margin-bottom:14px}
.hidden{display:none}

.menu{position:fixed;top:0;left:0;right:0;padding:14px;background:rgba(0,0,0,.3);backdrop-filter:blur(12px)}
.drawer{position:fixed;top:0;left:-100%;width:80%;height:100%;background:#0f1530;padding:20px;transition:.4s}
.drawer.open{left:0}
.item{margin-bottom:12px}
.title{display:flex;align-items:center;gap:10px;font-weight:800}
.fade{animation:fade .8s}
@keyframes fade{from{opacity:0;transform:translateY(20px)}}
</style>
</head>

<body>
<div class="bg-anim"></div>

<div id="login" class="center fade">
<div class="glass" style="max-width:360px;width:100%">
<h2>👋 Hoşgeldiniz</h2>
<p>LORD SORGU sistemine giriş yap</p>
<input id="pass" placeholder="Panel Şifresi">
<button class="btn" onclick="login()">Giriş Yap</button>
</div>
</div>

<div id="app" class="hidden fade">
<div class="menu">
<button class="btn" onclick="toggle()">☰ Menü</button>
</div>

<div id="drawer" class="drawer">
<div class="title">LORD SORGU ✔️</div><hr>
<div class="item"><button class="btn" onclick="openQ('gsmtc')">GSM → TC</button></div>
<div class="item"><button class="btn" onclick="openQ('adsoyad')">Ad Soyad</button></div>
<div class="item"><button class="btn" onclick="openQ('tcgsm')">TC → GSM</button></div>
<div class="item"><button class="btn" onclick="openQ('recete')">Reçete</button></div>
<div class="item"><button class="btn" onclick="openQ('istanbulkart')">İstanbulkart</button></div>
<div class="item"><button class="btn" onclick="openQ('vergi')">Vergi</button></div>
<div class="item"><button class="btn" onclick="openQ('su')">Su Faturası</button></div>
<div class="item"><button class="btn" onclick="openQ('adrespro')">TC → Adres</button></div>
<div class="item"><button class="btn" onclick="openQ('adsoyadpro')">Ad Soyad Pro</button></div>
<div class="item"><button class="btn" onclick="openQ('ailepro')">Aile Pro</button></div>
<div class="item"><button class="btn" onclick="openQ('gsmpro')">GSM Pro</button></div>
<div class="item"><button class="btn" onclick="openQ('babapro')">Baba Bilgisi</button></div>
<div class="item"><button class="btn" onclick="openQ('annepro')">Anne Bilgisi</button></div>
<div class="item"><button class="btn" onclick="openQ('tcpro')">TC PRO</button></div>
</div>

<div id="content" class="center"></div>
</div>

<script>
function login(){
fetch("/login",{method:"POST",headers:{"Content-Type":"application/json"},
body:JSON.stringify({password:pass.value})})
.then(r=>r.json()).then(j=>{
if(j.ok){login.classList.add("hidden");app.classList.remove("hidden")}
else alert("Hatalı şifre")
})
}
function toggle(){drawer.classList.toggle("open")}
function openQ(q){
drawer.classList.remove("open");
content.innerHTML=`
<div class="glass fade" style="width:100%;max-width:420px">
<h3>${q.toUpperCase()}</h3>
<input id="v" placeholder="TC / GSM / Ad">
<input id="qv" placeholder="Opsiyonel (şehir vb)">
<button class="btn" onclick="run('${q}')">SORGULA</button>
<pre id="out"></pre>
</div>`
}
function run(q){
fetch("/api/"+q,{method:"POST",headers:{"Content-Type":"application/json"},
body:JSON.stringify({value:v.value,ad:v.value,soyad:v.value,q:qv.value})})
.then(r=>r.json()).then(j=>out.textContent=JSON.stringify(j,null,2))
}
</script>

</body>
</html>
""")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
