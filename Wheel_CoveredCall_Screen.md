# Wheel & Covered Call Income Screen — Target: ~$2,500 / month

**Prepared as:** Options income strategist / CFA-style analysis
**Objective:** ~$2,500/month passive premium income from Cash-Secured Puts (CSP) and Covered Calls (CC)
**Universe:** U.S. + Canadian large caps under $50 (USD / CAD respectively)
**Style:** Capital preservation first, income second, growth third

> **CRITICAL DISCLAIMER**
> Numbers below are **modeled estimates** based on typical trailing ranges (price, IV, premium as a % of strike). Options premiums move continuously. **Verify every quote in your broker** (mid-price, open interest, IV, DTE) before placing an order. Nothing here is personalized investment advice.

---

## 1. Screening Methodology

Each candidate had to clear all of the following before being ranked:

**Fundamental gates**
- Price < $50 (USD for U.S., CAD for Canada)
- ≥ 10 years operating history
- 5-yr revenue trend flat-to-positive
- Positive operating cash flow (TTM)
- Debt/Equity within sector norm
- Market cap > $2B
- Profitable or breakeven TTM
- No going-concern flags

**Options gates**
- Weekly or monthly chain listed
- Avg daily share volume > 1M
- Front-month OI > 500 on near-ATM strikes
- IV (annualized) between 20% and 60%
- Bid/ask spread < ~5% of premium on liquid strikes
- Chain supports both CSPs and CCs at 30–45 DTE

**Scoring (0–10 each, higher = better)**
- **Wheel Score** = weighted avg of: annualized CSP yield (30%), assignment tolerance / willingness to own (25%), IV/HV ratio (15%), liquidity (15%), balance-sheet quality (15%)
- **CC Score** = weighted avg of: annualized CC yield at ~5% OTM (30%), upside cap acceptability (20%), dividend cushion (15%), IV stability (20%), liquidity (15%)

---

## 2. Master Screen Table

Prices, IVs, and premiums are **representative mid-range estimates**. Column definitions follow the table.

| Rank | Ticker | Exch | Sector | Px | Mkt Cap | Yrs | Rev Trend | Avg Vol | IV% | Wheel | CC | Capital / Contract | Est. Monthly Inc / Contract | Risk |
|------|--------|------|--------|----|---------|-----|-----------|---------|-----|-------|----|--------------------|-----------------------------|------|
| 1 | **F** | NYSE | Consumer Cyc (Auto) | ~$11 | $45B | 120+ | Flat-to-up | 70M+ | ~38% | 9.0 | 8.5 | ~$1,100 | ~$35–45 | Med |
| 2 | **PFE** | NYSE | Healthcare | ~$28 | $160B | 175+ | Slight decline post-COVID | 30M+ | ~26% | 8.8 | 8.2 | ~$2,800 | ~$55–75 | Low-Med |
| 3 | **KMI** | NYSE | Energy (Midstream) | ~$22 | $50B | 25+ | Positive | 12M+ | ~22% | 8.7 | 7.8 | ~$2,200 | ~$35–50 | Low-Med |
| 4 | **VZ** | NYSE | Communication | ~$42 | $175B | 40+ | Flat | 15M+ | ~22% | 8.6 | 8.0 | ~$4,200 | ~$70–95 | Low |
| 5 | **BAC** | NYSE | Financials | ~$42 | $325B | 100+ | Positive | 35M+ | ~28% | 8.5 | 8.7 | ~$4,200 | ~$95–130 | Med |
| 6 | **CSCO** | NASDAQ | Tech (Networking) | ~$48 | $195B | 40+ | Flat-to-up | 18M+ | ~24% | 8.4 | 8.6 | ~$4,800 | ~$95–125 | Low |
| 7 | **T** (AT&T) | NYSE | Communication | ~$22 | $155B | 40+ | Flat | 40M+ | ~25% | 8.3 | 7.6 | ~$2,200 | ~$40–55 | Med |
| 8 | **KHC** | NASDAQ | Consumer Def | ~$32 | $38B | 10+ (merged 2015) | Flat | 6M+ | ~24% | 7.9 | 7.7 | ~$3,200 | ~$55–75 | Med |
| 9 | **HBAN** | NASDAQ | Reg Bank | ~$14 | $20B | 150+ | Positive | 15M+ | ~30% | 7.8 | 7.5 | ~$1,400 | ~$25–35 | Med |
| 10 | **INTC** | NASDAQ | Semis | ~$24 | $105B | 55+ | Declining (turnaround) | 55M+ | ~50% | 7.0 | 8.9 | ~$2,400 | ~$85–120 | Med-High |
| 11 | **MFC.TO** | TSX | Financials (Insurer) | ~$38 CAD | $65B CAD | 135+ | Positive | 8M+ | ~22% | 8.5 | 7.9 | ~$3,800 CAD | ~$55–75 CAD | Low-Med |
| 12 | **ENB.TO** | TSX | Energy (Pipeline) | ~$48 CAD | $105B CAD | 75+ | Positive | 6M+ | ~20% | 8.4 | 7.7 | ~$4,800 CAD | ~$60–80 CAD | Low-Med |
| 13 | **SU.TO** | TSX | Energy (Integrated) | ~$48 CAD | $65B CAD | 70+ | Positive | 7M+ | ~30% | 8.0 | 8.4 | ~$4,800 CAD | ~$85–120 CAD | Med |
| 14 | **T.TO** (Telus) | TSX | Communication | ~$22 CAD | $32B CAD | 30+ | Positive | 5M+ | ~22% | 8.1 | 7.6 | ~$2,200 CAD | ~$30–45 CAD | Low-Med |
| 15 | **CVE.TO** | TSX | Energy | ~$25 CAD | $47B CAD | 25+ | Positive | 9M+ | ~34% | 7.7 | 8.2 | ~$2,500 CAD | ~$45–65 CAD | Med |

