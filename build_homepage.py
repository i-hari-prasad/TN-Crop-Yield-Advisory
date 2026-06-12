b64 = open('app/hero_web.b64', encoding='utf-8').read().strip()

template = """<!DOCTYPE html>
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
    *,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
    :root{
      --g900:#031203;--g800:#0b2010;--g700:#163a18;--g500:#287a26;--g400:#41b041;
      --g300:#72d472;--g100:#c5f0c5;--gold:#c9a032;
      --w60:rgba(255,255,255,0.60);--w80:rgba(255,255,255,0.80);
    }
    html{scroll-behavior:smooth}
    body{font-family:'Inter',sans-serif;background:#031203;color:#fff;overflow-x:hidden}

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar{width:4px}
    ::-webkit-scrollbar-track{background:var(--g900)}
    ::-webkit-scrollbar-thumb{background:var(--g500);border-radius:3px}

    /* ══════════ NAV ══════════ */
    nav{
      position:fixed;top:0;left:0;right:0;z-index:200;
      display:flex;align-items:center;justify-content:space-between;
      padding:0 5%;height:64px;
      background:rgba(3,18,3,0.45);
      backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
      border-bottom:1px solid rgba(255,255,255,0.06);
      transition:background .3s;
    }
    nav.scrolled{background:rgba(3,18,3,0.95)}

    .nav-brand{display:flex;align-items:center;gap:9px;text-decoration:none}
    .nav-icon{
      width:32px;height:32px;border-radius:8px;
      background:linear-gradient(135deg,var(--g500),var(--g400));
      display:flex;align-items:center;justify-content:center;
      font-size:.95rem;box-shadow:0 4px 12px rgba(65,176,65,.3);flex-shrink:0;
    }
    .nav-text strong{font-size:.88rem;font-weight:700;display:block;line-height:1.1;color:#fff}
    .nav-text span{font-size:.6rem;color:var(--g300);letter-spacing:1.5px;text-transform:uppercase;font-weight:600}

    .nav-links{display:flex;align-items:center;gap:28px;list-style:none}
    .nav-links a{text-decoration:none;color:rgba(255,255,255,.65);font-size:.86rem;font-weight:500;transition:color .2s;letter-spacing:.2px}
    .nav-links a:hover{color:#fff}

    .nav-cta{
      background:var(--g500)!important;color:#fff!important;
      padding:8px 20px;border-radius:50px;font-weight:700!important;font-size:.84rem;
      box-shadow:0 4px 16px rgba(65,176,65,.3);
      transition:all .25s!important;letter-spacing:.3px;
    }
    .nav-cta:hover{background:var(--g400)!important;transform:translateY(-1px);box-shadow:0 8px 24px rgba(65,176,65,.45)!important}

    /* ══════════ HERO ══════════ */
    .hero{
      position:relative;height:100vh;min-height:640px;
      display:flex;flex-direction:column;justify-content:center;
      padding:0 5%;overflow:hidden;
    }

    /* Background image */
    .hero-bg{
      position:absolute;inset:0;z-index:0;
      background:url("data:image/png;base64,BG_PLACEHOLDER") center/cover no-repeat;
    }
    /* Dark overlay to match screenshot */
    .hero-overlay{
      position:absolute;inset:0;z-index:1;
      background:linear-gradient(
        100deg,
        rgba(2,10,2,0.80) 0%,
        rgba(4,18,4,0.72) 45%,
        rgba(2,12,2,0.35) 100%
      );
    }

    .hero-content{
      position:relative;z-index:2;
      max-width:580px;
    }

    /* ── Badge ── */
    .hero-badge{
      display:inline-flex;align-items:center;gap:7px;
      border:1px solid rgba(65,176,65,0.45);
      border-radius:50px;padding:5px 14px;margin-bottom:28px;
    }
    .badge-dot{
      width:6px;height:6px;background:var(--g400);border-radius:50%;
      box-shadow:0 0 6px rgba(65,176,65,.8);
      animation:pulse 2s ease-in-out infinite;
    }
    .hero-badge span{
      font-size:.68rem;font-weight:700;color:var(--g300);
      letter-spacing:2px;text-transform:uppercase;
    }
    @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(1.5)}}

    /* ── Headline ── */
    .hero-title{
      font-family:'Playfair Display',serif;
      font-size:3.6rem;font-weight:800;line-height:1.08;
      margin-bottom:22px;color:#fff;
      text-shadow:0 2px 24px rgba(0,0,0,.5);
    }
    .hero-title .accent{
      color:var(--g300);
      text-shadow:0 0 32px rgba(65,176,65,.4);
    }

    /* ── Description ── */
    .hero-desc{
      font-size:1rem;line-height:1.78;
      color:rgba(255,255,255,.72);
      max-width:480px;margin-bottom:38px;
      font-weight:400;
    }

    /* ── CTA buttons ── */
    .hero-ctas{display:flex;align-items:center;gap:14px;flex-wrap:wrap}

    .btn-primary{
      display:inline-flex;align-items:center;gap:8px;
      background:var(--g500);color:#fff;
      padding:13px 28px;border-radius:50px;border:none;
      font-weight:700;font-size:.92rem;cursor:pointer;text-decoration:none;
      box-shadow:0 6px 24px rgba(65,176,65,.38);
      transition:all .25s;letter-spacing:.2px;
    }
    .btn-primary:hover{
      background:var(--g400);transform:translateY(-2px);
      box-shadow:0 10px 32px rgba(65,176,65,.55);
    }
    .btn-primary svg,.btn-primary .icon{font-size:1rem}

    .btn-secondary{
      display:inline-flex;align-items:center;gap:8px;
      background:rgba(255,255,255,0.06);color:#fff;
      padding:13px 28px;border-radius:50px;
      border:1px solid rgba(255,255,255,0.22);
      font-weight:600;font-size:.92rem;cursor:pointer;text-decoration:none;
      backdrop-filter:blur(8px);
      transition:all .25s;letter-spacing:.2px;
    }
    .btn-secondary:hover{
      background:rgba(255,255,255,0.12);
      border-color:rgba(255,255,255,0.4);
      transform:translateY(-2px);
    }

    /* ══════════ STATS BAR (bottom of hero) ══════════ */
    .hero-stats{
      position:absolute;bottom:0;left:0;right:0;z-index:2;
      display:flex;align-items:stretch;
      background:rgba(3,18,3,0.70);
      backdrop-filter:blur(16px);
      border-top:1px solid rgba(65,176,65,0.12);
    }
    .stat-item{
      flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;
      padding:20px 16px;
      border-right:1px solid rgba(255,255,255,0.06);
      transition:background .2s;
    }
    .stat-item:last-child{border-right:none}
    .stat-item:hover{background:rgba(65,176,65,0.06)}
    .stat-num{font-size:1.6rem;font-weight:800;color:var(--g300);line-height:1}
    .stat-label{font-size:.72rem;color:rgba(255,255,255,.5);margin-top:5px;
                letter-spacing:.8px;text-transform:uppercase;font-weight:500}

    /* ══════════ FEATURES SECTION ══════════ */
    .features{
      background:linear-gradient(180deg, #041504 0%, #071a07 100%);
      padding:90px 5%;
    }
    .section-tag{
      display:inline-flex;align-items:center;gap:6px;
      background:rgba(65,176,65,.08);border:1px solid rgba(65,176,65,.2);
      border-radius:50px;padding:5px 14px;margin-bottom:16px;
      font-size:.7rem;font-weight:700;color:var(--g300);
      letter-spacing:1.8px;text-transform:uppercase;
    }
    .section-title{font-size:2.2rem;font-weight:800;line-height:1.15;margin-bottom:12px}
    .section-sub{font-size:1rem;color:rgba(255,255,255,.5);max-width:520px;line-height:1.7}

    .features-grid{
      display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
      gap:24px;margin-top:52px;
    }
    .feat-card{
      background:rgba(255,255,255,.03);
      border:1px solid rgba(255,255,255,.07);
      border-radius:20px;padding:32px 28px;
      transition:all .3s;
    }
    .feat-card:hover{
      background:rgba(65,176,65,.06);
      border-color:rgba(65,176,65,.2);
      transform:translateY(-4px);
      box-shadow:0 16px 48px rgba(0,0,0,.3);
    }
    .feat-icon{
      width:52px;height:52px;border-radius:14px;
      display:flex;align-items:center;justify-content:center;
      font-size:1.5rem;margin-bottom:18px;
    }
    .feat-card h3{font-size:1.05rem;font-weight:700;margin-bottom:10px;color:#fff}
    .feat-card p{font-size:.87rem;color:rgba(255,255,255,.5);line-height:1.65}

    /* ══════════ HOW IT WORKS ══════════ */
    .how-it-works{padding:90px 5%;background:#031203}
    .steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px;margin-top:52px}
    .step{text-align:center}
    .step-num{
      width:52px;height:52px;border-radius:50%;
      background:linear-gradient(135deg,var(--g700),var(--g500));
      display:flex;align-items:center;justify-content:center;
      font-size:1.1rem;font-weight:800;margin:0 auto 16px;
      box-shadow:0 4px 18px rgba(65,176,65,.25);
    }
    .step h3{font-size:.98rem;font-weight:700;margin-bottom:8px}
    .step p{font-size:.84rem;color:rgba(255,255,255,.48);line-height:1.6}

    /* ══════════ DATA SOURCES ══════════ */
    .data-sources{
      padding:80px 5%;
      background:linear-gradient(180deg,#071a07 0%,#031203 100%);
    }
    .sources-grid{display:flex;flex-wrap:wrap;gap:16px;margin-top:48px;justify-content:center}
    .source-pill{
      display:flex;align-items:center;gap:10px;
      background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.09);
      border-radius:50px;padding:12px 22px;
      font-size:.88rem;font-weight:600;color:rgba(255,255,255,.75);
      transition:all .25s;
    }
    .source-pill:hover{background:rgba(65,176,65,.08);border-color:rgba(65,176,65,.25);color:#fff}
    .source-pill .dot{width:8px;height:8px;border-radius:50%}

    /* ══════════ FOOTER ══════════ */
    footer{
      background:#020d02;border-top:1px solid rgba(255,255,255,.06);
      padding:36px 5%;display:flex;align-items:center;justify-content:space-between;
      flex-wrap:wrap;gap:16px;
    }
    footer .brand{display:flex;align-items:center;gap:8px;text-decoration:none}
    footer .brand strong{font-size:.87rem;font-weight:700;color:#fff}
    footer .brand span{font-size:.65rem;color:var(--g300);letter-spacing:1.2px;text-transform:uppercase}
    footer p{font-size:.75rem;color:rgba(255,255,255,.28);line-height:1.8}

    /* ══════════ RESPONSIVE ══════════ */
    @media(max-width:768px){
      .nav-links{display:none}
      .hero-title{font-size:2.6rem}
      .hero-stats{flex-wrap:wrap}
      .stat-item{min-width:50%;border-bottom:1px solid rgba(255,255,255,.06)}
    }
  </style>
</head>
<body>

<!-- ═══════════ NAV ═══════════ -->
<nav id="navbar">
  <a class="nav-brand" href="#">
    <div class="nav-icon">🌾</div>
    <div class="nav-text">
      <strong>TN Crop Advisory</strong>
      <span>Tamil Nadu · AI Platform</span>
    </div>
  </a>
  <ul class="nav-links">
    <li><a href="#features">Features</a></li>
    <li><a href="#how-it-works">How it Works</a></li>
    <li><a href="#data-sources">Data Sources</a></li>
    <li><a href="http://localhost:8501" class="nav-cta">Open Dashboard &rarr;</a></li>
  </ul>
</nav>

<!-- ═══════════ HERO ═══════════ -->
<section class="hero" id="home">
  <div class="hero-bg"></div>
  <div class="hero-overlay"></div>

  <div class="hero-content">
    <!-- Badge -->
    <div class="hero-badge">
      <div class="badge-dot"></div>
      <span>AI-Powered Agricultural Intelligence</span>
    </div>

    <!-- Headline -->
    <h1 class="hero-title">
      Tamil Nadu<br>
      <span class="accent">Crop Yield</span><br>
      Advisory System
    </h1>

    <!-- Description -->
    <p class="hero-desc">
      Harness 20 years of NASA climate, soil health, and satellite data to
      predict district-level crop yields — powered by XGBoost and
      explained transparently with SHAP. Built for agricultural officers and
      researchers.
    </p>

    <!-- CTAs -->
    <div class="hero-ctas">
      <a href="http://localhost:8501" class="btn-primary">
        <span>🌾</span> Open Dashboard
      </a>
      <a href="#how-it-works" class="btn-secondary">
        <span>▶</span> See how it works
      </a>
    </div>
  </div>

  <!-- Stats bar -->
  <div class="hero-stats">
    <div class="stat-item">
      <div class="stat-num">38</div>
      <div class="stat-label">Districts</div>
    </div>
    <div class="stat-item">
      <div class="stat-num">6</div>
      <div class="stat-label">Crop Types</div>
    </div>
    <div class="stat-item">
      <div class="stat-num">20<small style="font-size:.9rem">yr</small></div>
      <div class="stat-label">Climate Data</div>
    </div>
    <div class="stat-item">
      <div class="stat-num">4</div>
      <div class="stat-label">ML Models</div>
    </div>
    <div class="stat-item">
      <div class="stat-num">98<small style="font-size:.9rem">%</small></div>
      <div class="stat-label">Accuracy</div>
    </div>
  </div>
</section>

<!-- ═══════════ FEATURES ═══════════ -->
<section class="features" id="features">
  <div style="max-width:760px">
    <div class="section-tag">⚡ Platform Features</div>
    <h2 class="section-title">Everything You Need for<br>Smart Crop Planning</h2>
    <p class="section-sub">A complete intelligence platform combining machine learning, satellite data, and geospatial analysis.</p>
  </div>
  <div class="features-grid">
    <div class="feat-card">
      <div class="feat-icon" style="background:rgba(65,176,65,.12)">🔮</div>
      <h3>Yield Prediction</h3>
      <p>Select any district, crop, and season to get instant XGBoost-powered yield forecasts with confidence intervals.</p>
    </div>
    <div class="feat-card">
      <div class="feat-icon" style="background:rgba(74,150,220,.12)">🧠</div>
      <h3>SHAP Explainability</h3>
      <p>Understand exactly which climate and soil factors drove each prediction with interactive SHAP waterfall charts.</p>
    </div>
    <div class="feat-card">
      <div class="feat-icon" style="background:rgba(201,160,50,.12)">🗺️</div>
      <h3>Geospatial Heatmap</h3>
      <p>Visualize predicted yield potential across all 38 Tamil Nadu districts on an interactive Folium map.</p>
    </div>
    <div class="feat-card">
      <div class="feat-icon" style="background:rgba(180,80,80,.12)">📋</div>
      <h3>Advisory PDF Reports</h3>
      <p>Download personalised agricultural advisory reports with actionable recommendations tailored to your district.</p>
    </div>
    <div class="feat-card">
      <div class="feat-icon" style="background:rgba(65,176,65,.12)">📈</div>
      <h3>Historical Trends</h3>
      <p>Explore 20 years of yield, rainfall, temperature, and soil health data with rich interactive visualizations.</p>
    </div>
    <div class="feat-card">
      <div class="feat-icon" style="background:rgba(74,150,220,.12)">⚖️</div>
      <h3>District Comparison</h3>
      <p>Side-by-side comparison of districts and crops using radar, violin, and bump charts for deep insights.</p>
    </div>
  </div>
</section>

<!-- ═══════════ HOW IT WORKS ═══════════ -->
<section class="how-it-works" id="how-it-works">
  <div style="max-width:760px">
    <div class="section-tag">🔄 Workflow</div>
    <h2 class="section-title">How It Works</h2>
    <p class="section-sub">From raw climate data to actionable advisory reports in four simple steps.</p>
  </div>
  <div class="steps">
    <div class="step">
      <div class="step-num">1</div>
      <h3>Data Ingestion</h3>
      <p>20 years of NASA POWER climate data, IMD rainfall records, and Soil Health Card portal data are ingested and cleaned.</p>
    </div>
    <div class="step">
      <div class="step-num">2</div>
      <h3>Feature Engineering</h3>
      <p>200+ features are engineered including lag variables, rolling averages, and interaction terms for soil-climate relationships.</p>
    </div>
    <div class="step">
      <div class="step-num">3</div>
      <h3>ML Prediction</h3>
      <p>XGBoost, Random Forest, LSTM, and Linear Regression models are trained and ensembled for robust yield forecasts.</p>
    </div>
    <div class="step">
      <div class="step-num">4</div>
      <h3>SHAP Explanation</h3>
      <p>SHAP values decompose each prediction, revealing which factors matter most for each specific district and crop.</p>
    </div>
  </div>
</section>

<!-- ═══════════ DATA SOURCES ═══════════ -->
<section class="data-sources" id="data-sources">
  <div style="max-width:760px">
    <div class="section-tag">🛰️ Data Sources</div>
    <h2 class="section-title">Powered by Authoritative Data</h2>
    <p class="section-sub">Every prediction is grounded in verified, high-quality datasets from trusted government and scientific sources.</p>
  </div>
  <div class="sources-grid">
    <div class="source-pill"><span class="dot" style="background:#4a96dc"></span>NASA POWER Climate Data</div>
    <div class="source-pill"><span class="dot" style="background:#72d472"></span>Soil Health Card Portal</div>
    <div class="source-pill"><span class="dot" style="background:#c9a032"></span>IMD Rainfall Records</div>
    <div class="source-pill"><span class="dot" style="background:#72d472"></span>TN Agriculture Department</div>
    <div class="source-pill"><span class="dot" style="background:#e88a8a"></span>ISRO Satellite Imagery</div>
    <div class="source-pill"><span class="dot" style="background:#4a96dc"></span>District Census Data</div>
  </div>
</section>

<!-- ═══════════ FOOTER ═══════════ -->
<footer>
  <a class="brand" href="#">
    <div class="nav-icon" style="width:28px;height:28px;font-size:.8rem">🌾</div>
    <div>
      <strong>TN Crop Advisory System</strong>
      <div style="font-size:.62rem;color:var(--g300);letter-spacing:1.2px;text-transform:uppercase;margin-top:1px">Tamil Nadu · AI Platform</div>
    </div>
  </a>
  <p>Data: NASA POWER &nbsp;·&nbsp; Soil Health Card Portal &nbsp;·&nbsp; IMD<br>ML Stack: XGBoost &nbsp;·&nbsp; SHAP &nbsp;·&nbsp; LSTM &nbsp;·&nbsp; Random Forest</p>
  <a href="http://localhost:8501" class="btn-primary" style="font-size:.82rem;padding:10px 22px">
    Launch Dashboard &rarr;
  </a>
</footer>

<script>
  // Nav scroll effect
  const nav = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if(target){ e.preventDefault(); target.scrollIntoView({behavior:'smooth'}); }
    });
  });
</script>
</body>
</html>"""

# Inject background image
html = template.replace('BG_PLACEHOLDER', b64)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Written index.html, size:', len(html))
