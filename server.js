const express = require('express');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());

// Giriş Bilgileri
const lordUsers = [{ user: "lord2026panel", pass: "lord2026freepanel" }];

// --- GÜÇLENDİRİLMİŞ BACKEND PROXY (Zorla Veri Çekme ve Temizleme) ---
app.post('/api/fetch-lord', async (req, res) => {
    const { targetUrl } = req.body;
    
    try {
        const response = await fetch(targetUrl, {
            method: 'GET',
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
                'Accept': 'application/json'
            },
            timeout: 15000
        });

        const rawData = await response.json();

        // Yasaklı Reklam Kelimeleri Listesi
        const forbidden = ["t.me", "http", "api", "auth", "sahibi", "reklam", "message", "status", "success", "developer"];

        // Derinlemesine Temizlik Fonksiyonu
        const clean = (obj) => {
            if (Array.isArray(obj)) return obj.map(clean);
            if (obj !== null && typeof obj === 'object') {
                let filtered = {};
                for (let key in obj) {
                    const val = String(obj[key]).toLowerCase();
                    const keyLower = key.toLowerCase();
                    // Reklam içermeyenleri ayıkla
                    if (!forbidden.some(f => val.includes(f) || keyLower.includes(f))) {
                        filtered[key] = obj[key];
                    }
                }
                return filtered;
            }
            return obj;
        };

        // Veri katmanını bul ve temizle
        const core = rawData.data || rawData.result || rawData.results || rawData.list || rawData;
        const finalResults = clean(core);

        res.json(finalResults);
    } catch (e) {
        res.status(500).json({ error: "API Bağlantı Hatası!", detay: e.message });
    }
});

app.post('/api/lord-login', (req, res) => {
    const { user, pass } = req.body;
    const found = lordUsers.find(u => u.user === user && u.pass === pass);
    res.json({ success: !!found });
});