**Column notes**
- **Px** = last representative price
- **Est. Monthly Inc / Contract** = expected premium per 1 CSP contract at ~30–45 DTE, ~0.30 delta (roughly ATM to slightly OTM), annualized then divided by 12
- **Risk** rating is qualitative: business durability + drawdown history + IV regime

---

## 3. Wheel Strategy Detail (Top 8)

Assumes: **30–45 DTE**, **~0.25–0.30 delta short put** (probability OTM ≈ 70–75%), premium as % of strike based on representative IV.

| Ticker | Px | Short Put Strike (≈0.30Δ) | Est. Premium | Ann. Yield on Cash Sec. | Prob OTM | HV | IV | IV/HV |
|--------|----|---------------------------|--------------|--------------------------|----------|----|----|-------|
| F | $11 | $10.5 | ~$0.35 | ~40% | ~72% | 32% | 38% | 1.19 |
| PFE | $28 | $27 | ~$0.65 | ~29% | ~72% | 22% | 26% | 1.18 |
| KMI | $22 | $21 | ~$0.40 | ~23% | ~72% | 20% | 22% | 1.10 |
| VZ | $42 | $40 | ~$0.80 | ~24% | ~73% | 20% | 22% | 1.10 |
| BAC | $42 | $40 | ~$1.05 | ~31% | ~72% | 24% | 28% | 1.17 |
| CSCO | $48 | $46 | ~$1.05 | ~27% | ~72% | 21% | 24% | 1.14 |
| MFC.TO | C$38 | C$36 | ~C$0.70 | ~24% | ~72% | 19% | 22% | 1.16 |
| SU.TO | C$48 | C$45 | ~C$1.50 | ~40% | ~70% | 28% | 30% | 1.07 |

Annualized yield = (premium ÷ strike) × (365 ÷ DTE). Assumes cash-secured, no margin.

**Wheel rank (best → worst): F, BAC, SU.TO, PFE, CSCO, MFC.TO, VZ, KMI.**
F and BAC lead on premium; PFE/KMI/VZ lead on business durability if assigned.

---

## 4. Covered Call Detail (Top 8)

Assumes you already own (or get assigned) 100 shares. Selling **30 DTE**, **~5% OTM** call.

| Ticker | Shares Cost / 100 | 5% OTM Strike | Est. Call Premium | Monthly Yield | Ann. Yield | Assignment Freq* |
|--------|------------------|----------------|--------------------|---------------|-------------|------------------|
| F | $1,100 | $11.5 | ~$0.20 | ~1.8% | ~22% | Low-Med |
| PFE | $2,800 | $29.5 | ~$0.40 | ~1.4% | ~17% | Low |
| BAC | $4,200 | $44 | ~$0.65 | ~1.5% | ~19% | Med |
| CSCO | $4,800 | $50.5 | ~$0.70 | ~1.5% | ~17% | Low-Med |
| INTC | $2,400 | $25 | ~$0.65 | ~2.7% | ~32% | Med-High |
| SU.TO | C$4,800 | C$50.5 | ~C$0.90 | ~1.9% | ~23% | Med |
| CVE.TO | C$2,500 | C$26.5 | ~C$0.45 | ~1.8% | ~22% | Med |
| VZ | $4,200 | $44 | ~$0.55 | ~1.3% | ~16% | Low |

*Assignment frequency = qualitative estimate of how often a 5% OTM 30-DTE call finishes ITM given historical realized moves.

**CC rank (best → worst): INTC, SU.TO, F, CVE.TO, BAC, CSCO, PFE, VZ.**
Higher IV = more premium but also more assignment / drawdown risk.

---

## 5. Sizing to the $2,500 / month Target

Using an average net premium of **~$60 per contract per month**, target income needs roughly **42 open short-option contracts spread across the month** (staggered weekly / bi-weekly). Because Wheel positions rotate (some contracts expire worthless, some get assigned and flip into CCs), a realistic capital plan:

