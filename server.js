const express = require('express');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3000;

let lordUsers = [{ user: "lord2026panel", pass: "lord2026freepanel" }];

app.use(bodyParser.json());

// --- GÜÇLENDİRİLMİŞ PROXY MOTORU ---
app.post('/api/lord-proxy', async (req, res) => {
    const { url } = req.body;
    try {
        const response = await fetch(url, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                'Accept': 'application/json'
            },
            timeout: 15000 
        });

        let data = await response.json();

        // Reklam ve gereksizleri temizle
        const bypass = ["ApiSahibi", "apiDiscordSunucusu", "apiTelegramGrubu", "gunlukKalanLimit", "responseSureMs", "status", "message"];
        
        // Veriyi ayıkla
        let core = data.data || data.result || data.results || data;

        if (Array.isArray(core)) {
            core = core.map(item => {
                bypass.forEach(k => delete item[k]);
                return item;
            });
            // GSM-TC 2015 için sadece eşleşen (boş olmayan) verileri filtrele
            if(url.includes("gsm_tc_2015")) {
                core = core.filter(i => (i.GSM || i.gsm) && (i.TC || i.tc));
            }
        }

        res.json(core);
    } catch (e) {
        res.status(500).json({ hata: "SİSTEM ZORLAMASI BAŞARISIZ", detay: e.message });
    }
});

app.post('/api/lord-login', (req, res) => {
    const { user, pass } = req.body;
    const found = lordUsers.find(u => u.user === user && u.pass === pass);
    res.json({ success: !!found });
});

