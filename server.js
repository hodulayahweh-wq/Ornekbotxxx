const express = require('express');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3000;

// Giriş Bilgilerin
let lordUsers = [{ user: "lord2026panel", pass: "lord2026freepanel" }];

app.use(bodyParser.json());

// --- LORD API TEMİZLEYİCİ PROXY ---
app.post('/api/lord-proxy', async (req, res) => {
    const { url } = req.body;
    try {
        const response = await fetch(url);
        let data = await response.json();
        const sil = ["ApiSahibi", "apiDiscordSunucusu", "apiTelegramGrubu", "gunlukKalanLimit", "responseSureMs", "status", "message"];
        
        if (Array.isArray(data)) {
            data = data.map(item => { sil.forEach(k => delete item[k]); return item; });
        } else {
            let core = data.data || data.result || data;
            if (typeof core === 'object' && core !== null) {
                sil.forEach(k => delete core[k]);
                data = core;
            }
        }
        res.setHeader('Content-Type', 'application/json');
        res.send(JSON.stringify(data, null, 4));
    } catch (e) {
        res.status(500).json({ hata: "Veri analiz edilemedi!" });
    }
});

app.post('/api/lord-login', (req, res) => {
    const { user, pass } = req.body;
    const found = lordUsers.find(u => u.user === user && u.pass === pass);
    res.json({ success: !!found });
});

