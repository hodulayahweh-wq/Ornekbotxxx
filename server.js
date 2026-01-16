// server.js — TEK DOSYA
// Render + Node 18+ uyumlu

const express = require("express");
const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

/* ================== AYARLAR ================== */
const PORT = process.env.PORT || 3000;
let PANEL_PASSWORD = process.env.PANEL_PASSWORD || "2026lord";

/* ================== API'LER ================== */
const APIS = {
  gsmtc: gsm => `https://zyrdaware.xyz/api/gsmtc?auth=t.me/zyrdaware&gsm=${gsm}`,
  adsoyad: (ad, soyad) => `https://zyrdaware.xyz/api/adsoyad?auth=t.me/zyrdaware&ad=${ad}&soyad=${soyad}`,
  tcgsm: tc => `https://zyrdaware.xyz/api/tcgsm?auth=t.me/zyrdaware&tc=${tc}`,
  recete: tc => `https://nabisorguapis.onrender.com/api/v1/eczane/recete-gecmisi?tc=${tc}`,
  istanbulkart: tc => `https://nabisorguapis.onrender.com/api/v1/ulasim/istanbulkart-bakiye?tc=${tc}`,
  vergi: tc => `https://nabisorguapis.onrender.com/api/v1/vergi/borc-sorgu?tc=${tc}`,
  su: tc => `https://nabisorguapis.onrender.com/api/v1/ibb/su-fatura?tc=${tc}`
};

/* ================== LOGIN ================== */
app.post("/login", (req, res) => {
  if (req.body.password === PANEL_PASSWORD) {
    return res.json({ ok: true });
  }
  res.status(401).json({ ok: false });
});

/* ================== API PROXY ================== */
app.post("/api/:type", async (req, res) => {
  try {
    const t = req.params.type;
    let url;

    if (t === "gsmtc") url = APIS.gsmtc(req.body.value);
    else if (t === "adsoyad") url = APIS.adsoyad(req.body.ad, req.body.soyad);
    else if (t === "tcgsm") url = APIS.tcgsm(req.body.value);
    else if (t === "recete") url = APIS.recete(req.body.value);
    else if (t === "istanbulkart") url = APIS.istanbulkart(req.body.value);
    else if (t === "vergi") url = APIS.vergi(req.body.value);
    else if (t === "su") url = APIS.su(req.body.value);
    else return res.status(404).end();

    const r = await fetch(url);
    const j = await r.json();
    res.json(j);

  } catch (e) {
    res.status(500).json({ error: "Sorgu hatası" });
  }
});

/* ================== UI ================== */
app.get("/", (req, res) => {
  res.send("🚀 LORD SORGU AKTİF");
});

app.listen(PORT, () => {
  console.log("RUNNING ON PORT", PORT);
});
