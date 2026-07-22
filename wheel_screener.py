"""
Wheel & Covered Call live screener — v2.

- Ticker universe & thresholds live in universe.json (auto-created on first run).
- Groups tickers by industry (Helium & Semi combined, Photonics separate, etc.).
- Portfolio ETFs and 'existing holdings you want to exit' are kept as their own
  groups so you can watch them alongside the wheel candidates.
- Auto-prunes any ticker that breaches thresholds (price too high, wheel score
  too low) for N consecutive runs. Strike counts persist in strikes.json.
- CLI:
      python wheel_screener.py              # normal run
      python wheel_screener.py --add NVDA:Helium & Semiconductor
      python wheel_screener.py --remove BULL
      python wheel_screener.py --no-prune   # skip auto-prune this run
      python wheel_screener.py --reset-strikes
      python wheel_screener.py --open       # open dashboard when done
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import webbrowser
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    sys.exit("Missing dependency. Run:  pip install yfinance pandas numpy")

# Corporate-proxy SSL workaround
_YF_SESSION = None
try:
    from curl_cffi import requests as _curl_requests  # type: ignore
    try:
        _YF_SESSION = _curl_requests.Session(impersonate="chrome")
        _YF_SESSION.get("https://finance.yahoo.com", timeout=5)
    except Exception:
        _YF_SESSION = _curl_requests.Session(impersonate="chrome", verify=False)
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        print("[warn] SSL verification disabled for yfinance (corporate proxy detected).")
except Exception:
    pass


HERE = Path(__file__).parent
UNIVERSE_FILE = HERE / "universe.json"
STRIKES_FILE = HERE / "strikes.json"
CSV_FILE = HERE / "wheel_snapshot.csv"
HTML_FILE = HERE / "Wheel_Dashboard.html"

TARGET_DTE_MIN = 25
TARGET_DTE_MAX = 50
FALLBACK_DTE_MIN = 15
FALLBACK_DTE_MAX = 70
TOP_N_PER_GROUP = 5

DEFAULT_UNIVERSE = {
    "thresholds": {
        "max_price_usd": 50.0,
        "max_price_cad": 50.0,
        "min_wheel_score": 3.0,
        "strikes_to_prune": 3,
    },
    "groups": {
        "Automobile": ["RIVN", "TM", "F", "GM", "TSLA"],
        "BFSI": ["UNH", "MFC", "V", "BN", "SE", "MELI", "TD", "BMO"],
        "Communications": ["T", "VZ", "ON"],
        "Consumer": ["OSCR", "BULL", "NKE", "KO", "MCD", "COST"],
        "Crypto & AI": ["TRON", "PATH"],
        "Energy": ["CVE", "SU", "ENB"],
        "Helium, Semiconductors & Photonic": [
            "USAR", "CLS", "LIN", "APD", "ALAB", "AVGO", "IRM", "IPGP",
            "SWKS", "VIAV", "COHR", "QCOM", "LRCX", "AMAT", "MRVL",
            "MU", "INTC", "AMD", "AXTI",
        ],
        "Technology": [
            "MSFT", "AMZN", "MSTR", "CDNS", "SNPS", "SMCI",
            "SOFI", "SHOP", "CSU", "GIB",
        ],
    },
}

PROTECTED_GROUPS: set[str] = set()


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------
def load_universe() -> dict:
    if not UNIVERSE_FILE.exists():
        UNIVERSE_FILE.write_text(json.dumps(DEFAULT_UNIVERSE, indent=2), encoding="utf-8")
        print(f"Created default universe at {UNIVERSE_FILE.name}")
        return DEFAULT_UNIVERSE
    return json.loads(UNIVERSE_FILE.read_text(encoding="utf-8"))


def save_universe(u: dict) -> None:
    u.pop("_comment", None)
    UNIVERSE_FILE.write_text(json.dumps(u, indent=2), encoding="utf-8")


def load_strikes() -> dict:
    if not STRIKES_FILE.exists():
        return {}
    try:
        return json.loads(STRIKES_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_strikes(s: dict) -> None:
    STRIKES_FILE.write_text(json.dumps(s, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Row + scoring
# ---------------------------------------------------------------------------
@dataclass
class Row:
    ticker: str
    group: str
    currency: str = "USD"
    price: Optional[float] = None
    market_cap: Optional[float] = None
    avg_volume: Optional[float] = None
    week_return_pct: Optional[float] = None
    dte: Optional[int] = None
    csp_strike: Optional[float] = None
    csp_premium: Optional[float] = None
    csp_oi: Optional[int] = None
    csp_iv: Optional[float] = None
    csp_ann_yield_pct: Optional[float] = None
    cc_strike: Optional[float] = None
    cc_premium: Optional[float] = None
    cc_oi: Optional[int] = None
    cc_ann_yield_pct: Optional[float] = None
    wheel_score: Optional[float] = None
    cc_score: Optional[float] = None
    risk: str = ""
    notes: str = ""
    strikes: int = 0


def pick_expiry(expiries: list[str]) -> Optional[str]:
    today = datetime.utcnow().date()
    parsed = []
    for exp in expiries:
        try:
            d = datetime.strptime(exp, "%Y-%m-%d").date()
        except ValueError:
            continue
        parsed.append((exp, (d - today).days))
    ideal = [(abs(dte - (TARGET_DTE_MIN + TARGET_DTE_MAX) / 2), exp)
             for exp, dte in parsed if TARGET_DTE_MIN <= dte <= TARGET_DTE_MAX]
    if ideal:
        ideal.sort()
        return ideal[0][1]
    fallback = [(abs(dte - 35), exp) for exp, dte in parsed
                if FALLBACK_DTE_MIN <= dte <= FALLBACK_DTE_MAX]
    if fallback:
        fallback.sort()
        return fallback[0][1]
    return None


def nearest_row(chain: pd.DataFrame, target_strike: float):
    if chain is None or chain.empty:
        return None
    idx = (chain["strike"] - target_strike).abs().idxmin()
    return chain.loc[idx]


def annualized_yield(premium: float, strike: float, dte: int) -> float:
    if not premium or not strike or not dte:
        return 0.0
    return (premium / strike) * (365.0 / dte) * 100.0


def scale(value: float, lo: float, hi: float) -> float:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return 0.0
    v = max(lo, min(hi, value))
    return (v - lo) / (hi - lo) * 10.0


def compute_wheel_score(csp_ann: float, iv: float, oi: int, mkt_cap: float) -> float:
    yld = scale(csp_ann, 8, 45)
    iv_s = scale(iv * 100 if iv else 0, 18, 55)
    liq = scale(oi or 0, 500, 20000)
    quality = scale((mkt_cap or 0) / 1e9, 2, 200)
    return round(0.35 * yld + 0.20 * iv_s + 0.20 * liq + 0.25 * quality, 2)


def compute_cc_score(cc_ann: float, iv: float, oi: int, mkt_cap: float) -> float:
    yld = scale(cc_ann, 8, 35)
    iv_s = scale(iv * 100 if iv else 0, 18, 50)
    liq = scale(oi or 0, 500, 20000)
    quality = scale((mkt_cap or 0) / 1e9, 2, 200)
    return round(0.35 * yld + 0.20 * iv_s + 0.20 * liq + 0.25 * quality, 2)


def risk_label(iv: float, mkt_cap: float) -> str:
    ivp = (iv or 0) * 100
    cap_b = (mkt_cap or 0) / 1e9
    if ivp < 25 and cap_b > 50:
        return "Low"
    if ivp < 35 and cap_b > 15:
        return "Low-Med"
    if ivp < 45:
        return "Medium"
    return "Med-High"


def fetch_row(sym: str, group: str) -> Row:
    row = Row(ticker=sym, group=group)
    try:
        tk = yf.Ticker(sym, session=_YF_SESSION) if _YF_SESSION else yf.Ticker(sym)
        fi = tk.fast_info
        row.price = float(getattr(fi, "last_price", 0) or 0) or None
        row.market_cap = float(getattr(fi, "market_cap", 0) or 0) or None
        row.avg_volume = float(getattr(fi, "ten_day_average_volume", 0)
                               or getattr(fi, "three_month_average_volume", 0) or 0)
        row.currency = getattr(fi, "currency", "USD") or "USD"

        hist = tk.history(period="10d", auto_adjust=False)
        if len(hist) >= 6:
            row.week_return_pct = round(
                (hist["Close"].iloc[-1] / hist["Close"].iloc[-6] - 1) * 100, 2)

        expiries = tk.options or []
        exp = pick_expiry(list(expiries))
        if not exp or not row.price:
            row.notes = ("no options data (TSX / ETF chains not on yfinance)"
                         if not expiries else "no valid expiry")
            row.wheel_score = 0
            row.cc_score = 0
            return row

        row.dte = (datetime.strptime(exp, "%Y-%m-%d").date() - datetime.utcnow().date()).days
        chain = tk.option_chain(exp)
        puts, calls = chain.puts, chain.calls

        put = nearest_row(puts, row.price * 0.95)
        if put is not None:
            row.csp_strike = float(put["strike"])
            bid, ask, last = put.get("bid", 0) or 0, put.get("ask", 0) or 0, put.get("lastPrice", 0) or 0
            row.csp_premium = round((bid + ask) / 2, 4) if (bid and ask) else float(last)
            row.csp_oi = int(put.get("openInterest") or 0)
            row.csp_iv = float(put.get("impliedVolatility") or 0)
            row.csp_ann_yield_pct = round(annualized_yield(row.csp_premium, row.csp_strike, row.dte), 2)

        call = nearest_row(calls, row.price * 1.05)
        if call is not None:
            row.cc_strike = float(call["strike"])
            bid, ask, last = call.get("bid", 0) or 0, call.get("ask", 0) or 0, call.get("lastPrice", 0) or 0
            row.cc_premium = round((bid + ask) / 2, 4) if (bid and ask) else float(last)
            row.cc_oi = int(call.get("openInterest") or 0)
            row.cc_ann_yield_pct = round(annualized_yield(row.cc_premium, row.price, row.dte), 2)

        row.wheel_score = compute_wheel_score(
            row.csp_ann_yield_pct or 0, row.csp_iv or 0,
            row.csp_oi or 0, row.market_cap or 0)
        row.cc_score = compute_cc_score(
            row.cc_ann_yield_pct or 0, row.csp_iv or 0,
            row.cc_oi or 0, row.market_cap or 0)
        row.risk = risk_label(row.csp_iv or 0, row.market_cap or 0)

    except Exception as e:
        row.notes = f"error: {e.__class__.__name__}"
        row.wheel_score = 0
        row.cc_score = 0
    return row


# ---------------------------------------------------------------------------
# Threshold enforcement
# ---------------------------------------------------------------------------
def evaluate_thresholds(row: Row, thresholds: dict) -> tuple[bool, str]:
    if row.group in PROTECTED_GROUPS:
        return False, ""
    if row.price is None:
        return False, ""
    max_px = thresholds.get("max_price_cad" if row.currency == "CAD" else "max_price_usd", 50.0)
    if row.price > max_px:
        return True, f"price {row.price:.2f} > {max_px:.0f}"
    if row.wheel_score is not None and row.wheel_score < thresholds.get("min_wheel_score", 3.0):
        return True, f"wheel {row.wheel_score:.1f} < min"
    return False, ""


def apply_auto_prune(universe: dict, rows: list[Row], strikes: dict, no_prune: bool):
    thresholds = universe["thresholds"]
    limit = thresholds.get("strikes_to_prune", 3)
    flagged: list[str] = []
    removed: list[str] = []

    for r in rows:
        breach, reason = evaluate_thresholds(r, thresholds)
        key = r.ticker
        if breach:
            current = strikes.get(key, {"count": 0, "reason": ""})
            current["count"] += 1
            current["reason"] = reason
            current["last_seen"] = datetime.now().strftime("%Y-%m-%d")
            strikes[key] = current
            r.strikes = current["count"]
            flagged.append(f"{key} strike {current['count']}/{limit} ({reason})")
            if not no_prune and current["count"] >= limit:
                for g, tickers in list(universe["groups"].items()):
                    if g in PROTECTED_GROUPS:
                        continue
                    if key in tickers:
                        tickers.remove(key)
                        removed.append(f"{key} from '{g}' — {reason}")
                strikes.pop(key, None)
        else:
            if key in strikes:
                strikes.pop(key, None)
                r.strikes = 0
    return flagged, removed


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------
HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Wheel & Covered Call Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0"></script>
<style>
  :root {{ --bg:#0f172a; --card:#1e293b; --ink:#e2e8f0; --muted:#94a3b8;
           --pos:#22c55e; --neg:#ef4444; --accent:#38bdf8; --violet:#a78bfa;
           --gold:#fbbf24; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,Segoe UI,Roboto,sans-serif;
          background:var(--bg); color:var(--ink); padding:24px; }}
  h1 {{ margin:0 0 4px 0; }}
  h2.section {{ color:var(--accent); margin-top:8px; font-size:18px; }}
  .sub {{ color:var(--muted); margin-bottom:20px; }}
  .banner {{ background:#312e81; border-left:4px solid var(--violet);
             padding:10px 14px; border-radius:6px; margin-bottom:20px;
             font-size:13px; }}
  .banner b {{ color:var(--gold); }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(400px,1fr));
           gap:18px; margin-bottom:24px; }}
  .card {{ background:var(--card); border-radius:12px; padding:16px 18px;
           box-shadow:0 4px 12px rgba(0,0,0,0.25); }}
  .card h2 {{ margin:0 0 6px 0; font-size:15px; color:var(--accent); }}
  .card .subtle {{ color:var(--muted); font-size:11px; margin-bottom:8px; }}
  canvas {{ max-height:260px; }}
  table {{ width:100%; border-collapse:collapse; font-size:12px; }}
  th, td {{ padding:6px 8px; border-bottom:1px solid #334155; text-align:right; }}
  th:first-child, td:first-child, th:nth-child(2), td:nth-child(2),
  th:nth-child(3), td:nth-child(3) {{ text-align:left; }}
  th {{ position:sticky; top:0; background:#334155; color:#e2e8f0; }}
  tr:hover td {{ background:#273449; }}
  .pos {{ color:var(--pos); font-weight:600; }}
  .neg {{ color:var(--neg); font-weight:600; }}
  .risk-Low {{ color:#22c55e; }}
  .risk-Low-Med {{ color:#84cc16; }}
  .risk-Medium {{ color:#f59e0b; }}
  .risk-Med-High {{ color:#ef4444; }}
  .flag {{ color:var(--gold); font-size:11px; }}
  .footer {{ color:var(--muted); font-size:12px; margin-top:24px; }}
</style>
</head>
<body>
  <h1>Wheel &amp; Covered Call Dashboard</h1>
  <div class="sub">Generated {generated_at} — target $2,500 / month options income</div>

  {banner_html}

  <h2 class="section">Overall Weekly Movers</h2>
  <div class="grid">
    <div class="card"><h2>Top 5 Gainers (past week)</h2><canvas id="gainers"></canvas></div>
    <div class="card"><h2>Top 5 Losers (past week)</h2><canvas id="losers"></canvas></div>
  </div>

  <h2 class="section">Industry-wise Weekly Movers</h2>
  <div class="grid" id="industryMoversGrid"></div>

  <h2 class="section">Top {top_n} per Industry — Wheel Score</h2>
  <div class="grid" id="industryGrid"></div>

  <div class="card">
    <h2>Master Screen (all tickers)</h2>
    <div style="overflow-x:auto">
      <table id="master">
        <thead><tr>
          <th>Rank</th><th>Ticker</th><th>Group</th>
          <th>Price</th><th>Ccy</th><th>Wk %</th><th>MCap ($B)</th><th>Avg Vol</th>
          <th>DTE</th><th>IV %</th>
          <th>CSP K</th><th>CSP Prem</th><th>CSP OI</th><th>CSP Ann %</th>
          <th>CC K</th><th>CC Prem</th><th>CC OI</th><th>CC Ann %</th>
          <th>Wheel</th><th>CC</th><th>Risk</th><th>Strk</th><th>Flags</th>
        </tr></thead>
        <tbody></tbody>
      </table>
    </div>
  </div>

  <div class="footer">Data via yfinance (15-min delayed). Verify all quotes in your broker before trading. Not investment advice.</div>

<script>
const DATA = {data_json};
const TOP_N = {top_n};

// Register datalabels plugin globally so all charts show values on the bars.
if (window.ChartDataLabels) Chart.register(ChartDataLabels);

function fmt(v, d=2) {{ return v==null || isNaN(v) ? '—' : Number(v).toFixed(d); }}
function fmtInt(v) {{ return v==null ? '—' : Number(v).toLocaleString(); }}
function pct(v) {{
  if (v==null) return '—';
  const cls = v >= 0 ? 'pos' : 'neg';
  return `<span class="${{cls}}">${{v.toFixed(2)}}%</span>`;
}}

// Master table — sort by risk (Low → Med-High), then wheel score desc within a bucket
const RISK_ORDER = {{ 'Low': 1, 'Low-Med': 2, 'Medium': 3, 'Med-High': 4 }};
const riskRank = r => RISK_ORDER[r] ?? 99;
const ranked = [...DATA].sort((a,b) => {{
  const dr = riskRank(a.risk) - riskRank(b.risk);
  if (dr !== 0) return dr;
  return (b.wheel_score||0) - (a.wheel_score||0);
}});
const tbody = document.querySelector('#master tbody');
ranked.forEach((r, i) => {{
  const tr = document.createElement('tr');
  const mcapB = r.market_cap ? (r.market_cap/1e9).toFixed(1) : '—';
  const ivPct = r.csp_iv ? (r.csp_iv*100).toFixed(1) : '—';
  tr.innerHTML = `
    <td>${{i+1}}</td><td><b>${{r.ticker}}</b></td><td>${{r.group}}</td>
    <td>${{fmt(r.price)}}</td><td>${{r.currency||'USD'}}</td>
    <td>${{pct(r.week_return_pct)}}</td><td>${{mcapB}}</td>
    <td>${{fmtInt(r.avg_volume)}}</td><td>${{r.dte ?? '—'}}</td>
    <td>${{ivPct}}</td>
    <td>${{fmt(r.csp_strike)}}</td><td>${{fmt(r.csp_premium)}}</td>
    <td>${{fmtInt(r.csp_oi)}}</td><td>${{fmt(r.csp_ann_yield_pct)}}</td>
    <td>${{fmt(r.cc_strike)}}</td><td>${{fmt(r.cc_premium)}}</td>
    <td>${{fmtInt(r.cc_oi)}}</td><td>${{fmt(r.cc_ann_yield_pct)}}</td>
    <td><b>${{fmt(r.wheel_score,1)}}</b></td>
    <td><b>${{fmt(r.cc_score,1)}}</b></td>
    <td class="risk-${{(r.risk||'').replace(' ','-')}}">${{r.risk||'—'}}</td>
    <td>${{r.strikes>0?r.strikes:''}}</td>
    <td class="flag">${{r.notes||''}}</td>
  `;
  tbody.appendChild(tr);
}});

// Weekly movers
const withWk = DATA.filter(d => d.week_return_pct != null);
const gainers = [...withWk].sort((a,b) => b.week_return_pct - a.week_return_pct).slice(0,5);
const losers  = [...withWk].sort((a,b) => a.week_return_pct - b.week_return_pct).slice(0,5);

function bar(id, rows, key, color, valueFmt) {{
  new Chart(document.getElementById(id), {{
    type:'bar',
    data:{{
      labels: rows.map(r => r.ticker + (r.group ? ' · '+r.group.slice(0,18):'') ),
      datasets:[{{ data: rows.map(r => r[key]), backgroundColor: color, borderRadius: 4 }}]
    }},
    options:{{
      indexAxis:'y',
      layout:{{ padding:{{ right: 42 }} }},
      plugins:{{
        legend:{{ display:false }},
        tooltip:{{ callbacks:{{ label:(c)=>valueFmt?valueFmt(c.parsed.x):c.parsed.x }} }},
        datalabels:{{
          anchor:'end', align:'end', clamp:true, clip:false,
          color:'#e2e8f0', font:{{ weight:'600', size:11 }},
          formatter:(v)=> v==null ? '' : (valueFmt ? valueFmt(v) : v)
        }}
      }},
      scales:{{
        x:{{ ticks:{{color:'#94a3b8'}}, grid:{{color:'#334155'}} }},
        y:{{ ticks:{{color:'#e2e8f0'}}, grid:{{display:false}} }}
      }}
    }}
  }});
}}

bar('gainers', gainers, 'week_return_pct', '#22c55e', v => v.toFixed(2)+'%');
bar('losers',  losers,  'week_return_pct', '#ef4444', v => v.toFixed(2)+'%');

// Per-industry top-N — preserve insertion order from DATA
const groupOrder = [];
DATA.forEach(d => {{ if (!groupOrder.includes(d.group)) groupOrder.push(d.group); }});
const grid = document.getElementById('industryGrid');
groupOrder.forEach((g, idx) => {{
  const rows = DATA.filter(d => d.group === g)
                   .sort((a,b) => (b.wheel_score||0) - (a.wheel_score||0))
                   .slice(0, TOP_N);
  if (rows.length === 0) return;
  const withPx = rows.filter(r=>r.price);
  const avgPx = withPx.length ? (withPx.reduce((s,r)=>s+r.price,0)/withPx.length) : 0;
  const card = document.createElement('div');
  card.className = 'card';
  const canvasId = 'grp_' + idx;
  card.innerHTML = `
    <h2>${{g}}</h2>
    <div class="subtle">${{rows.length}} shown · avg px ${{avgPx.toFixed(2)}}</div>
    <canvas id="${{canvasId}}"></canvas>
  `;
  grid.appendChild(card);
  bar(canvasId, rows, 'wheel_score', '#38bdf8', v => v.toFixed(1));
}});

// Per-industry weekly movers — top gainer + top loser per group
const moversGrid = document.getElementById('industryMoversGrid');
groupOrder.forEach((g, idx) => {{
  const rows = DATA.filter(d => d.group === g && d.week_return_pct != null);
  if (rows.length === 0) return;
  const sorted = [...rows].sort((a,b) => b.week_return_pct - a.week_return_pct);
  const gTop = sorted.slice(0, 3);
  const lTop = [...sorted].reverse().slice(0, 3);

  const card = document.createElement('div');
  card.className = 'card';
  const gId = 'mg_g_' + idx;
  const lId = 'mg_l_' + idx;
  card.innerHTML = `
    <h2>${{g}}</h2>
    <div class="subtle">Weekly gainers &amp; losers</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
      <div><div class="subtle">Gainers</div><canvas id="${{gId}}"></canvas></div>
      <div><div class="subtle">Losers</div><canvas id="${{lId}}"></canvas></div>
    </div>
  `;
  moversGrid.appendChild(card);
  bar(gId, gTop, 'week_return_pct', '#22c55e', v => v.toFixed(2)+'%');
  bar(lId, lTop, 'week_return_pct', '#ef4444', v => v.toFixed(2)+'%');
}});
</script>
</body>
</html>
"""


