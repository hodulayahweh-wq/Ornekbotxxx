from flask import Flask, request, jsonify, render_template_string
import requests, os

app = Flask(__name__)

PANEL_PASSWORD = os.environ.get("PANEL_PASSWORD", "2026lordfreepanel")

def call_api(url):
    r = requests.get(url, timeout=15)
    return r.json()

@app.post("/login")
def login():
    if request.json.get("password") == PANEL_PASSWORD:
        return {"ok": True}
    return {"ok": False}, 401

@app.post("/api/<q>")
def api(q):
    v = request.json.get("value","")
    a = request.json.get("ad","")
    s = request.json.get("soyad","")

    apis = {
        "gsmtc": f"https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm={v}",
        "adsoyad": f"https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad={a}&soyad={s}",
        "tcgsm": f"https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc={v}",
        "recete": f"https://nabisorguapis.onrender.com/api/v1/eczane/recete-gecmisi?tc={v}",
        "istanbulkart": f"https://nabisorguapis.onrender.com/api/v1/ulasim/istanbulkart-bakiye?tc={v}",
        "vergi": f"https://nabisorguapis.onrender.com/api/v1/vergi/borc-sorgu?tc={v}",
        "su": f"https://nabisorguapis.onrender.com/api/v1/ibb/su-fatura?tc={v}"
    }

    if q not in apis:
        return {"error":"Geçersiz"},404

    return jsonify(call_api(apis[q]))

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
body{
margin:0;
font-family:Inter;
background:radial-gradient(circle at top,#1D9BF0,#0b1020 60%);
color:#fff;
overflow-x:hidden
}
.bg-anim{
position:fixed;
inset:0;
background:linear-gradient(120deg,rgba(29,155,240,.15),transparent);
animation:move 6s infinite alternate;
z-index:-1
}
@keyframes move{to{transform:translateX(60px)}}

.glass{
background:rgba(255,255,255,.08);
backdrop-filter:blur(16px);
border-radius:20px;
padding:24px;
box-shadow:0 20px 40px rgba(0,0,0,.4)
}
.center{
min-height:100vh;
display:flex;
align-items:center;
justify-content:center;
padding:20px
}
.btn{
background:#1D9BF0;
border:0;
color:#fff;
padding:14px;
border-radius:14px;
width:100%;
font-weight:800;
cursor:pointer;
transition:.3s
}
.btn:hover{transform:scale(1.04)}
input{
width:100%;
padding:14px;
border-radius:14px;
border:0;
margin-bottom:14px
}
.hidden{display:none}

.menu{
position:fixed;
top:0;
left:0;
right:0;
padding:14px;
background:rgba(0,0,0,.3);
backdrop-filter:blur(12px)
}
.drawer{
position:fixed;
top:0;
left:-100%;
width:80%;
height:100%;
background:#0f1530;
padding:20px;
transition:.4s
}
.drawer.open{left:0}
.item{margin-bottom:12px}
.title{
display:flex;
align-items:center;
gap:10px;
font-weight:800
}
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
<div class="item"><button class="btn" onclick="location.reload()">Çıkış</button></div>
</div>

<div id="content" class="center"></div>
</div>

<script>
const loginBox=document.getElementById("login");
const appBox=document.getElementById("app");
const drawer=document.getElementById("drawer");
const content=document.getElementById("content");

function login(){
fetch("/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({password:pass.value})})
.then(r=>r.json()).then(j=>{
if(j.ok){loginBox.classList.add("hidden");appBox.classList.remove("hidden")}
else alert("Şifre yanlış")
})
}
function toggle(){drawer.classList.toggle("open")}
function openQ(q){
drawer.classList.remove("open");
content.innerHTML=`
<div class="glass fade" style="width:100%;max-width:420px">
<h3>${q.toUpperCase()}</h3>
<input id="v" placeholder="Değer">
<button class="btn" onclick="run('${q}')">SORGULA</button>
<pre id="out"></pre>
</div>`
}
function run(q){
fetch("/api/"+q,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({value:v.value,ad:v.value,soyad:v.value})})
.then(r=>r.json()).then(j=>out.textContent=JSON.stringify(j,null,2))
}
</script>

</body>
</html>
""")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
