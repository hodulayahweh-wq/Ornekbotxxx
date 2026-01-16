const express = require('express');
const bodyParser = require('body-parser');
const fetch = require('node-fetch');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Geçici Veritabanı (Admin sabit, diğerleri kayıt oldukça eklenir)
let users = [{ user: "admin", pass: "admin123" }];

app.use(bodyParser.json());

// --- API PROXY (CORS HATASINI ÖNLER) ---
app.post('/api/proxy', async (req, res) => {
    const { url } = req.body;
    try {
        const response = await fetch(url);
        let text = await response.text();
        // Telegram linklerini ve reklamları temizle
        text = text.replace(/t\.me\/[\w\d]+/gi, '[Sistem]');
        res.send(text);
    } catch (error) {
        res.status(500).send("API Erişim Hatası!");
    }
});

// --- KAYIT VE GİRİŞ SİSTEMİ ---
app.post('/api/register', (req, res) => {
    const { user, pass } = req.body;
    if (users.find(u => u.user === user)) {
        return res.json({ success: false, msg: "Bu kullanıcı adı alınmış!" });
    }
    users.push({ user, pass });
    res.json({ success: true });
});

app.post('/api/login', (req, res) => {
    const { user, pass } = req.body;
    const found = users.find(u => u.user === user && u.pass === pass);
    if (found) {
        res.json({ success: true });
    } else {
        res.json({ success: false, msg: "Kullanıcı adı veya şifre hatalı!" });
    }
});

