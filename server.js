const express = require('express');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3000;

let lordUsers = [{ user: "lord2026panel", pass: "lord2026freepanel" }];

app.use(bodyParser.json());

// --- REKLAM TEMİZLEYİCİ VE VERİ DÜZENLEYİCİ ---
app.post('/api/lord-proxy', async (req, res) => {
    const { url } = req.body;
    try {
        const response = await fetch(url, {
            headers: { 'User-Agent': 'Mozilla/5.0' },
            timeout: 15000 
        });
        let data = await response.json();

        // Yasaklı kelimeler (Reklamları siler)
        const yasaklılar = ["t.me", "http", "api", "auth", "message", "status", "sahibi", "reklam"];

        function temizle(obj) {
            if (Array.isArray(obj)) return obj.map(temizle);
            if (obj !== null && typeof obj === 'object') {
                let yeniObj = {};
                for (let anahtar in obj) {
                    // Anahtar veya değer yasaklı kelime içermiyorsa ekle
                    const deger = String(obj[anahtar]).toLowerCase();
                    const anahtarAlt = anahtar.toLowerCase();
                    
                    if (!yasaklılar.some(y => deger.includes(y) || anahtarAlt.includes(y))) {
                        yeniObj[anahtar] = obj[anahtar];
                    }
                }
                return yeniObj;
            }
            return obj;
        }

        // Ana veriyi bul ve temizle
        let anaVeri = data.data || data.result || data.results || data;
        res.json(temizle(anaVeri));
    } catch (e) {
        res.status(500).json({ hata: "Veri alınamadı veya API kapalı." });
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
    <title>Lord Özel Panel</title>
    <style>
        :root { --p: #00ffcc; --bg: #000; }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { margin:0; background:var(--bg); color:var(--p); font-family: sans-serif; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.3; }
        .box { width: 92%; max-width: 400px; margin: 40px auto; background: rgba(0,0,0,0.9); padding: 25px; border: 1px solid var(--p); border-radius: 15px; text-align: center; box-shadow: 0 0 15px var(--p); position: relative; }
        input { width: 100%; padding: 15px; margin: 10px 0; background: #000; border: 1px solid var(--p); color: #fff; border-radius: 8px; font-size: 16px; outline: none; }
        button { width: 100%; padding: 15px; background: var(--p); border: none; color: #000; font-weight: bold; border-radius: 8px; cursor: pointer; font-size: 16px; }
        
        #main-panel { display: none; padding-top: 70px; }
        .header { position: fixed; top: 0; width: 100%; height: 60px; background: #000; border-bottom: 1px solid var(--p); display: flex; align-items: center; justify-content: space-between; padding: 0 15px; z-index: 1000; }
        .sidebar { position: fixed; left: -100%; top: 0; width: 85%; height: 100%; background: #0a0a0a; border-right: 2px solid var(--p); transition: 0.3s; z-index: 2000; padding: 20px; }
        .sidebar.active { left: 0; }
        .overlay { position: fixed; display: none; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index: 1500; }
        .overlay.active { display: block; }
        
        .menu-item { padding: 15px; border-bottom: 1px solid #111; color: var(--p); font-size: 14px; cursor: pointer; }
        .menu-item:active { background: var(--p); color: #000; }
        
        .result-container { width: 95%; margin: 15px auto; }
        pre { background: #050505; border: 1px solid var(--p); padding: 15px; color: #fff; font-size: 13px; text-align: left; white-space: pre-wrap; line-height: 1.6; border-radius: 10px; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <audio id="bgMusic" loop preload="auto"><source src="https://files.catbox.moe/5f6a9e.mp3" type="audio/mpeg"></audio>

    <div id="auth-screen">
        <div class="box">
            <h2 style="color:var(--p)">LORD V6</h2>
            <input type="text" id="user" placeholder="Kullanıcı">
            <input type="password" id="pass" placeholder="Şifre">
            <button onclick="login()">GİRİŞ</button>
            <button onclick="fastLogin()" style="background:#111; color:var(--p); margin-top:10px; border:1px solid var(--p)">⚡ HEMENGİR</button>
        </div>
    </div>

    <div id="main-panel">
        <div class="header">
            <button onclick="menu()" style="background:none; border:none; color:var(--p); font-size:25px;">☰</button>
            <span>LORD SİSTEM</span>
            <button onclick="location.reload()" style="background:none; border:none; color:red;">❌</button>
        </div>
        <div class="overlay" id="overlay" onclick="menu()"></div>
        <div class="sidebar" id="sidebar">
            <h3 style="text-align:center">SORGULAR</h3>
            <div class="menu-item" onclick="set('🆔 OLD TC-GSM', 'TC...', 'https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc=')">Old TC -> GSM</div>
            <div class="menu-item" onclick="set('📞 OLD GSM-TC', 'Numara...', 'https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm=')">Old GSM -> TC</div>
            <div class="menu-item" onclick="set('👤 AD SOYAD', 'İsim Soyisim...', 'https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad=')">Ad Soyad Sorgu</div>
            <div class="menu-item" onclick="set('📞 YENİ GSM-TC', 'Numara...', 'https://gamebzhhshs.onrender.com/api/v1/search/gsm_tc_2015?gsm=')">Yeni GSM-TC (2015)</div>
            <div class="menu-item" onclick="set('💊 REÇETE GEÇMİŞİ', 'TC...', 'https://nabisorguapis.onrender.com/api/v1/eczane/recete-gecmisi?tc=')">Reçete Geçmişi</div>
            <div class="menu-item" onclick="set('🏠 ADRES PRO', 'TC...', 'https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc=')">Adres Sorgu PRO</div>
        </div>

        <div class="box" style="width:95%; margin-top:10px;">
            <h4 id="st">İşlem Seçin</h4>
            <input type="text" id="qi" placeholder="Veri girin...">
            <button onclick="run()">SORGULA</button>
            <div class="result-container"><pre id="res">Sonuçlar burada...</pre></div>
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
            const res = await fetch('/api/lord-login', { 
                method: 'POST', 
                headers: {'Content-Type': 'application/json'}, 
                body: JSON.stringify({user: document.getElementById('user').value, pass: document.getElementById('pass').value}) 
            });
            if((await res.json()).success) {
                // ŞARKI BURADA BAŞLIYOR
                const music = document.getElementById('bgMusic');
                music.play().catch(() => console.log("Müzik izni bekliyor"));
                
                const s = new SpeechSynthesisUtterance("Lord sisteme hoşgeldin sevgilim.");
                s.lang='tr-TR'; window.speechSynthesis.speak(s);

                document.getElementById('auth-screen').style.display='none'; 
                document.getElementById('main-panel').style.display='block';
            } else { alert("Hata!"); }
        }

        let api = ''; function set(n,h,u) { api=u; document.getElementById('st').innerText=n; document.getElementById('qi').placeholder=h; menu(); }
        
        async function run() {
            const v = document.getElementById('qi').value; if(!api || !v) return;
            document.getElementById('res').innerText = "VERİ ALINIYOR...";
            try {
                const res = await fetch('/api/lord-proxy', { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify({ url: api + v }) 
                });
                const data = await res.json();
                
                // Veriyi düzgün formatta alt alta yazdır
                let çıktı = "";
                if(Array.isArray(data)) {
                    data.forEach(item => {
                        for(let k in item) çıktı += "• " + k + ": " + item[k] + "\\n";
                        çıktı += "------------------\\n";
                    });
                } else {
                    for(let k in data) çıktı += "• " + k + ": " + data[k] + "\\n";
                }
                document.getElementById('res').innerText = çıktı || "Sonuç bulunamadı.";
            } catch(e) { document.getElementById('res').innerText = "HATA: API bağlantısı sağlanamadı."; }
        }
    </script>
</body>
</html>
    `);
});

app.listen(PORT, () => console.log("Lord Ready"));
