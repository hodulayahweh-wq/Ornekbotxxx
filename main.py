// server.js — TEK DOSYA // npm i express node-fetch

const express = require('express'); const fetch = require('node-fetch');

const app = express(); app.use(express.json()); app.use(express.urlencoded({ extended: true }));

// ================== AYARLAR ================== const PORT = process.env.PORT || 3000; let PANEL_PASSWORD = process.env.PANEL_PASSWORD || '2026lord'; // admin değiştirince herkeste değişir

// ================== API'LER ================== // KULLANICIYA ASLA GÖSTERİLMEZ const APIS = { gsmtc: (gsm) => https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm=${gsm}, adsoyad: (ad, soyad) => https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad=${ad}&soyad=${soyad}, tcgsm: (tc) => https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc=${tc}, adres: (tc) => https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc=${tc}, aile: (tc) => https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc=${tc}, gsm: (q) => https://sorgum.2026tr.xyz/nabi/api/v1/gsm?q=${q}, baba: (tc) => https://sorgum.2026tr.xyz/nabi/api/v1/baba?tc=${tc}, anne: (tc) => https://sorgum.2026tr.xyz/nabi/api/v1/anne?tc=${tc}, tcpro: (tc) => https://sorgum.2026tr.xyz/nabi/api/v1/tcpro?tc=${tc} };

// ================== AUTH ================== app.post('/login', (req, res) => { const { password } = req.body; if (password === PANEL_PASSWORD) { return res.json({ ok: true }); } res.status(401).json({ ok: false }); });

app.post('/admin/change-password', (req, res) => { const { newPassword } = req.body; if (!newPassword) { return res.status(400).json({ ok: false }); } PANEL_PASSWORD = newPassword; res.json({ ok: true }); });

// ================== PROXY ================== app.post('/api/:name', async (req, res) => { try { const { name } = req.params; let url;

switch (name) {
  case 'gsmtc':
    url = APIS.gsmtc(req.body.gsm);
    break;
  case 'adsoyad':
    url = APIS.adsoyad(req.body.ad, req.body.soyad);
    break;
  case 'tcgsm':
    url = APIS.tcgsm(req.body.tc);
    break;
  case 'adres':
    url = APIS.adres(req.body.tc);
    break;
  case 'aile':
    url = APIS.aile(req.body.tc);
    break;
  case 'gsm':
    url = APIS.gsm(req.body.q);
    break;
  case 'baba':
    url = APIS.baba(req.body.tc);
    break;
  case 'anne':
    url = APIS.anne(req.body.tc);
    break;
  case 'tcpro':
    url = APIS.tcpro(req.body.tc);
    break;
  default:
    return res.status(404).end();
}

const r = await fetch(url);
const j = await r.json();
res.json(j);

} catch (e) { res.status(500).json({ error: 'Sorgu hatası' }); } });

// ================== UI ================== app.get('/', (req, res) => { res.send(`<!DOCTYPE html>

<html lang="tr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>LORD SORGU</title>
  <style>
    body { margin:0; background:#0b1020; color:#fff; font-family:system-ui }
    .hidden { display:none }
    .btn { background:#4f7cff; border:0; color:#fff; padding:14px; border-radius:12px; width:100%; font-weight:800 }
    .card { background:#0f1530; margin:14px; border-radius:16px; padding:14px }
    input { width:100%; padding:12px; border-radius:12px; border:0 }
    .menu { position:fixed; top:0; left:0; right:0; background:#0f1530; padding:14px }
    .drawer { position:fixed; top:0; left:-100%; width:80%; height:100%; background:#0f1530; transition:.3s; padding:16px }
    .drawer.open { left:0 }
    .verified { display:flex; gap:8px; align-items:center }
    @keyframes glow {
      0% { filter:drop-shadow(0 0 0 #1D9BF0) }
      50% { filter:drop-shadow(0 0 6px #1D9BF0) }
      100% { filter:drop-shadow(0 0 0 #1D9BF0) }
    }
    .verified svg { animation:glow 2s infinite }
  </style>
</head>
<body><div id="login" class="card">
  <h2>Giriş</h2>
  <input id="pass" placeholder="Panel Şifresi" />
  <br><br>
  <button class="btn" onclick="login()">GİRİŞ</button>
</div><div id="app" class="hidden">
  <div class="menu">
    <button class="btn" onclick="toggle()">☰ Menü</button>
  </div>  <div id="drawer" class="drawer">
    <div class="verified">
      <b>LORD SORGU</b>
      <svg width="20" height="20" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="12" fill="#1D9BF0" />
        <path d="M10.2 14.3L7.9 12l-1.1 1.1 3.4 3.4 7-7-1.1-1.1z" fill="#fff" />
      </svg>
    </div>
    <hr>
    <button class="btn" onclick="openQ('gsmtc')">GSM → TC</button><br><br>
    <button class="btn" onclick="openQ('adsoyad')">Ad Soyad</button><br><br>
    <button class="btn" onclick="openQ('tcgsm')">TC → GSM</button><br><br>
    <button class="btn" onclick="openQ('adres')">Adres</button><br><br>
    <button class="btn" onclick="openQ('aile')">Aile</button><br><br>
    <button class="btn" onclick="openQ('baba')">Baba</button><br><br>
    <button class="btn" onclick="openQ('anne')">Anne</button><br><br>
    <button class="btn" onclick="openQ('tcpro')">TC PRO</button><br><br>
    <button class="btn" onclick="logout()">Çıkış</button>
  </div>  <div id="content" style="margin-top:70px"></div>
</div><script>
  function login() {
    fetch('/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: pass.value })
    })
    .then(r => r.json())
    .then(j => { if (j.ok) loginDiv(); });
  }

  function loginDiv() {
    document.getElementById('login').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
  }

  function toggle() {
    drawer.classList.toggle('open');
  }

  function logout() {
    location.reload();
  }

  function openQ(name) {
    drawer.classList.remove('open');
    content.innerHTML = `
      <div class='card'>
        <h3>${name}</h3>
        <input id='v' />
        <br><br>
        <button class='btn' onclick='run("${name}")'>SORGULA</button>
        <pre id='out'></pre></div>`;

}

function run(name) { fetch('/api/' + name, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ gsm: v.value, tc: v.value, ad: v.value, soyad: v.value, q: v.value }) }) .then(r => r.json()) .then(j => out.textContent = JSON.stringify(j, null, 2)); } </script>

</body>
</html>`);
});app.listen(PORT, () => console.log('RUN', PORT));
