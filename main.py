# -- coding: utf-8 --
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import os
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Tüm origin'lere izin (test için) → production'da kısıtla!

# Şifreler (gerçek kullanımda environment variable yap!)
USER_PASSWORD = "2026lordvipfree"
ADMIN_PASSWORD = "@lorddestekhatvip"

PORT = int(os.environ.get("PORT", 5000))
DATA_FILE = "apis.json"

# Varsayılan API'ler
DEFAULT_APIS = {
    "adrespro": "https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc={v}",
    "adsoyadpro": "https://sorgum.2026tr.xyz/nabi/api/v1/adsoyad?ad={a}&soyad={s}&q={q}",
    "ailepro": "https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc={v}",
    "gsmpro": "https://sorgum.2026tr.xyz/nabi/api/v1/gsm?q={v}",
    "babapro": "https://sorgum.2026tr.xyz/nabi/api/v1/baba?tc={v}",
    "annepro": "https://sorgum.2026tr.xyz/nabi/api/v1/anne?tc={v}",
    "tcpro": "https://sorgum.2026tr.xyz/nabi/api/v1/tcpro?tc={v}"
}

def load_apis():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_APIS, f, ensure_ascii=False, indent=2)
        return DEFAULT_APIS.copy()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    for k, v in DEFAULT_APIS.items():
        data.setdefault(k, v)
    return data

