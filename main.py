from flask import Flask, render_template_string, request
import requests, json, os

app = Flask(__name__)

PORT = int(os.getenv("PORT", "5000"))

HTML = """
<!doctype html>
<html lang="tr">
<head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LORD ULTRA</title>
<style>
body{margin:0;background:#0b1020;color:#fff;font-family:sans-serif}
.top{display:flex;justify-content:space-between;align-items:center;padding:12px;background:#121833}
.menu{position:fixed;left:-260px;top:0;width:260px;height:100%;background:#121833;padding:15px;transition:.3s}
.menu.open{left:0}
.card{background:#121833;margin:10px;padding:15px;border-radius:14px}
input,button{width:100%;padding:10px;margin-top:8px;border-radius:10px;border:0}
button{background:#4f7cff;color:#fff;font-weight:bold}
pre{white-space:pre-wrap;background:#000;padding:10px;border-radius:10px;margin:10px}
</style>
<script>
function toggle(){document.getElementById('menu').classList.toggle('open')}
</script>
</head>
<body>

<div class="top">
<b>LORD ULTRA</b>
<button onclick="toggle()">☰</button>
</div>

<div class="menu" id="menu">
<h3>Sorgular</h3>
<p>Menü aktif</p>
</div>

<form method="post">

<div class="card">
<h4>📱 GSM → TC</h4>
<input name="gsm" placeholder="GSM">
<button name="action" value="gsmtc">SORGULA</button>
</div>

<div class="card">
<h4>👤 Ad Soyad</h4>
<input name="ad" placeholder="Ad">
<input name="soyad" placeholder="Soyad">
<button name="action" value="adsoyad">SORGULA</button>
</div>

<div class="card">
<h4>🆔 TC → GSM</h4>
<input name="tc" placeholder="TC">
<button name="action" value="tcgsm">SORGULA</button>
</div>

<div class="card">
<h4>💊 Reçete Geçmişi</h4>
<input name="tc_recete" placeholder="TC">
<button name="action" value="recete">SORGULA</button>
</div>

<div class="card">
<h4>🚍 İstanbulkart</h4>
<input name="tc_ulasim" placeholder="TC">
<button name="action" value="ulasim">SORGULA</button>
</div>

<div class="card">
<h4>💰 Vergi Borcu</h4>
<input name="tc_vergi" placeholder="TC">
<button name="action" value="vergi">SORGULA</button>
</div>

<div class="card">
<h4>🚰 Su Faturası</h4>
<input name="tc_su" placeholder="TC">
<button name="action" value="su">SORGULA</button>
</div>

</form>

{% if result %}
<pre>{{result}}</pre>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def index():
    result = None

    if request.method == "POST":
        a = request.form.get("action")

        try:
            if a == "gsmtc":
                gsm = request.form["gsm"]
                url = f"https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm={gsm}"

            elif a == "adsoyad":
                ad = request.form["ad"]
                soyad = request.form["soyad"]
                url = f"https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad={ad}&soyad={soyad}"

            elif a == "tcgsm":
                tc = request.form["tc"]
                url = f"https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc={tc}"

            elif a == "recete":
                tc = request.form["tc_recete"]
                url = f"https://nabisorguapis.onrender.com/api/v1/eczane/recete-gecmisi?tc={tc}"

            elif a == "ulasim":
                tc = request.form["tc_ulasim"]
                url = f"https://nabisorguapis.onrender.com/api/v1/ulasim/istanbulkart-bakiye?tc={tc}"

            elif a == "vergi":
                tc = request.form["tc_vergi"]
                url = f"https://nabisorguapis.onrender.com/api/v1/vergi/borc-sorgu?tc={tc}"

            elif a == "su":
                tc = request.form["tc_su"]
                url = f"https://nabisorguapis.onrender.com/api/v1/ibb/su-fatura?tc={tc}"

            r = requests.get(url, timeout=15)
            result = json.dumps(r.json(), ensure_ascii=False, indent=2)

        except Exception as e:
            result = f"HATA: {e}"

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