// --- TEK SAYFA FULL HTML ---
app.get('*', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GameDev Master - Create & Play</title>
    <style>
        :root { --neon: #00ffcc; --dark: #050505; --panel: #0a0015; }
        * { margin:0; padding:0; box-sizing:border-box; font-family: 'Segoe UI', sans-serif; }
        body { background: var(--dark); color: white; overflow-x: hidden; }

        /* KAMUFLAJ: OYUN SİTESİ */
        #game-site { padding: 40px 20px; text-align: center; }
        .hero { background: linear-gradient(135deg, #121212, #1a1a2e); padding: 50px; border-radius: 20px; border: 1px solid #333; margin-bottom: 30px; }
        .btn-start { padding: 15px 30px; background: var(--neon); color: black; border: none; font-weight: bold; border-radius: 5px; cursor: pointer; transition: 0.3s; }
        .btn-start:hover { box-shadow: 0 0 20px var(--neon); }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }
        .card { background: #111; padding: 20px; border-radius: 10px; border: 1px solid #222; }

        /* SİSTEM PANELLERİ */
        .hidden { display: none !important; }
        .container { max-width: 500px; margin: 80px auto; background: var(--panel); padding: 30px; border-radius: 15px; border: 1px solid var(--neon); box-shadow: 0 0 40px rgba(0,255,200,0.2); text-align: center; }
        
        input { width: 100%; padding: 12px; margin: 10px 0; background: #000; border: 1px solid #444; color: white; border-radius: 8px; outline: none; }
        input:focus { border-color: var(--neon); }
        .main-btn { width: 100%; padding: 12px; background: var(--neon); border: none; color: #000; font-weight: bold; cursor: pointer; border-radius: 8px; margin-top: 10px; }
        
        /* SIDEBAR & CHECKER */
        .sidebar { position: fixed; left: 0; top: 0; height: 100%; width: 260px; background: #000; border-right: 1px solid var(--neon); padding: 20px; transform: translateX(-100%); transition: 0.3s; z-index: 1000; overflow-y: auto; }
        .sidebar.open { transform: translateX(0); }
        .menu-item { padding: 12px; border-bottom: 1px solid #1a1a1a; cursor: pointer; font-size: 14px; transition: 0.2s; }
        .menu-item:hover { color: var(--neon); background: #0a0a0a; }
        
        pre { background: #000; color: var(--neon); padding: 15px; border-radius: 8px; overflow-x: auto; text-align: left; font-size: 13px; margin-top: 20px; border: 1px solid #222; min-height: 100px; white-space: pre-wrap; }
        .badge { background: var(--neon); color: black; padding: 2px 6px; border-radius: 4px; font-size: 10px; font-weight: bold; margin-left: 5px; }
        
        #nav-header { position: sticky; top: 0; background: rgba(0,0,0,0.9); padding: 10px; border-bottom: 1px solid #222; display: flex; justify-content: space-between; align-items: center; z-index: 900; }
    </style>
</head>
<body>

    <div id="game-site">
        <div class="hero">
            <h1 style="font-size: 2.5rem; margin-bottom: 15px;">GameDev Studio v5.0</h1>
            <p style="color: #aaa; margin-bottom: 25px;">Web tabanlı oyunlarınızı saniyeler içinde geliştirin ve yayınlayın.</p>
            <button class="btn-start" onclick="showLogin()">Projeye Başla</button>
        </div>
        <div class="grid">
            <div class="card"><h4>Asset Store</h4></div>
            <div class="card"><h4>Physics SDK</h4></div>
            <div class="card"><h4>API Docs</h4></div>
            <div class="card"><h4>Cloud Save</h4></div>
        </div>
        <p style="margin-top: 60px; color: #1a1a1a; font-size: 10px;">Giriş için: Shift + L</p>
    </div>

    <div id="auth-panel" class="hidden">
        <div class="container">
            <h2 id="auth-title" style="color: var(--neon); margin-bottom: 20px;">Sistem Girişi</h2>
            <input type="text" id="user" placeholder="Kullanıcı Adı">
            <input type="password" id="pass" placeholder="Şifre">
            <button class="main-btn" onclick="handleAuth()" id="auth-btn">Giriş Yap</button>
            <p id="toggle-text" onclick="toggleAuth()" style="margin-top: 20px; font-size: 13px; cursor: pointer; color: #888;">Hesabın yok mu? <span style="color: var(--neon)">Kayıt Ol</span></p>
        </div>
    </div>

    <div id="checker-panel" class="hidden">
        <div id="nav-header">
            <button onclick="toggleSidebar()" style="background:none; border:none; color:var(--neon); font-size:24px; cursor:pointer;">☰</button>
            <div style="font-weight:bold">ShadowHunter <span class="badge">PREMIUM</span></div>
            <button onclick="logout()" style="background:none; border:none; color:red; font-size:12px; cursor:pointer;">Çıkış</button>
        </div>

        <div class="sidebar" id="sidebar">
            <h2 style="color:var(--neon); margin-bottom:20px;">Sorgu Listesi</h2>
            <div class="menu-item" onclick="setApi('GSM - TC Sorgu', 'https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm=')">📞 GSM - TC Sorgu</div>
            <div class="menu-item" onclick="setApi('TC - GSM Sorgu', 'https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc=')">🆔 TC - GSM Sorgu</div>
            <div class="menu-item" onclick="setApi('Ad Soyad Sorgu', 'https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad=')">👤 Ad Soyad Sorgu</div>
            <div class="menu-item" onclick="setApi('Aile Sorgu', 'https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc=')">👨‍👩‍👧 Aile Sorgu</div>
            <div class="menu-item" onclick="setApi('TC Pro Full', 'https://sorgum.2026tr.xyz/nabi/api/v1/tcpro?tc=')">💎 TC Pro Full</div>
            <div class="menu-item" onclick="setApi('Eczane Reçete', 'https://nabisorguapis.onrender.com/api/v1/eczane/recete-gecmisi?tc=')">💊 Reçete Geçmişi</div>
            <div class="menu-item" onclick="setApi('Adres Sorgu', 'https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc=')">🏠 Adres Sorgu</div>
            <div class="menu-item" onclick="setApi('Istanbul Kart', 'https://nabisorguapis.onrender.com/api/v1/ulasim/istanbulkart-bakiye?tc=')">💳 Istanbul Kart</div>
        </div>

        <div class="container" style="margin-top: 40px;">
            <h3 id="current-op" style="color: var(--neon); margin-bottom: 15px;">Sorgu Seçiniz</h3>
            <input type="text" id="id-input" placeholder="ID Giriniz...">
            <input type="text" id="query-val" placeholder="Sorgulanacak veriyi girin...">
            <input type="text" id="count-input" placeholder="Kaç adet gönderilecek?">
            <button class="main-btn" onclick="executeSorgu()">SORGULA & GÖNDER</button>
            <pre id="result">Sonuçlar burada filtrelenmiş olarak görünecek...</pre>
        </div>
    </div>

    <script>
        let authMode = 'login';
        let selectedApi = '';

        // Gizli Kısayol: Shift + L
        document.addEventListener('keydown', (e) => {
            if(e.shiftKey && e.key === 'L') showLogin();
        });

        function showLogin() {
            document.getElementById('game-site').classList.add('hidden');
            document.getElementById('auth-panel').classList.remove('hidden');
        }

        function toggleAuth() {
            authMode = (authMode === 'login') ? 'register' : 'login';
            document.getElementById('auth-title').innerText = authMode === 'login' ? 'Sistem Girişi' : 'Yeni Kayıt';
            document.getElementById('auth-btn').innerText = authMode === 'login' ? 'Giriş Yap' : 'Kayıt Ol';
            document.getElementById('toggle-text').innerHTML = authMode === 'login' ? 'Hesabın yok mu? <span style="color: var(--neon)">Kayıt Ol</span>' : 'Zaten hesabın var mı? <span style="color: var(--neon)">Giriş Yap</span>';
        }

        async function handleAuth() {
            const user = document.getElementById('user').value;
            const pass = document.getElementById('pass').value;
            if(!user || !pass) return alert("Boş bırakma!");

            const res = await fetch(authMode === 'login' ? '/api/login' : '/api/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user, pass})
            });
            const data = await res.json();

            if(data.success) {
                if(authMode === 'register') {
                    alert("Kayıt Başarılı! Şimdi giriş yapın.");
                    toggleAuth();
                } else {
                    localStorage.setItem('doc_session', 'true');
                    openChecker();
                }
            } else {
                alert(data.msg);
            }
        }

        function openChecker() {
            document.getElementById('auth-panel').classList.add('hidden');
            document.getElementById('game-site').classList.add('hidden');
            document.getElementById('checker-panel').classList.remove('hidden');
        }

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('open');
        }

        function setApi(name, url) {
            selectedApi = url;
            document.getElementById('current-op').innerText = name;
            toggleSidebar();
        }

        async function executeSorgu() {
            const val = document.getElementById('query-val').value;
            const rid = document.getElementById('id-input').value;
            const rcount = document.getElementById('count-input').value;

            if(!selectedApi || !val) return alert("Sorgu türü ve veri girin!");

            document.getElementById('result').innerText = "Sorgulanıyor...";

            const res = await fetch('/api/proxy', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ url: selectedApi + val })
            });
            let data = await res.text();
            
            // ID ve Sayı Bilgisini sona ekle (Mühürleme)
            const footer = "\\n\\n🆔 ID: " + (rid || "Belirtilmedi") + "\\n📊 Dağıtım: " + (rcount || "1") + " Kanal";
            document.getElementById('result').innerText = data + footer;
        }

        function logout() {
            localStorage.clear();
            location.reload();
        }

        if(localStorage.getItem('doc_session')) openChecker();
    </script>
</body>
</html>
    `);
});

app.listen(PORT, () => console.log("Lord Server Running on Port " + PORT));
