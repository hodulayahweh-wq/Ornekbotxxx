from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

# ================== AYAR ==================
PANEL_PASSWORD = os.environ.get("PANEL_PASSWORD", "2026lord")

# ================== GİZLİ API'LER ==================
def gsmtc(gsm):
    return f"https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm={gsm}"

def adsoyad(ad, soyad):
    return f"https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad={ad}&soyad={soyad}"

def tcgsm(tc):
    return f"https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc={tc}"

def recete(tc):
    return f"https://nabisorguapis.onrender.com/api/v1/eczane/recete-gecmisi?tc={tc}"

def istanbulkart(tc):
    return f"https://nabisorguapis.onrender.com/api/v1/ulasim/istanbulkart-bakiye?tc={tc}"

def vergi(tc):
    return f"https://nabisorguapis.onrender.com/api/v1/vergi/borc-sorgu?tc={tc}"

def su(tc):
    return f"https://nabisorguapis.onrender.com/api/v1/ibb/su-fatura?tc={tc}"

# ================== LOGIN ==================
@app.post("/login")
def login():
    if request.json.get("password") == PANEL_PASSWORD:
        return {"ok": True}
    return {"ok": False}, 401

# ================== API PROXY ==================
@app.post("/api/<t>")
def api_proxy(t):
    try:
        data = request.json.get("value", "")
        ad = request.json.get("ad", "")
        soyad = request.json.get("soyad", "")

        if t == "gsmtc":
            url = gsmtc(data)
        elif t == "adsoyad":
            url = adsoyad(ad, soyad)
        elif t == "tcgsm":
            url = tcgsm(data)
        elif t == "recete":
            url = recete(data)
        elif t == "istanbulkart":
            url = istanbulkart(data)
        elif t == "vergi":
            url = vergi(data)
        elif t == "su":
            url = su(data)
        else:
            return {"error": "Geçersiz sorgu"}, 404

        r = requests.get(url, timeout=15)
        return jsonify(r.json())
    except Exception as e:
        return {"error": "Sorgu hatası"}, 500

# ================== UI ==================
@app.get("/")
def index():
    return render_template_string("""
<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>LORD SORGU</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{margin:0;background:#0b1020;color:#fff;font-family:system-ui}
.card{background:#0f1530;margin:20px;padding:20px;border-radius:16px}
.btn{background:#1D9BF0;border:0;padding:14px;width:100%;color:#fff;font-weight:800;border-radius:12px}
input{width:100%;padding:12px;border-radius:12px;border:0;margin-bottom:10px}
.hidden{display:none}
.menu{padding:14px;background:#0f1530;position:fixed;top:0;left:0;right:0}
.drawer{position:fixed;top:0;left:-100%;width:80%;height:100%;background:#0f1530;transition:.3s;padding:20px}
.drawer.open{left:0}
.verified{display:flex;gap:8px;align-items:center;font-weight:800}
</style>
</head>
<body>

<div id="login" class="card">
<h2>Panel Girişi</h2>
<input id="pass" placeholder="Panel Şifresi">
<button class="btn" onclick="login()">GİRİŞ</button>
</div>

<div id="app" class="hidden">
<div class="menu">
<button class="btn" onclick="toggle()">☰ Menü</button>
</div>

<div id="drawer" class="drawer">
<div class="verified">LORD SORGU ✅</div><hr>
<button class="btn" onclick="openQ('gsmtc')">GSM → TC</button><br><br>
<button class="btn" onclick="openQ('adsoyad')">Ad Soyad</button><br><br>
<button class="btn" onclick="openQ('tcgsm')">TC → GSM</button><br><br>
<button class="btn" onclick="openQ('recete')">Reçete</button><br><br>
<button class="btn" onclick="openQ('istanbulkart')">İstanbulkart</button><br><br>
<button class="btn" onclick="openQ('vergi')">Vergi</button><br><br>
<button class="btn" onclick="openQ('su')">Su Faturası</button><br><br>
<button class="btn" onclick="location.reload()">Çıkış</button>
</div>

<div id="content" style="margin-top:80px"></div>
</div>

<script>
function login(){
fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:pass.value})})
.then(r=>r.json()).then(j=>{if(j.ok){login.classList.add('hidden');app.classList.remove('hidden')}})
}
function toggle(){drawer.classList.toggle('open')}
function openQ(t){
drawer.classList.remove('open');
content.innerHTML=`
<div class="card">
<h3>${t.toUpperCase()}</h3>
<input id="val" placeholder="Değer">
<button class="btn" onclick="run('${t}')">SORGULA</button>
<pre id="out"></pre>
</div>`
}
function run(t){
fetch('/api/'+t,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({value:val.value,ad:val.value,soyad:val.value})})
.then(r=>r.json()).then(j=>out.textContent=JSON.stringify(j,null,2))
}
</script>

</body>
</html>
""")

# ================== START ==================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