def render_html(rows: list[Row], flagged: list[str], removed: list[str]) -> None:
    banner_bits = []
    if removed:
        banner_bits.append("<b>Auto-pruned:</b> " + "; ".join(removed))
    if flagged:
        banner_bits.append("<b>Watch flags:</b> " + "; ".join(flagged))
    banner_html = f'<div class="banner">{"<br>".join(banner_bits)}</div>' if banner_bits else ""

    html = HTML_TEMPLATE.format(
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        data_json=json.dumps([asdict(r) for r in rows]),
        top_n=TOP_N_PER_GROUP,
        banner_html=banner_html,
    )
    HTML_FILE.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Wheel screener + auto-prune dashboard")
    p.add_argument("--add", metavar="TICKER:GROUP",
                   help='Add a ticker to a group. e.g. --add "NVDA:Helium & Semiconductor"')
    p.add_argument("--remove", metavar="TICKER", help="Remove a ticker from every group")
    p.add_argument("--no-prune", action="store_true",
                   help="Compute strikes but don't remove anything this run")
    p.add_argument("--reset-strikes", action="store_true",
                   help="Clear all accumulated strike counts")
    p.add_argument("--open", action="store_true",
                   help="Open dashboard in default browser at end")
    return p.parse_args()


def cli_mutations(args: argparse.Namespace, universe: dict) -> None:
    if args.reset_strikes and STRIKES_FILE.exists():
        STRIKES_FILE.unlink()
        print("Cleared strikes.json")

    if args.remove:
        removed_from = []
        for g, tickers in universe["groups"].items():
            if args.remove in tickers:
                tickers.remove(args.remove)
                removed_from.append(g)
        if removed_from:
            print(f"Removed {args.remove} from: {', '.join(removed_from)}")
            save_universe(universe)
        else:
            print(f"{args.remove} not found in any group.")

    if args.add:
        if ":" not in args.add:
            sys.exit('--add expects TICKER:GROUP  (e.g. "NVDA:Helium & Semiconductor")')
        ticker, group = args.add.split(":", 1)
        ticker, group = ticker.strip().upper(), group.strip()
        universe["groups"].setdefault(group, [])
        if ticker not in universe["groups"][group]:
            universe["groups"][group].append(ticker)
            save_universe(universe)
            print(f"Added {ticker} to '{group}'")
        else:
            print(f"{ticker} already in '{group}'")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    args = parse_args()
    universe = load_universe()
    cli_mutations(args, universe)

    strikes = load_strikes()
    all_tickers: list[tuple[str, str]] = []
    seen = set()
    for group, tickers in universe["groups"].items():
        for t in tickers:
            if t in seen:
                continue
            seen.add(t)
            all_tickers.append((t, group))

    print(f"Screening {len(all_tickers)} tickers across {len(universe['groups'])} groups...")
    rows: list[Row] = []
    for sym, group in all_tickers:
        r = fetch_row(sym, group)
        if sym in strikes:
            r.strikes = strikes[sym].get("count", 0)
        px = f"{r.price:.2f}" if r.price else "n/a"
        ws = f"{r.wheel_score:.1f}" if r.wheel_score is not None else "n/a"
        note = f"  {r.notes}" if r.notes else ""
        print(f"  {sym:<10s} [{group[:30]:<30s}] px={px:<8s} wheel={ws}{note}")
        rows.append(r)

    flagged, removed = apply_auto_prune(universe, rows, strikes, args.no_prune)
    save_strikes(strikes)
    if removed:
        save_universe(universe)

    pd.DataFrame([asdict(r) for r in rows]).to_csv(CSV_FILE, index=False)
    render_html(rows, flagged, removed)

    print(f"\nWrote {HTML_FILE.name} and {CSV_FILE.name}")
    if flagged:
        print("Watch flags:")
        for f in flagged:
            print("  •", f)
    if removed:
        print("Auto-removed (universe.json updated):")
        for f in removed:
            print("  •", f)
    if args.open:
        webbrowser.open(HTML_FILE.as_uri())


if __name__ == "__main__":
    main()
