"""
Build script: generates a self-contained index.html for GitHub Pages
embedding hero_bg.png as base64.
"""
import base64, pathlib, textwrap

ROOT = pathlib.Path(__file__).parent
img_path = ROOT / "app" / "hero_bg.png"
b64 = base64.b64encode(img_path.read_bytes()).decode() if img_path.exists() else ""

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>TN Crop Yield Advisory System | AI-Powered Agriculture</title>
  <meta name="description" content="AI-powered crop yield prediction for Tamil Nadu. XGBoost · SHAP · 20 years of NASA climate data."/>
  <link rel="preconnect" href="https://fonts.googleapis.com"/>
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,700;0,800;1,700&display=swap" rel="stylesheet"/>
  <style>
    *,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
    :root{{
      --g900:#031203;--g800:#0b2010;--g700:#163a18;--g500:#287a26;--g400:#41b041;
      --g300:#72d472;--g100:#c5f0c5;--gold:#c9a032;
      --w100:rgba(255,255,255,0.08);--w200:rgba(255,255,255,0.14);
      --w400:rgba(255,255,255,0.40);--w600:rgba(255,255,255,0.62);
    }}
    html{{scroll-behavior:smooth}}
    body{{font-family:'Inter',sans-serif;background:var(--g900);color:#fff;overflow-x:hidden}}
    ::-webkit-scrollbar{{width:5px}}
    ::-webkit-scrollbar-track{{background:var(--g900)}}
    ::-webkit-scrollbar-thumb{{background:var(--g500);border-radius:3px}}

    /* ── NAV ── */
    nav{{
      position:fixed;top:0;left:0;right:0;z-index:200;
      display:flex;align-items:center;justify-content:space-between;
      padding:0 6%;height:68px;
      background:rgba(3,18,3,0.50);
      backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px);
      border-bottom:1px solid rgba(255,255,255,0.06);
      transition:background .35s;
    }}
    nav.scrolled{{background:rgba(3,18,3,0.94)}}
    .nav-brand{{display:flex;align-items:center;gap:10px;text-decoration:none}}
    .nav-icon{{
      width:34px;height:34px;border-radius:9px;
      background:linear-gradient(135deg,var(--g500),var(--g400));
      display:flex;align-items:center;justify-content:center;
      font-size:1rem;box-shadow:0 4px 14px rgba(65,176,65,.3);
      flex-shrink:0;
    }}
    .nav-text strong{{font-size:.9rem;font-weight:700;display:block;line-height:1.1}}
    .nav-text span{{font-size:.65rem;color:var(--g300);letter-spacing:1.3px;text-transform:uppercase;font-weight:500}}
    .nav-links{{display:flex;align-items:center;gap:32px;list-style:none}}
    .nav-links a{{text-decoration:none;color:var(--w600);font-size:.87rem;font-weight:500;transition:color .2s}}
    .nav-links a:hover{{color:#fff}}
    .nav-cta{{
      background:var(--g500)!important;color:#fff!important;
      padding:8px 22px;border-radius:50px;font-weight:700!important;
      box-shadow:0 4px 16px rgba(65,176,65,.25);
      transition:all .25s!important;
    }}
    .nav-cta:hover{{background:var(--g400)!important;transform:translateY(-1px);box-shadow:0 7px 22px rgba(65,176,65,.4)!important}}

    /* ── HERO ── */
    .hero{{
      position:relative;min-height:100vh;
      display:flex;flex-direction:column;justify-content:center;
      padding:130px 6% 0;overflow:hidden;
    }}
    .hero-bg{{
      position:absolute;inset:0;z-index:0;
      background:url("data:image/png;base64,{b64}") center 30%/cover no-repeat;
      transform:scale(1.06);
      filter:brightness(.55) saturate(1.15);
      will-change:transform;
    }}
    .hero-grad{{
      position:absolute;inset:0;z-index:1;
      background:linear-gradient(130deg,rgba(3,18,3,.88) 0%,rgba(8,28,8,.62) 55%,rgba(18,45,10,.28) 100%);
    }}
    .hero-fade{{
      position:absolute;bottom:0;left:0;right:0;height:300px;z-index:2;
      background:linear-gradient(to top,var(--g900),transparent);
    }}
    .blob{{position:absolute;border-radius:50%;filter:blur(90px);z-index:1;pointer-events:none}}
    .b1{{width:550px;height:550px;top:-120px;right:-120px;
         background:radial-gradient(circle,rgba(65,176,65,.14) 0%,transparent 65%);
         animation:blobFloat 12s ease-in-out infinite}}
    .b2{{width:320px;height:320px;bottom:120px;right:28%;
         background:radial-gradient(circle,rgba(201,160,50,.09) 0%,transparent 65%);
         animation:blobFloat 15s ease-in-out infinite;animation-delay:5s}}
    .hero-body{{position:relative;z-index:3;max-width:800px}}
    .eyebrow{{
      display:inline-flex;align-items:center;gap:10px;
      background:rgba(65,176,65,.12);border:1px solid rgba(65,176,65,.35);
      border-radius:50px;padding:8px 20px;margin-bottom:30px;
      animation:slideUp .7s ease both .15s;
    }}
    .eyebrow-dot{{width:8px;height:8px;background:var(--g400);border-radius:50%;flex-shrink:0;animation:blink 2s ease-in-out infinite}}
    .eyebrow span{{font-size:.73rem;font-weight:700;color:var(--g300);letter-spacing:1.8px;text-transform:uppercase}}
    h1{{
      font-family:'Playfair Display',serif;
      font-size:clamp(3rem,6vw,5.2rem);font-weight:800;line-height:1.06;
      color:#fff;margin-bottom:26px;text-shadow:0 4px 30px rgba(0,0,0,.45);
      animation:slideUp .8s ease both .3s;
    }}
    h1 em{{
      font-style:normal;
      background:linear-gradient(120deg,#80e680,#d0faa0,#41b041);
      background-size:200% auto;
      -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
      animation:shimmer 4s linear infinite;
    }}
    .hero-desc{{
      font-size:clamp(1rem,1.55vw,1.12rem);line-height:1.8;
      color:rgba(255,255,255,.70);max-width:620px;margin-bottom:46px;
      animation:slideUp .8s ease both .45s;
    }}
    .hero-btns{{display:flex;align-items:center;gap:14px;flex-wrap:wrap;animation:slideUp .8s ease both .6s}}
    .btn-p{{
      display:inline-flex;align-items:center;gap:8px;
      background:linear-gradient(135deg,#287a26,#41b041);
      color:#fff;padding:14px 32px;border-radius:50px;
      font-weight:700;font-size:.93rem;text-decoration:none;
      box-shadow:0 8px 28px rgba(65,176,65,.35);transition:all .3s;
    }}
    .btn-p:hover{{transform:translateY(-3px);box-shadow:0 16px 40px rgba(65,176,65,.55)}}
    .btn-o{{
      display:inline-flex;align-items:center;gap:8px;
      background:transparent;border:1.5px solid rgba(255,255,255,.28);
      color:#fff;padding:14px 32px;border-radius:50px;
      font-weight:600;font-size:.93rem;text-decoration:none;
      transition:all .3s;backdrop-filter:blur(8px);
    }}
    .btn-o:hover{{border-color:rgba(255,255,255,.55);background:rgba(255,255,255,.08);transform:translateY(-3px)}}

    /* hero stats row */
    .hstats{{
      position:relative;z-index:3;display:flex;
      border-top:1px solid rgba(255,255,255,.09);
      border-bottom:1px solid rgba(255,255,255,.09);
      margin-top:72px;animation:fadeIn 1s ease both .9s;
    }}
    .hs{{flex:1;padding:26px 22px;border-right:1px solid rgba(255,255,255,.07);transition:background .3s}}
    .hs:last-child{{border-right:none}}
    .hs:hover{{background:rgba(255,255,255,.04)}}
    .hs-val{{font-family:'Playfair Display',serif;font-size:2.3rem;font-weight:800;color:var(--g300);line-height:1;margin-bottom:6px}}
    .hs-lbl{{font-size:.73rem;color:var(--w400);text-transform:uppercase;letter-spacing:1.3px;font-weight:500}}

    /* scroll mouse */
    .scroll-m{{
      position:absolute;bottom:38px;left:50%;transform:translateX(-50%);
      z-index:4;display:flex;flex-direction:column;align-items:center;gap:7px;
      animation:fadeIn 1s ease both 1.4s;
    }}
    .scroll-mouse{{width:22px;height:36px;border:2px solid rgba(255,255,255,.22);border-radius:11px;display:flex;justify-content:center;padding-top:6px}}
    .scroll-wheel{{width:3px;height:7px;background:rgba(255,255,255,.45);border-radius:2px;animation:wheel 1.8s ease-in-out infinite}}
    .scroll-txt{{font-size:.64rem;color:rgba(255,255,255,.28);letter-spacing:2px;text-transform:uppercase}}

    /* ── TRUST STRIP ── */
    .trust{{
      background:var(--g800);
      border-top:1px solid rgba(65,176,65,.13);border-bottom:1px solid rgba(65,176,65,.13);
      padding:18px 6%;display:flex;align-items:center;gap:36px;overflow:hidden;flex-wrap:wrap;
    }}
    .trust-lbl{{font-size:.7rem;color:var(--w400);text-transform:uppercase;letter-spacing:1.6px;white-space:nowrap;font-weight:600}}
    .trust-div{{width:1px;height:18px;background:rgba(255,255,255,.09);flex-shrink:0}}
    .trust-items{{display:flex;align-items:center;gap:36px;flex-wrap:wrap}}
    .trust-item{{font-size:.82rem;font-weight:700;color:rgba(255,255,255,.38);white-space:nowrap;transition:color .2s;cursor:default}}
    .trust-item:hover{{color:rgba(255,255,255,.72)}}

    /* ── SECTIONS ── */
    .sec{{padding:100px 6%}}
    .sec-alt{{padding:100px 6%;background:var(--g800)}}
    .sec-tag{{font-size:.7rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--g400);margin-bottom:12px;display:block}}
    h2.sec-h{{font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3rem);font-weight:800;color:#fff;line-height:1.15;margin-bottom:16px}}
    .sec-sub{{font-size:1rem;color:var(--w600);line-height:1.75;max-width:540px;margin-bottom:60px}}

    /* ── HOW IT WORKS ── */
    .steps{{display:grid;grid-template-columns:repeat(3,1fr);gap:26px}}
    .step{{
      background:rgba(255,255,255,.03);border:1px solid rgba(255,255,255,.07);
      border-radius:20px;padding:36px 28px;position:relative;overflow:hidden;transition:all .35s;
    }}
    .step::before{{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(65,176,65,.07),transparent 60%);opacity:0;transition:opacity .35s;border-radius:20px}}
    .step:hover{{border-color:rgba(65,176,65,.3);transform:translateY(-6px);box-shadow:0 24px 60px rgba(0,0,0,.25)}}
    .step:hover::before{{opacity:1}}
    .step-n{{font-family:'Playfair Display',serif;font-size:4.5rem;font-weight:800;color:rgba(65,176,65,.08);line-height:1;margin-bottom:18px}}
    .step-ico{{font-size:2rem;margin-bottom:14px;display:block}}
    .step-t{{font-size:1.02rem;font-weight:700;color:#fff;margin-bottom:9px}}
    .step-d{{font-size:.86rem;color:var(--w600);line-height:1.7}}

    /* ── FEATURE CARDS ── */
    .feat-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}}
    .fc{{
      background:rgba(255,255,255,.035);border:1px solid rgba(255,255,255,.07);
      border-radius:18px;padding:30px 24px;transition:all .35s;cursor:default;position:relative;overflow:hidden;
    }}
    .fc::after{{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(65,176,65,.06),transparent 60%);opacity:0;transition:opacity .35s;border-radius:18px}}
    .fc:hover{{border-color:rgba(65,176,65,.32);background:rgba(65,176,65,.04);transform:translateY(-5px);box-shadow:0 20px 50px rgba(0,0,0,.2)}}
    .fc:hover::after{{opacity:1}}
    .fc.wide{{grid-column:span 2;display:flex;gap:36px;align-items:flex-start}}
    .fc-icon{{
      width:50px;height:50px;border-radius:13px;
      display:flex;align-items:center;justify-content:center;
      font-size:1.45rem;margin-bottom:18px;flex-shrink:0;transition:transform .3s;
    }}
    .fc:hover .fc-icon{{transform:scale(1.1) rotate(-4deg)}}
    .fc.wide .fc-icon{{width:66px;height:66px;font-size:1.9rem;margin-bottom:0}}
    .ic-g{{background:rgba(65,176,65,.15)}}
    .ic-b{{background:rgba(65,150,220,.15)}}
    .ic-y{{background:rgba(201,160,50,.15)}}
    .fc-t{{font-size:1rem;font-weight:700;color:#fff;margin-bottom:9px}}
    .fc-d{{font-size:.845rem;color:var(--w600);line-height:1.65}}
    .fc-lnk{{
      display:inline-flex;align-items:center;gap:6px;margin-top:18px;
      font-size:.78rem;font-weight:600;color:var(--g400);text-decoration:none;transition:gap .2s;
    }}
    .fc-lnk:hover{{gap:10px}}
    .feat-hdr{{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:end;margin-bottom:60px}}

    /* ── BIG STATS ── */
    .bigstats{{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;position:relative;z-index:1}}
    .bs{{padding:50px 36px;border-right:1px solid rgba(255,255,255,.06);text-align:center;transition:background .3s}}
    .bs:last-child{{border-right:none}}
    .bs:hover{{background:rgba(255,255,255,.03)}}
    .bs-v{{font-family:'Playfair Display',serif;font-size:3.6rem;font-weight:800;color:var(--g300);line-height:1;margin-bottom:10px}}
    .bs-l{{font-size:.85rem;color:var(--w600);line-height:1.5}}
    .bs-s{{font-size:.7rem;color:var(--g400);font-weight:600;margin-top:4px;letter-spacing:.5px}}
    .bigstats-wrap{{position:relative;overflow:hidden}}
    .bigstats-wrap::before{{
      content:'';position:absolute;inset:0;
      background:radial-gradient(ellipse 80% 60% at 50% 50%,rgba(65,176,65,.07),transparent);
    }}

    /* ── DATA SOURCES ── */
    .data-grid{{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center}}
    .chips{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
    .chip{{
      background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);
      border-radius:14px;padding:22px 18px;transition:all .3s;
    }}
    .chip:hover{{border-color:rgba(65,176,65,.3);background:rgba(65,176,65,.05);transform:translateY(-3px)}}
    .chip-ico{{font-size:1.6rem;margin-bottom:10px}}
    .chip-n{{font-size:.88rem;font-weight:700;color:#fff;margin-bottom:5px}}
    .chip-d{{font-size:.74rem;color:var(--w400);line-height:1.55}}

    /* ── CTA ── */
    .cta-wrap{{
      max-width:760px;margin:0 auto;text-align:center;
      background:linear-gradient(145deg,rgba(255,255,255,.06),rgba(255,255,255,.02));
      border:1px solid rgba(255,255,255,.1);border-radius:28px;
      padding:72px 56px;backdrop-filter:blur(12px);position:relative;z-index:1;
    }}
    .cta-wrap h2{{font-family:'Playfair Display',serif;font-size:clamp(1.9rem,3.8vw,2.8rem);font-weight:800;color:#fff;line-height:1.2;margin-bottom:18px}}
    .cta-wrap p{{font-size:1rem;color:var(--w600);line-height:1.75;margin-bottom:42px}}
    .cta-btns{{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap}}
    .cta-sec{{position:relative;padding:100px 6%;overflow:hidden}}
    .cta-sec::before{{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 70% 70% at 50% 50%,rgba(65,176,65,.09),transparent)}}

    /* ── FOOTER ── */
    footer{{background:#020902;border-top:1px solid rgba(255,255,255,.05);padding:60px 6% 36px}}
    .footer-grid{{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:56px;margin-bottom:48px}}
    .footer-brand p{{font-size:.875rem;color:var(--w400);line-height:1.8;margin-top:14px;max-width:290px}}
    .fc-col h4{{font-size:.75rem;font-weight:700;color:rgba(255,255,255,.4);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:16px}}
    .fc-col ul{{list-style:none}}
    .fc-col ul li{{margin-bottom:9px}}
    .fc-col ul li a{{font-size:.875rem;color:var(--w400);text-decoration:none;transition:color .2s}}
    .fc-col ul li a:hover{{color:#fff}}
    .footer-bottom{{display:flex;align-items:center;justify-content:space-between;padding-top:26px;border-top:1px solid rgba(255,255,255,.05)}}
    .footer-bottom p{{font-size:.78rem;color:var(--w400)}}
    .ftags{{display:flex;gap:8px;flex-wrap:wrap}}
    .ftag{{font-size:.68rem;padding:4px 12px;border-radius:20px;background:rgba(65,176,65,.1);border:1px solid rgba(65,176,65,.2);color:var(--g400);font-weight:600;letter-spacing:.3px}}

    /* ── REVEAL ── */
    .reveal{{opacity:0;transform:translateY(28px);transition:opacity .65s ease,transform .65s ease}}
    .reveal.visible{{opacity:1;transform:translateY(0)}}
    .reveal-d1{{transition-delay:.1s}}.reveal-d2{{transition-delay:.2s}}.reveal-d3{{transition-delay:.3s}}

    /* ── ANIMATIONS ── */
    @keyframes slideUp{{from{{opacity:0;transform:translateY(36px)}}to{{opacity:1;transform:translateY(0)}}}}
    @keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
    @keyframes shimmer{{0%{{background-position:0% center}}100%{{background-position:200% center}}}}
    @keyframes blink{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.55;transform:scale(.82)}}}}
    @keyframes blobFloat{{0%,100%{{transform:translateY(0) scale(1)}}50%{{transform:translateY(-28px) scale(1.04)}}}}
    @keyframes wheel{{0%{{opacity:1;transform:translateY(0)}}100%{{opacity:0;transform:translateY(12px)}}}}

    /* ── RESPONSIVE ── */
    @media(max-width:900px){{
      .steps,.feat-grid,.bigstats,.data-grid,.footer-grid{{grid-template-columns:1fr}}
      .fc.wide{{grid-column:span 1;flex-direction:column}}
      .feat-hdr{{grid-template-columns:1fr}}
      .hstats{{flex-wrap:wrap}}
      .hs{{flex:none;width:50%}}
      .nav-links{{display:none}}
    }}
  </style>
</head>
<body>

<!-- NAV -->
<nav id="nav">
  <a href="#" class="nav-brand">
    <div class="nav-icon">🌾</div>
    <div class="nav-text"><strong>TN Crop Advisory</strong><span>Tamil Nadu · AI Platform</span></div>
  </a>
  <ul class="nav-links">
    <li><a href="#features">Features</a></li>
    <li><a href="#how">How It Works</a></li>
    <li><a href="#data">Data</a></li>
    <li><a href="#stats">Impact</a></li>
    <li><a href="https://share.streamlit.io" target="_blank" class="nav-cta">Open Dashboard →</a></li>
  </ul>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-bg" id="heroBg"></div>
  <div class="hero-grad"></div>
  <div class="hero-fade"></div>
  <div class="blob b1"></div>
  <div class="blob b2"></div>

  <div class="hero-body">
    <div class="eyebrow">
      <div class="eyebrow-dot"></div>
      <span>AI-Powered Agricultural Intelligence</span>
    </div>
    <h1>Tamil Nadu<br><em>Crop Yield</em><br>Advisory System</h1>
    <p class="hero-desc">
      Harness 20 years of NASA climate, soil health, and satellite data to predict 
      district-level crop yields — powered by XGBoost and explained transparently 
      with SHAP. Built for agricultural officers and researchers.
    </p>
    <div class="hero-btns">
      <a href="https://share.streamlit.io" target="_blank" class="btn-p">🔮 &nbsp;Open Dashboard</a>
      <a href="#how" class="btn-o">▶ &nbsp;See how it works</a>
    </div>
  </div>

  <div class="hstats">
    <div class="hs"><div class="hs-val">38</div><div class="hs-lbl">Districts Covered</div></div>
    <div class="hs"><div class="hs-val">6</div><div class="hs-lbl">Major Crops</div></div>
    <div class="hs"><div class="hs-val">21</div><div class="hs-lbl">Years of Data</div></div>
    <div class="hs"><div class="hs-val">4</div><div class="hs-lbl">ML Models</div></div>
    <div class="hs"><div class="hs-val">SHAP</div><div class="hs-lbl">Explainability</div></div>
  </div>

  <div class="scroll-m">
    <div class="scroll-mouse"><div class="scroll-wheel"></div></div>
    <div class="scroll-txt">Scroll</div>
  </div>
</section>

<!-- TRUST -->
<div class="trust">
  <span class="trust-lbl">Powered by</span>
  <div class="trust-div"></div>
  <div class="trust-items">
    <span class="trust-item">🛰 NASA POWER API</span>
    <span class="trust-item">🌱 Soil Health Card Portal</span>
    <span class="trust-item">⚡ XGBoost</span>
    <span class="trust-item">🔍 SHAP Explainability</span>
    <span class="trust-item">🧠 LSTM Neural Network</span>
    <span class="trust-item">📊 Random Forest</span>
    <span class="trust-item">📈 Statsmodels</span>
  </div>
</div>

<!-- HOW IT WORKS -->
<section class="sec" id="how">
  <div class="reveal">
    <span class="sec-tag">✦ &nbsp;How it works</span>
    <h2 class="sec-h">From raw data to<br>actionable decisions</h2>
    <p class="sec-sub">Three simple steps turn 20 years of climate and soil records into a personalised advisory report for any district in Tamil Nadu.</p>
  </div>
  <div class="steps">
    <div class="step reveal reveal-d1">
      <div class="step-n">01</div>
      <span class="step-ico">📍</span>
      <div class="step-t">Select District &amp; Crop</div>
      <div class="step-d">Choose any of the 38 Tamil Nadu districts, select your crop — Paddy, Sugarcane, Groundnut, Cotton, Maize, or Ragi — and specify the growing season.</div>
    </div>
    <div class="step reveal reveal-d2">
      <div class="step-n">02</div>
      <span class="step-ico">🤖</span>
      <div class="step-t">AI Predicts Yield</div>
      <div class="step-d">Our XGBoost model — trained on 20+ years of NASA climate, soil pH, organic matter, and historical yield data — generates an accurate t/ha prediction in milliseconds.</div>
    </div>
    <div class="step reveal reveal-d3">
      <div class="step-n">03</div>
      <span class="step-ico">📋</span>
      <div class="step-t">Download Advisory</div>
      <div class="step-d">Get a print-ready PDF report with SHAP factor charts, comparative district analysis, risk flags, and targeted soil and irrigation recommendations.</div>
    </div>
  </div>
</section>

<!-- FEATURES -->
<section class="sec-alt" id="features">
  <div class="feat-hdr reveal">
    <div>
      <span class="sec-tag">✦ &nbsp;Platform Features</span>
      <h2 class="sec-h">A complete intelligence<br>toolkit for agriculture</h2>
    </div>
    <p class="sec-sub" style="margin-bottom:0">Everything agricultural officers and researchers need — from interactive maps to downloadable PDF reports — in one unified platform.</p>
  </div>
  <div class="feat-grid">
    <div class="fc wide reveal">
      <div class="fc-icon ic-g">🔮</div>
      <div>
        <div class="fc-t">Yield Prediction Engine</div>
        <div class="fc-d">Select any district, crop, and season to get an XGBoost-powered yield forecast. SHAP waterfall charts reveal exactly which climate and soil factors are driving the prediction — full transparency, no black box.</div>
        <a href="https://share.streamlit.io" target="_blank" class="fc-lnk">Open Predictor →</a>
      </div>
    </div>
    <div class="fc reveal reveal-d1">
      <div class="fc-icon ic-b">🗺️</div>
      <div class="fc-t">Interactive Heatmap</div>
      <div class="fc-d">Visualise predicted yield potential across all 38 TN districts on an interactive Folium map. Identify high-yield zones instantly.</div>
      <a href="https://share.streamlit.io" target="_blank" class="fc-lnk">View Map →</a>
    </div>
    <div class="fc reveal reveal-d2">
      <div class="fc-icon ic-y">📋</div>
      <div class="fc-t">PDF Advisory Reports</div>
      <div class="fc-d">Download a personalised, print-ready PDF with predictions, SHAP charts, risk flags, and a targeted action plan for your district.</div>
      <a href="https://share.streamlit.io" target="_blank" class="fc-lnk">Generate Report →</a>
    </div>
    <div class="fc reveal reveal-d1">
      <div class="fc-icon ic-g">📈</div>
      <div class="fc-t">20-Year Trend Explorer</div>
      <div class="fc-d">Drill into two decades of yield, rainfall, temperature, and soil data with fully interactive Plotly charts and filters.</div>
      <a href="https://share.streamlit.io" target="_blank" class="fc-lnk">Explore Trends →</a>
    </div>
    <div class="fc reveal reveal-d2">
      <div class="fc-icon ic-b">⚖️</div>
      <div class="fc-t">Crop &amp; District Comparator</div>
      <div class="fc-d">Side-by-side comparison with radar charts, violin plots, and bump charts across multiple districts and crop varieties.</div>
      <a href="https://share.streamlit.io" target="_blank" class="fc-lnk">Compare Now →</a>
    </div>
  </div>
</section>

<!-- BIG STATS -->
<section class="sec bigstats-wrap" id="stats">
  <div class="reveal" style="text-align:center;margin-bottom:60px">
    <span class="sec-tag">✦ &nbsp;By the numbers</span>
    <h2 class="sec-h">Built on two decades<br>of real field data</h2>
  </div>
  <div class="bigstats reveal">
    <div class="bs"><div class="bs-v">38</div><div class="bs-l">Districts<br>Covered</div><div class="bs-s">All of Tamil Nadu</div></div>
    <div class="bs"><div class="bs-v">21</div><div class="bs-l">Years of<br>Data</div><div class="bs-s">2003 – 2023</div></div>
    <div class="bs"><div class="bs-v">4</div><div class="bs-l">ML Models<br>Compared</div><div class="bs-s">LR · RF · XGB · LSTM</div></div>
    <div class="bs"><div class="bs-v">6</div><div class="bs-l">Major<br>Crops</div><div class="bs-s">Paddy to Maize</div></div>
  </div>
</section>

<!-- DATA SOURCES -->
<section class="sec-alt" id="data">
  <div class="data-grid">
    <div class="reveal">
      <span class="sec-tag">✦ &nbsp;Data Sources</span>
      <h2 class="sec-h">Grounded in verified,<br>scientific data</h2>
      <p class="sec-sub" style="margin-bottom:34px">Every prediction is backed by authoritative climate, soil, and agricultural yield datasets — ensuring reliability for real-world farming decisions.</p>
      <a href="https://share.streamlit.io" target="_blank" class="btn-p" style="display:inline-flex">Explore the Data →</a>
    </div>
    <div class="chips reveal reveal-d1">
      <div class="chip">
        <div class="chip-ico">🛰️</div>
        <div class="chip-n">NASA POWER API</div>
        <div class="chip-d">Daily climate parameters — rainfall, temperature, solar radiation — at district level resolution.</div>
      </div>
      <div class="chip">
        <div class="chip-ico">🌱</div>
        <div class="chip-n">Soil Health Card Portal</div>
        <div class="chip-d">District-level soil pH, organic carbon, nitrogen, phosphorus, and potassium values.</div>
      </div>
      <div class="chip">
        <div class="chip-ico">🌾</div>
        <div class="chip-n">TN Agriculture Dept.</div>
        <div class="chip-d">Historical crop yield records from the Tamil Nadu Agriculture Department's official portal.</div>
      </div>
      <div class="chip">
        <div class="chip-ico">🔬</div>
        <div class="chip-n">Feature Engineering</div>
        <div class="chip-d">30+ engineered features — GDD, aridity index, drought indicators, and composite soil scores.</div>
      </div>
    </div>
  </div>
</section>

<!-- CTA -->
<section class="cta-sec">
  <div class="cta-wrap reveal">
    <h2>Ready to make smarter<br>farming decisions?</h2>
    <p>Open the live dashboard and get your first yield prediction in under 60 seconds. No sign-up needed.</p>
    <div class="cta-btns">
      <a href="https://share.streamlit.io" target="_blank" class="btn-p">🚀 &nbsp;Launch Dashboard</a>
      <a href="#features" class="btn-o">Learn more →</a>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="footer-grid">
    <div class="footer-brand">
      <a href="#" class="nav-brand"><div class="nav-icon">🌾</div><div class="nav-text"><strong>TN Crop Advisory</strong><span>Tamil Nadu · AI Platform</span></div></a>
      <p>An AI-powered crop yield advisory platform for Tamil Nadu, built on open scientific data and modern machine learning.</p>
    </div>
    <div class="fc-col">
      <h4>Platform</h4>
      <ul>
        <li><a href="https://share.streamlit.io" target="_blank">Yield Predictor</a></li>
        <li><a href="https://share.streamlit.io" target="_blank">District Heatmap</a></li>
        <li><a href="https://share.streamlit.io" target="_blank">Trend Explorer</a></li>
        <li><a href="https://share.streamlit.io" target="_blank">Comparator</a></li>
        <li><a href="https://share.streamlit.io" target="_blank">PDF Reports</a></li>
      </ul>
    </div>
    <div class="fc-col">
      <h4>Technology</h4>
      <ul>
        <li><a href="#">XGBoost</a></li>
        <li><a href="#">SHAP Analysis</a></li>
        <li><a href="#">LSTM Network</a></li>
        <li><a href="#">Random Forest</a></li>
        <li><a href="#">Statsmodels</a></li>
      </ul>
    </div>
    <div class="fc-col">
      <h4>Data Sources</h4>
      <ul>
        <li><a href="#">NASA POWER API</a></li>
        <li><a href="#">Soil Health Card</a></li>
        <li><a href="#">TN Agri Dept.</a></li>
        <li><a href="#">Feature Engineering</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2024 TN Crop Advisory System &nbsp;·&nbsp; Tamil Nadu, India &nbsp;·&nbsp; Data: 2003–2023</p>
    <div class="ftags">
      <span class="ftag">XGBoost</span><span class="ftag">SHAP</span>
      <span class="ftag">LSTM</span><span class="ftag">Streamlit</span>
      <span class="ftag">NASA POWER</span><span class="ftag">Open Source</span>
    </div>
  </div>
</footer>

<script>
  // Navbar scroll
  const nav = document.getElementById('nav');
  window.addEventListener('scroll', () => nav.classList.toggle('scrolled', scrollY > 55), {{passive:true}});

  // Parallax
  const bg = document.getElementById('heroBg');
  window.addEventListener('scroll', () => {{
    bg.style.transform = `scale(1.06) translateY(${{scrollY * 0.22}}px)`;
  }}, {{passive:true}});

  // Reveal
  const els = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver(entries => {{
    entries.forEach(e => {{
      if(e.isIntersecting){{ e.target.classList.add('visible'); io.unobserve(e.target); }}
    }});
  }}, {{threshold:0.1}});
  els.forEach(e => io.observe(e));

  // Smooth anchors
  document.querySelectorAll('a[href^="#"]').forEach(a => {{
    a.addEventListener('click', e => {{
      const t = document.querySelector(a.getAttribute('href'));
      if(t){{ e.preventDefault(); t.scrollIntoView({{behavior:'smooth'}}); }}
    }});
  }});
</script>
</body>
</html>"""

out = ROOT / "index.html"
out.write_text(HTML, encoding="utf-8")
print(f"Written {len(HTML):,} bytes to {out}")
