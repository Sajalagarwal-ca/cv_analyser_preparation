"""Personalized 1-Year ETF Strategy using ACTUAL holdings from InvestmentSummary.xlsx."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = "ETF_Strategy_1Year.xlsx"

THIN = Side(border_style="thin", color="BFBFBF")
BORDER = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
HDR_FILL = PatternFill("solid", fgColor="1F4E78")
TOTAL_FILL = PatternFill("solid", fgColor="FFE699")
SELL_FILL = PatternFill("solid", fgColor="F8CBAD")
KEEP_FILL = PatternFill("solid", fgColor="C6EFCE")
BUY_FILL  = PatternFill("solid", fgColor="BDD7EE")
HDR_FONT = Font(bold=True, color="FFFFFF", size=11)
SUB_FONT = Font(bold=True, color="1F4E78", size=12)
TITLE_FONT = Font(bold=True, size=14, color="1F4E78")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)


def write_header(ws, row, headers, widths=None):
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.fill = HDR_FILL
        c.font = HDR_FONT
        c.alignment = CENTER
        c.border = BORDER
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w


def row_out(ws, row, values, bold=False, fill=None, money_cols=None, pct_cols=None):
    money_cols = money_cols or []
    pct_cols = pct_cols or []
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.border = BORDER
        c.alignment = LEFT if i == 1 else CENTER
        if bold:
            c.font = Font(bold=True)
        if fill:
            c.fill = fill
        if i in money_cols and isinstance(v, (int, float)):
            c.number_format = '"$"#,##0.00'
        if i in pct_cols and isinstance(v, (int, float)):
            c.number_format = "0.00%"


FX = 1.4194
wb = Workbook()

# Summary
ws = wb.active
ws.title = "Summary"
ws.cell(row=1, column=1, value="1-Year ETF Strategy — Personalized").font = TITLE_FONT
ws.merge_cells("A1:G1")
ws.cell(row=2, column=1,
        value="Based on your actual InvestmentSummary holdings. Target 8-10% on equity sleeves; FHSA stays conservative."
        ).font = Font(italic=True, color="595959")
ws.merge_cells("A2:G2")

write_header(ws, 4,
             ["Account", "Current Total (CAD)", "Cash", "GIC", "ETF/Stock",
              "Year-1 Target", "Strategy"],
             widths=[10, 18, 12, 12, 14, 14, 50])

rows = [
    ("FHSA", 17428.71, 250.17, 13400, 3778.54, 0.045,
     "Keep GIC and ETFs; DCA new cash into PSA/CASH and a bit of XEQT"),
    ("RRSP", 36072.43, 8460.86, 25000, 2611.57, 0.075,
     "Deploy $8,461 cash NOW into 50/25/15/10 ETF mix; redeploy GIC Nov 2026"),
    ("TFSA", 7914.41, 84.79, 0, 7829.62, 0.085,
     "SELL BULL & TRON, then rebuild into 50/25/15/10 ETF core"),
]
r = 5
for v in rows:
    row_out(ws, r, list(v), money_cols=[2, 3, 4, 5], pct_cols=[6])
    r += 1
total = 17428.71 + 36072.43 + 7914.41
row_out(ws, r,
        ["TOTAL", total, 250.17+8460.86+84.79, 13400+25000,
         3778.54+2611.57+7829.62, 0.068,
         "Blended ~6.8% Year-1 (GIC drag); rises to ~8-9% Year-2"],
        bold=True, fill=TOTAL_FILL, money_cols=[2, 3, 4, 5], pct_cols=[6])

r += 3
ws.cell(row=r, column=1, value="Quick wins (do this week)").font = SUB_FONT
for i, t in enumerate([
    "1. TFSA: SELL BULL (~$3,388) and TRON (~$3,343). Frees ~$6,730.",
    "2. RRSP: DEPLOY $8,461 cash into XEQT 50% / VFV 25% / XIC 15% / XEI 10%.",
    "3. FHSA: keep GIC; park $250 cash into PSA.TO.",
    "4. Set monthly auto-buys per 'Monthly DCA' tab.",
    "5. Calendar reminder: Nov 23, 2026 — RRSP GIC matures, redeploy $25,000.",
], 1):
    ws.cell(row=r+i, column=1, value=t).alignment = LEFT
    ws.merge_cells(start_row=r+i, start_column=1, end_row=r+i, end_column=7)

# Current Holdings
ws = wb.create_sheet("Current Holdings")
ws.cell(row=1, column=1, value="Actual Holdings (from InvestmentSummary.xlsx)").font = TITLE_FONT
ws.merge_cells("A1:H1")
write_header(ws, 3,
             ["Account", "Symbol", "Type", "Qty", "Cost ($)",
              "Market Value (CAD)", "P/L ($)", "% Return"],
             widths=[10, 14, 8, 10, 14, 18, 14, 12])

positions = [
    ("TFSA", "XEI",  "ETF",  1,    37.87,    39.10,             1.23,    0.0325),
    ("TFSA", "XEQT", "ETF",  4,   176.86,   178.16,             1.30,    0.0074),
    ("TFSA", "MSTR", "STK",  1,   177.24*FX, 82.31*FX,         (82.31-177.24)*FX, -0.536),
    ("TFSA", "MSFT", "STK",  0.1245, 50.17*FX, 46.43*FX,       (46.43-50.17)*FX,  -0.0745),
    ("TFSA", "SHOP", "STK",  2,   274.00,   330.10,            56.10,    0.2047),
    ("TFSA", "TRON", "STK",  1500, 4970*FX,  2355*FX,          (2355-4970)*FX,   -0.526),
    ("TFSA", "VFV",  "ETF",  2,   343.00,   368.74,            25.74,    0.0750),
    ("TFSA", "BULL", "STK",  350,  4815*FX,  2387*FX,          (2387-4815)*FX,   -0.504),
    ("FHSA", "GIC 3.30% (Community Trust, mat 2027-05-04)", "GIC",
              None, 13400, 13400, 0, 0),
    ("FHSA", "XEI",  "ETF", 14,   460.49,  547.40,  86.91, 0.1887),
    ("FHSA", "XIC",  "ETF", 18,   926.17, 1000.08,  73.91, 0.0798),
    ("FHSA", "VDY",  "ETF", 10,   642.41,  756.10, 113.69, 0.1770),
    ("FHSA", "VFV",  "ETF",  8,  1341.31, 1474.96, 133.65, 0.0996),
    ("RRSP", "GIC 2.85% (MCAN Mortgage, mat 2026-11-23)", "GIC",
              None, 25000, 25000, 0, 0),
    ("RRSP", "XEI",  "ETF", 10,   364.73,  391.00, 26.27, 0.0720),
    ("RRSP", "XEQT", "ETF", 10,   438.62,  445.40,  6.78, 0.0155),
    ("RRSP", "XIC",  "ETF",  6,   313.71,  333.36, 19.65, 0.0626),
    ("RRSP", "VDY",  "ETF",  2,   128.25,  151.22, 22.97, 0.1791),
    ("RRSP", "VFV",  "ETF",  7,  1241.66, 1290.59, 48.93, 0.0394),
]
r = 4
for p in positions:
    row_out(ws, r, list(p), money_cols=[5, 6, 7], pct_cols=[8])
    r += 1

# TFSA Cleanup
ws = wb.create_sheet("TFSA Cleanup")
ws.cell(row=1, column=1, value="TFSA — Sell / Keep / Redeploy").font = TITLE_FONT
ws.merge_cells("A1:F1")
write_header(ws, 3,
             ["Action", "Holding", "Approx Value (CAD)", "P/L", "Decision", "Reason"],
             widths=[10, 12, 18, 12, 16, 55])
bull_cad = 2387 * FX
tron_cad = 2355 * FX
mstr_cad = 82.31 * FX
msft_cad = 46.43 * FX
decisions = [
    ("SELL", "BULL", bull_cad, "-50.4%", "Exit ALL",
     "Single name -50%; binary outcome. Free ~$3,388."),
    ("SELL", "TRON", tron_cad, "-52.6%", "Exit ALL",
     "Speculative single crypto stock -53%. Free ~$3,343."),
    ("SELL", "MSTR", mstr_cad, "-53.6%", "Exit ALL",
     "Leveraged BTC proxy; not core. Free ~$117."),
    ("SELL", "MSFT", msft_cad, "-7.5%",  "Exit (fractional)",
     "Only 0.12 share — not meaningful. Free ~$66."),
    ("KEEP", "SHOP", 330.10,   "+20.5%", "Hold for now",
     "Single name in profit; cap at 5% of TFSA going forward."),
    ("KEEP", "XEQT", 178.16,   "+0.7%",  "Hold + add",
     "Core all-equity ETF — keep adding via DCA."),
    ("KEEP", "VFV",  368.74,   "+7.5%",  "Hold + add",
     "S&P 500 core — keep adding."),
    ("KEEP", "XEI",   39.10,   "+3.2%",  "Hold + add",
     "Dividend ballast — keep small."),
]
r = 4
freed = 0
for action, sym, val, pl, dec, why in decisions:
    fill = SELL_FILL if action == "SELL" else KEEP_FILL
    if action == "SELL":
        freed += val
    row_out(ws, r, [action, sym, val, pl, dec, why], fill=fill, money_cols=[3])
    r += 1
row_out(ws, r, ["FREED CASH", "", freed, "", "Redeploy",
                "Buy XEQT/VFV/XIC/XEI in 50/25/15/10 split"],
        bold=True, fill=TOTAL_FILL, money_cols=[3])

r += 3
ws.cell(row=r, column=1, value="Redeploy freed cash into TFSA ETF core").font = SUB_FONT
r += 1
write_header(ws, r, ["ETF", "Target %", "Buy ($)", "Role", "", ""],
             widths=[10, 12, 18, 55, 4, 4])
r += 1
for sym, pct, role in [
    ("XEQT", 0.50, "Global all-equity core"),
    ("VFV",  0.25, "US S&P 500"),
    ("XIC",  0.15, "Canadian broad market"),
    ("XEI",  0.10, "Canadian dividend"),
]:
    row_out(ws, r, [sym, pct, freed*pct, role, "", ""],
            fill=BUY_FILL, money_cols=[3], pct_cols=[2])
    r += 1
ws.cell(row=r+1, column=1,
        value="Important: TFSA capital losses are NOT tax-deductible. Selling does not recover losses for tax purposes."
        ).font = Font(italic=True, color="C00000")
ws.merge_cells(start_row=r+1, start_column=1, end_row=r+1, end_column=6)

# RRSP Plan
ws = wb.create_sheet("RRSP Plan")
ws.cell(row=1, column=1, value="RRSP — Deploy $8,461 Now + Plan for GIC Maturity").font = TITLE_FONT
ws.merge_cells("A1:F1")
write_header(ws, 3,
             ["Stage", "When", "ETF", "Target %", "Amount (CAD)", "Role"],
             widths=[12, 26, 10, 12, 18, 38])
stage1 = 8460.86
stage2 = 25000
alloc = [
    ("XEQT", 0.50, "Global all-equity core"),
    ("VFV",  0.25, "US S&P 500"),
    ("XIC",  0.15, "Canadian broad market"),
    ("XEI",  0.10, "Canadian dividend"),
]
r = 4
for sym, pct, role in alloc:
    row_out(ws, r, ["Stage 1", "This week", sym, pct, stage1*pct, role],
            fill=BUY_FILL, money_cols=[5], pct_cols=[4])
    r += 1
row_out(ws, r, ["Stage 1 TOTAL", "", "", 1.0, stage1, ""],
        bold=True, fill=TOTAL_FILL, money_cols=[5], pct_cols=[4])
r += 2
for sym, pct, role in alloc:
    row_out(ws, r, ["Stage 2", "Nov 23, 2026 (GIC matures)", sym, pct, stage2*pct, role],
            fill=BUY_FILL, money_cols=[5], pct_cols=[4])
    r += 1
row_out(ws, r, ["Stage 2 TOTAL", "", "", 1.0, stage2, ""],
        bold=True, fill=TOTAL_FILL, money_cols=[5], pct_cols=[4])

r += 3
ws.cell(row=r, column=1, value="RRSP final target after both stages").font = SUB_FONT
r += 1
write_header(ws, r, ["ETF", "Target %", "Final $ Target", "Existing $", "Top-up Needed", ""],
             widths=[10, 12, 20, 18, 20, 4])
r += 1
final = stage1 + stage2 + 2611.57
existing_rrsp = {"XEQT": 445.40, "VFV": 1290.59, "XIC": 333.36, "XEI": 391.00 + 151.22}
for sym, pct, _ in alloc:
    tgt = final * pct
    have = existing_rrsp.get(sym, 0)
    row_out(ws, r, [sym, pct, tgt, have, tgt - have, ""],
            money_cols=[3, 4, 5], pct_cols=[2])
    r += 1

# FHSA Plan
ws = wb.create_sheet("FHSA Plan")
ws.cell(row=1, column=1, value="FHSA — Hold + DCA (home <3 years)").font = TITLE_FONT
ws.merge_cells("A1:F1")
write_header(ws, 3,
             ["Holding", "Value (CAD)", "Action", "Yield/Return", "Notes", ""],
             widths=[36, 16, 18, 16, 55, 4])
fhsa_current = [
    ("GIC 3.30% (mat 2027-05-04)", 13400, "HOLD",         0.033, "Guaranteed; matches home timeline"),
    ("VFV (S&P 500)",              1474.96, "HOLD",       0.10,  "Long-term growth"),
    ("XIC (Canadian broad)",       1000.08, "HOLD",       0.08,  "Diversification"),
    ("VDY (Canadian dividend)",     756.10, "HOLD",       0.07,  "Dividend income"),
    ("XEI (Dividend)",              547.40, "HOLD",       0.07,  "Slight overlap with VDY"),
    ("Cash",                        250.17, "Move to PSA",0.045, "Park in CASH/PSA"),
]
r = 4
for h, v, a, ret, note in fhsa_current:
    row_out(ws, r, [h, v, a, ret, note, ""],
            money_cols=[2], pct_cols=[4])
    r += 1
row_out(ws, r, ["TOTAL", 17428.71, "", 0.045, "Blended ~4.5%", ""],
        bold=True, fill=TOTAL_FILL, money_cols=[2], pct_cols=[4])

r += 3
ws.cell(row=r, column=1, value="New monthly contributions ($666/month)").font = SUB_FONT
r += 1
write_header(ws, r, ["Vehicle", "Allocation %", "$/month", "Annual $", "Notes", ""],
             widths=[18, 14, 14, 14, 55, 4])
r += 1
for sym, pct, note in [
    ("PSA.TO", 0.70, "Capital preservation; near-term home purchase"),
    ("XEQT.TO", 0.20, "Small growth sleeve — optional"),
    ("XIC.TO",  0.10, "Canadian equity"),
]:
    row_out(ws, r, [sym, pct, 666*pct, 666*pct*12, note, ""],
            fill=BUY_FILL, money_cols=[3, 4], pct_cols=[2])
    r += 1

# Monthly DCA
ws = wb.create_sheet("Monthly DCA")
ws.cell(row=1, column=1, value="12-Month Monthly DCA schedule").font = TITLE_FONT
ws.merge_cells("A1:I1")
write_header(ws, 3,
             ["Month", "FHSA→PSA", "FHSA→XEQT",
              "RRSP→XEQT", "RRSP→VFV", "RRSP→XIC", "RRSP→XEI",
              "TFSA→ETFs", "Month Total"],
             widths=[10, 12, 12, 12, 12, 12, 12, 12, 14])
fhsa_psa  = 466
fhsa_xeqt = 200
rrsp_xeqt = 734
rrsp_vfv  = 367
rrsp_xic  = 220
rrsp_xei  = 147
tfsa_dca  = 300
monthly_total = fhsa_psa + fhsa_xeqt + rrsp_xeqt + rrsp_vfv + rrsp_xic + rrsp_xei + tfsa_dca
months = ["Jul 26", "Aug 26", "Sep 26", "Oct 26", "Nov 26", "Dec 26",
          "Jan 27", "Feb 27", "Mar 27", "Apr 27", "May 27", "Jun 27"]
r = 4
for m in months:
    row_out(ws, r,
            [m, fhsa_psa, fhsa_xeqt, rrsp_xeqt, rrsp_vfv, rrsp_xic, rrsp_xei,
             tfsa_dca, monthly_total],
            money_cols=list(range(2, 10)))
    r += 1
row_out(ws, r,
        ["YEAR TOTAL",
         fhsa_psa*12, fhsa_xeqt*12, rrsp_xeqt*12, rrsp_vfv*12, rrsp_xic*12,
         rrsp_xei*12, tfsa_dca*12, monthly_total*12],
        bold=True, fill=TOTAL_FILL, money_cols=list(range(2, 10)))

# Expected Return
ws = wb.create_sheet("Expected Return")
ws.cell(row=1, column=1, value="Year-1 Expected Return (actual balances)").font = TITLE_FONT
ws.merge_cells("A1:E1")
write_header(ws, 3,
             ["Account", "Avg Capital (CAD)", "Blended Return", "Expected $ Gain", "Notes"],
             widths=[10, 22, 18, 22, 55])

fhsa_start = 17428.71
rrsp_start = 36072.43
tfsa_start = 7914.41
fhsa_contrib = 666*12
rrsp_contrib = 1468*12
tfsa_contrib = 300*12
fhsa_avg = fhsa_start + fhsa_contrib/2
rrsp_avg = rrsp_start + rrsp_contrib/2
tfsa_avg = tfsa_start + tfsa_contrib/2
fhsa_ret = 0.045
rrsp_ret = 0.075
tfsa_ret = 0.085

rows_er = [
    ("FHSA", fhsa_avg, fhsa_ret, "GIC + ETFs; conservative for home timeline"),
    ("RRSP", rrsp_avg, rrsp_ret, "GIC drag first half; ETF deployment lifts H2"),
    ("TFSA", tfsa_avg, tfsa_ret, "Post-cleanup ETF core + small SHOP"),
]
r = 4
total_gain = 0
total_avg = 0
for acct, avg, ret, note in rows_er:
    gain = avg * ret
    total_gain += gain
    total_avg += avg
    row_out(ws, r, [acct, avg, ret, gain, note],
            money_cols=[2, 4], pct_cols=[3])
    r += 1
blended = total_gain / total_avg
row_out(ws, r, ["TOTAL", total_avg, blended, total_gain,
                f"Blended Year-1 ~{blended*100:.2f}%"],
        bold=True, fill=TOTAL_FILL, money_cols=[2, 4], pct_cols=[3])

r += 3
ws.cell(row=r, column=1, value="Scenario sensitivity").font = SUB_FONT
r += 1
write_header(ws, r, ["Scenario", "Return %", "$ Impact", "", ""],
             widths=[28, 14, 24, 4, 4])
r += 1
for name, ret in [
    ("Bear (-15% equities)", -0.05),
    ("Base (expected)",       blended),
    ("Bull (+18% equities)",  0.13),
    ("Long-run CAGR target",  0.09),
]:
    row_out(ws, r, [name, ret, total_avg*ret, "", ""],
            money_cols=[3], pct_cols=[2])
    r += 1

r += 2
ws.cell(row=r, column=1,
        value="Note: Year-1 is dragged by GICs (RRSP matures Nov 2026, FHSA May 2027). From Year-2, blended rises to ~8-9% as GIC capital moves to ETFs."
        ).alignment = LEFT
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)

# Action Checklist
ws = wb.create_sheet("Action Checklist")
ws.cell(row=1, column=1, value="One-Year Action Checklist").font = TITLE_FONT
ws.merge_cells("A1:D1")
write_header(ws, 3, ["When", "Account", "Action", "Status"],
             widths=[18, 10, 80, 10])
actions = [
    ("This week",    "TFSA", "SELL BULL (350 sh) and TRON (1500 sh). Frees ~$6,730."),
    ("This week",    "TFSA", "SELL MSTR (1 sh) and MSFT (0.12 sh)."),
    ("This week",    "TFSA", "BUY XEQT 50% / VFV 25% / XIC 15% / XEI 10% with freed cash."),
    ("This week",    "RRSP", "DEPLOY $8,461 → XEQT $4,230 / VFV $2,115 / XIC $1,269 / XEI $846."),
    ("This week",    "FHSA", "Move $250 cash into PSA.TO."),
    ("Week 2",       "ALL",  "Set up monthly DCA per 'Monthly DCA' tab."),
    ("Month 3",      "ALL",  "Confirm DCA executing; review allocations."),
    ("Month 5",      "RRSP", "Prepare: GIC matures Nov 23, 2026."),
    ("Nov 23, 2026", "RRSP", "REDEPLOY $25,000 into XEQT 50 / VFV 25 / XIC 15 / XEI 10."),
    ("Month 9",      "ALL",  "Mid-year rebalance; trim anything >5% over target."),
    ("Month 12",     "ALL",  "Annual review; reassess FHSA timeline."),
    ("May 4, 2027",  "FHSA", "GIC matures — decide based on home purchase timing."),
]
r = 4
for when, acct, act in actions:
    row_out(ws, r, [when, acct, act, "☐"])
    r += 1

wb.save(OUT)
print(f"Created: {OUT}")