| Portfolio Size | Est. Monthly Premium | Est. Annual Premium | Return on Capital |
|----------------|----------------------|----------------------|-------------------|
| $75,000 | ~$1,500 | ~$18,000 | ~24% |
| **$120,000** | **~$2,500** | **~$30,000** | **~25%** |
| $180,000 | ~$3,750 | ~$45,000 | ~25% |

$120K is the practical floor to reliably clear $2,500/month **cash-secured** without over-concentration. Using portfolio margin can cut required capital 30–50% but raises risk rating one full notch.

---

## 6. Three Model Portfolios

All three assume ~$120K deployable, laddered expirations, and staggered strike entries.

### A) Conservative Portfolio — priority: capital preservation + dividends

| Ticker | Contracts (CSP) | Capital | Role |
|--------|-----------------|---------|------|
| VZ | 4 | $16,800 | Dividend anchor, low IV |
| PFE | 5 | $14,000 | Healthcare defensive, dividend |
| KMI | 6 | $13,200 | Midstream cash flow, dividend |
| CSCO | 3 | $14,400 | Cash-rich tech, dividend |
| ENB.TO | 3 | C$14,400 | Canadian pipeline, dividend |
| MFC.TO | 4 | C$15,200 | Canadian insurer, dividend |
| **Cash buffer** | — | ~$32,000 | Assignment reserve |
| **Total** | | **~$120,000** | |

- Blended IV ~23%
- Est. monthly premium: **~$2,100–$2,400**
- Risk: **Low**
- Assignment plan: if assigned, immediately write 30-DTE 3–5% OTM CCs. All names pay dividends while you hold.

### B) Balanced Portfolio — mix of income + moderate growth

| Ticker | Contracts (CSP) | Capital | Role |
|--------|-----------------|---------|------|
| BAC | 4 | $16,800 | Financials, rate-sensitive |
| CSCO | 3 | $14,400 | Tech quality + dividend |
| PFE | 4 | $11,200 | Defensive income |
| F | 8 | $8,800 | High-yield premium engine |
| KMI | 5 | $11,000 | Midstream dividend |
| SU.TO | 3 | C$14,400 | Canadian energy, high premium |
| T.TO (Telus) | 5 | C$11,000 | Canadian telecom, dividend |
| **Cash buffer** | — | ~$32,000 | Assignment reserve |
| **Total** | | **~$120,000** | |

- Blended IV ~28%
- Est. monthly premium: **~$2,500–$2,900**
- Risk: **Low-Medium**
- Assignment plan: rotate assigned shares into CCs at 5–7% OTM to allow modest upside capture.

### C) Aggressive Income Portfolio — priority: max premium (higher risk)

| Ticker | Contracts (CSP) | Capital | Role |
|--------|-----------------|---------|------|
| INTC | 6 | $14,400 | High-IV premium engine |
| F | 12 | $13,200 | High-IV, low absolute price |
| BAC | 4 | $16,800 | Financials leverage |
| SU.TO | 3 | C$14,400 | Canadian energy |
| CVE.TO | 5 | C$12,500 | Canadian energy |
| KHC | 4 | $12,800 | Consumer staple, dividend |
| HBAN | 8 | $11,200 | Regional bank |
| **Cash buffer** | — | ~$25,000 | Assignment reserve |
| **Total** | | **~$120,000** | |

- Blended IV ~34%
- Est. monthly premium: **~$3,200–$3,800**
- Risk: **Medium-High** (higher assignment frequency, more mark-to-market noise)
- Assignment plan: expect frequent assignment on INTC / F / HBAN; write CCs aggressively 2–4% OTM.

---

## 7. Execution Rules (works for all three portfolios)

1. **Sell CSPs at 0.20–0.30 delta**, 30–45 DTE — sweet spot for theta vs. assignment risk.
2. **Roll at 21 DTE or 50% max profit**, whichever comes first (Tastyworks study rule).
3. **Never sell a put on a stock you would not be happy owning at the strike price** — this is the core Wheel discipline.
4. **On assignment**, immediately write a CC at strike ≥ your cost basis so early assignment is always profitable.
5. **Skip earnings weeks** on any single-name with > 5% expected move (or size down 50%).
6. **Cap any single ticker at 15% of portfolio** notional.
7. **Keep ≥ 20% cash buffer** for assignments and margin calls.
8. **Track after-tax yield**, not gross premium — CSPs / CCs are short-term gains in a taxable account.

---

## 8. What to Verify Before Trading

For every candidate above, pull in your broker:
- Live price vs. the ~$50 ceiling
- Front-month and next-month **open interest** on your target strike (need > 500)
- **Bid/ask spread** on that strike (need < ~$0.05 on names <$30, < ~$0.10 on names $30–50)
- Realized 30-day IV vs. current IV (want IV Rank > 30 for CSP entry)
- **Ex-dividend date** — CC assignment risk spikes the day before

If any name fails the live check, drop it and reallocate to the next-ranked candidate in the same portfolio bucket.

---

*End of screen. Re-run monthly or when VIX changes regime (± 5 points).*
