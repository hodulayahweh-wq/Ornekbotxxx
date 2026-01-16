const express = require('express');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3000;

// Geçici Kullanıcı Veritabanı
let lordUsers = [{ user: "lord2026panel", pass: "lord2026freepanel" }];

app.use(bodyParser.json());

// --- LORD API TEMİZLEYİCİ PROXY ---
app.post('/api/lord-proxy', async (req, res) => {
    const { url } = req.body;
    try {
        const response = await fetch(url);
        let data = await response.json();
        
        // Silinecek reklam ve meta veriler
        const sil = ["ApiSahibi", "apiDiscordSunucusu", "apiTelegramGrubu", "gunlukKalanLimit", "responseSureMs", "status", "message"];
        
        // JSON Temizleme İşlemi
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
        res.status(500).json({ hata: "Veri çekilemedi veya temizlenemedi!" });
    }
});

app.post('/api/lord-login', (req, res) => {
    const { user, pass } = req.body;
    const found = lordUsers.find(u => u.user === user && u.pass === pass);
    res.json({ success: !!found });
});

// --- LORD FULL FRONTEND (HACKER EDITION) ---
app.get('*', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lord System v3 | Hacker Panel</title>
    <style>
        :root { --p: #00ffcc; --bg: #000; }
        * { box-sizing: border-box; }
        body { margin:0; background:var(--bg); color:var(--p); font-family:'Courier New', monospace; overflow:hidden; }
        
        /* MATRIX ARKA PLAN */
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.4; }
        
        .hidden { display: none !important; }
        
        /* GİRİŞ KUTUSU */
        .box { max-width:400px; margin:100px auto; background:rgba(0,0,0,0.85); padding:30px; border:1px solid var(--p); border-radius:10px; box-shadow:0 0 25px var(--p); text-align:center; position:relative; z-index:10; }
        
        input { width:100%; padding:12px; margin:10px 0; background:#000; border:1px solid var(--p); color:var(--p); outline:none; text-align:center; font-size: 16px; }
        button { width:100%; padding:12px; background:var(--p); border:none; color:#000; font-weight:bold; cursor:pointer; margin-top:10px; box-shadow:0 0 10px var(--p); transition: 0.3s; }
        button:hover { transform: scale(1.02); background: #fff; }
        
        /* TELEGRAM BUTONU */
        .tg-link { margin-top:20px; text-decoration:none; display:inline-block; transition:0.3s; }
        .tg-icon { width: 50px; height: 50px; background: #222; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 1px solid var(--p); font-size: 24px; }
        .tg-link:hover .tg-icon { background: var(--p); color: #000; transform: rotate(360deg); }

        /* ANA PANEL */
        #main-panel { height: 100vh; overflow-y: auto; padding: 20px; }
        .nav { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--p); padding-bottom: 10px; margin-bottom: 20px; }
        
        .sidebar { position:fixed; left:0; top:0; height:100%; width:280px; background:rgba(0,0,0,0.95); border-right:1px solid var(--p); transform:translateX(-100%); transition:0.4s; z-index:100; padding:20px; }
        .sidebar.open { transform:translateX(0); }
        .menu-item { padding:15px; border-bottom: 1px solid #111; cursor:pointer; font-size:14px; transition: 0.2s; }
        .menu-item:hover { background:var(--p); color:#000; padding-left: 25px; }
        
        pre { background:rgba(0,0,0,0.9); color:var(--p); padding:15px; border:1px solid var(--p); border-radius: 5px; margin-top:20px; white-space:pre-wrap; text-align:left; font-size:12px; max-height: 400px; overflow-y: auto; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>

    <div id="auth-screen">
        <div class="box">
            <h1 style="font-size:22px; letter-spacing: 2px;">LORD SYSTEM LOGIN</h1>
            <input type="text" id="l-user" placeholder="Lord Kullanıcı Adı">
            <input type="password" id="l-pass" placeholder="Lord Şifresi">
            <button onclick="attemptLogin()">SİSTEME GİRİŞ YAP</button>
            
            <a href="https://t.me/lordsystemv3" target="_blank" class="tg-link">
                <div class="tg-icon">💬</div>
                <p style="font-size:11px; margin-top:8px; color: #fff;">@lordsystemv3</p>
            </a>
        </div>
    </div>

    <div id="main-panel" class="hidden">
        <div class="nav">
            <button onclick="toggleSide()" style="width:60px;">☰</button>
            <div style="font-weight:bold; letter-spacing: 1px;">LORD MULTI-CHECKER v3</div>
            <button onclick="location.reload()" style="width:90px; background:#ff0000; box-shadow: 0 0 10px #ff0000;">GÜVENLİ ÇIKIŞ</button>
        </div>

        <div class="sidebar" id="sidebar">
            <h2 style="border-bottom: 2px solid var(--p); padding-bottom: 10px; margin-bottom: 20px;">LORD COMMANDS</h2>
            <div class="menu-item" onclick="setupQuery('🆔 TC - GSM', 'TC Girin ve Numarayı Bulun...', 'https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc=')">TC - GSM Sorgu</div>
            <div class="menu-item" onclick="setupQuery('📞 GSM - TC', 'Numara Girin ve TC Bulun...', 'https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm=')">GSM - TC Sorgu</div>
            <div class="menu-item" onclick="setupQuery('👤 AD SOYAD', 'İsim Soyisim Girin...', 'https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad=')">Ad Soyad Sorgu</div>
            <div class="menu-item" onclick="setupQuery('👨‍👩‍👧 AİLE', 'TC Girin Aile Bilgisi Getirilsin...', 'https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc=')">Aile Sorgu</div>
            <div class="menu-item" onclick="setupQuery('🏠 ADRES', 'TC Girin Adres Getirilsin...', 'https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc=')">Adres Sorgu</div>
            <div class="menu-item" onclick="setupQuery('💎 LORD PRO', 'TC Girin Tüm Detayları Alın...', 'https://sorgum.2026tr.xyz/nabi/api/v1/tcpro?tc=')">Lord Pro Full</div>
        </div>

        <div class="box" style="max-width:700px; margin-top:20px;">
            <h2 id="query-title" style="margin-bottom: 15px; color: #fff;">Sorgu Seçimi Yapın</h2>
            <input type="text" id="query-input" placeholder="Lütfen yandaki menüden bir sorgu seçin...">
            <button onclick="executeLordQuery()">VERİLERİ ANALİZ ET VE ÇEK</button>
            <pre id="query-result">Sistem analiz için veri girişi bekliyor...</pre>
        </div>
    </div>

    <script>
        // MATRIX ARKA PLAN EFEKTİ
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const chars = "0123456789ABCDEFHIJKLMNOPRSTUVZ<>{}[]#@$";
        const fontSize = 16;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);
        
        function drawMatrix() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#0F0";
            ctx.font = fontSize + "px arial";
            drops.forEach((y, i) => {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, y * fontSize);
                if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(drawMatrix, 35);

        // HACKER SESİ (TTS)
        function playWelcomeVoice() {
            const msg = new SpeechSynthesisUtterance("Lord sorgu paneline hoşgeldiniz. Bütün sorgular güncel ve aktiftir. İyi sorgular.");
            msg.lang = 'tr-TR';
            msg.rate = 0.9;
            msg.pitch = 0.7;
            window.speechSynthesis.speak(msg);
        }

        // LOGIN İŞLEMİ
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
                playWelcomeVoice();
                document.getElementById('auth-screen').classList.add('hidden');
                document.getElementById('main-panel').classList.remove('hidden');
            } else { 
                alert("LORD ERİŞİMİ REDDEDİLDİ: HATALI KİMLİK!"); 
            }
        }

        // PANEL YÖNETİMİ
        let activeUrl = '';
        function toggleSide() { document.getElementById('sidebar').classList.toggle('open'); }
        
        function setupQuery(name, hint, url) {
            activeUrl = url;
            document.getElementById('query-title').innerText = name;
            document.getElementById('query-input').placeholder = hint;
            document.getElementById('query-input').value = "";
            toggleSide();
        }

        async function executeLordQuery() {
            const val = document.getElementById('query-input').value;
            if(!activeUrl || !val) return alert("HATA: Eksik veri veya sorgu seçimi!");
            
            document.getElementById('query-result').innerText = "[INFO] LORD BYTES ANALYZING DATA... PLEASE WAIT.";
            
            try {
                const res = await fetch('/api/lord-proxy', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ url: activeUrl + val })
                });
                const resultData = await res.json();
                document.getElementById('query-result').innerText = JSON.stringify(resultData, null, 4);
            } catch (err) {
                document.getElementById('query-result').innerText = "HATA: Veri işlenirken bir sorun oluştu.";
            }
        }
    </script>
</body>
</html>
    `);
});

app.listen(PORT, () => console.log("Lord System v3 is online on port " + PORT));
