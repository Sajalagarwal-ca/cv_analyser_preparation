# CV Analyser & Interview Preparation

A personal workspace for data-science interview preparation, Python refreshers, and portfolio-supporting tools.

## Contents

### Interview prep (HTML — open in browser)
- **[DataScientist_Interview_Playbook.html](DataScientist_Interview_Playbook.html)** — opening pitches (30s / 60s / 2min), STAR project narratives, technical + behavioural + GenAI Q&A drills.
- **[Python_DataScience_Refresher.html](Python_DataScience_Refresher.html)** — short course covering Python basics, NumPy, Pandas (load / clean / transform / merge), feature engineering, viz, and scikit-learn workflow.
- **[Interview_Prep.html](Interview_Prep.html)** — general 2-hour prep sheet.
- **[Interview_Prep_PostgreSQL.html](Interview_Prep_PostgreSQL.html)** / [`.md`](Interview_Prep_PostgreSQL.md) — SQL / PostgreSQL prep.
- **[Tiger_Analytics_Interview_Prep.html](Tiger_Analytics_Interview_Prep.html)** — company-specific prep.
- **[python_practice.html](python_practice.html)** — practice snippets.
- **[AI_Agency_7Day_Roadmap.html](AI_Agency_7Day_Roadmap.html)** — 7-day GenAI upskilling plan.

### Resume & portfolio artefacts
- **[Sajal_Agarwal_Resume_Updated.md](Sajal_Agarwal_Resume_Updated.md)** — canonical resume in Markdown.
- Various PDF/DOCX exports (`Sajal_Agarwal_*.pdf/docx`).
- Project portfolio PDFs: Credit Risk, Healthcare Premium, RAG Document Reader, LangChain NL-to-PostgreSQL.

### Utility scripts
- **[_build_resume.py](_build_resume.py)** — generates resume DOCX/PDF from the Markdown source.
- **[_build_etf_strategy.py](_build_etf_strategy.py)** — builds ETF strategy workbook.
- **[wheel_screener.py](wheel_screener.py)** + **[Wheel_Dashboard.html](Wheel_Dashboard.html)** — options wheel-strategy screener + dashboard.
- **[refresh_dashboard.bat](refresh_dashboard.bat)** — Windows helper to refresh the wheel dashboard.

## Quick start

```powershell
# create & activate a venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install core deps
pip install pandas numpy scikit-learn xgboost prophet matplotlib seaborn streamlit
```

Open any `.html` file directly in a browser — everything is self-contained (no build step).

## Author

**Sajal Agarwal** — Senior Data Scientist / GenAI Engineer
Portfolio: <https://sajalagarwal-ca.github.io/portfolio.github.io/>
