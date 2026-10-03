# Dark Store Down — Streamlit version

Zipto Quick Commerce · Noida Cluster Review. This is the Python / Streamlit / Plotly
conversion of the validated HTML dashboard. No JavaScript app, no HTML dashboard, no iframe.

## Files

| File | Purpose |
|---|---|
| `app.py` | The complete application (data, calculations, charts, all pages) |
| `requirements.txt` | Python dependencies |
| `.streamlit/config.toml` | Dark theme so native Streamlit widgets match the design |
| `README_STREAMLIT.md` | This file |

Keep `app.py` and the `.streamlit` folder in the same directory.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## Pages

- **Home** – business question, executive snapshot, 8-step story, three lanes
- **Dashboard** – tabs: A · Store Performance, B · Delivery & Fulfilment, C · Product & Promotion
- **Findings** – F1–F5, supporting exploratory evidence, Data Quality Audit — After Cleaning,
  validation note, reconciliation (✅ checks), Methodology & Definitions
- **COO Decision** – Priority Investigation: S07 & S03, action plan, "What would make us wrong?"

## How the numbers work

The validated dataset extracted from the HTML dashboard is embedded in `app.py` (`DATA`).
Every displayed metric is calculated from it in Python (`build_store_dataframe()`), e.g.

```
Normalized Monthly Profit = contribution × 30 ÷ operating days − monthly rent
```

The reconciliation table on the Findings page compares the dashboard values against the
MySQL-verified results and shows ✅ when they match.

## Notes

- The only raw HTML in the app is a small CSS block and the brand/title text (styling only).
- Hover any bar in a chart to see the arithmetic behind it.
- Promo-floor leakage is *potential* discount leakage, not guaranteed savings. The exploratory
  benchmark gaps overlap and must not be summed into one financial impact.
