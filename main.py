from flask import Flask, render_template_string, request, session, redirect
import requests, json, os, datetime

app = Flask(__name__)
app.secret_key = "lord-ultra-secret"
PORT = int(os.getenv("PORT", "5000"))

# Giriş bilgileri
DATA = {
    "admin_pass": "2026xlord",
    "user_pass": "2026lordcheck",
    "logs": [],
    "apis": {
        "gsmtc": {
            "name": "GSM → TC",
            "enabled": True
        },
        "adsoyad": {
            "name": "Ad Soyad",
            "enabled": True
        },
        "tcgsm": {
            "name": "TC → GSM",
            "enabled": True
        },
        "recete": {
            "name": "Reçete",
            "enabled": True
        },
        "ulasim": {
            "name": "İstanbulkart",
            "enabled": True
        },
        "vergi": {
            "name": "Vergi Borcu",
            "enabled": True
        },
        "su": {
            "name": "Su Faturası",
            "enabled": True
        },
        # Yeni API'ler
        "adres": {
            "name": "Adres Sorgulama",
            "enabled": True
        },
        "aile": {
            "name": "Aile Sorgulama",
            "enabled": True
        },
        "gsm": {
            "name": "GSM Sorgulama",
            "enabled": True
        },
        "baba": {
            "name": "Baba Sorgulama",
            "enabled": True
        },
        "anne": {
            "name": "Anne Sorgulama",
            "enabled": True
        },
        "tcpro": {
            "name": "TC Pro Sorgulama",
            "enabled": True
        }
    }
}

# API URL'lerini gizleyeceğiz
API_URLS = {
    "gsmtc": "https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm={}",
    "adsoyad": "https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad={}&soyad={}",
    "tcgsm": "https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc={}",
    "recete": "https://nabisorguapis.onrender.com/api/v1/eczane/recete-gecmisi?tc={}",
    "ulasim": "https://nabisorguapis.onrender.com/api/v1/ulasim/istanbulkart-bakiye?tc={}",
    "vergi": "https://nabisorguapis.onrender.com/api/v1/vergi/borc-sorgu?tc={}",
    "su": "https://nabisorguapis.onrender.com/api/v1/ibb/su-fatura?tc={}",
    "adres": "https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc={}",
    "aile": "https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc={}",
    "gsm": "https://sorgum.2026tr.xyz/nabi/api/v1/gsm?q={}",
    "baba": "https://sorgum.2026tr.xyz/nabi/api/v1/baba?tc={}",
    "anne": "https://sorgum.2026tr.xyz/nabi/api/v1/anne?tc={}",
    "tcpro": "https://sorgum.2026tr.xyz/nabi/api/v1/tcpro?tc={}"
}

def log(action, ip):
    DATA["logs"].append({
        "time": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        "action": action,
        "ip": ip
    })

HTML = """
<!doctype html>
<html><head>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>LORD ULTRA</title>
<style>
body{margin:0;background:#0b1020;color:#fff;font-family:sans-serif}
.card{background:#121833;padding:15px;margin:10px;border-radius:14px}
input,button{width:100%;padding:10px;margin-top:8px;border-radius:10px;border:0}
button{background:#4f7cff;color:#fff;font-weight:bold}
pre{background:#000;padding:10px;border-radius:10px;white-space:pre-wrap}
.menu{position:fixed;left:-260px;top:0;width:260px;height:100%;background:#121833;padding:15px;transition:.3s}
.menu.open{left:0}
.menu a{color:#fff;padding:10px;text-decoration:none;display:block}
.menu a:hover{background:#4f7cff}
</style>
<script>
function toggle(){document.getElementById('menu').classList.toggle('open')}
</script>
</head><body>

{% if not session.get('role') %}
<div class=card>
<h3>🔐 Giriş</h3>
<form method=post>
<input name=pass placeholder="Şifre">
<button>Giriş</button>
</form>
</div>
{% endif %}

{% if session.get('role') %}
<div class=card>
<h3>📌 Sorgular</h3>
<button onclick="toggle()">☰ Menü</button>
<div class="menu" id="menu">
{% for k,v in apis.items() if v.enabled %}
    <a href="#{{k}}">{{v.name}}</a>
{% endfor %}
</div>
</div>

<form method=post>
{% for k,v in apis.items() if v.enabled %}
<div class="card">
<h4>{{v.name}}</h4>
<input name="val1_{{k}}" placeholder="Değer">
{% if k == 'adsoyad' %}
<input name="val2_{{k}}" placeholder="Soyad">
{% endif %}
<button name="do" value="{{k}}">SORGULA</button>
</div>
{% endfor %}
</form>

{% if result %}
<pre>{{result}}</pre>
{% endif %}

{% if session.get('role') == 'admin' %}
<div class="card">
<h3>👑 Admin Panel</h3>
<form method=post>
<input name=newpass placeholder="Yeni Admin Şifresi">
<button name=admin value=pass>Şifre Değiştir</button>
</form>
<pre>{{logs}}</pre>
</div>
{% endif %}
{% endif %}

</body></html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    result = None
    ip = request.remote_addr

    if request.method == "POST":
        if "pass" in request.form:
            p = request.form["pass"]
            if p == DATA["admin_pass"]:
                session["role"] = "admin"
                log("Admin giriş", ip)
            elif p == DATA["user_pass"]:
                session["role"] = "user"
                log("User giriş", ip)

        if "do" in request.form:
            k = request.form["do"]
            api = DATA["apis"][k]
            v1 = request.form.get(f"val1_{k}")
            v2 = request.form.get(f"val2_{k}")

            # API URL'lerini gizledik, backend'de çağrılıyor
            url = API_URLS[k].format(v1, v2) if "{}" in API_URLS[k][API_URLS[k].find("{}")+2:] else API_URLS[k].format(v1)
            r = requests.get(url, timeout=15)
            result = json.dumps(r.json(), ensure_ascii=False, indent=2)
            log(f"Sorgu: {k}", ip)

        if request.form.get("admin") == "pass":
            DATA["admin_pass"] = request.form["newpass"]
            log("Admin şifre değişti", ip)

    return render_template_string(
        HTML,
        apis=DATA["apis"],
        result=result,
        logs=json.dumps(DATA["logs"], ensure_ascii=False, indent=2)
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