// --- FULL FRONTEND ---
app.get('*', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Lord System v3 | PRO & OLD Unified</title>
    <style>
        :root { --p: #00ffcc; --bg: #000; }
        body { margin:0; background:var(--bg); color:var(--p); font-family:'Courier New', monospace; overflow:hidden; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.4; }
        .hidden { display: none !important; }
        
        /* BOX TASARIMI */
        .box { max-width:400px; margin:60px auto; background:rgba(0,0,0,0.85); padding:30px; border:1px solid var(--p); border-radius:10px; box-shadow:0 0 25px var(--p); text-align:center; position:relative; z-index:10; }
        input { width:100%; padding:12px; margin:10px 0; background:#000; border:1px solid var(--p); color:var(--p); outline:none; text-align:center; font-size:15px; }
        button { width:100%; padding:12px; background:var(--p); border:none; color:#000; font-weight:bold; cursor:pointer; margin-top:10px; box-shadow:0 0 10px var(--p); transition: 0.3s; }
        button:hover { background: #fff; }
        .fast-btn { background: #111; color: var(--p); border: 1px solid var(--p); margin-top: 15px; font-size: 11px; }

        /* PANEL TASARIMI */
        #main-panel { height: 100vh; overflow-y: auto; padding: 20px; }
        .nav { display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--p); padding-bottom:10px; }
        
        .sidebar { position:fixed; left:0; top:0; height:100%; width:280px; background:rgba(0,0,0,0.95); border-right:1px solid var(--p); transform:translateX(-100%); transition:0.4s; z-index:100; padding:20px; overflow-y:auto; }
        .sidebar.open { transform:translateX(0); }
        
        .menu-title { color: #fff; border-bottom: 1px solid var(--p); padding: 10px 0; margin-top: 20px; font-size: 14px; letter-spacing: 1px; }
        .menu-item { padding:12px; border-bottom: 1px solid #111; cursor:pointer; font-size:13px; transition:0.2s; }
        .menu-item:hover { background:var(--p); color:#000; padding-left:20px; }
        
        .pro-tag { background: red; color: white; font-size: 9px; padding: 2px 4px; border-radius: 3px; margin-left: 5px; }
        .old-tag { background: #444; color: #fff; font-size: 9px; padding: 2px 4px; border-radius: 3px; margin-left: 5px; }
        
        pre { background:rgba(0,0,0,0.9); color:var(--p); padding:15px; border:1px solid var(--p); margin-top:20px; white-space:pre-wrap; text-align:left; font-size:12px; max-height:400px; overflow-y:auto; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    
    <audio id="bgMusic" loop>
        <source src="https://www.mboxdrive.com/Oriental%20Poison.mp3" type="audio/mpeg">
    </audio>

    <div id="auth-screen">
        <div class="box">
            <h1 style="font-size:22px;">LORD UNIFIED LOGIN</h1>
            <input type="text" id="l-user" placeholder="Kullanıcı Adı">
            <input type="password" id="l-pass" placeholder="Şifre">
            <button onclick="attemptLogin()">SİSTEME GİRİŞ YAP</button>
            <button class="fast-btn" onclick="fastLogin()">⚡ HEMENGİR (OTOMATİK)</button>
            <a href="https://t.me/lordsystemv3" target="_blank" style="display:block; margin-top:20px; color:var(--p); text-decoration:none; font-size:12px;">💬 @lordsystemv3</a>
        </div>
    </div>

    <div id="main-panel" class="hidden">
        <div class="nav">
            <button onclick="toggleSide()" style="width:50px;">☰</button>
            <div style="font-weight:bold; letter-spacing:1px;">LORD MULTI-PANEL V3</div>
            <button onclick="location.reload()" style="width:80px; background:red;">ÇIKIŞ</button>
        </div>

        <div class="sidebar" id="sidebar">
            <div class="menu-title">💎 YENİ PRO SORGULAR</div>
            <div class="menu-item" onclick="setupQuery('🏠 ADRES PRO', 'TC Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc=')">Adres Sorgu <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="setupQuery('👤 AD SOYAD PRO', 'İsim Soyisim Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/adsoyad?ad=')">Ad Soyad Sorgu <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="setupQuery('👨‍👩‍👧 AİLE PRO', 'TC Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc=')">Aile Sorgu <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="setupQuery('📞 GSM PRO', 'GSM Numarası Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/gsm?q=')">GSM Sorgu <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="setupQuery('👴 BABA BİLGİ PRO', 'TC Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/baba?tc=')">Baba Bilgisi <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="setupQuery('👵 ANNE BİLGİ PRO', 'TC Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/anne?tc=')">Anne Bilgisi <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="setupQuery('💎 TC FULL PRO', 'TC Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/tcpro?tc=')">TC PRO (Full) <span class="pro-tag">PRO</span></div>

            <div class="menu-title">📜 ESKİ SORGULAR</div>
            <div class="menu-item" onclick="setupQuery('🆔 TC - GSM (ESKİ)', 'TC Giriniz...', 'https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc=')">TC'den GSM <span class="old-tag">ESKİ</span></div>
            <div class="menu-item" onclick="setupQuery('📞 GSM - TC (ESKİ)', 'Numara Giriniz...', 'https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm=')">GSM'den TC <span class="old-tag">ESKİ</span></div>
            <div class="menu-item" onclick="setupQuery('👤 AD SOYAD (ESKİ)', 'Ad Soyad Giriniz...', 'https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad=')">Ad Soyad <span class="old-tag">ESKİ</span></div>
        </div>

        <div class="box" style="max-width:700px; margin-top:30px;">
            <h2 id="query-title" style="font-size:18px;">Lütfen Bir Sorgu Seçin</h2>
            <input type="text" id="query-input" placeholder="Seçtiğiniz API'ye göre veri girin...">
            <button onclick="executeLordQuery()">ANALİZİ BAŞLAT</button>
            <pre id="query-result">Sistem sorgu emri bekliyor...</pre>
        </div>
    </div>

    <script>
        // MATRIX EFEKTİ
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const chars = "0123456789"; const fontSize = 16;
        const columns = canvas.width / fontSize; const drops = Array(Math.floor(columns)).fill(1);
        function draw() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.05)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#0F0"; ctx.font = fontSize + "px arial";
            drops.forEach((y, i) => {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, y * fontSize);
                if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 35);

        // SES VE MÜZİK
        function playEffects() {
            const msg = new SpeechSynthesisUtterance("Lord sorgu paneline hoşgeldiniz. Bütün sorgular güncel ve aktiftir. İyi sorgular.");
            msg.lang = 'tr-TR'; msg.rate = 0.85;
            window.speechSynthesis.speak(msg);
            
            const music = document.getElementById('bgMusic');
            music.volume = 0.4;
            music.play().catch(e => console.log("Müzik tetiklenemedi."));
        }

        // GİRİŞ FONKSİYONLARI
        function fastLogin() {
            document.getElementById('l-user').value = "lord2026panel";
            document.getElementById('l-pass').value = "lord2026freepanel";
            attemptLogin();
        }

        async function attemptLogin() {
            const user = document.getElementById('l-user').value;
            const pass = document.getElementById('l-pass').value;
            const res = await fetch('/api/lord-login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user, pass})
            });
            const data = await res.json();
            if(data.success) {
                playEffects();
                document.getElementById('auth-screen').classList.add('hidden');
                document.getElementById('main-panel').classList.remove('hidden');
            } else { alert("Erişim Reddedildi!"); }
        }

        // PANEL YÖNETİMİ
        let activeUrl = '';
        function toggleSide() { document.getElementById('sidebar').classList.toggle('open'); }
        
        function setupQuery(name, hint, url) {
            activeUrl = url;
            document.getElementById('query-title').innerText = name;
            document.getElementById('query-input').placeholder = hint;
            document.getElementById('query-input').value = "";
            toggleSide(); // Menüyü kapat
        }

        async function executeLordQuery() {
            const val = document.getElementById('query-input').value;
            if(!activeUrl || !val) return alert("Sorgu türü seçin ve veri girin!");
            
            document.getElementById('query-result').innerText = ">>> LORD ANALYZING BYTES...";
            
            try {
                const res = await fetch('/api/lord-proxy', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: activeUrl + val })
                });
                const result = await res.json();
                document.getElementById('query-result').innerText = JSON.stringify(result, null, 4);
            } catch (err) {
                document.getElementById('query-result').innerText = "Hata: Veri çekilemedi.";
            }
        }
    </script>
</body>
</html>
    `);
});

app.listen(PORT, () => console.log("Lord Unified Panel Online"));
