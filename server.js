// server.js — TEK DOSYA
// npm install express node-fetch

const express = require('express');
const fetch = require('node-fetch');
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// ================== AYARLAR ==================
const PORT = process.env.PORT || 3000;
let PANEL_PASSWORD = process.env.PANEL_PASSWORD || '2026lord';

// ================== API'LER (GİZLİ) ==================
const APIS = {
  gsmtc: gsm => `https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm=${gsm}`,
  adsoyad: (ad, soyad) => `https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad=${ad}&soyad=${soyad}`,
  tcgsm: tc => `https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc=${tc}`,
  recete: tc => `https://nabisorguapis.onrender.com/api/v1/eczane/recete-gecmisi?tc=${tc}`,
  istanbulkart: tc => `https://nabisorguapis.onrender.com/api/v1/ulasim/istanbulkart-bakiye?tc=${tc}`,
  vergi: tc => `https://nabisorguapis.onrender.com/api/v1/vergi/borc-sorgu?tc=${tc}`,
  su: tc => `https://nabisorguapis.onrender.com/api/v1/ibb/su-fatura?tc=${tc}`
};

// ================== LOGIN ==================
app.post('/login', (req, res) => {
  if (req.body.password === PANEL_PASSWORD) {
    return res.json({ ok: true });
  }
  res.status(401).json({ ok: false });
});

// ================== ADMIN ==================
app.post('/admin/change-password', (req, res) => {
  const { newPassword } = req.body;
  if (!newPassword) return res.status(400).json({ ok: false });
  PANEL_PASSWORD = newPassword;
  res.json({ ok: true });
});

// ================== API PROXY ==================
app.post('/api/:type', async (req, res) => {
  try {
    const t = req.params.type;
    let url;

    if (t === 'gsmtc') url = APIS.gsmtc(req.body.value);
    else if (t === 'adsoyad') url = APIS.adsoyad(req.body.ad, req.body.soyad);
    else if (t === 'tcgsm') url = APIS.tcgsm(req.body.value);
    else if (t === 'recete') url = APIS.recete(req.body.value);
    else if (t === 'istanbulkart') url = APIS.istanbulkart(req.body.value);
    else if (t === 'vergi') url = APIS.vergi(req.body.value);
    else if (t === 'su') url = APIS.su(req.body.value);
    else return res.status(404).end();

    const r = await fetch(url);
    const j = await r.json();
    res.json(j);
  } catch {
    res.status(500).json({ error: "Sorgu hatası" });
  }
});

// ================== UI ==================
app.get('/', (req, res) => res.send(`
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
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
.then(r=>r.json()).then(j=>{if(j.ok){loginDiv()}})
}
function loginDiv(){
login.classList.add('hidden');
app.classList.remove('hidden');
}
function toggle(){drawer.classList.toggle('open')}
function openQ(t){
drawer.classList.remove('open');
content.innerHTML=\`
<div class="card">
<h3>\${t.toUpperCase()}</h3>
<input id="val" placeholder="Değer gir">
<button class="btn" onclick="run('\${t}')">SORGULA</button>
<pre id="out"></pre>
</div>\`
}
function run(t){
fetch('/api/'+t,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({value:val.value,ad:val.value,soyad:val.value})})
.then(r=>r.json()).then(j=>out.textContent=JSON.stringify(j,null,2))
}
</script>

</body>
</html>
`));

app.listen(PORT, () => console.log("RUNNING", PORT));