app.get('*', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Lord PRO Ultimate v5</title>
    <style>
        :root { --p: #00ffcc; --bg: #000; }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { margin:0; background:var(--bg); color:var(--p); font-family: 'Courier New', monospace; overflow-x:hidden; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.3; }
        .box { width: 92%; max-width: 450px; margin: 40px auto; background: rgba(0,0,0,0.9); padding: 25px; border: 1px solid var(--p); border-radius: 15px; text-align: center; box-shadow: 0 0 20px var(--p); position: relative; z-index: 10; }
        input { width: 100%; padding: 15px; margin: 10px 0; background: #000; border: 1px solid var(--p); color: #fff; border-radius: 8px; font-size: 16px; outline: none; text-align: center; }
        button { width: 100%; padding: 15px; background: var(--p); border: none; color: #000; font-weight: bold; border-radius: 8px; cursor: pointer; font-size: 16px; transition: 0.3s; }
        button:active { transform: scale(0.95); background: #fff; }
        .fast-btn { background: #111; color: var(--p); border: 1px solid var(--p); margin-top: 15px; font-size: 12px; }
        #main-panel { display: none; padding-top: 70px; }
        .header { position: fixed; top: 0; width: 100%; height: 60px; background: #000; border-bottom: 1px solid var(--p); display: flex; align-items: center; justify-content: space-between; padding: 0 15px; z-index: 1000; }
        .sidebar { position: fixed; left: -100%; top: 0; width: 85%; height: 100%; background: #0a0a0a; border-right: 2px solid var(--p); transition: 0.4s; z-index: 2000; padding: 20px; overflow-y: auto; }
        .sidebar.active { left: 0; }
        .overlay { position: fixed; display: none; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index: 1500; }
        .overlay.active { display: block; }
        .menu-title { color: #fff; border-bottom: 1px solid #333; padding: 10px 0; margin-top: 15px; font-size: 12px; }
        .menu-item { padding: 15px; border-bottom: 1px solid #111; color: var(--p); font-size: 14px; cursor: pointer; }
        .pro-tag { background: red; color: white; font-size: 10px; padding: 2px 4px; border-radius: 3px; float: right; }
        pre { background: #050505; border: 1px solid var(--p); padding: 15px; color: var(--p); font-size: 11px; text-align: left; white-space: pre-wrap; word-wrap: break-word; max-height: 350px; overflow-y: auto; margin-top: 15px; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <audio id="bgMusic" loop preload="auto"><source src="https://files.catbox.moe/5f6a9e.mp3" type="audio/mpeg"></audio>

    <div id="auth-screen">
        <div class="box">
            <h1 style="font-size:24px;">LORD PRO V5</h1>
            <input type="text" id="user" placeholder="Kullanıcı">
            <input type="password" id="pass" placeholder="Şifre">
            <button onclick="login()">SİSTEMİ AÇ</button>
            <button class="fast-btn" onclick="fastLogin()">⚡ HEMENGİR (MÜZİKLİ)</button>
        </div>
    </div>

    <div id="main-panel">
        <div class="header">
            <button onclick="menu()" style="background:none; border:none; color:var(--p); font-size:28px;">☰</button>
            <span style="font-weight:bold;">LORD FORCE PANEL</span>
            <button onclick="location.reload()" style="background:none; border:none; color:red;">❌</button>
        </div>
        <div class="overlay" id="overlay" onclick="menu()"></div>
        <div class="sidebar" id="sidebar">
            <div class="menu-title">💎 ÖZEL SORGULAR (FORCE)</div>
            <div class="menu-item" onclick="set('📞 GSM-TC 2015', 'Numara...', 'https://gamebzhhshs.onrender.com/api/v1/search/gsm_tc_2015?gsm=')">GSM-TC 2015 <span class="pro-tag">YENİ</span></div>
            
            <div class="menu-title">💎 PRO APİLER</div>
            <div class="menu-item" onclick="set('🏠 ADRES PRO', 'TC...', 'https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc=')">Adres Sorgu <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="set('👤 AD SOYAD PRO', 'İsim...', 'https://sorgum.2026tr.xyz/nabi/api/v1/adsoyad?ad=')">Ad Soyad <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="set('👨‍👩‍👧 AİLE PRO', 'TC...', 'https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc=')">Aile Sorgu <span class="pro-tag">PRO</span></div>
            <div class="menu-item" onclick="set('💎 TC FULL PRO', 'TC...', 'https://sorgum.2026tr.xyz/nabi/api/v1/tcpro?tc=')">TC PRO Full <span class="pro-tag">PRO</span></div>

            <div class="menu-title">📜 ESKİ SORGULAR</div>
            <div class="menu-item" onclick="set('🆔 TC-GSM (OLD)', 'TC...', 'https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc=')">Eski TC-GSM</div>
        </div>

        <div class="box" style="width:96%; margin-top:10px;">
            <h4 id="st">Sorgu Seçin</h4>
            <input type="text" id="qi" placeholder="Veri giriniz...">
            <button onclick="run()">SORGULAMAYI BAŞLAT</button>
            <pre id="res">Sonuçlar analiz edilecek...</pre>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('matrix'); const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        function draw() { ctx.fillStyle = "rgba(0,0,0,0.05)"; ctx.fillRect(0,0,canvas.width,canvas.height); ctx.fillStyle = "#0F0"; ctx.font = "15px arial"; } setInterval(draw, 50);

        function menu() { document.getElementById('sidebar').classList.toggle('active'); document.getElementById('overlay').classList.toggle('active'); }
        
        function fastLogin() {
            document.getElementById('user').value = "lord2026panel";
            document.getElementById('pass').value = "lord2026freepanel";
            login();
        }

        async function login() {
            const u = document.getElementById('user').value; const p = document.getElementById('pass').value;
            const res = await fetch('/api/lord-login', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({user:u, pass:p}) });
            if((await res.json()).success) {
                // MÜZİK BURADA TETİKLENİYOR
                const music = document.getElementById('bgMusic');
                music.play();
                
                const s = new SpeechSynthesisUtterance("Lord sisteme hoşgeldin sevgilim. Tüm hatlar zorlanıyor.");
                s.lang='tr-TR'; window.speechSynthesis.speak(s);

                document.getElementById('auth-screen').style.display='none'; 
                document.getElementById('main-panel').style.display='block';
            } else { alert("Hata!"); }
        }

        let api = ''; function set(n,h,u) { api=u; document.getElementById('st').innerText=n; document.getElementById('qi').placeholder=h; menu(); }
        
        async function run() {
            const v = document.getElementById('qi').value; if(!api || !v) return;
            document.getElementById('res').innerText = "VERİ SÖKÜLÜYOR...";
            try {
                const res = await fetch('/api/lord-proxy', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ url: api + v }) });
                const data = await res.json();
                document.getElementById('res').innerText = JSON.stringify(data, null, 2);
            } catch(e) { document.getElementById('res').innerText = "HATA: VERİ ALINAMADI."; }
        }
    </script>
</body>
</html>
    `);
});

app.listen(PORT, () => console.log("Lord PRO v5 Active"));