// --- MOBİL FRONTEND ---
app.get('*', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Lord PRO v6</title>
    <style>
        :root { --p: #00ffcc; --bg: #000; }
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { margin:0; background:var(--bg); color:var(--p); font-family: 'Courier New', monospace; overflow:hidden; }
        canvas { position: fixed; top: 0; left: 0; z-index: -1; opacity: 0.3; }
        
        .box { width: 92%; max-width: 400px; margin: 50px auto; background: rgba(0,0,0,0.9); padding: 30px; border: 1px solid var(--p); border-radius: 15px; text-align: center; box-shadow: 0 0 15px var(--p); position: relative; z-index: 10; }
        input { width: 100%; padding: 15px; margin: 10px 0; background: #000; border: 1px solid var(--p); color: #fff; border-radius: 8px; font-size: 16px; outline: none; }
        button { width: 100%; padding: 15px; background: var(--p); border: none; color: #000; font-weight: bold; border-radius: 8px; cursor: pointer; font-size: 16px; transition: 0.2s; }
        button:active { transform: scale(0.95); }

        #panel { display: none; padding-top: 70px; }
        .header { position: fixed; top: 0; width: 100%; height: 60px; background: #000; border-bottom: 1px solid var(--p); display: flex; align-items: center; justify-content: space-between; padding: 0 15px; z-index: 100; }
        
        .sidebar { position: fixed; left: -100%; top: 0; width: 85%; height: 100%; background: #080808; border-right: 2px solid var(--p); transition: 0.3s; z-index: 200; padding: 20px; overflow-y: auto; }
        .sidebar.active { left: 0; }
        .overlay { position: fixed; display: none; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index: 150; }
        .overlay.active { display: block; }
        
        .menu-item { padding: 15px; border-bottom: 1px solid #111; color: var(--p); font-size: 14px; cursor: pointer; }
        .menu-item:active { background: var(--p); color: #000; }
        
        #res-box { background: #050505; border: 1px solid var(--p); padding: 15px; margin-top: 20px; border-radius: 10px; max-height: 400px; overflow-y: auto; text-align: left; line-height: 1.8; color: #fff; font-size: 13px; }
        hr { border: 0; border-top: 1px solid #222; margin: 10px 0; }
    </style>
</head>
<body>
    <canvas id="matrix"></canvas>
    <audio id="bgMusic" loop preload="auto"><source src="https://files.catbox.moe/5f6a9e.mp3" type="audio/mpeg"></audio>

    <div id="login-screen">
        <div class="box">
            <h2 style="letter-spacing:2px;">LORD PRO V6</h2>
            <input type="text" id="user" placeholder="Kullanıcı">
            <input type="password" id="pass" placeholder="Şifre">
            <button onclick="login()">SİSTEME GİRİŞ</button>
            <button onclick="fast()" style="background:#111; color:var(--p); margin-top:15px; border:1px solid var(--p); font-size:12px;">⚡ HIZLI GİRİŞ (MÜZİKLİ)</button>
        </div>
    </div>

    <div id="panel">
        <div class="header">
            <button onclick="toggleMenu()" style="background:none; border:none; color:var(--p); font-size:25px;">☰</button>
            <span style="font-weight:bold;">LORD FORCE PANEL</span>
            <button onclick="location.reload()" style="background:none; border:none; color:red; font-size:20px;">✕</button>
        </div>
        <div class="overlay" id="overlay" onclick="toggleMenu()"></div>
        <div class="sidebar" id="sidebar">
            <h3 style="text-align:center; border-bottom:1px solid var(--p); padding-bottom:10px;">SORGULAR</h3>
            <div class="menu-item" onclick="set('🆔 OLD TC-GSM', 'https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc=')">Old TC-GSM</div>
            <div class="menu-item" onclick="set('📞 OLD GSM-TC', 'https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm=')">Old GSM-TC</div>
            <div class="menu-item" onclick="set('👤 AD SOYAD', 'https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad=')">Ad Soyad Sorgu</div>
            <div class="menu-item" onclick="set('📞 YENİ GSM-TC 2015', 'https://gamebzhhshs.onrender.com/api/v1/search/gsm_tc_2015?gsm=')">Yeni GSM-TC (2015)</div>
            <div class="menu-item" onclick="set('💊 REÇETE GEÇMİŞİ', 'https://nabisorguapis.onrender.com/api/v1/eczane/recete-gecmisi?tc=')">Reçete Geçmişi</div>
            <div class="menu-item" onclick="set('🏠 ADRES PRO', 'https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc=')">Adres PRO</div>
        </div>

        <div class="box" style="width:95%; margin-top:10px;">
            <h4 id="st-title">Bir Sorgu Seçin</h4>
            <input type="text" id="qi" placeholder="Veri girin...">
            <button onclick="run()">SORGULA</button>
            <div id="res-box">Sonuçlar burada alt alta listelenecek...</div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('matrix'); const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        function draw() { ctx.fillStyle = "rgba(0,0,0,0.05)"; ctx.fillRect(0,0,canvas.width,canvas.height); ctx.fillStyle = "#0F0"; ctx.font = "15px arial"; drops.forEach((y, i) => { ctx.fillText("01"[Math.floor(Math.random()*2)], i*15, y*15); if(y*15 > canvas.height && Math.random()>0.975) drops[i]=0; drops[i]++; }); }
        const drops = Array(Math.floor(canvas.width/15)).fill(1); setInterval(draw, 50);

        function toggleMenu() { document.getElementById('sidebar').classList.toggle('active'); document.getElementById('overlay').classList.toggle('active'); }
        function fast() { document.getElementById('user').value="lord2026panel"; document.getElementById('pass').value="lord2026freepanel"; login(); }

        async function login() {
            const res = await fetch('/api/lord-login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user: document.getElementById('user').value, pass: document.getElementById('pass').value})
            });
            const d = await res.json();
            if(d.success) {
                // ŞARKIYI VE SESİ BAŞLAT
                const m = document.getElementById('bgMusic');
                m.play().catch(() => console.log("Müzik için dokunuş bekleniyor."));
                
                const s = new SpeechSynthesisUtterance("Sisteme hoşgeldin sevgilim.");
                s.lang='tr-TR'; window.speechSynthesis.speak(s);

                document.getElementById('login-screen').style.display='none';
                document.getElementById('panel').style.display='block';
            } else { alert("Bilgiler Hatalı!"); }
        }

        let targetApi = '';
        function set(name, url) { targetApi = url; document.getElementById('st-title').innerText = name; toggleMenu(); }

        async function run() {
            const val = document.getElementById('qi').value;
            if(!targetApi || !val) return alert("Sorgu seçin!");
            document.getElementById('res-box').innerText = "Backend veriyi zorluyor...";
            
            try {
                const res = await fetch('/api/fetch-lord', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ targetUrl: targetApi + val })
                });
                const data = await res.json();
                
                let html = "";
                if(Array.isArray(data)) {
                    data.forEach(item => {
                        for(let k in item) html += "<b>• " + k + ":</b> " + item[k] + "<br>";
                        html += "<hr>";
                    });
                } else {
                    for(let k in data) html += "<b>• " + k + ":</b> " + data[k] + "<br>";
                }
                document.getElementById('res-box').innerHTML = html || "Sonuç bulunamadı.";
            } catch(e) { document.getElementById('res-box').innerText = "Hata: Backend API'ye ulaşamadı."; }
        }
    </script>
</body>
</html>
    `);
});

app.listen(PORT, () => console.log("Lord PRO v6 Online"));