def save_apis(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def call_api(url):
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        try:
            json_data = r.json()
            return json_data.get("veri", json_data)
        except:
            return {"raw_response": r.text}
    except Exception as e:
        return {"error": f"API çağrı hatası: {str(e)}"}

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    pw = data.get("password")
    if pw == ADMIN_PASSWORD:
        return jsonify({"ok": True, "admin": True})
    if pw == USER_PASSWORD:
        return jsonify({"ok": True, "admin": False})
    return jsonify({"ok": False, "message": "Geçersiz şifre"}), 401

@app.route("/api/<api_name>", methods=["POST"])
def proxy_api(api_name):
    apis = load_apis()
    if api_name not in apis:
        return jsonify({"error": "Böyle bir sorgu yok"}), 404

    data = request.get_json(silent=True) or {}
    value = data.get("value", "")

    if value.endswith(".txt") and os.path.exists(value):
        try:
            with open(value, "r", encoding="utf-8") as f:
                results = []
                for line in f:
                    v = line.strip()
                    if not v:
                        continue
                    url = apis[api_name].format(v=v, a="", s="", q=v)
                    results.append({"input": v, "result": call_api(url)})
            return jsonify({"batch_results": results})
        except Exception as e:
            return jsonify({"error": f"TXT okuma hatası: {str(e)}"}), 500

    url = apis[api_name].format(
        v=value,
        a=data.get("ad", ""),
        s=data.get("soyad", ""),
        q=data.get("q", value)
    )
    return jsonify(call_api(url))

@app.route("/admin/apis", methods=["GET"])
def admin_list_apis():
    return jsonify(load_apis())

@app.route("/admin/add", methods=["POST"])
def admin_add():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip().lower()
    url = str(data.get("url", "")).strip()
    if not name or not url:
        return jsonify({"error": "Ad ve URL zorunlu"}), 400
    apis = load_apis()
    apis[name] = url
    save_apis(apis)
    return jsonify({"success": True})

@app.route("/admin/edit", methods=["POST"])
def admin_edit():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip().lower()
    url = str(data.get("url", "")).strip()
    if not name or not url:
        return jsonify({"error": "Ad ve URL zorunlu"}), 400
    apis = load_apis()
    if name not in apis:
        return jsonify({"error": "API bulunamadı"}), 404
    apis[name] = url
    save_apis(apis)
    return jsonify({"success": True})

@app.route("/admin/delete", methods=["POST"])
def admin_delete():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip().lower()
    apis = load_apis()
    if name in apis:
        del apis[name]
        save_apis(apis)
        return jsonify({"success": True})
    return jsonify({"error": "API bulunamadı"}), 404

@app.route("/")
def index():
    apis = load_apis()
    return render_template_string('''<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>LORD PANEL 2026</title>
  <style>
    :root { --bg: #0a0e17; --text: #00ff41; --accent: #00bfff; --card: #111827; }
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      background: var(--bg); color: var(--text); font-family: 'Courier New', monospace;
      min-height: 100vh; position: relative; overflow-x: hidden;
    }
    canvas#matrix { position: fixed; inset: 0; z-index: -2; opacity: 0.4; }
    header {
      position: fixed; top: 0; left: 0; right: 0; background: rgba(17,24,39,0.85);
      backdrop-filter: blur(8px); padding: 1rem; display: flex; align-items: center;
      z-index: 1000; border-bottom: 1px solid #00ff4133;
    }
    #menu-btn { font-size: 1.8rem; cursor: pointer; margin-right: 1rem; color: var(--accent); }
    #brand { font-size: 1.4rem; font-weight: bold; display: flex; align-items: center; gap: 0.5rem; }
    .verified { color: var(--accent); font-size: 1.1em; }
    #side-menu {
      position: fixed; top: 0; left: -280px; width: 280px; height: 100%;
      background: var(--card); padding: 5rem 1.5rem 1.5rem; transition: left 0.4s ease;
      z-index: 999; border-right: 1px solid #00ff4133; overflow-y: auto;
    }
    #side-menu.open { left: 0; }
    #side-menu a {
      display: block; color: var(--text); text-decoration: none; padding: 0.9rem 0;
      border-bottom: 1px solid #00ff4122; transition: 0.2s;
    }
    #side-menu a:hover { color: var(--accent); padding-left: 0.8rem; }
    main { margin-top: 70px; padding: 1.5rem; }
    .hidden { display: none !important; }
    .card {
      background: var(--card); border: 1px solid #00ff4133; border-radius: 12px;
      padding: 1.5rem; margin: 1rem 0; box-shadow: 0 4px 20px rgba(0,255,65,0.08);
    }
    input, button {
      width: 100%; padding: 0.9rem; margin: 0.6rem 0; border-radius: 8px; border: 1px solid #00ff4133;
      background: #0f172a; color: var(--text); font-family: inherit;
    }
    button {
      background: linear-gradient(90deg, #00bfff, #00ff41); color: #000; font-weight: bold;
      cursor: pointer; transition: 0.3s; border: none;
    }
    button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,191,255,0.3); }
    pre { background: #000; padding: 1rem; border-radius: 8px; overflow-x: auto; font-size: 0.9rem; }
    .loading { text-align: center; color: var(--accent); font-style: italic; }
  </style>
</head>
<body>
  <canvas id="matrix"></canvas>

  <header>
    <div id="menu-btn">☰</div>
    <div id="brand">LORD PANEL <span class="verified">✔</span></div>
  </header>

  <div id="side-menu">
    <a href="https://t.me/lordsystemv3" target="_blank">Telegram: @lordsystemv3</a>
    <div id="query-list"></div>
    <hr style="border-color:#00ff4122; margin:1.5rem 0;">
    <a href="#" onclick="logout(); return false;">Çıkış Yap</a>
  </div>

  <main>
    <div id="login-page" class="card">
      <h2 style="text-align:center; margin-bottom:1.5rem;">LORD PANEL <span class="verified">✔</span></h2>
      <input id="password" type="password" placeholder="Şifrenizi girin" autocomplete="off"/>
      <button id="login-btn">GİRİŞ YAP</button>
      <p style="text-align:center; margin-top:1rem;">
        <a href="https://t.me/lordsystemv3" target="_blank" style="color:var(--accent);">Telegram Kanalı: @lordsystemv3</a>
      </p>
      <p id="login-status" class="loading hidden"></p>
    </div>

    <div id="main-page" class="hidden">
      <div class="card">
        <h2 class="verified">HOŞ GELDİNİZ – DOĞRULANDI</h2>
        <div id="content-area"></div>
      </div>
    </div>

    <div id="admin-page" class="hidden card">
      <h2>ADMIN KONTROL PANELİ</h2>
      <h3>Yeni Sorgu Ekle</h3>
      <input id="new-name" placeholder="Sorgu adı (örn: yenitcpro)"/>
      <input id="new-url" placeholder="API URL (örn: https://api.com?tc={v})"/>
      <button onclick="addQuery()">EKLE</button>

      <h3>Düzenle</h3>
      <input id="edit-name" placeholder="Düzenlenecek sorgu adı"/>
      <input id="edit-url" placeholder="Yeni URL"/>
      <button onclick="editQuery()">DÜZENLE</button>

      <h3>Sil</h3>
      <input id="del-name" placeholder="Silinecek sorgu adı"/>
      <button onclick="deleteQuery()">SİL</button>

      <h3>Mevcut Sorgular</h3>
      <pre id="api-list"></pre>
    </div>
  </main>

  <script>
    const menu = document.getElementById("side-menu");
    const menuBtn = document.getElementById("menu-btn");
    menuBtn.onclick = () => menu.classList.toggle("open");

    // Matrix efekti
    const canvas = document.getElementById("matrix");
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    window.addEventListener("resize", () => {
      canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    });

    const chars = "01LORD✔✪";
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = Array(Math.floor(columns)).fill(1);

    function drawMatrix() {
      ctx.fillStyle = "rgba(10,14,23,0.05)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "#00ff41";
      ctx.font = fontSize + "px monospace";
      drops.forEach((y, i) => {
        const text = chars[Math.floor(Math.random() * chars.length)];
        const x = i * fontSize;
        ctx.fillText(text, x, y * fontSize);
        if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
      });
    }
    setInterval(drawMatrix, 40);

    let isAdmin = false;
    let isLoggedIn = false;

    function loadQueries() {
      fetch("/admin/apis")
        .then(r => r.json())
        .then(apis => {
          const list = document.getElementById("query-list");
          list.innerHTML = "<hr>SORGULAR<hr>";
          Object.keys(apis).forEach(key => {
            const a = document.createElement("a");
            a.href = "#";
            a.textContent = key;
            a.onclick = () => openQueryPage(key);
            list.appendChild(a);
          });
          document.getElementById("api-list").textContent = JSON.stringify(apis, null, 2);
        })
        .catch(err => console.error("Sorgu listesi yüklenemedi:", err));
    }

    function openQueryPage(name) {
      menu.classList.remove("open");
      document.getElementById("content-area").innerHTML = `
        <div class="card">
          <h3>${name.toUpperCase()} SORGUSU</h3>
          <input id="qvalue-${name}" placeholder="Değer veya .txt dosya yolu"/>
          <small style="color:#aaa;">.txt → satır satır sorgular (örn: /sdcard/list.txt)</small>
          <button onclick="runQuery('${name}')">SORGULA</button>
          <pre id="result-${name}" style="margin-top:1rem; min-height:100px;"></pre>
        </div>`;
    }

    async function runQuery(name) {
      const val = document.getElementById(`qvalue-${name}`).value.trim();
      if (!val) return alert("Değer girin!");
      const resultEl = document.getElementById(`result-${name}`);
      resultEl.textContent = "Sorgulanıyor...";

      try {
        const res = await fetch(`/api/${name}`, {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({value: val})
        });
        if (!res.ok) throw new Error(`Sunucu hatası: ${res.status}`);
        const data = await res.json();
        resultEl.textContent = data.batch_results
          ? "Toplu sonuç:\\n" + JSON.stringify(data.batch_results, null, 2)
          : JSON.stringify(data, null, 2);
      } catch (err) {
        resultEl.textContent = "HATA: " + err.message;
      }
    }

    async function login() {
      const pw = document.getElementById("password").value;
      const status = document.getElementById("login-status");
      const btn = document.getElementById("login-btn");

      if (!pw) return alert("Şifre boş olamaz!");
      status.classList.remove("hidden");
      status.textContent = "Giriş yapılıyor... (Render cold-start olabilir, 30-60 sn bekleyin)";
      btn.disabled = true;

      try {
        const res = await fetch("/login", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({password: pw})
        });
        if (!res.ok) throw new Error(await res.text());
        const data = await res.json();

        if (data.ok) {
          localStorage.setItem("lord_auth", pw);
          isLoggedIn = true;
          isAdmin = data.admin;
          document.getElementById("login-page").classList.add("hidden");
          document.getElementById("main-page").classList.remove("hidden");
          if (isAdmin) document.getElementById("admin-page").classList.remove("hidden");
          loadQueries();
        } else {
          alert(data.message || "Giriş başarısız!");
        }
      } catch (err) {
        alert("Bağlantı hatası: " + err.message + "\\n\\nRender free tier'da ilk istek yavaş olabilir.");
      } finally {
        status.classList.add("hidden");
        btn.disabled = false;
      }
    }

    document.getElementById("login-btn").onclick = login;
    document.getElementById("password").addEventListener("keyup", e => { if (e.key === "Enter") login(); });

    function addQuery()    { adminAction("/admin/add",    {name: "new-name", url: "new-url"}); }
    function editQuery()   { adminAction("/admin/edit",   {name: "edit-name", url: "edit-url"}); }
    function deleteQuery() { adminAction("/admin/delete", {name: "del-name"}); }

    async function adminAction(endpoint, fields) {
      if (!isAdmin) return alert("Admin yetkisi yok!");
      const body = {};
      for (const [k, id] of Object.entries(fields)) {
        body[k] = document.getElementById(id).value.trim();
        if (k === "name" && !body[k]) return alert("Ad zorunlu!");
      }
      try {
        const res = await fetch(endpoint, {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(body)
        });
        if (!res.ok) throw new Error(await res.text());
        loadQueries();
        alert("İşlem başarılı!");
      } catch (err) {
        alert("Hata: " + err.message);
      }
    }

    function logout() {
      localStorage.removeItem("lord_auth");
      location.reload();
    }

    if (localStorage.getItem("lord_auth")) {
      document.getElementById("password").value = ""; // güvenlik
      login();  // auto-login denemesi
    }
  </script>
</body>
</html>''', apis=apis)

if __name__ == "__main__":
    # Render'da debug=False kullan (production)
    # app.run(host="0.0.0.0", port=PORT, debug=False)
    app.run(host="0.0.0.0", port=PORT)ringify(j,null,2);
        }
    }).catch(e=>alert("Hata: "+e));
}

function ekle(){
    if(!isAdmin)return alert('Sadece admin');
    let ad=document.getElementById('yeniad').value.trim();
    let url=document.getElementById('yeniurl').value.trim();
    if(!ad||!url)return alert('Boş bırakmayın');
    fetch('/admin/ekle',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:ad,url:url})})
    .then(()=>yukleSorgular());
}

function duzenle(){
    if(!isAdmin)return alert('Sadece admin');
    let ad=document.getElementById('duzenad').value.trim();
    let url=document.getElementById('duzenurl').value.trim();
    if(!ad||!url)return alert('Boş bırakmayın');
    fetch('/admin/duzenle',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:ad,url:url})})
    .then(()=>yukleSorgular());
}

function sil(){
    if(!isAdmin)return alert('Sadece admin');
    let ad=document.getElementById('silad').value.trim();
    if(!ad)return alert('Ad girin');
    fetch('/admin/sil',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:ad})})
    .then(()=>yukleSorgular());
}

function cikis(){
    localStorage.removeItem('auth');
    loggedIn=false;
    isAdmin=false;
    location.reload();
}

if(localStorage.getItem('auth'))giris();
</script>
</body></html>""",apis=apiler)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=PORT)
