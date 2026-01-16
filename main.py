# -- coding: utf-8 --
from flask import Flask,request,jsonify,render_template_string
import requests,os,json

app=Flask(__name__)

# sifreler
USER_PASSWORD="2026lordvipfree"
ADMIN_PASSWORD="@lorddestekhatvip"

PORT=int(os.environ.get("PORT",5000))
DATA_FILE="apis.json"

# default apiler
apis={
"adrespro":"https://sorgum.2026tr.xyz/nabi/api/v1/tc/adres?tc={v}",
"adsoyadpro":"https://sorgum.2026tr.xyz/nabi/api/v1/adsoyad?ad={a}&soyad={s}&q={q}",
"ailepro":"https://sorgum.2026tr.xyz/nabi/api/v1/aile?tc={v}",
"gsmpro":"https://sorgum.2026tr.xyz/nabi/api/v1/gsm?q={v}",
"babapro":"https://sorgum.2026tr.xyz/nabi/api/v1/baba?tc={v}",
"annepro":"https://sorgum.2026tr.xyz/nabi/api/v1/anne?tc={v}",
"tcpro":"https://sorgum.2026tr.xyz/nabi/api/v1/tcpro?tc={v}"
}

def yukle():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE,"w",encoding="utf-8") as f:
            json.dump(apis,f,ensure_ascii=False,indent=2)
        return apis.copy()
    with open(DATA_FILE,"r",encoding="utf-8") as f:
        data=json.load(f)
    for k in apis:
        if k not in data:
            data[k]=apis[k]
    return data

def kaydet(d):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(d,f,ensure_ascii=False,indent=2)

def api_cagir(url):
    try:
        r=requests.get(url,timeout=15)
        try:return r.json().get("veri",r.json())
        except:return {"hata":r.text}
    except:
        return {"hata":"baglanti yok"}

@app.route("/login",methods=["POST"])
def giris():
    pw=request.json.get("password")
    if pw==ADMIN_PASSWORD:return {"ok":1,"admin":1}
    if pw==USER_PASSWORD:return {"ok":1,"admin":0}
    return {"ok":0},401

@app.route("/api/<adi>",methods=["POST"])
def sorgu(adi):
    apiler=yukle()
    if adi not in apiler:return {"hata":"yok bu api"},404
    
    veri=request.json
    deger=veri.get("value","")
    
    # .txt dosyası varsa satır satır sorgula
    if deger.endswith(".txt") and os.path.exists(deger):
        try:
            with open(deger,"r",encoding="utf-8") as f:
                sonuclar=[]
                for satir in f:
                    v=satir.strip()
                    if not v:continue
                    url=apiler[adi].format(
                        v=v,
                        a=veri.get("ad",""),
                        s=veri.get("soyad",""),
                        q=veri.get("q",v)
                    )
                    sonuc=api_cagir(url)
                    sonuclar.append({"deger":v,"sonuc":sonuc})
                return jsonify({"toplu_sonuc":sonuclar})
        except Exception as e:
            return {"hata":f"txt okuma hatasi: {str(e)}"}
    
    # normal tek sorgu
    url=apiler[adi].format(
        v=deger,
        a=veri.get("ad",""),
        s=veri.get("soyad",""),
        q=veri.get("q",deger)
    )
    return jsonify(api_cagir(url))

@app.route("/admin/apis")
def listele():
    return jsonify(yukle())

@app.route("/admin/ekle",methods=["POST"])
def ekle():
    d=request.json
    ad=str(d.get("name","")).lower().strip()
    url=str(d.get("url","")).strip()
    if not ad or not url:return {"hata":"eksik bilgi"},400
    apiler=yukle()
    apiler[ad]=url
    kaydet(apiler)
    return {"tamam":1}

@app.route("/admin/duzenle",methods=["POST"])
def duzenle():
    d=request.json
    ad=str(d.get("name","")).lower().strip()
    yeni_url=str(d.get("url","")).strip()
    if not ad or not yeni_url:return {"hata":"eksik"},400
    apiler=yukle()
    if ad in apiler:
        apiler[ad]=yeni_url
        kaydet(apiler)
        return {"tamam":1}
    return {"hata":"bulunamadi"},404

@app.route("/admin/sil",methods=["POST"])
def sil():
    ad=str(request.json.get("name","")).lower().strip()
    apiler=yukle()
    if ad in apiler:
        apiler.pop(ad)
        kaydet(apiler)
        return {"tamam":1}
    return {"hata":"bulunamadi"},404

