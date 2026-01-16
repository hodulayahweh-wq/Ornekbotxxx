const express = require('express');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3000;

// Senin belirlediğin giriş bilgileri
let lordUsers = [{ user: "lord2026panel", pass: "lord2026freepanel" }];

app.use(bodyParser.json());

// --- LORD API PROXY (ZyrDa Reklamlarını Temizler) ---
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
        res.status(500).json({ hata: "Sorgu sırasında bir hata oluştu!" });
    }
});

app.post('/api/lord-login', (req, res) => {
    const { user, pass } = req.body;
    const found = lordUsers.find(u => u.user === user && u.pass === pass);
    res.json({ success: !!found });
});

// --- FRONTEND (MOBİL TASARIM) ---
app.get('*', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Lord Mobile PRO v3</title>
    <style>
        :root { --p: #00ffcc; --bg: #000; }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { margin:0; background:var(--bg); color:var(--p); font-family: 'Courier New', monospace; overflow-x:hidden; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.3; }
        
        /* GİRİŞ EKRANI */
        .box { width: 92%; max-width: 400px; margin: 50px auto; background: rgba(0,0,0,0.9); padding: 30px; border: 1px solid var(--p); border-radius: 15px; text-align: center; box-shadow: 0 0 20px var(--p); position: relative; z-index: 10; }
        input { width: 100%; padding: 15px; margin: 10px 0; background: #000; border: 1px solid var(--p); color: #fff; border-radius: 8px; font-size: 16px; outline: none; text-align: center; }
        button { width: 100%; padding: 15px; background: var(--p); border: none; color: #000; font-weight: bold; border-radius: 8px; cursor: pointer; font-size: 16px; margin-top: 10px; }
        .fast-btn { background: #111; color: var(--p); border: 1px solid var(--p); font-size: 12px; margin-top: 15px; }

        /* ANA PANEL */
        #main-panel { display: none; padding-top: 70px; }
        .header { position: fixed; top: 0; width: 100%; height: 65px; background: #000; border-bottom: 1px solid var(--p); display: flex; align-items: center; justify-content: space-between; padding: 0 15px; z-index: 1000; }
        
        /* MOBİL MENÜ (SIDEBAR) */
        .sidebar { position: fixed; left: -100%; top: 0; width: 85%; height: 100%; background: #0a0a0a; border-right: 2px solid var(--p); transition: 0.4s; z-index: 2000; padding: 20px; overflow-y: auto; }
        .sidebar.active { left: 0; }
        .overlay { position: fixed; display: none; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index: 1500; }
        .overlay.active { display: block; }

        .menu-title { color: #fff; border-bottom: 1px solid #333; padding: 15px 0; margin-top: 20px; font-weight: bold; font-size: 14px; }
        .menu-item { padding: 15px; border-bottom: 1px solid #111; color: var(--p); font-size: 14px; cursor: pointer; }
        .menu-item:active { background: var(--p); color: #000; }
        .pro-tag { background: red; color: white; font-size: 10px; padding: 2px 5px; border-radius: 4px; float: right; font-weight: bold; }

        /* SORGU ALANI */
        .query-container { width: 95%; margin: 20px auto; background: rgba(0,0,0,0.9); border: 1px solid var(--p); border-radius: 12px; padding: 20px; text-align: center; }
        pre { background: #050505; border: 1px solid #222; padding: 15px; color: var(--p); font-size: 12px; text-align: left; white-space: pre-wrap; word-wrap: break-word; max-height: 400px; overflow-y: auto; margin-top: 20px; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    
    <audio id="bgMusic" loop preload="auto">
        <source src="https://files.catbox.moe/5f6a9e.mp3" type="audio/mpeg">
    </audio>

    <div id="auth-screen">
        <div class="box">
            <h2 style="letter-spacing:3px;">LORD V3 PRO</h2>
            <input type="text" id="user" placeholder="Kullanıcı Adı">
            <input type="password" id="pass" placeholder="Şifre">
            <button onclick="login()">SİSTEME GİRİŞ YAP</button>
            <button class="fast-btn" onclick="fastLogin()">⚡ HEMENGİR (OTOMATİK)</button>
            <p style="font-size: 11px; margin-top: 20px; color: #444;">LORD SYSTEM © 2026</p>
        </div>
    </div>

    <div id="main-panel">
        <div class="header">
            <button onclick="toggleMenu()" style="background:none; border:none; color:var(--p); font-size:30px;">☰</button>
            <span style="font-weight:bold; letter-spacing:1px;">LORD CHECKER</span>
            <button onclick="location.reload()" style="background:none; border:none; color:red; font-size:22px;">✕</button>
        </div>

        <div class="overlay" id="overlay" onclick="toggleMenu()"></div>
        
        <div class="sidebar" id="sidebar">
            <h2 style="text-align: center; color: #fff; border-bottom: 2px solid var(--p); padding-bottom: 10px;">SORGU MENÜSÜ</h2>
            
            <div class="menu-title">💎 PRO SORGULAR</div>
            <div class="menu-item" onclick="selectQuery('🏠 ADRES PRO', 'TC Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc=')">Adres Sorgu <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="selectQuery('👤 AD SOYAD PRO', 'Ad Soyad Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/adsoyad?ad=')">Ad Soyad <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="selectQuery('👨‍👩‍👧 AİLE PRO', 'TC Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc=')">Aile Sorgu <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="selectQuery('📞 GSM PRO', 'GSM No Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/gsm?q=')">GSM Sorgu <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="selectQuery('👴 BABA PRO', 'TC Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/baba?tc=')">Baba Bilgi <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="selectQuery('👵 ANNE PRO', 'TC Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/anne?tc=')">Anne Bilgi <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="selectQuery('💎 TC FULL PRO', 'TC Giriniz...', 'https://sorgum.2026tr.xyz/nabi/api/v1/tcpro?tc=')">TC PRO Full <span class="pro-tag">PRO</span></div>
            
            <div class="menu-title">📜 ESKİ SORGULAR</div>
            <div class="menu-item" onclick="selectQuery('🆔 TC - GSM', 'TC Giriniz...', 'https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc=')">TC'den GSM</div>
            <div class="menu-item" onclick="selectQuery('📞 GSM - TC', 'GSM Giriniz...', 'https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm=')">GSM'den TC</div>
            <div class="menu-item" onclick="selectQuery('👤 AD SOYAD (OLD)', 'İsim...', 'https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad=')">Ad Soyad (Old)</div>
        </div>

        <div class="query-container">
            <h3 id="current-title" style="font-size: 16px;">Bir Sorgu Seçin</h3>
            <input type="text" id="query-input" placeholder="Lütfen menüden bir işlem seçin...">
            <button onclick="startQuery()">ANALİZİ BAŞLAT</button>
            <pre id="result-box">Sonuçlar burada görünecek...</pre>
        </div>
    </div>

    <script>
        // Matrix Arkaplan
        const canvas = document.getElementById('matrix'); const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const chars = "01"; const fontSize = 15; const columns = canvas.width / fontSize; const drops = Array(Math.floor(columns)).fill(1);
        function draw() {
            ctx.fillStyle = "rgba(0,0,0,0.05)"; ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle = "#0F0"; ctx.font = fontSize + "px arial";
            drops.forEach((y, i) => {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, y * fontSize);
                if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 40);

        // Menü Kontrolü
        function toggleMenu() {
            document.getElementById('sidebar').classList.toggle('active');
            document.getElementById('overlay').classList.toggle('active');
        }

        // Hızlı Giriş
        function fastLogin() {
            document.getElementById('user').value = "lord2026panel";
            document.getElementById('pass').value = "lord2026freepanel";
            login();
        }

        // Giriş ve Müzik Başlatma
        async function login() {
            const u = document.getElementById('user').value;
            const p = document.getElementById('pass').value;
            const res = await fetch('/api/lord-login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user:u, pass:p})
            });
            const data = await res.json();
            
            if(data.success) {
                // Müzik Başlat (Kullanıcı etkileşimi olduğu için çalacaktır)
                const music = document.getElementById('bgMusic');
                music.play().catch(e => console.log("Müzik engellendi."));
                
                // Bot Karşılama
                const speech = new SpeechSynthesisUtterance("Lord mobil sisteme hoşgeldiniz sevgilim. İyi sorgular.");
                speech.lang = 'tr-TR';
                window.speechSynthesis.speak(speech);

                document.getElementById('auth-screen').style.display = 'none';
                document.getElementById('main-panel').style.display = 'block';
            } else {
                alert("Hatalı Giriş!");
            }
        }

        let currentApiUrl = '';
        function selectQuery(name, hint, url) {
            currentApiUrl = url;
            document.getElementById('current-title').innerText = name;
            document.getElementById('query-input').placeholder = hint;
            document.getElementById('query-input').value = "";
            toggleMenu();
        }

        async function startQuery() {
            const val = document.getElementById('query-input').value;
            if(!currentApiUrl || !val) return alert("Sorgu seçin ve veri girin!");
            
            document.getElementById('result-box').innerText = ">>> LORD ANALİZ EDİYOR...";
            
            const res = await fetch('/api/lord-proxy', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ url: currentApiUrl + val })
            });
            const finalData = await res.json();
            document.getElementById('result-box').innerText = JSON.stringify(finalData, null, 2);
        }
    </script>
</body>
</html>
    `);
});

app.listen(PORT, () => console.log("Lord Mobile Unified Active"));