@app.route("/")
def ana():
    apiler=yukle()
    return render_template_string("""<!DOCTYPE html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LORD 2026</title>
<style>
body{margin:0;padding:0;background:#000;color:#0f0;font-family:monospace;position:relative;overflow:hidden}
#simulation{position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;opacity:0.5}
#bgtext{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);font-size:5em;color:rgba(0,255,0,0.1);z-index:-1;white-space:nowrap}
button, input{width:100%;margin:6px 0;padding:10px;border:1px solid #0f0;background:#111;color:#0f0}
pre{color:#0f0;word-break:break-all}
.hidden{display:none}
header{position:fixed;top:0;left:0;width:100%;background:#111;padding:10px;display:flex;align-items:center;z-index:10}
#hamburger{font-size:24px;cursor:pointer;margin-right:10px}
#title{font-size:20px;display:flex;align-items:center;gap:8px}
#menu{position:fixed;top:50px;left:0;background:#111;padding:10px;display:none;z-index:10;width:250px}
#menu a{display:block;color:#0f0;text-decoration:none;margin:5px 0}
#main-content{margin-top:60px;padding:10px}
.verified::after{content:"✔";color:#1DA1F2;font-size:1.2em;margin-left:6px}
a{color:#0f0}
#sorgu-sayfa{padding:20px;background:#111;border:1px solid #0f0;margin:10px;border-radius:8px}
</style></head><body>
<canvas id="simulation"></canvas>
<div id="bgtext">LORD SORGU</div>

<header>
<span id="hamburger" onclick="toggleMenu()">☰</span>
<span id="title">LORD PANEL <span class="verified"></span></span>
</header>

<div id="menu">
<a href="https://t.me/lordsystemv3" target="_blank">Telegram Kanalı: @lordsystemv3</a>
<div id="sorgu-menu"></div>
<a href="#" onclick="cikis()">ÇIKIŞ YAP</a>
</div>

<div id="giris" class="main-content">
<h3>LORD PANEL <span class="verified"></span></h3>
<input id="sifre" type="password" placeholder="Şifrenizi girin">
<button onclick="giris()">GİRİŞ YAP</button>
<a href="https://t.me/lordsystemv3" target="_blank">Telegram Kanalı: @lordsystemv3</a>
</div>

<div id="ana" class="hidden main-content">
<h3 class="verified">HOŞGELDİNİZ (GERÇEK DOĞRULANDI)</h3>
<div id="icerik"></div>
</div>

<div id="adminpanel" class="hidden main-content">
<h3>ADMIN PANEL (ULTRA)</h3>
<h4>Yeni Sorgu Ekle</h4>
<input id="yeniad" placeholder="api adi (örn: yenipro)">
<input id="yeniurl" placeholder="url (örn: https://api.com?q={v})">
<button onclick="ekle()">EKLE</button>

<h4>Sorgu Düzenle</h4>
<input id="duzenad" placeholder="düzenlenecek api adı">
<input id="duzenurl" placeholder="yeni url">
<button onclick="duzenle()">DÜZENLE</button>

<h4>Sorgu Sil</h4>
<input id="silad" placeholder="silinecek api adı">
<button onclick="sil()">SİL</button>

<h4>Tüm Sorgular (JSON)</h4>
<pre id="apiler"></pre>
</div>

<script>
let isAdmin=false;
let loggedIn=false;

function toggleMenu(){
    let m=document.getElementById('menu');
    m.style.display=m.style.display==='block'?'none':'block';
}

function initSimulation(){
    let c=document.getElementById('simulation');
    c.width=window.innerWidth;
    c.height=window.innerHeight;
    let ctx=c.getContext('2d');
    let chars='01LORD';
    let fontSize=10;
    let columns=c.width/fontSize;
    let drops=[];
    for(let x=0;x<columns;x++)drops[x]=1;
    function draw(){
        ctx.fillStyle='rgba(0,0,0,0.05)';
        ctx.fillRect(0,0,c.width,c.height);
        ctx.fillStyle='#0f0';
        ctx.font=fontSize+'px monospace';
        for(let i=0;i<drops.length;i++){
            let text=chars[Math.floor(Math.random()*chars.length)];
            ctx.fillText(text,i*fontSize,drops[i]*fontSize);
            if(drops[i]*fontSize>c.height&&Math.random()>0.975)drops[i]=0;
            drops[i]++;
        }
    }
    setInterval(draw,33);
}
initSimulation();
window.addEventListener('resize',()=>{let c=document.getElementById('simulation');c.width=window.innerWidth;c.height=window.innerHeight;});

function yukleSorgular(){
    fetch('/admin/apis').then(r=>r.json()).then(veri=>{
        let smenu=document.getElementById('sorgu-menu');
        smenu.innerHTML='<hr>SORGULAR<hr>';
        for(let k in veri){
            let a=document.createElement('a');
            a.textContent=k;
            a.href='#';
            a.onclick=()=>acSorguSayfa(k);
            smenu.appendChild(a);
        }
        document.getElementById('apiler').textContent=JSON.stringify(veri,null,2);
    });
}

function acSorguSayfa(adi){
    toggleMenu();
    let icerik=document.getElementById('icerik');
    icerik.innerHTML=`
    <div id="sorgu-sayfa">
    <h3>${adi.toUpperCase()} SORGUSU</h3>
    <input id="deger-${adi}" placeholder="Değer gir (veya .txt dosya yolu)">
    <small>Not: .txt dosyası yüklerseniz satır satır sorgulanır (Termux'ta dosya yolu ör: /sdcard/liste.txt)</small>
    <button onclick="sorgula('${adi}')">SORGULA</button>
    <pre id="sonuc-${adi}"></pre>
    </div>`;
}

function giris(){
    let pw=document.getElementById('sifre').value;
    fetch('/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:pw})})
    .then(r=>r.json()).then(d=>{
        if(d.ok){
            localStorage.setItem('auth',pw);
            loggedIn=true;
            isAdmin=d.admin;
            document.getElementById('giris').classList.add('hidden');
            document.getElementById('ana').classList.remove('hidden');
            if(isAdmin)document.getElementById('adminpanel').classList.remove('hidden');
            yukleSorgular();
        }else alert('YANLIŞ ŞİFRE!');
    });
}

function sorgula(adi){
    if(!loggedIn)return alert('Giriş yapın');
    let v=document.getElementById(`deger-${adi}`).value.trim();
    if(!v)return alert('Değer girin');
    fetch('/api/'+adi,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({value:v})})
    .then(r=>r.json()).then(j=>{
        let out=document.getElementById(`sonuc-${adi}`);
        if(j.toplu_sonuc){
            out.textContent="Toplu sorgu sonuçları:\n"+JSON.stringify(j.toplu_sonuc,null,2);
        }else{
            out.textContent=JSON.stringify(j,null,2);
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
