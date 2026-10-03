"""
DARK STORE DOWN — Zipto Quick Commerce — Noida Cluster Review
Streamlit + Pandas + Plotly version of the validated HTML dashboard.

Run with:   streamlit run app.py

All analytical content (data, formulas, findings, wording) is carried over from the
validated HTML dashboard. The embedded dataset below was extracted from that file;
every displayed metric is calculated from it in Python.
"""
from __future__ import annotations

import html as _htmllib
import inspect
import re

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Dark Store Down · Zipto Noida Cluster Review",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------------
# DESIGN TOKENS (same palette as the HTML dashboard)
# ----------------------------------------------------------------------------------
BG, SURFACE, SURFACE2, BORDER = "#070B12", "#0D1420", "#111B2A", "#1D2A3A"
TEXT, MUTED = "#F3F7FA", "#8B9AAF"
ACCENT, DANGER, WARNING, INFO, NEUTRAL = "#35E0C0", "#FF5C62", "#F4B942", "#5B8DEF", "#66758A"
DANGER_SOFT = "#FF9AA0"

# Streamlit markdown colour names for inline colouring
TONE = {"teal": "green", "info": "blue", "red": "red", "amber": "orange", "neutral": "gray", "": None}

# ----------------------------------------------------------------------------------
# VALIDATED DATASET (extracted from the HTML dashboard — do not edit)
# ----------------------------------------------------------------------------------
DATA = {'S': [{'id': 'S01',
        'operating_days': 42,
        'same_ts': 0,
        'name': 'Sector 18 Hub',
        'rent': 178000,
        'orders': 6091,
        'deliv': 5772,
        'ret': 201,
        'canc': 118,
        'contrib': 459494.7,
        'dcost_sum': 170790.95,
        'late': 2879,
        'mins_sum': 61138.0,
        'dist_sum': 17277.7,
        'dist_n': 5702,
        'promo_n': 1269,
        'disc_sum': 147289.07,
        'dlv_contrib': 547526.24,
        'dlv_dcost': 161918.51,
        'fresh50': 43},
       {'id': 'S02',
        'operating_days': 42,
        'same_ts': 0,
        'name': 'Sector 62 Express',
        'rent': 162000,
        'orders': 5877,
        'deliv': 5584,
        'ret': 178,
        'canc': 115,
        'contrib': 457583.42,
        'dcost_sum': 164705.42,
        'late': 2810,
        'mins_sum': 59322.0,
        'dist_sum': 16508.18,
        'dist_n': 5523,
        'promo_n': 1217,
        'disc_sum': 141549.21,
        'dlv_contrib': 535758.45,
        'dlv_dcost': 156391.31,
        'fresh50': 46},
       {'id': 'S03',
        'operating_days': 42,
        'same_ts': 933,
        'trips': 5564,
        'name': 'Sector 137 Riverside',
        'rent': 196000,
        'orders': 5564,
        'deliv': 5001,
        'ret': 442,
        'canc': 121,
        'contrib': 79735.03,
        'dcost_sum': 233600.32,
        'late': 3617,
        'mins_sum': 62605.0,
        'dist_sum': 14788.79,
        'dist_n': 4949,
        'promo_n': 1448,
        'disc_sum': 245933.38,
        'dlv_contrib': 278970.11,
        'dlv_dcost': 209970.68,
        'fresh50': 557},
       {'id': 'S04',
        'operating_days': 42,
        'same_ts': 0,
        'name': 'Greater Noida Alpha',
        'rent': 152000,
        'orders': 5622,
        'deliv': 5333,
        'ret': 166,
        'canc': 123,
        'contrib': 444250.81,
        'dcost_sum': 157039.62,
        'late': 2723,
        'mins_sum': 56975.0,
        'dist_sum': 15828.38,
        'dist_n': 5265,
        'promo_n': 1158,
        'disc_sum': 132192.85,
        'dlv_contrib': 513361.63,
        'dlv_dcost': 148952.71,
        'fresh50': 33},
       {'id': 'S05',
        'operating_days': 42,
        'same_ts': 0,
        'name': 'Sector 76 Central',
        'rent': 181000,
        'orders': 4688,
        'deliv': 4436,
        'ret': 150,
        'canc': 102,
        'contrib': 359050.77,
        'dcost_sum': 130964.33,
        'late': 2211,
        'mins_sum': 46889.0,
        'dist_sum': 13151.11,
        'dist_n': 4391,
        'promo_n': 941,
        'disc_sum': 108483.31,
        'dlv_contrib': 425106.3,
        'dlv_dcost': 124023.57,
        'fresh50': 31},
       {'id': 'S06',
        'operating_days': 42,
        'same_ts': 0,
        'name': 'Noida Extension North',
        'rent': 158000,
        'orders': 6153,
        'deliv': 5811,
        'ret': 210,
        'canc': 132,
        'contrib': 460390.89,
        'dcost_sum': 172101.53,
        'late': 2916,
        'mins_sum': 61657.0,
        'dist_sum': 17191.59,
        'dist_n': 5759,
        'promo_n': 1166,
        'disc_sum': 129870.21,
        'dlv_contrib': 549893.47,
        'dlv_dcost': 162453.78,
        'fresh50': 37},
       {'id': 'S07',
        'operating_days': 42,
        'same_ts': 1082,
        'trips': 5687,
        'name': 'Sector 44 Metro',
        'rent': 228000,
        'orders': 5687,
        'deliv': 4763,
        'ret': 797,
        'canc': 127,
        'contrib': -202668.46,
        'dcost_sum': 239530.15,
        'late': 3434,
        'mins_sum': 59421.0,
        'dist_sum': 14235.59,
        'dist_n': 4716,
        'promo_n': 1366,
        'disc_sum': 231901.38,
        'dlv_contrib': 171825.86,
        'dlv_dcost': 200416.31,
        'fresh50': 523},
       {'id': 'S08',
        'operating_days': 42,
        'same_ts': 0,
        'name': 'Sector 104 Gardens',
        'rent': 146000,
        'orders': 5309,
        'deliv': 5041,
        'ret': 162,
        'canc': 106,
        'contrib': 423669.02,
        'dcost_sum': 148857.98,
        'late': 2542,
        'mins_sum': 53664.0,
        'dist_sum': 15134.52,
        'dist_n': 4993,
        'promo_n': 1052,
        'disc_sum': 118119.69,
        'dlv_contrib': 488388.6,
        'dlv_dcost': 141255.0,
        'fresh50': 30},
       {'id': 'S09',
        'operating_days': 14,
        'same_ts': 0,
        'name': 'Sector 150 Sports City',
        'rent': 172000,
        'orders': 1815,
        'deliv': 1712,
        'ret': 72,
        'canc': 31,
        'contrib': 134691.69,
        'dcost_sum': 50728.75,
        'late': 872,
        'mins_sum': 18052.0,
        'dist_sum': 5185.02,
        'dist_n': 1694,
        'promo_n': 378,
        'disc_sum': 41840.39,
        'dlv_contrib': 165689.21,
        'dlv_dcost': 47869.42,
        'fresh50': 6},
       {'id': 'S10',
        'operating_days': 42,
        'same_ts': 0,
        'name': 'Sector 51 Junction',
        'rent': 165000,
        'orders': 5327,
        'deliv': 5057,
        'ret': 178,
        'canc': 92,
        'contrib': 409561.23,
        'dcost_sum': 149503.58,
        'late': 2529,
        'mins_sum': 53335.0,
        'dist_sum': 14978.63,
        'dist_n': 4997,
        'promo_n': 1101,
        'disc_sum': 126318.97,
        'dlv_contrib': 487453.59,
        'dlv_dcost': 141913.37,
        'fresh50': 34}],
 'C': {'OTH': {'BAKERY': [1334498.12, 1086804.51],
               'BEVERAGES': [3790891.0, 2863160.81],
               'DAIRY & EGGS': [2373308.05, 1954363.07],
               'FRUITS & VEGETABLES': [2844688.78, 2152634.03],
               'HOUSEHOLD': [2434754.13, 1485275.36],
               'MEAT & SEAFOOD': [1858082.17, 1733778.35],
               'PERSONAL CARE': [2964207.28, 1892617.16],
               'SNACKS & PACKAGED': [3769796.28, 2270089.41]},
       'S03': {'BAKERY': [161417.86, 131807.08],
               'BEVERAGES': [485654.55, 369098.36],
               'DAIRY & EGGS': [300170.52, 247685.78],
               'FRUITS & VEGETABLES': [369144.17, 277948.64],
               'HOUSEHOLD': [304750.04, 186217.61],
               'MEAT & SEAFOOD': [246533.94, 229670.41],
               'PERSONAL CARE': [381846.96, 243307.75],
               'SNACKS & PACKAGED': [489552.39, 295622.63]},
       'S07': {'BAKERY': [250755.7, 205892.21],
               'BEVERAGES': [295515.77, 223566.19],
               'DAIRY & EGGS': [448162.89, 368912.71],
               'FRUITS & VEGETABLES': [538747.28, 405572.08],
               'HOUSEHOLD': [192322.29, 117728.98],
               'MEAT & SEAFOOD': [358312.37, 334979.48],
               'PERSONAL CARE': [233349.36, 149740.42],
               'SNACKS & PACKAGED': [288595.22, 175027.96]}},
 'P': [{'store': 'S03', 'promo': 'FLAT75', 'n': 220, 'disc': 74.81, 'cpo': 40.88},
       {'store': 'S03', 'promo': 'FRESH50', 'n': 557, 'disc': 290.28, 'cpo': -178.93},
       {'store': 'S03', 'promo': 'NEW100', 'n': 117, 'disc': 99.26, 'cpo': 33.95},
       {'store': 'S03', 'promo': 'No Promo', 'n': 3553, 'disc': 0.0, 'cpo': 101.71},
       {'store': 'S03', 'promo': 'SAVE20', 'n': 304, 'disc': 117.48, 'cpo': -4.96},
       {'store': 'S03', 'promo': 'WEEKEND15', 'n': 250, 'disc': 81.85, 'cpo': 23.24},
       {'store': 'S07', 'promo': 'FLAT75', 'n': 194, 'disc': 74.91, 'cpo': 20.26},
       {'store': 'S07', 'promo': 'FRESH50', 'n': 523, 'disc': 291.73, 'cpo': -205.48},
       {'store': 'S07', 'promo': 'NEW100', 'n': 112, 'disc': 100.0, 'cpo': 3.05},
       {'store': 'S07', 'promo': 'No Promo', 'n': 3397, 'disc': 0.0, 'cpo': 82.87},
       {'store': 'S07', 'promo': 'SAVE20', 'n': 302, 'disc': 113.65, 'cpo': -24.69},
       {'store': 'S07', 'promo': 'WEEKEND15', 'n': 235, 'disc': 82.0, 'cpo': 4.06}],
 'NET': [{'promo': 'CITY150', 'n': 82, 'cpo': 95.6},
         {'promo': 'FLAT75', 'n': 2099, 'cpo': 76.14},
         {'promo': 'FRESH50', 'n': 1340, 'cpo': -205.88},
         {'promo': 'NEW100', 'n': 973, 'cpo': 74.03},
         {'promo': 'No Promo', 'n': 37414, 'cpo': 108.11},
         {'promo': 'SAVE20', 'n': 3466, 'cpo': 8.32},
         {'promo': 'WEEKEND15', 'n': 3136, 'cpo': 40.34}],
 'days': 42,
 'R': {'same': {'n': 2015, 'ret': 689}, 'normal': {'n': 50118, 'ret': 1867}},
 'PF': {'S03': {'promo_orders': 1625, 'below': 679, 'leak42': 120209.78},
        'S07': {'promo_orders': 1663, 'below': 706, 'leak42': 124040.72}},
 'FLOOR50': 800}

PRIORITY = ("S07", "S03")          # the two negative normalized stores
PROMO_ORDER = ["No Promo", "WEEKEND15", "NEW100", "FLAT75", "SAVE20", "FRESH50"]
DELIVERY_COST_BENCHMARK = 28       # ₹/order benchmark used in the exploratory section


# ----------------------------------------------------------------------------------
# FORMATTING HELPERS
# ----------------------------------------------------------------------------------
def format_currency(v: float, d: int = 0) -> str:
    """₹ with thousands separators; negative sign in front of the symbol."""
    return f"{'-' if v < 0 else ''}₹{abs(v):,.{d}f}"


def format_k(v: float) -> str:
    return f"₹{v / 1000:.1f}K"


def format_lakh(v: float) -> str:
    return f"₹{v / 1e5:.2f}L"


def format_pct(v: float, d: int = 2) -> str:
    return f"{v:.{d}f}%"


def n2(v: float) -> str:
    return f"{v:.2f}"


def fmt_int(v: float) -> str:
    return f"{int(round(v)):,}"


def colorize(text: str, tone: str = "") -> str:
    c = TONE.get(tone)
    return f":{c}[{text}]" if c else text


def tag(text: str, tone: str = "teal") -> str:
    return colorize(f"**{text.upper()}**", tone)


# ----------------------------------------------------------------------------------
# CALCULATION LAYER
# ----------------------------------------------------------------------------------
def normalized_monthly_profit(contribution, operating_days, rent):
    """Normalized Monthly Profit = (42-day contribution × 30 ÷ operating days) − monthly rent."""
    return contribution * 30 / operating_days - rent


@st.cache_data(show_spinner=False)
def build_store_dataframe() -> pd.DataFrame:
    df = pd.DataFrame(DATA["S"])
    if "trips" not in df.columns:
        df["trips"] = np.nan
    df["nmc"] = df["contrib"] * 30 / df["operating_days"]
    df["pnl"] = normalized_monthly_profit(df["contrib"], df["operating_days"], df["rent"])
    df["cpo"] = df["contrib"] / df["orders"]
    df["opd"] = df["orders"] / df["operating_days"]
    has_trips = df["trips"].fillna(0) > 0
    df["sts"] = np.where(has_trips, df["same_ts"] / df["trips"].where(has_trips, 1) * 100, 0.0)
    df["rr"] = df["ret"] / df["orders"] * 100
    df["lr"] = df["late"] / df["deliv"] * 100
    df["dc"] = df["dcost_sum"] / df["orders"]
    df["tm"] = df["mins_sum"] / df["deliv"]
    df["ds"] = df["dist_sum"] / df["dist_n"]
    df["pu"] = df["promo_n"] / df["deliv"] * 100
    df["di"] = df["disc_sum"] / df["deliv"]
    df["dcpo"] = df["dlv_contrib"] / df["deliv"]
    return df


DF = build_store_dataframe()
STORES = {r["id"]: r for r in DF.to_dict("records")}
OTH_DF = DF[~DF["id"].isin(PRIORITY)]
b, a, s9 = STORES["S07"], STORES["S03"], STORES["S09"]
DAYS = DATA["days"]
ORDERS = int(DF["orders"].sum())
TOTAL_CONTRIB = float(DF["contrib"].sum())
NEG_STORES = sorted(DF.loc[DF["pnl"] < 0, "id"].tolist(), reverse=True)
POS_COUNT = len(DF) - len(NEG_STORES)


def oth_avg(col: str) -> float:
    """Simple average of store-level values across the 8 stores other than S03/S07."""
    return float(OTH_DF[col].mean())


B_RR = float((OTH_DF["rr"] / 100).mean())   # other-8 return rate (fraction)
B_DI = oth_avg("di")                         # other-8 discount per delivered order

PF = {}
for _sid, _p in DATA["PF"].items():
    PF[_sid] = {
        **_p,
        "pct": _p["below"] / _p["promo_orders"] * 100,
        "leak30": _p["leak42"] * 30 / DAYS,
    }
RET = DATA["R"]
RR_SAME = RET["same"]["ret"] / RET["same"]["n"] * 100
RR_NORMAL = RET["normal"]["ret"] / RET["normal"]["n"] * 100
FLOOR50 = DATA["FLOOR50"]

PROMO = {(p["store"], p["promo"]): p for p in DATA["P"]}
NET_PROMO = {p["promo"]: p for p in DATA["NET"]}
FRESH50_ALL = int(DF["fresh50"].sum())
FRESH50_PRIORITY = int(a["fresh50"] + b["fresh50"])
CATS = list(DATA["C"]["OTH"].keys())


def category_margin(group: str, cat: str) -> float:
    rev, cost = DATA["C"][group][cat]
    return (rev - cost) / rev * 100


def opportunity(store_id: str) -> dict:
    """Exploratory benchmark gaps (supporting analysis only, overlapping, not additive)."""
    s = STORES[store_id]
    excess_returns = s["ret"] - B_RR * s["orders"]
    ret = excess_returns * s["dcpo"] * 30 / DAYS
    dc42 = s["dcost_sum"] - DELIVERY_COST_BENCHMARK * s["orders"]
    dis42 = (s["di"] - B_DI) * s["deliv"]
    return {
        "s": s, "excess_returns": excess_returns, "ret": ret,
        "dc42": dc42, "dc": dc42 * 30 / DAYS, "dis42": dis42, "dis": dis42 * 30 / DAYS,
    }


OPP = {"S03": opportunity("S03"), "S07": opportunity("S07")}


# ----------------------------------------------------------------------------------
# STYLING (CSS only — no HTML pages, no JavaScript)
# ----------------------------------------------------------------------------------
CSS = f"<style>:root{{--bg:{BG};--surface:{SURFACE};--surface2:{SURFACE2};--border:{BORDER};--text:{TEXT};--muted:{MUTED};--accent:{ACCENT};--danger:{DANGER};--warning:{WARNING};--info:{INFO};--neutral:{NEUTRAL};}}" + """
/* =============== BASE =============== */
html, body, .stApp { background: var(--bg); color: var(--text);
  font-family: Inter, "Segoe UI", system-ui, -apple-system, Roboto, "Helvetica Neue", Arial, sans-serif; }
.stApp [data-testid="stAppViewContainer"] {
  background: radial-gradient(1100px 520px at 78% -8%, rgba(53,224,192,.07), transparent 60%),
              radial-gradient(900px 480px at 8% 4%, rgba(91,141,239,.05), transparent 60%), var(--bg); }
#MainMenu, footer, [data-testid="stDecoration"], [data-testid="stToolbar"], [data-testid="stStatusWidget"] { visibility: hidden; display: none; }
[data-testid="stHeader"] { background: transparent; height: 2.4rem; }
.block-container, [data-testid="stMainBlockContainer"] {
  max-width: 100% !important; width: 100% !important; padding: 1.1rem 2.4rem 3rem 2.4rem !important; }
h1, h2, h3, h4 { letter-spacing: -0.01em; }
h3 { font-size: 1.1rem; font-weight: 700; padding-top: .25rem; }
h4 { font-weight: 700; }
code { background: rgba(53,224,192,.10); color: #8FF0DC; border-radius: 5px; padding: .08rem .35rem; font-size: .88em; }
[data-testid="stCaptionContainer"], .stCaption { color: var(--muted); }
hr { border-color: var(--border); }
::-webkit-scrollbar { width: 10px; height: 10px; } ::-webkit-scrollbar-thumb { background: #1d2a3a; border-radius: 8px; }
/* =============== PAGE HEADER =============== */
.ph { margin: .2rem 0 1.4rem; }
.ph-e { color: var(--accent); font-size: .78rem; font-weight: 800; letter-spacing: .2em; margin-bottom: .45rem; }
.ph-e::before { content: ""; display: inline-block; width: 22px; height: 2px; background: var(--accent); vertical-align: middle; margin-right: .6rem; }
.ph-t { font-size: 2.55rem; font-weight: 850; letter-spacing: -0.025em; line-height: 1.08; margin: 0; padding: 0; color: var(--text); }
.ph-s { color: var(--muted); font-size: 1.02rem; max-width: 980px; margin: .6rem 0 0; line-height: 1.55; }
.sec { margin: 2.1rem 0 .9rem; display: flex; align-items: baseline; gap: .9rem; flex-wrap: wrap; border-left: 3px solid var(--accent); padding-left: .8rem; }
.sec-t { font-size: 1.4rem; font-weight: 780; letter-spacing: -0.01em; }
.sec-c { color: var(--muted); font-size: .9rem; }
.eb { color: var(--accent); font-size: .74rem; font-weight: 800; letter-spacing: .18em; margin: .2rem 0 .3rem; }
/* =============== GLASS CARDS =============== */
[data-testid="stVerticalBlockBorderWrapper"] {
  background: linear-gradient(150deg, rgba(20,31,48,.82), rgba(12,19,31,.88));
  border: 1px solid rgba(255,255,255,.07) !important; border-radius: 16px;
  box-shadow: 0 1px 2px rgba(0,0,0,.4), 0 10px 28px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.04);
  backdrop-filter: blur(6px); transition: border-color .2s ease, transform .2s ease, box-shadow .2s ease; }
[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: rgba(53,224,192,.28) !important; }
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"] { box-shadow: none; background: rgba(255,255,255,.025); backdrop-filter: none; }
[data-testid="stAlert"] { border-radius: 12px; border: 1px solid rgba(255,255,255,.07); }
[data-testid="stDataFrame"] { overflow-x: auto; border-radius: 12px; border: 1px solid var(--border); }
[data-testid="stPlotlyChart"] { width: 100%; }
[data-testid="stMetric"] { background: transparent; padding: .1rem 0; }
[data-testid="stMetricValue"] { font-weight: 800; font-size: 1.8rem; }
[data-testid="stMetricLabel"] p { color: var(--muted); font-size: .85rem; }
/* =============== KPI CARDS =============== */
.kpi { position: relative; overflow: hidden; border-radius: 16px; padding: 1.05rem 1.2rem 1rem; min-height: 124px; height: 100%;
  background: linear-gradient(150deg, rgba(22,34,52,.9), rgba(12,19,31,.92)); border: 1px solid rgba(255,255,255,.07);
  box-shadow: 0 10px 26px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.05);
  transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease; margin-bottom: .6rem; }
.kpi::before { content: ""; position: absolute; left: 0; top: 0; right: 0; height: 3px; background: var(--ac, var(--accent)); box-shadow: 0 0 18px var(--ac, var(--accent)); opacity: .95; }
.kpi::after { content: ""; position: absolute; right: -40px; top: -40px; width: 130px; height: 130px; border-radius: 50%; background: var(--ac, var(--accent)); opacity: .07; filter: blur(8px); }
.kpi:hover { transform: translateY(-2px); border-color: rgba(255,255,255,.16); box-shadow: 0 14px 32px rgba(0,0,0,.36); }
.kpi-teal { --ac: #35E0C0; } .kpi-red { --ac: #FF5C62; } .kpi-amber { --ac: #F4B942; } .kpi-neutral { --ac: #66758A; } .kpi-info { --ac: #5B8DEF; }
.kpi-l { color: var(--muted); font-size: .72rem; font-weight: 750; letter-spacing: .13em; text-transform: uppercase; }
.kpi-v { font-size: 2rem; font-weight: 850; letter-spacing: -0.02em; margin: .35rem 0 .25rem; line-height: 1.1; color: var(--ac, var(--accent)); word-break: break-word; }
.kpi-s { color: var(--muted); font-size: .82rem; line-height: 1.4; }
/* =============== PILLS / TEXT COLOURS =============== */
.pill { display: inline-block; font-size: .68rem; font-weight: 800; letter-spacing: .12em; padding: .22rem .6rem; border-radius: 999px; border: 1px solid; text-transform: uppercase; white-space: nowrap; }
.pill-teal { color: #35E0C0; background: rgba(53,224,192,.10); border-color: rgba(53,224,192,.35); }
.pill-red { color: #FF7C81; background: rgba(255,92,98,.10); border-color: rgba(255,92,98,.38); }
.pill-amber { color: #F4B942; background: rgba(244,185,66,.10); border-color: rgba(244,185,66,.38); }
.pill-info { color: #7FA6F5; background: rgba(91,141,239,.10); border-color: rgba(91,141,239,.38); }
.pill-neutral { color: #A6B3C4; background: rgba(102,117,138,.14); border-color: rgba(102,117,138,.4); }
.neg { color: var(--danger); } .pos { color: var(--accent); } .amb { color: var(--warning); } .mut { color: var(--muted); }
/* =============== HERO =============== */
.hero { position: relative; border-radius: 22px; padding: 2.2rem 2.4rem 2rem; margin-bottom: 1.2rem; overflow: hidden;
  background: linear-gradient(135deg, rgba(20,34,52,.95), rgba(9,15,25,.96)); border: 1px solid rgba(255,255,255,.08);
  box-shadow: 0 18px 50px rgba(0,0,0,.4); }
.hero::before { content: ""; position: absolute; right: -90px; top: -110px; width: 380px; height: 380px; border-radius: 50%;
  background: radial-gradient(circle, rgba(53,224,192,.22), transparent 65%); }
.hero::after { content: ""; position: absolute; left: 0; bottom: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--accent), transparent 70%); }
.hero-title { position: relative; font-size: 3.7rem; font-weight: 900; letter-spacing: -0.03em; line-height: 1.02; margin: .4rem 0 .5rem; }
.hero-title span { color: var(--accent); }
.hero-sub { position: relative; color: var(--muted); font-size: .98rem; letter-spacing: .16em; font-weight: 600; margin-bottom: 1.4rem; }
.bq-prem { position: relative; border-radius: 16px; padding: 1.1rem 1.4rem; background: linear-gradient(120deg, rgba(53,224,192,.14), rgba(53,224,192,.04));
  border: 1px solid rgba(53,224,192,.35); box-shadow: 0 0 0 1px rgba(53,224,192,.05), 0 8px 30px rgba(53,224,192,.08); }
.bq-l { color: var(--accent); font-size: .72rem; font-weight: 800; letter-spacing: .2em; margin-bottom: .4rem; }
.bq-t { font-size: 1.4rem; font-weight: 650; line-height: 1.4; letter-spacing: -0.01em; }
.logo-mark { display: inline-block; width: 38px; height: 38px; border-radius: 11px; position: relative;
  background: linear-gradient(135deg, #35E0C0, #1fa88f); box-shadow: 0 0 22px rgba(53,224,192,.45); }
.logo-mark::after { content: ""; position: absolute; left: 11px; top: 11px; width: 16px; height: 16px; border-radius: 4px; background: #07131a; }
.logo-mark::before { content: ""; position: absolute; left: 17px; top: 17px; width: 4px; height: 4px; border-radius: 50%; background: #35E0C0; z-index: 2; }
/* =============== GENERIC GRIDS & PANELS =============== */
.cards { display: grid; gap: 1rem; margin: .4rem 0 .6rem; }
.cards-2 { grid-template-columns: repeat(auto-fit, minmax(440px, 1fr)); }
.cards-3 { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); }
.cards-4 { grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); }
.panel { position: relative; border-radius: 16px; padding: 1.15rem 1.3rem; height: 100%;
  background: linear-gradient(150deg, rgba(20,31,48,.82), rgba(12,19,31,.88)); border: 1px solid rgba(255,255,255,.07);
  box-shadow: 0 10px 26px rgba(0,0,0,.26), inset 0 1px 0 rgba(255,255,255,.04); transition: transform .2s ease, border-color .2s ease; }
.panel:hover { transform: translateY(-2px); border-color: rgba(53,224,192,.30); }
.panel h3 { margin: .55rem 0 .35rem; padding: 0; font-size: 1.12rem; }
.panel p, .panel .tx { color: #C8D3E0; font-size: .92rem; line-height: 1.55; margin: .25rem 0; }
.panel .mutp { color: var(--muted); font-size: .88rem; }
.p-red { border-top: 3px solid var(--danger); } .p-amber { border-top: 3px solid var(--warning); }
.p-teal { border-top: 3px solid var(--accent); } .p-neutral { border-top: 3px solid var(--neutral); } .p-info { border-top: 3px solid var(--info); }
.panel-amber { background: linear-gradient(150deg, rgba(244,185,66,.12), rgba(20,26,36,.9)); border-color: rgba(244,185,66,.38); }
.stepno { display: inline-flex; width: 28px; height: 28px; align-items: center; justify-content: center; border-radius: 50%;
  background: rgba(53,224,192,.14); border: 1px solid rgba(53,224,192,.45); color: var(--accent); font-weight: 800; font-size: .85rem; margin-right: .5rem; }
/* =============== DECISION FLOW =============== */
.flow { display: flex; align-items: stretch; margin: 1rem 0 1.2rem; }
.fl-step { flex: 1 1 0; min-width: 0; border-radius: 14px; padding: .9rem .9rem 1rem; text-align: left;
  background: linear-gradient(150deg, rgba(22,34,52,.9), rgba(12,19,31,.92)); border: 1px solid rgba(255,255,255,.08); transition: transform .2s ease, border-color .2s ease; }
.fl-step:hover { transform: translateY(-2px); border-color: rgba(53,224,192,.4); }
.fl-n { width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 850; font-size: .9rem;
  color: #04231d; background: var(--accent); box-shadow: 0 0 14px rgba(53,224,192,.5); margin-bottom: .6rem; }
.fl-t { font-weight: 800; font-size: .74rem; letter-spacing: .1em; margin-bottom: .35rem; }
.fl-d { color: var(--muted); font-size: .82rem; line-height: 1.4; }
.fl-last { background: linear-gradient(150deg, rgba(53,224,192,.18), rgba(12,19,31,.92)); border-color: rgba(53,224,192,.55); }
.fl-last .fl-t { color: var(--accent); }
.fl-arrow { flex: 0 0 30px; align-self: center; height: 2px; position: relative; background: linear-gradient(90deg, rgba(53,224,192,.15), var(--accent)); }
.fl-arrow::after { content: ""; position: absolute; right: -1px; top: -5px; border: 6px solid transparent; border-left: 8px solid var(--accent); border-right: 0; }
/* =============== EVIDENCE / ROWS =============== */
.evrow { display: flex; justify-content: space-between; gap: 1rem; padding: .42rem 0; border-bottom: 1px dashed rgba(255,255,255,.07); font-size: .92rem; }
.evrow:last-child { border-bottom: 0; } .evrow span { color: var(--muted); } .evrow b { font-weight: 750; text-align: right; }
.mgrid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: .7rem; margin: .6rem 0 .8rem; }
.mtile { border-radius: 12px; padding: .7rem .8rem; background: rgba(0,0,0,.22); border: 1px solid rgba(255,255,255,.06); }
.mtile span { display: block; color: var(--muted); font-size: .7rem; letter-spacing: .08em; text-transform: uppercase; font-weight: 700; }
.mtile b { display: block; font-size: 1.3rem; font-weight: 850; margin-top: .2rem; letter-spacing: -0.01em; word-break: break-word; }
.ro-x { color: var(--muted); font-weight: 800; margin-right: .3rem; }
/* =============== FINDING CARDS =============== */
.fcard { display: flex; flex-direction: column; }
.fc-tag { font-size: .72rem; font-weight: 800; letter-spacing: .16em; text-transform: uppercase; }
.fc-red .fc-tag { color: #FF7C81; } .fc-amber .fc-tag { color: var(--warning); } .fc-teal .fc-tag { color: var(--accent); }
.fcard h3 { font-size: 1.22rem; margin: .45rem 0 .7rem; line-height: 1.3; }
.fc-dl { margin-top: .5rem; display: grid; gap: .55rem; }
.fc-dl div { padding-left: .8rem; border-left: 2px solid rgba(255,255,255,.1); font-size: .9rem; line-height: 1.5; color: #C8D3E0; }
.fc-dl div b { display: block; color: var(--muted); font-size: .68rem; letter-spacing: .14em; text-transform: uppercase; margin-bottom: .1rem; }
.fc-red .fc-dl div { border-left-color: rgba(255,92,98,.45); } .fc-amber .fc-dl div { border-left-color: rgba(244,185,66,.45); } .fc-teal .fc-dl div { border-left-color: rgba(53,224,192,.4); }
.badge-line { margin-top: .6rem; }
/* =============== COO =============== */
.exec { position: relative; border-radius: 20px; padding: 1.4rem 1.5rem 1.3rem; height: 100%;
  background: linear-gradient(150deg, rgba(34,22,30,.9), rgba(12,19,31,.95)); border: 1px solid rgba(255,92,98,.35);
  box-shadow: 0 16px 40px rgba(0,0,0,.34), 0 0 0 1px rgba(255,92,98,.05); transition: transform .2s ease; }
.exec:hover { transform: translateY(-2px); }
.exec::before { content: ""; position: absolute; left: 0; top: 0; right: 0; height: 3px; background: var(--danger); box-shadow: 0 0 22px var(--danger); border-radius: 20px 20px 0 0; }
.exec h3 { font-size: 1.6rem; margin: .6rem 0 1rem; padding: 0; font-weight: 850; letter-spacing: -0.02em; }
.exec-hero { border-radius: 14px; padding: .9rem 1.1rem; background: rgba(255,92,98,.09); border: 1px solid rgba(255,92,98,.3); margin-bottom: .9rem; }
.exec-hero span { color: var(--muted); font-size: .72rem; font-weight: 750; letter-spacing: .13em; text-transform: uppercase; }
.exec-hero b { display: block; font-size: 2.5rem; font-weight: 900; letter-spacing: -0.03em; color: var(--danger); line-height: 1.15; }
.exec-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: .7rem; }
.exposure { border-radius: 16px; padding: 1.2rem 1.4rem; background: linear-gradient(120deg, rgba(244,185,66,.12), rgba(12,19,31,.92)); border: 1px solid rgba(244,185,66,.38); }
.exposure-t { color: var(--warning); font-size: .74rem; font-weight: 800; letter-spacing: .18em; text-transform: uppercase; }
.exposure b { font-size: 2.2rem; font-weight: 900; color: var(--warning); letter-spacing: -0.02em; }
.warnbox { border-radius: 14px; padding: 1rem 1.2rem; background: rgba(244,185,66,.08); border: 1px solid rgba(244,185,66,.4); border-left: 4px solid var(--warning); margin: .2rem 0 1rem; }
.warnbox .wt { color: var(--warning); font-weight: 800; letter-spacing: .1em; font-size: .78rem; text-transform: uppercase; margin-bottom: .4rem; }
.warnbox ul { margin: 0; padding-left: 1.1rem; color: #D7DFEA; font-size: .92rem; line-height: 1.65; }
.act { display: flex; gap: .8rem; align-items: flex-start; padding: .75rem .2rem; border-bottom: 1px dashed rgba(255,255,255,.08); }
.act:last-child { border-bottom: 0; }
.act .no { flex: 0 0 30px; height: 30px; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-weight: 850; font-size: .85rem;
  color: #04231d; background: var(--accent); }
.act .ic { color: var(--accent); font-weight: 800; width: 1.2rem; text-align: center; }
.act .tx2 { font-size: .96rem; line-height: 1.4; color: #E3EAF2; flex: 1; }
.risk .ri { color: var(--warning); font-size: 1.2rem; font-weight: 800; }
.risk h4 { margin: .35rem 0 .25rem; font-size: 1rem; }
/* =============== TABS = SEGMENTED CONTROL =============== */
div[data-testid="stTabs"] [role="tablist"] { gap: .25rem; background: rgba(255,255,255,.04); border: 1px solid var(--border); border-radius: 14px; padding: .3rem; width: fit-content; max-width: 100%; overflow-x: auto; border-bottom: 1px solid var(--border); }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"], div[data-testid="stTabs"] [data-baseweb="tab-border"] { display: none !important; }
div[data-testid="stTabs"] button[role="tab"] { border-radius: 10px; padding: .55rem 1.2rem; font-weight: 700; font-size: .98rem; color: #A9B6C7; transition: all .18s ease; height: auto; }
div[data-testid="stTabs"] button[role="tab"]:hover { background: rgba(255,255,255,.06); color: var(--text); }
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] { background: rgba(53,224,192,.14); color: var(--accent);
  box-shadow: inset 0 0 0 1px rgba(53,224,192,.45), 0 0 18px rgba(53,224,192,.14); }
div[data-testid="stTabs"] [data-baseweb="tab-panel"] { padding-top: 1.1rem; }
[data-testid="stExpander"] { background: rgba(255,255,255,.03); border: 1px solid var(--border); border-radius: 14px; transition: border-color .2s ease; }
[data-testid="stExpander"]:hover { border-color: rgba(53,224,192,.35); }
[data-testid="stExpander"] summary { font-weight: 700; }
/* =============== BUTTONS / PILL RADIO =============== */
.stButton > button { border-radius: 12px; padding: .6rem 1.4rem; font-weight: 700; border: 1px solid var(--border); transition: all .18s ease; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, #35E0C0, #22b79d); color: #04231d; border: 0; box-shadow: 0 6px 20px rgba(53,224,192,.25); }
.stButton > button[kind="primary"]:hover { transform: translateY(-1px); box-shadow: 0 10px 26px rgba(53,224,192,.35); }
div[role="radiogroup"] { gap: .4rem; }
div[role="radiogroup"] > label { background: rgba(255,255,255,.04); border: 1px solid var(--border); border-radius: 999px; padding: .25rem .95rem; transition: all .15s; }
div[role="radiogroup"] > label:hover { border-color: var(--accent); }
div[role="radiogroup"] > label:has(input:checked) { background: var(--accent); border-color: var(--accent); }
div[role="radiogroup"] > label:has(input:checked) p { color: #04231d !important; font-weight: 800; }
/* =============== SIDEBAR =============== */
section[data-testid="stSidebar"] { background: linear-gradient(180deg, #08101a 0%, #060A10 100%); border-right: 1px solid rgba(255,255,255,.07); box-shadow: 6px 0 30px rgba(0,0,0,.35); }
section[data-testid="stSidebar"][aria-expanded="true"] { width: 276px !important; min-width: 276px !important; max-width: 276px !important; }
section[data-testid="stSidebar"] [data-testid="stSidebarContent"] { padding: 0; }
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] { padding: 1.5rem 1.1rem 1.2rem; }
.sb-top { display: flex; align-items: center; gap: .75rem; }
.sb-brand { font-size: 1.35rem; font-weight: 900; line-height: 1.05; letter-spacing: .03em; }
.sb-brand span { color: var(--accent); }
.sb-sub { color: var(--muted); font-size: .82rem; margin: 1rem 0 1.2rem; line-height: 1.5; padding-bottom: 1.1rem; border-bottom: 1px solid var(--border); }
.sb-label { color: #6f7f94; font-size: .7rem; font-weight: 800; letter-spacing: .2em; margin: 0 0 .5rem .25rem; }
section[data-testid="stSidebar"] div[role="radiogroup"] { flex-direction: column; gap: .3rem; width: 100%; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label { width: 100%; border-radius: 12px; background: transparent; border: 1px solid transparent; border-left: 3px solid transparent; padding: .7rem .85rem; margin: 0; transition: all .18s ease; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child { display: none; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label p { color: #B7C3D3; font-size: 1rem; font-weight: 600; transition: color .18s ease; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover { background: rgba(255,255,255,.05); border-color: rgba(255,255,255,.08); transform: translateX(2px); }
section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover p { color: #fff; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) { background: linear-gradient(90deg, rgba(53,224,192,.18), rgba(53,224,192,.05));
  border: 1px solid rgba(53,224,192,.4); border-left: 3px solid var(--accent); box-shadow: 0 0 22px rgba(53,224,192,.14); }
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p { color: var(--accent) !important; font-weight: 800; }
.sb-stats { margin-top: 1.5rem; border-radius: 14px; padding: .35rem .9rem; background: rgba(255,255,255,.03); border: 1px solid var(--border); }
.sb-stat { display: flex; align-items: baseline; justify-content: space-between; padding: .6rem 0; border-bottom: 1px solid rgba(255,255,255,.06); }
.sb-stat:last-child { border-bottom: 0; }
.sb-stat b { font-size: 1.15rem; font-weight: 850; color: var(--accent); letter-spacing: -0.01em; }
.sb-stat span { font-size: .7rem; letter-spacing: .16em; color: #9FB0C4; font-weight: 750; }
/* =============== RESPONSIVE =============== */
@media (max-width: 1500px) { .ph-t { font-size: 2.2rem; } .hero-title { font-size: 3.1rem; } .bq-t { font-size: 1.25rem; } .cards-2 { grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); } }
@media (max-width: 1200px) { .flow { flex-wrap: wrap; gap: .6rem; } .fl-step { flex: 1 1 30%; } .fl-arrow { display: none; } .block-container, [data-testid="stMainBlockContainer"] { padding: 1rem 1.4rem 3rem !important; } }
@media (max-width: 768px) {
  .block-container, [data-testid="stMainBlockContainer"] { padding: .7rem .8rem 2rem !important; }
  .ph-t { font-size: 1.7rem; } .hero { padding: 1.3rem 1.1rem; } .hero-title { font-size: 2.2rem; } .bq-t { font-size: 1.05rem; }
  .kpi-v { font-size: 1.55rem; } .cards-2, .cards-3, .cards-4 { grid-template-columns: 1fr; } .fl-step { flex: 1 1 100%; }
  .exec-hero b { font-size: 1.9rem; } [data-testid="stMetricValue"] { font-size: 1.4rem; }
  section[data-testid="stSidebar"][aria-expanded="true"] { width: 82vw !important; min-width: 0 !important; max-width: 82vw !important; }
  div[data-testid="stTabs"] button[role="tab"] { padding: .45rem .7rem; font-size: .88rem; }
}
</style>
"""


# ----------------------------------------------------------------------------------
# STREAMLIT UTILITIES
# ----------------------------------------------------------------------------------
def _stretch(fn) -> dict:
    """Return the 'full width' kwarg supported by the installed Streamlit version."""
    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return {}
    if "use_container_width" in params:
        return {"use_container_width": True}
    if "width" in params:
        return {"width": "stretch"}
    return {}


def show_chart(fig: go.Figure, key: str) -> None:
    st.plotly_chart(fig, key=key, config={"displayModeBar": False}, **_stretch(st.plotly_chart))


def show_table(df: pd.DataFrame) -> None:
    st.dataframe(df, hide_index=True, **_stretch(st.dataframe))


def _h(text) -> str:
    """Escape text for HTML and convert **bold** and `code` markdown."""
    t = _htmllib.escape(str(text), quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return re.sub(r"`(.+?)`", r"<code>\1</code>", t)


def emit(block: str) -> None:
    """Render a single-line HTML block (styling only; no scripts)."""
    st.markdown(block.replace("\n", ""), unsafe_allow_html=True)


def pill(text: str, tone: str = "teal") -> str:
    return f"<span class='pill pill-{tone}'>{_h(text)}</span>"


def section(title: str, caption: str | None = None) -> None:
    emit(f"<div class='sec'><div class='sec-t'>{_h(title)}</div>"
         + (f"<div class='sec-c'>{_h(caption)}</div>" if caption else "") + "</div>")


def page_header(eye: str, title: str, sub: str | None = None) -> None:
    emit(f"<div class='ph'><div class='ph-e'>{_h(eye.upper())}</div><h1 class='ph-t'>{_h(title)}</h1>"
         + (f"<p class='ph-s'>{_h(sub)}</p>" if sub else "") + "</div>")


def eyebrow(text: str) -> None:
    emit(f"<div class='eb'>{_h(text.upper())}</div>")


def render_kpi_card(label: str, value: str, sub: str = "", tone: str = "teal") -> None:
    emit(f"<div class='kpi kpi-{tone}'><div class='kpi-l'>{_h(label)}</div><div class='kpi-v'>{_h(value)}</div>"
         f"<div class='kpi-s'>{_h(sub)}</div></div>")


def html_cards(cards: list, cols: int = 3) -> None:
    """Responsive equal-height CSS grid of pre-built HTML cards."""
    emit(f"<div class='cards cards-{cols}'>" + "".join(cards) + "</div>")


def business_question(text: str) -> None:
    st.info(f"**Business question:** {text}")


def grid(items, ncols: int, renderer) -> None:
    for i in range(0, len(items), ncols):
        cols = st.columns(ncols)
        for col, item in zip(cols, items[i:i + ncols]):
            with col:
                renderer(item)


# ----------------------------------------------------------------------------------
# CHART HELPERS (Plotly)
# ----------------------------------------------------------------------------------
def _base_layout(fig: go.Figure, height: int, top: int = 8, showlegend: bool = False) -> None:
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=MUTED, size=13, family='Inter, "Segoe UI", system-ui, sans-serif'),
        margin=dict(l=4, r=4, t=top, b=4), height=height, showlegend=showlegend,
        hoverlabel=dict(bgcolor="#0E1826", bordercolor="rgba(53,224,192,.5)",
                        font=dict(color=TEXT, size=13, family='Inter, "Segoe UI", system-ui, sans-serif')),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )


def _bar_color(store_id: str, s09_amber: bool) -> str:
    if store_id in PRIORITY:
        return DANGER
    if s09_amber and store_id == "S09":
        return WARNING
    return NEUTRAL


def render_bar_chart(value_fn, fmt, hover_fn, key: str, *, descending: bool = False,
                     s09: bool = False, ref: tuple | None = None, x_range: tuple | None = None) -> None:
    """Horizontal bar chart over the 10 stores. S07/S03 red, S09 amber (optional), others neutral.
    Diverging (zero line) when negatives exist. `ref` = (value, label) draws a dashed reference line."""
    rows = [{"id": sid, "v": float(value_fn(s)), "hover": hover_fn(s)} for sid, s in STORES.items()]
    rows.sort(key=lambda r: r["v"], reverse=descending)
    vals = [r["v"] for r in rows]
    hi, lo = max([0.0] + vals), min([0.0] + vals)
    if ref:
        hi, lo = max(hi, ref[0] * 1.05), min(lo, ref[0])
    if x_range:
        lo, hi = x_range
    span = (hi - lo) or 1.0
    rng = [lo - (span * 0.22 if lo < 0 else 0), hi + span * 0.22]

    fig = go.Figure(go.Bar(
        x=[r["v"] for r in rows], y=[r["id"] for r in rows], orientation="h",
        marker=dict(color=[_bar_color(r["id"], s09) for r in rows]),
        text=[fmt(r["v"]) for r in rows], textposition="outside", cliponaxis=False,
        textfont=dict(color=TEXT, size=12),
        customdata=[r["hover"] for r in rows],
        hovertemplate="<b>%{y}</b><br>%{customdata}<extra></extra>",
    ))
    _base_layout(fig, height=52 + 35 * len(rows) + (22 if ref else 0), top=30 if ref else 8)
    fig.update_layout(bargap=0.34)
    fig.update_traces(marker_line_width=0)
    fig.update_xaxes(range=rng, showgrid=True, gridcolor="rgba(139,154,175,.10)", gridwidth=1, zeroline=False,
                     showticklabels=False, fixedrange=True)
    fig.update_yaxes(categoryorder="array", categoryarray=[r["id"] for r in rows],
                     autorange="reversed", tickfont=dict(color=TEXT, size=13), fixedrange=True)
    fig.add_vline(x=0, line_width=1.2, line_color=MUTED if lo < 0 else "#2a3d54")
    if ref:
        fig.add_vline(x=ref[0], line_width=1.3, line_dash="dash", line_color=WARNING,
                      annotation_text=ref[1], annotation_position="top",
                      annotation_font=dict(color=WARNING, size=11))
    show_chart(fig, key)


def render_grouped_chart(groups: list, series: list, fmt, key: str) -> None:
    """Grouped horizontal bars. groups: [{'n': label, 'x': [extra hover per series]}],
    series: [{'n': name, 'c': colour, 'v': [value per group]}]."""
    fig = go.Figure()
    for si, s in enumerate(series):
        fig.add_trace(go.Bar(
            name=s["n"], x=s["v"], y=[g["n"] for g in groups], orientation="h",
            marker=dict(color=s["c"]), text=[fmt(v) for v in s["v"]], textposition="outside",
            cliponaxis=False, textfont=dict(color=TEXT, size=11),
            customdata=[g["x"][si] if g.get("x") else "" for g in groups],
            hovertemplate="<b>%{y}</b><br>" + s["n"] + ": %{text}<br>%{customdata}<extra></extra>",
        ))
    allv = [v for s in series for v in s["v"]]
    hi, lo = max([0.0] + allv), min([0.0] + allv)
    span = (hi - lo) or 1.0
    _base_layout(fig, height=76 + len(groups) * (len(series) * 24 + 16), top=34, showlegend=True)
    fig.update_layout(barmode="group", bargap=0.28, bargroupgap=0.06)
    fig.update_traces(marker_line_width=0)
    fig.update_xaxes(range=[lo - (span * 0.2 if lo < 0 else 0), hi + span * 0.2], showgrid=True,
                     gridcolor="rgba(139,154,175,.10)",
                     zeroline=False, showticklabels=False, fixedrange=True)
    fig.update_yaxes(categoryorder="array", categoryarray=[g["n"] for g in groups],
                     autorange="reversed", tickfont=dict(color=TEXT, size=12), fixedrange=True)
    fig.add_vline(x=0, line_width=1.2, line_color=MUTED)
    show_chart(fig, key)


def render_return_comparison() -> None:
    labels = ["Same timestamp", "Normal timestamp"]
    vals = [RR_SAME, RR_NORMAL]
    hover = [f"{fmt_int(RET['same']['n'])} orders · {fmt_int(RET['same']['ret'])} returned",
             f"{fmt_int(RET['normal']['n'])} orders · {fmt_int(RET['normal']['ret'])} returned"]
    fig = go.Figure(go.Bar(
        x=vals, y=labels, orientation="h", marker=dict(color=[DANGER, NEUTRAL]),
        text=[format_pct(v) for v in vals], textposition="outside", cliponaxis=False,
        textfont=dict(color=TEXT, size=16), customdata=hover,
        hovertemplate="<b>%{y}</b><br>Return rate %{text}<br>%{customdata}<extra></extra>",
    ))
    _base_layout(fig, height=190)
    fig.update_layout(bargap=0.4)
    fig.update_traces(marker_line_width=0)
    fig.update_xaxes(range=[0, max(vals) * 1.3], showgrid=True, gridcolor="rgba(139,154,175,.10)", zeroline=False,
                     showticklabels=False, fixedrange=True)
    fig.update_yaxes(autorange="reversed", tickfont=dict(color=TEXT, size=13), fixedrange=True)
    show_chart(fig, "ch_return_cmp")


# ----------------------------------------------------------------------------------
# CONTENT BUILDERS (text that depends on computed values)
# ----------------------------------------------------------------------------------
def story_steps() -> list:
    return [
        ("1", "Ten stores analysed",
         f"{fmt_int(ORDERS)} orders across 10 dark stores over 42 days; contribution "
         f"{format_currency(TOTAL_CONTRIB, 2)} before rent."),
        ("2", "Stores normalized for operating days",
         "Monthly profit = contribution × 30 ÷ operating days − rent, so a 14-day store is "
         "compared fairly with 42-day stores."),
        ("3", "S07 and S03 are the only negative stores",
         f"Normalized monthly profit {format_currency(b['pnl'], 2)} (S07) and "
         f"{format_currency(a['pnl'], 2)} (S03); the other {POS_COUNT} stores are positive."),
        ("4", "S09 looks weak in raw totals but is profitable",
         f"S09 operated {s9['operating_days']} days; normalized monthly profit is "
         f"+{format_currency(s9['pnl'], 2)}. It is not a problem store."),
        ("5", "Same-timestamp delivery scans are concentrated at S07/S03",
         f"{n2(b['sts'])}% of S07 trips and {n2(a['sts'])}% of S03 trips, versus 0% at the other stores."),
        ("6", "Those orders return far more often",
         f"{n2(RR_SAME)}% return rate for same-timestamp orders vs {n2(RR_NORMAL)}% for normal-timestamp "
         "orders — a strong association, not proof of causation."),
        ("7", "Promotional orders show below-floor rule violations",
         f"{n2(PF['S03']['pct'])}% of S03 and {n2(PF['S07']['pct'])}% of S07 promotional orders were below "
         "the applicable minimum-order value."),
        ("8", "Measurable potential financial leakage",
         f"Potential below-floor discount leakage of about {format_k(PF['S03']['leak30'])}/month (S03) and "
         f"{format_k(PF['S07']['leak30'])}/month (S07). Potential, not guaranteed savings."),
    ]


DATA_QUALITY = [
    ("Corrected", "teal", "Timestamps", "`dd-mm-yyyy hh.mm` text",
     "Standardised to real date-times before computing delivery minutes."),
    ("Corrected", "teal", "Hidden carriage return", "CHAR(13) in order-side delivery partner IDs",
     "Stripped; all 11,251 S03/S07 orders now match a partner."),
    ("Corrected", "teal", "Currency symbols", "“₹” prefixes on product MRP and Unit_Cost",
     "Stripped before converting to numbers."),
    ("Corrected", "teal", "Text trimming", "Trailing spaces; blank promo codes",
     "Trimmed; blank promo = “No Promo”."),
    ("Retained NULL", "info", "Legitimate NULLs",
     "S08 `staff_count`; 1,067 delivered timestamps on cancelled trips; 2,113 order lines with no `unit_cost`",
     "Left as NULL, not imputed."),
    ("Excluded invalid", "red", "Invalid distances", "573 trips with negative distance",
     "Flagged Invalid and excluded from distance averages."),
    ("Schema", "amber", "Order_Item schema", "Header mismatch",
     "Corrected to Order_Item_ID, Order_ID, SKU, Unit_Price, unit_cost, Quantity (177,017 rows, all joins resolve)."),
    ("Cosmetic", "neutral", "Header apostrophe", "Stray apostrophe in `Joined_Date'`", "Removed."),
    ("Cosmetic", "neutral", "City typo", "“Nodia” for S04 and S09 in Dark_Stores",
     "Left as is; not used in any metric."),
]

VALIDATION_NOTE = (
    "**VALIDATION NOTE** — Distance was investigated as a possible explanation and ruled out. Recomputed from "
    "raw Trip_Logs, the longest valid trip is 5.4 km and 0% of trips exceed 10 km; average distance is ≈3.0 km "
    "at every store. Two further notes: the Trip_Logs `Delivery_Performance` flag marks ≥10 min as late "
    "(S03 77%, S07 76%), while this dashboard uses the SQL definition of more than 10 min (72%). And "
    "`promised_minutes` in orders is 15 for every order. Against the 15-minute promised time, S03/S07 also show "
    "higher late rates than the other stores; this is supporting evidence, not the primary root-cause finding."
)

METHODOLOGY_LEFT = (
    "- Delivered contribution = Net Amount − COGS − Delivery Cost\n"
    "- Returned contribution = −(COGS + Delivery Cost)\n"
    "- Cancelled contribution = 0"
)
METHODOLOGY_RIGHT = (
    "- Normalized Monthly Contribution = 42-day contribution × 30 ÷ operating days\n"
    "- Normalized Monthly Profit = Normalized Monthly Contribution − Monthly Rent\n"
    "- Late delivery = Pickup-to-delivery time > 10 minutes\n"
    "- Analysis period = 42 days; S09 operated 14 days"
)
METHODOLOGY_NOTE = (
    f"Benchmarks: “other 8” = the eight stores other than S03 and S07, simple average of store-level values. "
    f"Delivery cost benchmark is ₹28/order (other-8 average ≈ ₹{oth_avg('dc'):.2f}). Monthly opportunity = "
    "42-day gap × 30/42. Same-timestamp scan = a trip whose picked and delivered timestamps are identical. "
    "Below-floor order = a promotional order whose value is under the applicable promotion’s minimum-order "
    "value. Promo-floor leakage = discount value given on below-floor orders (potential, not guaranteed savings)."
)


# ----------------------------------------------------------------------------------
# FINDINGS
# ----------------------------------------------------------------------------------
def finding_html(f: dict) -> str:
    cls = {"red": "red", "amber": "amber"}.get(f["tone"], "teal")
    tiles = "".join(
        f"<div class='mtile'><span>{_h(label)}</span><b class='{ {'red': 'neg', 'amber': 'amb'}.get(tone, '') }'>{_h(value)}</b></div>"
        for value, label, tone in f["big"])
    badge = (f"<div class='badge-line'>{pill('Potential discount leakage', 'amber')} "
             f"{pill('Not guaranteed savings', 'amber')}</div>") if f.get("badge") else ""
    return (f"<div class='panel fcard p-{cls} fc-{cls}'><div class='fc-tag'>{_h(f['tag'])}</div>"
            f"<h3>{_h(f['title'])}</h3><div class='mgrid'>{tiles}</div>{badge}"
            f"<div class='fc-dl'><div><b>Observation</b>{_h(f['obs'])}</div><div><b>Evidence</b>{_h(f['evid'])}</div>"
            f"<div><b>Insight</b>{_h(f['insight'])}</div><div><b>Implication</b>{_h(f['impl'])}</div></div></div>")


def render_findings_grid(items: list) -> None:
    html_cards([finding_html(f) for f in items], cols=2)


def findings_primary() -> list:
    flo = DF.loc[DF["pnl"] >= 0, "pnl"]
    return [
        dict(tag="F1 · Store economics", tone="red",
             title="S07 and S03 are the only stores with negative normalized monthly profit",
             big=[(format_currency(b["pnl"], 2), "S07 normalized profit / month", "red"),
                  (format_currency(a["pnl"], 2), "S03 normalized profit / month", "red")],
             obs="S07 and S03 are the only stores with negative normalized monthly profit.",
             evid=f"Normalized monthly profit = contribution × 30 ÷ operating days − rent. The other {POS_COUNT} "
                  f"stores are positive, from {format_currency(flo.min(), 2)} to {format_currency(DF['pnl'].max(), 2)}. "
                  f"S09 operated {s9['operating_days']} days and is +{format_currency(s9['pnl'], 2)} after normalization.",
             insight="Raw 42-day totals are not comparable for a 14-day store; once normalized, S09 is profitable "
                     "and is not a problem store.",
             impl="S07 and S03 are the priority investigation stores."),
        dict(tag="F2 · Delivery process", tone="red",
             title="Same-timestamp delivery scans are concentrated at S07/S03",
             big=[(f"{n2(b['sts'])}%", "S07 same-timestamp scans", "red"),
                  (f"{n2(a['sts'])}%", "S03 same-timestamp scans", "red"),
                  ("0%", "other 8 stores", "")],
             obs=f"Same-timestamp delivery scans are concentrated at S07/S03: {n2(b['sts'])}% at S07 and "
                 f"{n2(a['sts'])}% at S03, versus 0% elsewhere.",
             evid=f"S07: {fmt_int(b['same_ts'])} of {fmt_int(b['trips'])} trips. S03: {fmt_int(a['same_ts'])} of "
                  f"{fmt_int(a['trips'])} trips. The other stores show none.",
             insight="These are unusual delivery scans in the data; the evidence flags them but does not by itself "
                     "establish why they occur.",
             impl="Audit the delivery-scan process at both stores."),
        dict(tag="F3 · Return consequence", tone="red",
             title="Same-timestamp orders return far more often",
             big=[(f"{n2(RR_SAME)}%", "same-timestamp orders", "red"),
                  (f"{n2(RR_NORMAL)}%", "normal-timestamp orders", "")],
             obs=f"Same-timestamp orders return at {n2(RR_SAME)}% versus {n2(RR_NORMAL)}% for normal-timestamp orders.",
             evid=f"{fmt_int(RET['same']['n'])} same-timestamp orders with {fmt_int(RET['same']['ret'])} returned; "
                  f"{fmt_int(RET['normal']['n'])} normal-timestamp orders with {fmt_int(RET['normal']['ret'])} returned.",
             insight="This is a strong association in the supplied data, but it does not by itself prove causation.",
             impl="Audit return reasons, starting with same-timestamp orders."),
        dict(tag="F4 · Promotion rule", tone="red",
             title="Many promotional orders are below the minimum-order threshold",
             big=[(f"{n2(PF['S03']['pct'])}%", "S03 promotional orders below floor", "red"),
                  (f"{n2(PF['S07']['pct'])}%", "S07 promotional orders below floor", "red")],
             obs=f"{n2(PF['S03']['pct'])}% of S03 and {n2(PF['S07']['pct'])}% of S07 promotional orders are below the "
                 "applicable minimum-order threshold.",
             evid=f"S03: {PF['S03']['below']} of {fmt_int(PF['S03']['promo_orders'])} promotional orders. "
                  f"S07: {PF['S07']['below']} of {fmt_int(PF['S07']['promo_orders'])}. FRESH50 minimum order value is "
                  f"{format_currency(FLOOR50)} (Promo_Codes).",
             insight="The check applies each promotion’s own minimum-order value across all promotions.",
             impl="Review how promo minimum-order rules are enforced at S03 and S07."),
        dict(tag="F5 · Financial impact", tone="amber",
             title="Potential below-floor discount leakage",
             big=[(f"{format_k(PF['S03']['leak30'])}/month", "S03 potential leakage", "amber"),
                  (f"{format_k(PF['S07']['leak30'])}/month", "S07 potential leakage", "amber")],
             obs=f"S03 ≈ {format_k(PF['S03']['leak30'])}/month and S07 ≈ {format_k(PF['S07']['leak30'])}/month in "
                 "below-floor discount leakage.",
             evid=f"Over 42 days, below-floor promotional orders received {format_currency(PF['S03']['leak42'], 2)} (S03) "
                  f"and {format_currency(PF['S07']['leak42'], 2)} (S07) of discount value, i.e. about "
                  f"{format_lakh(PF['S03']['leak42'])} and {format_lakh(PF['S07']['leak42'])}.",
             insight="These are potential discount leakage figures, not guaranteed savings.",
             impl="Quantifies what promo-rule enforcement may be worth; validate with a pilot.", badge=True),
    ]


def findings_secondary() -> list:
    meat = "MEAT & SEAFOOD"
    max_diff = max(abs(category_margin(g, c) - category_margin("OTH", c)) for c in CATS for g in ("S03", "S07"))
    o3, o7 = OPP["S03"], OPP["S07"]
    f_s03, f_s07 = PROMO[("S03", "FRESH50")]["cpo"], PROMO[("S07", "FRESH50")]["cpo"]
    return [
        dict(tag="Product · supporting", tone="amber", title="Category margins are similar — secondary evidence",
             big=[(f"{category_margin('S07', meat):.1f}% / {category_margin('S03', meat):.1f}%",
                   "Meat & Seafood margin S07 / S03", ""),
                  (f"{category_margin('OTH', meat):.1f}%", "other-8 Meat & Seafood margin", "")],
             obs="Meat & Seafood is the weakest category everywhere.",
             evid=f"S03 and S07 category margins are within {max_diff:.1f} percentage points of the other-8 margin "
                  "in every category.",
             insight="Product mix may contribute, but the evidence does not point to it as the primary driver.",
             impl="Treat product mix as secondary. Note: 2,113 order lines have no unit cost (kept as NULL), which "
                  "may flatter margins slightly."),
        dict(tag="Exploratory · delivery", tone="neutral", title="High lateness and high delivery cost",
             big=[(f"{n2(b['lr'])}% / {n2(a['lr'])}%", "late rate S07 / S03", "red"),
                  (f"{format_currency(b['dc'], 2)} / {format_currency(a['dc'], 2)}", "cost per order vs ₹28", "red")],
             obs=f"Late rate {oth_avg('lr'):.1f}% at the other 8 stores.",
             evid=f"Avg delivery {n2(b['tm'])} / {n2(a['tm'])} min vs {oth_avg('tm'):.1f}. Avg distance "
                  f"{n2(b['ds'])} / {n2(a['ds'])} km vs {n2(oth_avg('ds'))} — approximately 3 km everywhere.",
             insight="Distance was investigated and ruled out; it does not materially differentiate S03/S07 from "
                     "the other stores.",
             impl="Review dispatch, batching and delivery economics at both stores."),
        dict(tag="Exploratory · returns", tone="neutral", title="Return rates are above the benchmark",
             big=[(f"{n2(b['rr'])}%", f"S07 · {b['rr'] / (B_RR * 100):.1f}× other-8 avg", "red"),
                  (f"{n2(a['rr'])}%", f"S03 · {a['rr'] / (B_RR * 100):.1f}× other-8 avg", "red")],
             obs=f"{b['ret']} returned orders at S07 and {a['ret']} at S03 vs a {B_RR * 100:.2f}% other-8 average.",
             evid="A returned order contributes −(COGS + delivery cost) with no revenue.",
             insight="Returns directly reduce contribution, most visibly at S07.",
             impl=f"Benchmark gap: return recovery of {format_k(o7['ret'])}/month (S07) and {format_k(o3['ret'])}/month "
                  "(S03) if rates moved to the benchmark."),
        dict(tag="Exploratory · promotion", tone="neutral", title="High promo usage and discount burden",
             big=[(f"{n2(a['pu'])}% / {n2(b['pu'])}%", "promo usage S03 / S07", "red"),
                  (f"{format_currency(a['di'], 2)} / {format_currency(b['di'], 2)}",
                   f"discount / delivered order vs {format_currency(B_DI, 2)}", "red")],
             obs=f"Other-8 promo usage is {OTH_DF['pu'].min():.0f}–{OTH_DF['pu'].max():.0f}%.",
             evid=f"FRESH50 average contribution/order: {format_currency(f_s03, 2)} (S03), {format_currency(f_s07, 2)} "
                  f"(S07); {FRESH50_PRIORITY / FRESH50_ALL * 100:.0f}% of FRESH50 orders are at these two stores.",
             insight="FRESH50 is associated with strongly negative average contribution per order at both stores; "
                     "this does not prove FRESH50 alone caused the store losses.",
             impl=f"Benchmark gap: excess discount of {format_k(o3['dis'])}/month (S03) and {format_k(o7['dis'])}/month "
                  "(S07). This earlier screening view overlaps with, and is separate from, promo-floor leakage."),
    ]


# ----------------------------------------------------------------------------------
# DATA QUALITY + RECONCILIATION
# ----------------------------------------------------------------------------------
def render_data_quality() -> None:
    cards = []
    for status, tone, title, issue, treatment in DATA_QUALITY:
        cards.append(f"<div class='panel p-{tone if tone != 'info' else 'info'}'><div style='display:flex;justify-content:space-between;"
                     f"align-items:center;gap:.6rem'><b style='font-size:1.02rem'>{_h(title)}</b>{pill(status, tone)}</div>"
                     f"<div class='evrow' style='flex-direction:column;gap:.1rem;border:0'><span>ISSUE</span><b style='text-align:left;font-weight:600'>{_h(issue)}</b></div>"
                     f"<div class='evrow' style='flex-direction:column;gap:.1rem;border:0'><span>TREATMENT</span><b style='text-align:left;font-weight:600'>{_h(treatment)}</b></div></div>")
    html_cards(cards, cols=3)


def render_reconciliation() -> None:
    def close(x, y, t=0.01):
        return abs(x - y) <= t

    f50_s03, f50_s07 = PROMO[("S03", "FRESH50")]["cpo"], PROMO[("S07", "FRESH50")]["cpo"]
    np_s03, np_s07 = PROMO[("S03", "No Promo")]["cpo"], PROMO[("S07", "No Promo")]["cpo"]
    delivered, returned, cancelled = int(DF["deliv"].sum()), int(DF["ret"].sum()), int(DF["canc"].sum())
    checks = [
        ("Orders", fmt_int(ORDERS), "52,133", ORDERS == 52133),
        ("Delivered / returned / cancelled", f"{delivered:,} / {returned:,} / {cancelled:,}",
         "48,510 / 2,556 / 1,067", (delivered, returned, cancelled) == (48510, 2556, 1067)),
        ("Contribution before rent", format_currency(TOTAL_CONTRIB, 2), "₹3,025,759.10", close(TOTAL_CONTRIB, 3025759.10)),
        ("S07 normalized monthly profit", format_currency(b["pnl"], 2), "-₹372,763.19", close(b["pnl"], -372763.19)),
        ("S03 normalized monthly profit", format_currency(a["pnl"], 2), "-₹139,046.41", close(a["pnl"], -139046.41)),
        ("S09 normalized monthly profit", format_currency(s9["pnl"], 2), "₹116,625.05", close(s9["pnl"], 116625.05)),
        ("Negative normalized stores", ", ".join(NEG_STORES), "S07, S03",
         len(NEG_STORES) == 2 and all(x in PRIORITY for x in NEG_STORES)),
        ("S09 operating days · orders/day · contrib/order",
         f"{s9['operating_days']} · {n2(s9['opd'])} · {format_currency(s9['cpo'], 2)}", "14 · 129.64 · ₹74.21",
         s9["operating_days"] == 14 and close(s9["opd"], 129.64) and close(s9["cpo"], 74.21)),
        ("S07 / S03 contrib per order", f"{format_currency(b['cpo'], 2)} / {format_currency(a['cpo'], 2)}",
         "-₹35.64 / ₹14.33", close(b["cpo"], -35.64) and close(a["cpo"], 14.33)),
        ("Same-timestamp scans S07 / S03 / others",
         f"{n2(b['sts'])}% / {n2(a['sts'])}% / {n2(OTH_DF['sts'].max())}%", "19.03% / 16.77% / 0.00%",
         close(b["sts"], 19.03) and close(a["sts"], 16.77) and bool((OTH_DF["sts"] == 0).all())),
        ("Return rate: same vs normal timestamp", f"{n2(RR_SAME)}% / {n2(RR_NORMAL)}%", "34.19% / 3.73%",
         close(RR_SAME, 34.19) and close(RR_NORMAL, 3.73)),
        ("Promo-floor violations S03 / S07", f"{n2(PF['S03']['pct'])}% / {n2(PF['S07']['pct'])}%", "41.78% / 42.45%",
         close(PF["S03"]["pct"], 41.78) and close(PF["S07"]["pct"], 42.45)),
        ("Promo-floor leakage / month S03 / S07",
         f"{format_currency(PF['S03']['leak30'], 2)} / {format_currency(PF['S07']['leak30'], 2)}",
         "₹85,864.13 / ₹88,600.51", close(PF["S03"]["leak30"], 85864.13) and close(PF["S07"]["leak30"], 88600.51)),
        ("FRESH50 contrib/order S03 / S07", f"{format_currency(f50_s03, 2)} / {format_currency(f50_s07, 2)}",
         "-₹178.93 / -₹205.48", close(f50_s03, -178.93) and close(f50_s07, -205.48)),
        ("No Promo contrib/order S03 / S07", f"{format_currency(np_s03, 2)} / {format_currency(np_s07, 2)}",
         "₹101.71 / ₹82.87", close(np_s03, 101.71) and close(np_s07, 82.87)),
        ("S07 / S03 return rate", f"{n2(b['rr'])}% / {n2(a['rr'])}%", "14.01% / 7.94%",
         close(b["rr"], 14.01) and close(a["rr"], 7.94)),
        ("S07 / S03 late rate", f"{n2(b['lr'])}% / {n2(a['lr'])}%", "72.10% / 72.33%",
         close(b["lr"], 72.10) and close(a["lr"], 72.33)),
        ("S07 / S03 delivery cost/order", f"{n2(b['dc'])} / {n2(a['dc'])}", "≈42.12 / 41.98",
         close(b["dc"], 42.12) and close(a["dc"], 41.98)),
        ("S07 / S03 avg distance", f"{n2(b['ds'])} / {n2(a['ds'])} km", "≈3.02 / 2.99",
         close(b["ds"], 3.02) and close(a["ds"], 2.99)),
        ("S07 / S03 promo usage", f"{n2(b['pu'])}% / {n2(a['pu'])}%", "28.68% / 28.95%",
         close(b["pu"], 28.68) and close(a["pu"], 28.95)),
        ("S07 / S03 discount/order", f"{n2(b['di'])} / {n2(a['di'])}", "48.69 / 49.18",
         close(b["di"], 48.69) and close(a["di"], 49.18)),
    ]
    table = pd.DataFrame({
        "Check": [c[0] for c in checks],
        "Dashboard": [c[1] for c in checks],
        "MySQL result": [c[2] for c in checks],
        "Status": ["MATCH" if c[3] else "MISMATCH" for c in checks],
    })
    passed = sum(1 for c in checks if c[3])
    if passed == len(checks):
        st.success(f"All {len(checks)} reconciliation checks match the MySQL-verified results.")
    else:
        st.error(f"{len(checks) - passed} of {len(checks)} checks do not match — review the table.")
    def _status_style(v):
        return ("color:#35E0C0;font-weight:800" if v == "MATCH" else "color:#FF5C62;font-weight:800")
    try:
        styler = table.style
        styler = (styler.map if hasattr(styler, "map") else styler.applymap)(_status_style, subset=["Status"])
        show_table(styler)
    except Exception:  # Styler needs jinja2; fall back to the plain table
        show_table(table)


# ----------------------------------------------------------------------------------
# PAGE: HOME
# ----------------------------------------------------------------------------------
def render_home() -> None:
    emit("<div class='hero'><span class='logo-mark'></span><div class='hero-title'>DARK STORE <span>DOWN</span></div>"
         "<div class='hero-sub'>ZIPTO QUICK COMMERCE · NOIDA CLUSTER REVIEW</div>"
         "<div class='bq-prem'><div class='bq-l'>BUSINESS QUESTION</div><div class='bq-t'>Which two stores should we "
         "investigate first, what looks weak in each, and what is it potentially worth in rupees?</div></div></div>")
    kk = st.columns(4)
    with kk[0]:
        render_kpi_card("42 DAYS", "42 days", "18 May – 28 Jun 2026", "teal")
    with kk[1]:
        render_kpi_card("10 STORES", "10", "dark stores", "info")
    with kk[2]:
        render_kpi_card(f"{fmt_int(ORDERS)} ORDERS", fmt_int(ORDERS), "orders analysed", "neutral")
    with kk[3]:
        render_kpi_card("CONTRIBUTION", f"₹{TOTAL_CONTRIB / 1e5:.1f}L", "network contribution before rent", "teal")

    section("The Business Problem")
    emit("<div class='panel p-teal'><p style='font-size:1.02rem;color:#D7DFEA'>Most Zipto dark stores make money. Some do not. "
         "We have six weeks of order, delivery and product data across ten stores and one decision to make: after "
         "normalizing for operating days, which two stores to investigate first, what looks weak in each, and what that "
         "is potentially worth per month.</p></div>")

    section("Executive Snapshot", "42-day audit · all figures computed from the embedded dataset")
    k = st.columns(4)
    with k[0]:
        render_kpi_card("Network contribution", f"₹{TOTAL_CONTRIB / 1e5:.1f}L",
                        f"before rent · {format_currency(TOTAL_CONTRIB, 2)} over 42 days", "teal")
    with k[1]:
        render_kpi_card("S07", "S07", f"Negative normalized monthly profit · {format_currency(b['pnl'], 2)}", "red")
    with k[2]:
        render_kpi_card("S03", "S03", f"Negative normalized monthly profit · {format_currency(a['pnl'], 2)}", "red")
    with k[3]:
        render_kpi_card("Late delivery at S03/S07", f"{int(np.floor(min(a['lr'], b['lr'])))}%+",
                        f"vs {oth_avg('lr'):.1f}% other-8 average", "red")
    st.info("S07 and S03 are the only stores with negative normalized monthly profit. They combine weak unit "
            "economics with delivery-process anomalies, elevated returns and promotion-rule leakage despite "
            "substantial order volume. These are associations in the supplied data, not proven causes.")

    section("The story, step by step")
    html_cards([f"<div class='panel p-teal'><div><span class='stepno'>{_h(n)}</span>"
                f"<b style='font-size:1.02rem'>{_h(t)}</b></div><p class='mutp' style='margin-top:.55rem'>{_h(d)}</p></div>"
                for n, t, d in story_steps()], cols=3)

    section("Where to look")
    lanes = [
        ("Lane A", "Store performance", "Normalized monthly profit per store, and why S07 and S03 were selected."),
        ("Lane B", "Delivery & fulfilment",
         "Late rate, delivery time, cost per order, distance, same-timestamp scans and returns."),
        ("Lane C", "Product & promotions",
         "Category margins, promo usage, promo-floor validation and discount leakage."),
    ]
    html_cards([f"<div class='panel p-teal'>{pill(t, 'teal')}<h3>{_h(h)}</h3><p class='mutp'>{_h(d)}</p></div>"
                for t, h, d in lanes], cols=3)
    st.button("Open the dashboard →", type="primary", on_click=go_to, args=("Dashboard",))


# ----------------------------------------------------------------------------------
# PAGE: DASHBOARD — LANE A (STORE PERFORMANCE)
# ----------------------------------------------------------------------------------
def chart_card(title: str, unit: str, tag_text: str | None = None, tag_tone: str = "neutral"):
    """Open a bordered container with a title and unit caption; returns the container."""
    box = st.container(border=True)
    with box:
        st.markdown(f"### {title}" + (f"  {tag(tag_text, tag_tone)}" if tag_text else ""))
        st.caption(unit)
    return box


def render_lane_a() -> None:
    k = st.columns(4)
    with k[0]:
        render_kpi_card("S07 normalized profit / month", format_currency(b["pnl"], 2),
                        "negative normalized monthly profit", "red")
    with k[1]:
        render_kpi_card("S03 normalized profit / month", format_currency(a["pnl"], 2),
                        "negative normalized monthly profit", "red")
    with k[2]:
        render_kpi_card("S07 contribution / order", format_currency(b["cpo"], 2),
                        f"other-8 average {format_currency(oth_avg('cpo'), 2)}", "red")
    with k[3]:
        render_kpi_card("S03 contribution / order", format_currency(a["cpo"], 2),
                        f"other-8 average {format_currency(oth_avg('cpo'), 2)}", "red")
    emit("<div style='display:flex;gap:1.2rem;flex-wrap:wrap;margin:.2rem 0 .8rem;font-size:.85rem;color:#A9B6C7'>"
         f"<span><i style='display:inline-block;width:11px;height:11px;border-radius:3px;background:{DANGER};margin-right:.4rem'></i>S07 / S03 (priority)</span>"
         f"<span><i style='display:inline-block;width:11px;height:11px;border-radius:3px;background:{WARNING};margin-right:.4rem'></i>S09 (14-day comparison case)</span>"
         f"<span><i style='display:inline-block;width:11px;height:11px;border-radius:3px;background:{NEUTRAL};margin-right:.4rem'></i>Other stores</span></div>")

    c1, c2 = st.columns(2)
    with c1:
        with chart_card("Normalized monthly profit",
                        "₹ thousands · Normalized monthly profit · adjusted for operating days · "
                        "sorted most negative → most positive"):
            render_bar_chart(
                lambda s: s["pnl"] / 1000,
                lambda v: f"{'-' if v < 0 else '+'}₹{abs(v):.0f}K",
                lambda s: (f"Normalized monthly profit {format_currency(s['pnl'], 2)}<br>"
                           f"Contribution {format_currency(s['contrib'], 2)} × 30 ÷ {s['operating_days']} days = "
                           f"{format_currency(s['nmc'], 2)}<br>− monthly rent {format_currency(s['rent'])}"),
                "ch_pnl", s09=True)
    with c2:
        with chart_card("Contribution per order", "₹ per order (all orders) · sorted lowest → highest"):
            render_bar_chart(
                lambda s: s["cpo"], lambda v: format_currency(v, 1),
                lambda s: (f"{format_currency(s['cpo'], 2)} per order<br>"
                           f"{format_currency(s['contrib'])} ÷ {fmt_int(s['orders'])} orders"),
                "ch_cpo", s09=True)
    c3, c4 = st.columns(2)
    with c3:
        with chart_card("Orders per day", "orders ÷ operating days (S09 = 14 days) · sorted highest → lowest"):
            render_bar_chart(
                lambda s: s["opd"], lambda v: f"{v:.1f}",
                lambda s: f"{fmt_int(s['orders'])} orders ÷ {s['operating_days']} operating days = {n2(s['opd'])}",
                "ch_opd", descending=True, s09=True)
            st.info("S07 and S03 are among the higher-volume stores. S09 looks small only in raw totals because "
                    "it operated 14 days; per operating day it is comparable.")
    with c4:
        with chart_card("Return rate", "% of all orders · sorted highest → lowest · dashed line = other-8 average"):
            render_bar_chart(
                lambda s: s["rr"], lambda v: f"{v:.1f}%",
                lambda s: f"{s['ret']} returned of {fmt_int(s['orders'])} orders = {n2(s['rr'])}%",
                "ch_rr", descending=True, s09=True, ref=(B_RR * 100, f"other-8 avg {B_RR * 100:.1f}%"))

    render_selection_logic()
    render_ruled_out()


def render_selection_logic() -> None:
    eyebrow("Selection logic")
    section("How We Selected S07 & S03")
    st.markdown("We screened all 10 stores on a normalized monthly basis before selecting the two stores for "
                "deeper operational investigation.")
    flow = [
        ("ALL 10 STORES", "Every store screened"),
        ("NORMALIZE", f"Contribution × 30 ÷ operating days; S09 ran {s9['operating_days']} days"),
        ("MONTHLY PROFIT SCREEN", f"{len(NEG_STORES)} of 10 negative: {', '.join(NEG_STORES)}"),
        ("CONTRIBUTION / ORDER", f"S07 negative; S03 {format_currency(a['cpo'], 2)}"),
        ("ORDER VOLUME CHECK", f"S07/S03 ≈ {round(a['opd'])}–{round(b['opd'])} orders/day"),
        ("S07 + S03 SELECTED", "Deeper investigation"),
    ]
    parts = []
    for i, (t, d) in enumerate(flow, start=1):
        last = i == len(flow)
        parts.append(f"<div class='fl-step{' fl-last' if last else ''}'><div class='fl-n'>{'✓' if last else i}</div>"
                     f"<div class='fl-t'>{_h(t)}</div><div class='fl-d'>{_h(d)}</div></div>")
        if not last:
            parts.append("<div class='fl-arrow'></div>")
    emit("<div class='flow'>" + "".join(parts) + "</div>")

    def ev(sid, tone, label):
        s = STORES[sid]
        pcls = "neg" if s["pnl"] < 0 else "pos"
        sign = "" if s["pnl"] < 0 else "+"
        ccls = "neg" if s["cpo"] < 0 else ""
        return (f"<div class='panel p-{tone}'><div style='display:flex;justify-content:space-between;align-items:center;gap:.6rem'>"
                f"<b style='font-size:1.4rem'>{sid}</b>{pill(label, tone)}</div>"
                f"<div class='evrow'><span>Normalized profit / month</span><b class='{pcls}'>{sign}{format_currency(s['pnl'], 2)}</b></div>"
                f"<div class='evrow'><span>Operating days</span><b>{s['operating_days']}</b></div>"
                f"<div class='evrow'><span>Contribution / order</span><b class='{ccls}'>{format_currency(s['cpo'], 2)}</b></div>"
                f"<div class='evrow'><span>Orders / day</span><b>{n2(s['opd'])}</b></div></div>")
    html_cards([ev("S07", "red", "Negative normalized profit"), ev("S03", "red", "Negative normalized profit"),
                ev("S09", "amber", "14-day comparison case")], cols=3)

    dec = ("<div class='panel p-teal'>" + pill("Decision", "teal") + "<h3>Why S07 &amp; S03?</h3>"
           "<p>We screened all 10 stores using normalized monthly profit, contribution per order and order volume. "
           "S07 and S03 are the only stores with negative normalized monthly profit. S07 also has negative contribution "
           "per order; S03 has very weak contribution per order. Both handle roughly 132–135 orders per day, so low "
           "demand alone does not explain their weak economics. S09 appeared weak in raw totals but is profitable after "
           "normalization, so it is shown as a 14-day comparison case.</p></div>")
    tiles = [("Operating days", str(s9["operating_days"])), ("Orders", fmt_int(s9["orders"])),
             ("Orders / day", n2(s9["opd"])), ("Contribution / order", format_currency(s9["cpo"], 2)),
             ("Normalized profit / month", "+" + format_currency(s9["pnl"], 2))]
    nine = ("<div class='panel panel-amber p-amber'>" + pill("Normalization comparison", "amber") + "<h3>Why not S09?</h3>"
            "<div class='mgrid'>" + "".join(
                f"<div class='mtile'><span>{_h(l)}</span><b class='{'amb' if 'profit' not in l else 'pos'}'>{_h(v)}</b></div>"
                for l, v in tiles) + "</div>"
            "<p>S09 operated for only 14 days. Raw totals are therefore not directly comparable with the 42-day stores. "
            "After normalizing for operating days, S09 is profitable and is not one of the two negative stores.</p></div>")
    html_cards([dec, nine], cols=2)
    st.caption("Screening used only normalized monthly profit, contribution per order and order volume — no "
               "composite score or weights. Selection identifies where to investigate; it does not by itself "
               "establish causes.")


def render_ruled_out() -> None:
    section("What We Ruled Out", "What does not explain the gap?")
    items = [
        ("Low demand",
         f"S03 ≈ **{a['opd']:.1f}** and S07 ≈ **{b['opd']:.1f}** orders/day, versus {oth_avg('opd'):.1f} average at "
         "the other 8 stores.", "Ruled out", "neutral"),
        ("Delivery distance",
         f"S03 **{n2(a['ds'])} km**, S07 **{n2(b['ds'])} km** vs **{n2(oth_avg('ds'))} km** other-8 average. "
         "Average delivery distance is approximately 3 km and does not materially differentiate S03/S07 from the "
         "other stores.", "Ruled out", "neutral"),
        ("One individual rider",
         "We make no claim that any single delivery partner caused the gap; the evidence here is at store level.",
         "No claim", "info"),
        ("S09 raw-total weakness",
         f"S09 operated only {s9['operating_days']} days, so raw totals are not comparable with 42-day stores. "
         f"After normalizing, S09 is +{format_currency(s9['pnl'], 2)}/month.", "Resolved", "teal"),
    ]
    html_cards([f"<div class='panel p-{tone}'>{pill(badge, tone)}<h3><span class='ro-x'>✕</span>{i}. {_h(t)}</h3>"
                f"<p>{_h(body)}</p></div>" for i, (t, body, badge, tone) in enumerate(items, start=1)], cols=4)
    st.info("The evidence points toward delivery-process anomalies, elevated returns and promotion-rule leakage "
            "rather than a simple demand, distance or raw-total problem. These are associations, not proven causes.")


# ----------------------------------------------------------------------------------
# PAGE: DASHBOARD — LANE B (DELIVERY & FULFILMENT)
# ----------------------------------------------------------------------------------
def render_same_timestamp_callout() -> None:
    tiles = [("S07", f"{n2(b['sts'])}%", "neg"), ("S03", f"{n2(a['sts'])}%", "neg"), ("Other 8", "0%", "")]
    left = ("<div class='panel p-red'>" + pill("Same-timestamp delivery scans", "red") +
            "<div class='mgrid'>" + "".join(f"<div class='mtile'><span>{l}</span><b class='{c}' style='font-size:1.9rem'>{v}</b></div>"
                                            for l, v, c in tiles) + "</div>"
            "<p class='mutp'>Share of trips with identical picked and delivered timestamps.</p></div>")
    mx = max(RR_SAME, RR_NORMAL)
    right = ("<div class='panel p-red'>" + pill("Return rate by timestamp type", "red") +
             "<div class='mgrid'><div class='mtile'><span>Same-timestamp return rate</span>"
             f"<b class='neg' style='font-size:1.9rem'>{n2(RR_SAME)}%</b></div>"
             "<div class='mtile'><span>Normal-timestamp return rate</span>"
             f"<b style='font-size:1.9rem'>{n2(RR_NORMAL)}%</b></div></div>"
             f"<div style='height:10px;border-radius:6px;background:rgba(255,255,255,.07);margin:.3rem 0 .15rem'><div style='width:{RR_SAME / mx * 100:.1f}%;height:100%;border-radius:6px;background:{DANGER}'></div></div>"
             f"<div style='height:10px;border-radius:6px;background:rgba(255,255,255,.07);margin:.3rem 0'><div style='width:{RR_NORMAL / mx * 100:.1f}%;height:100%;border-radius:6px;background:{NEUTRAL}'></div></div>"
             "<p class='mutp'>This is a strong association in the supplied data, but it does not by itself prove causation.</p></div>")
    html_cards([left, right], cols=2)


def render_lane_b() -> None:
    section("Delivery Performance")
    st.info("**Important finding.** High lateness and high delivery cost occur at S03/S07 despite average delivery "
            "distance being similar to the network.")
    c1, c2 = st.columns(2)
    with c1:
        with chart_card("Late rate", "% of delivered orders with pickup-to-delivery time > 10 min · "
                                     "dashed line = other-8 average"):
            render_bar_chart(
                lambda s: s["lr"], lambda v: f"{v:.1f}%",
                lambda s: f"{fmt_int(s['late'])} late of {fmt_int(s['deliv'])} delivered = {n2(s['lr'])}%",
                "ch_late", descending=True, ref=(oth_avg("lr"), f"other-8 avg {oth_avg('lr'):.1f}%"))
    with c2:
        with chart_card("Delivery cost per order",
                        f"₹ per order (all orders) · dashed line = ₹28 benchmark (other-8 average "
                        f"₹{oth_avg('dc'):.2f})"):
            render_bar_chart(
                lambda s: s["dc"], lambda v: f"₹{v:.1f}",
                lambda s: f"{format_currency(s['dcost_sum'])} ÷ {fmt_int(s['orders'])} orders = {format_currency(s['dc'], 2)}",
                "ch_dc", descending=True, ref=(DELIVERY_COST_BENCHMARK, "₹28 benchmark"))
    c3, c4 = st.columns(2)
    with c3:
        with chart_card("Average delivery time", "minutes (delivered orders) · dashed line = 10-minute late threshold"):
            render_bar_chart(
                lambda s: s["tm"], lambda v: f"{v:.1f}", lambda s: f"{n2(s['tm'])} min average",
                "ch_tm", descending=True, ref=(10, "10-min late threshold"))
    with c4:
        with chart_card("Average delivery distance", "km (valid trips) · axis starts at 0", "Ruled out", "neutral"):
            render_bar_chart(
                lambda s: s["ds"], lambda v: f"{v:.2f}",
                lambda s: f"{n2(s['ds'])} km over {fmt_int(s['dist_n'])} valid trips",
                "ch_ds", descending=True, x_range=(0, 4))
            st.info("Average delivery distance is approximately 3 km and does not materially differentiate S03/S07 "
                    "from the other stores.")

    section("Delivery-scan validation", "deeper validation · S07 & S03")
    render_same_timestamp_callout()
    v1, v2 = st.columns(2)
    with v1, st.container(border=True):
        st.markdown(tag("Evidence", "info"))
        st.markdown("### Same-Timestamp Delivery Scans")
        business_question("Are there unusual delivery records where picked and delivered timestamps are identical?")
        st.caption("% of trips with identical picked and delivered timestamps · sorted highest → lowest")
        render_bar_chart(
            lambda s: s["sts"], lambda v: f"{v:.2f}%",
            lambda s: (f"{fmt_int(s['same_ts'])} same-timestamp trips of {fmt_int(s['trips'])} trips = {n2(s['sts'])}%"
                       if s["trips"] and s["trips"] > 0 else "0% — no same-timestamp trips"),
            "ch_sts", descending=True)
        sts_table = pd.DataFrame(
            [{"Store": s["id"], "Same-timestamp trips": fmt_int(s["same_ts"]), "Total trips": fmt_int(s["trips"]),
              "Share": f"{n2(s['sts'])}%"} for s in (b, a)]
            + [{"Store": "Other 8 stores", "Same-timestamp trips": "0", "Total trips": "—", "Share": "0%"}])
        show_table(sts_table)
        st.success("**Finding:** Same-timestamp delivery scans are concentrated at S07 and S03, while the other "
                   "stores show 0%.")
        st.caption("These are unusual delivery scans flagged for audit; the data alone does not establish why they occur.")
    with v2, st.container(border=True):
        st.markdown(tag("Consequence", "info"))
        st.markdown("### Same-Timestamp Scans & Returns")
        business_question("Do orders with same-timestamp delivery scans have a higher return rate?")
        st.caption("% of orders returned")
        render_return_comparison()
        rt = pd.DataFrame([
            {"Group": "Same timestamp", "Orders": fmt_int(RET["same"]["n"]), "Returned": fmt_int(RET["same"]["ret"]),
             "Return rate": f"{n2(RR_SAME)}%"},
            {"Group": "Normal timestamp", "Orders": fmt_int(RET["normal"]["n"]),
             "Returned": fmt_int(RET["normal"]["ret"]), "Return rate": f"{n2(RR_NORMAL)}%"},
        ])
        show_table(rt)
        st.success(f"**Finding:** Orders with same-timestamp delivery scans have a {n2(RR_SAME)}% return rate "
                   f"versus {n2(RR_NORMAL)}% for normal-timestamp orders.")
        st.caption("This is a strong association in the supplied data, but it does not by itself prove causation.")

    render_store_comparison()


def render_store_comparison() -> None:
    with st.container(border=True):
        st.markdown("### S03 vs S07 vs the other 8 stores")
        sid = st.radio("Store", ["S03", "S07"], horizontal=True, label_visibility="collapsed", key="cmp_store")
        s = STORES[sid]
        metrics = [("Late rate", "lr", "%"), ("Delivery cost / order", "dc", "₹"), ("Avg delivery time", "tm", " min"),
                   ("Avg distance", "ds", " km"), ("Return rate", "rr", "%"), ("Promo usage", "pu", "%"),
                   ("Discount / delivered order", "di", "₹")]
        rows = []
        for label, k, u in metrics:
            f = (lambda v, u=u: f"₹{v:.2f}" if u == "₹" else f"{v:.2f}{u}")
            x = oth_avg(k)
            gap = s[k] - x
            rows.append({"Metric": label, sid: f(s[k]), "Other 8 avg": f(x), "Gap": f"{'+' if gap >= 0 else ''}{gap:.2f}"})
        rows.append({"Metric": "Normalized profit / month", sid: format_currency(s["pnl"], 2),
                     "Other 8 avg": format_currency(oth_avg("pnl"), 2),
                     "Gap": format_currency(s["pnl"] - oth_avg("pnl"), 2)})
        rows.append({"Metric": "Same-timestamp scans", sid: f"{n2(s['sts'])}%", "Other 8 avg": "0.00%",
                     "Gap": f"+{n2(s['sts'])}"})
        show_table(pd.DataFrame(rows))
        st.caption("Distance is the one metric that does not differ — it was investigated and ruled out as an "
                   "explanation. Lateness, cost and delivery-scan patterns differ sharply at the same distance.")


# ----------------------------------------------------------------------------------
# PAGE: DASHBOARD — LANE C (PRODUCT & PROMOTION)
# ----------------------------------------------------------------------------------
def render_lane_c() -> None:
    c1, c2 = st.columns(2)
    order = sorted(CATS, key=lambda c: category_margin("OTH", c))
    short = {"FRUITS & VEGETABLES": "FRUITS & VEG", "SNACKS & PACKAGED": "SNACKS & PACK."}
    with c1:
        with chart_card("Category margin %",
                        "(revenue − cost) ÷ revenue, delivered orders · sorted by other-8 margin"):
            groups = [{"n": short.get(c, c)} for c in order]
            series = [
                {"n": "S07", "c": DANGER, "v": [category_margin("S07", c) for c in order]},
                {"n": "S03", "c": DANGER_SOFT, "v": [category_margin("S03", c) for c in order]},
                {"n": "Other 8", "c": NEUTRAL, "v": [category_margin("OTH", c) for c in order]},
            ]
            render_grouped_chart(groups, series, lambda v: f"{v:.1f}%", "ch_cat")
    with c2:
        with chart_card("Promo usage", "% of delivered orders · sorted highest → lowest"):
            render_bar_chart(
                lambda s: s["pu"], lambda v: f"{v:.1f}%",
                lambda s: f"{fmt_int(s['promo_n'])} promo orders of {fmt_int(s['deliv'])} delivered = {n2(s['pu'])}%",
                "ch_pu", descending=True)
    c3, c4 = st.columns(2)
    with c3:
        with chart_card("Discount per delivered order", "₹ per delivered order · sorted highest → lowest"):
            render_bar_chart(
                lambda s: s["di"], lambda v: f"₹{v:.1f}",
                lambda s: f"{format_currency(s['disc_sum'])} ÷ {fmt_int(s['deliv'])} delivered = {format_currency(s['di'], 2)}",
                "ch_di", descending=True)
    with c4:
        with chart_card("Contribution per order by promo", "₹ per delivered order · zero line shown"):
            groups = [{"n": p, "x": [f"{PROMO[('S07', p)]['n']} orders", f"{PROMO[('S03', p)]['n']} orders"]}
                      for p in PROMO_ORDER]
            series = [
                {"n": "S07", "c": DANGER, "v": [PROMO[("S07", p)]["cpo"] for p in PROMO_ORDER]},
                {"n": "S03", "c": DANGER_SOFT, "v": [PROMO[("S03", p)]["cpo"] for p in PROMO_ORDER]},
            ]
            render_grouped_chart(groups, series, lambda v: format_currency(v, 0), "ch_promo")

    nf, nn = NET_PROMO["FRESH50"], NET_PROMO["No Promo"]
    with st.container(border=True):
        st.markdown(tag("FRESH50 highlight", "red"))
        m = st.columns(3)
        with m[0]:
            st.markdown(f"## {colorize(format_currency(PROMO[('S03', 'FRESH50')]['cpo'], 2), 'red')}")
            st.caption(f"S03 average contribution/order on FRESH50 (No Promo: "
                       f"{format_currency(PROMO[('S03', 'No Promo')]['cpo'], 2)})")
        with m[1]:
            st.markdown(f"## {colorize(format_currency(PROMO[('S07', 'FRESH50')]['cpo'], 2), 'red')}")
            st.caption(f"S07 average contribution/order on FRESH50 (No Promo: "
                       f"{format_currency(PROMO[('S07', 'No Promo')]['cpo'], 2)})")
        with m[2]:
            st.markdown(f"## {colorize(f'{FRESH50_PRIORITY / FRESH50_ALL * 100:.0f}%', 'amber')}")
            st.caption(f"of FRESH50 orders ({fmt_int(FRESH50_PRIORITY)} of {fmt_int(FRESH50_ALL)}) are at S03 and S07")
        st.markdown("FRESH50 is associated with strongly negative average contribution per order at both S03 and S07.")
        st.caption(f"Network-wide, the FRESH50 average is also negative ({format_currency(nf['cpo'], 2)} over "
                   f"{fmt_int(nf['n'])} orders vs {format_currency(nn['cpo'], 2)} for No Promo), so a negative "
                   "average is not unique to these two stores; S03 and S07 differ mainly in how heavily it is used. "
                   "This does not prove FRESH50 alone caused the store losses.")

    section("Promotion-rule validation", "deeper validation · S03 & S07")
    p1, p2 = st.columns(2)
    with p1, st.container(border=True):
        st.markdown(tag("Evidence", "info"))
        st.markdown("### Promo Floor Validation")
        business_question("Are promotional orders meeting the minimum-order value required by their promotion rule?")
        show_table(pd.DataFrame([
            {"Store": s["id"], "Promotional orders": fmt_int(PF[s["id"]]["promo_orders"]),
             "Below floor": fmt_int(PF[s["id"]]["below"]), "Share": f"{n2(PF[s['id']]['pct'])}%"} for s in (a, b)]))
        st.caption(f"The Promo_Codes table shows the FRESH50 minimum order value is {format_currency(FLOOR50)}. The "
                   "check covers all promotions against each promotion’s applicable minimum-order value.")
        st.success(f"**Finding:** Approximately 42% of promotional orders at S03 and S07 were below the applicable "
                   f"minimum-order value ({n2(PF['S03']['pct'])}% and {n2(PF['S07']['pct'])}%).")
    with p2, st.container(border=True):
        st.markdown(tag("Financial evidence", "amber"))
        st.markdown("### Promo-Floor Discount Leakage")
        business_question("What is the discount value given on below-floor promotional orders?")
        emit("<div class='exposure' style='margin-bottom:.8rem'><div class='exposure-t'>Potential discount leakage · not guaranteed savings</div>"
             "<div class='mgrid'>"
             f"<div class='mtile'><span>S03 per month</span><b class='amb' style='font-size:1.9rem'>{format_k(PF['S03']['leak30'])}</b></div>"
             f"<div class='mtile'><span>S07 per month</span><b class='amb' style='font-size:1.9rem'>{format_k(PF['S07']['leak30'])}</b></div></div></div>")
        show_table(pd.DataFrame([
            {"Store": s["id"], "Below-floor orders": fmt_int(PF[s["id"]]["below"]),
             "42-day leakage": format_currency(PF[s["id"]]["leak42"], 2),
             "Per month": format_currency(PF[s["id"]]["leak30"], 2)} for s in (a, b)]))
        st.success(f"**Finding:** Below-floor promotional orders received approximately "
                   f"{format_lakh(PF['S03']['leak42'])} of discount value at S03 and {format_lakh(PF['S07']['leak42'])} "
                   "at S07 over the 42-day period.")
        st.warning(f"**Potential monthly equivalent:** S03 ≈ {format_k(PF['S03']['leak30'])} · "
                   f"S07 ≈ {format_k(PF['S07']['leak30'])}")
        st.caption("This is potential discount leakage, not guaranteed savings. Monthly equivalent = 42-day leakage × 30 ÷ 42.")


def render_dashboard() -> None:
    page_header("Dashboard", "Network Analytics",
                "All ten stores. S07 and S03 in red; S09 in amber as the 14-day normalization comparison case "
                "(Lane A). Hover any bar for the arithmetic.")
    tab_a, tab_b, tab_c = st.tabs(["A · Store Performance", "B · Delivery & Fulfilment", "C · Product & Promotion"])
    with tab_a:
        render_lane_a()
    with tab_b:
        render_lane_b()
    with tab_c:
        render_lane_c()


# ----------------------------------------------------------------------------------
# PAGE: FINDINGS
# ----------------------------------------------------------------------------------
def render_findings() -> None:
    page_header("Findings", "What the evidence shows",
                "The investigation moved from initial exploration → store screening → deeper validation → final "
                "findings. Each card follows Observation → Evidence → Insight → Implication. Wording is “associated "
                "with”, not “caused by”, wherever the data cannot prove causation.")
    render_findings_grid(findings_primary())

    section("Supporting exploratory evidence", "earlier screening work · secondary to F1–F5")
    render_findings_grid(findings_secondary())

    section("Data Quality Audit — After Cleaning", "issue → treatment")
    st.caption("Counts shown here refer to the processed analytical dataset after cleaning; original raw-input "
               "defect counts are documented separately in the cleaning log.")
    render_data_quality()
    st.info(VALIDATION_NOTE)

    section("Reconciliation: dashboard vs. MySQL-verified results")
    render_reconciliation()

    with st.expander("Methodology & Definitions"):
        left, right = st.columns(2)
        left.markdown(METHODOLOGY_LEFT)
        right.markdown(METHODOLOGY_RIGHT)
        st.caption(METHODOLOGY_NOTE)


# ----------------------------------------------------------------------------------
# PAGE: COO DECISION
# ----------------------------------------------------------------------------------
def exec_card_html(store_id: str) -> str:
    s, p = STORES[store_id], PF[store_id]
    tiles = [("Return rate", f"{n2(s['rr'])}%"), ("Same-timestamp scans", f"{n2(s['sts'])}%"),
             ("Promo-floor violations", f"{n2(p['pct'])}%"), ("Promo-floor leakage", f"{format_k(p['leak30'])}/month")]
    return (f"<div class='exec'>{pill('Priority investigation', 'red')}<h3>{store_id} · {_h(s['name'])}</h3>"
            f"<div class='exec-hero'><span>Normalized profit / month</span><b>{format_currency(s['pnl'], 2)}</b></div>"
            "<div class='exec-grid'>" + "".join(
                f"<div class='mtile'><span>{_h(l)}</span><b{' class=amb' if 'leakage' in l else ''}>{_h(v)}</b></div>"
                for l, v in tiles) + "</div></div>")


def exploratory_block(store_id: str) -> None:
    o, s, p = OPP[store_id], STORES[store_id], PF[store_id]
    st.markdown(f"#### {store_id} · {s['name']}")
    show_table(pd.DataFrame([
        {"Metric": "Contribution / order",
         "Value": f"{format_currency(s['cpo'], 2)} · {'negative' if s['cpo'] < 0 else 'weak'}"},
        {"Metric": "Return rate vs other-8", "Value": f"{n2(s['rr'])}% vs {B_RR * 100:.2f}%"},
        {"Metric": "Delivery cost / order", "Value": f"{format_currency(s['dc'], 2)} vs ₹28"},
        {"Metric": "Late rate", "Value": f"{n2(s['lr'])}% vs {oth_avg('lr'):.1f}%"},
        {"Metric": "Promotion burden",
         "Value": f"{format_currency(s['di'], 2)} discount/order vs {format_currency(B_DI, 2)}; "
                  f"{n2(s['pu'])}% promo use"},
        {"Metric": "Benchmark gap: return recovery", "Value": format_k(o["ret"])},
        {"Metric": "Benchmark gap: excess delivery cost", "Value": format_k(o["dc"])},
        {"Metric": "Benchmark gap: excess discount", "Value": format_k(o["dis"])},
    ]))
    st.text(
        f"Promo-floor leakage: {p['below']} below-floor orders · 42-day discount "
        f"{format_currency(p['leak42'], 2)} × 30/42 = {format_currency(p['leak30'], 2)}/month\n\n"
        f"Return: excess returns = {s['ret']} − {B_RR * 100:.3f}% × {s['orders']} = {o['excess_returns']:.1f}\n"
        f"{o['excess_returns']:.1f} × {format_currency(s['dcpo'], 2)} (delivered contribution/order) × 30/42 = "
        f"{format_currency(o['ret'])}\n\n"
        f"Delivery: 42-day cost {format_currency(s['dcost_sum'])} − ₹28 × {s['orders']} orders = "
        f"{format_currency(o['dc42'])}\n× 30/42 = {format_currency(o['dc'])}\n\n"
        f"Discount: ({format_currency(s['di'], 2)} − {format_currency(B_DI, 2)}) × {s['deliv']} delivered = "
        f"{format_currency(o['dis42'])}\n× 30/42 = {format_currency(o['dis'])}"
    )


def render_coo() -> None:
    page_header("COO Decision", "Priority Investigation: S07 & S03",
                "After normalizing for operating days, S07 and S03 are the only stores with negative monthly "
                "profit. The evidence then points to delivery-process anomalies, elevated returns and "
                "promotion-rule leakage.")
    c1, c2 = st.columns(2)
    with c1:
        emit(exec_card_html("S07"))
    with c2:
        emit(exec_card_html("S03"))
    st.write("")
    st.warning("**S07 & S03 — priority investigation.** Both were selected through the same normalized "
               "store-screening process. Promo-floor leakage is potential discount leakage, not a guaranteed "
               "saving, and the supporting exploratory benchmark gaps overlap, so they should not be added "
               "together. Associations here do not by themselves prove causation.")

    section("Potential Monthly Financial Exposure")
    emit("<div class='exposure'><div class='exposure-t'>Potential promo-floor discount leakage · potential, not guaranteed savings</div>"
         "<div class='mgrid' style='grid-template-columns:repeat(auto-fit,minmax(220px,1fr))'>"
         f"<div class='mtile'><span>S07 per month</span><b class='amb' style='font-size:2.2rem'>{format_k(PF['S07']['leak30'])}</b></div>"
         f"<div class='mtile'><span>S03 per month</span><b class='amb' style='font-size:2.2rem'>{format_k(PF['S03']['leak30'])}</b></div>"
         "</div></div>")

    st.write("")
    with st.expander("Supporting Exploratory Metrics & Benchmark Gaps", expanded=False):
        emit("<div class='warnbox'><div class='wt'>Supporting exploratory analysis</div><ul>"
             "<li>Separate from the final validated recoverable value.</li><li>Not guaranteed savings.</li>"
             "<li>Figures overlap and must not be summed into one final financial impact.</li></ul></div>")
        st.caption("These benchmark-gap figures are supporting exploratory estimates from earlier analysis. "
                   "They are not the final recoverable-value calculation, are not guaranteed savings, and "
                   "should not be summed into one final financial impact.")
        e1, e2 = st.columns(2)
        with e1:
            exploratory_block("S07")
        with e2:
            exploratory_block("S03")
        st.caption(f"Exploratory benchmarks: return rate and discount/order = other-8 average; delivery cost "
                   f"₹28/order (other-8 average ₹{oth_avg('dc'):.2f}). These overlap and are not additive.")

    section("Monday Morning Action Plan")
    plans = {
        "S07": ["Audit same-timestamp delivery scans", "Audit return reasons, starting with same-timestamp orders",
                "Review promo minimum-order rule enforcement (FRESH50 floor ₹800)", "Review delivery process and cost"],
        "S03": ["Audit same-timestamp delivery scans", "Audit return reasons, starting with same-timestamp orders",
                "Review promo minimum-order rule enforcement", "Review product mix as secondary evidence"],
    }
    icons = ["⌕", "↺", "％", "➜"]
    cards = []
    for sid, steps in plans.items():
        rows = "".join(f"<div class='act'><div class='no'>{i}</div><div class='ic'>{icons[i - 1]}</div>"
                       f"<div class='tx2'>{_h(t)}</div></div>" for i, t in enumerate(steps, start=1))
        cards.append(f"<div class='panel p-red'><div style='display:flex;justify-content:space-between;align-items:center'>"
                     f"<b style='font-size:1.3rem'>{sid}</b>{pill('Action checklist', 'neutral')}</div>{rows}</div>")
    html_cards(cards, cols=2)
    st.caption("Piloting changes at one store and tracking late rate, return rate and contribution per order for "
               "2–3 weeks would show how much of the opportunity is real.")

    section("What Would Make Us Wrong?", "a strength, not something to hide")
    risks = [
        ("Unrepresentative period", "The 42-day period may not represent normal operations."),
        ("Association ≠ causation", "Associations may not be causal."),
        ("Missing factors", "Some operational costs or factors may be absent from the supplied datasets."),
        ("Potential, not guaranteed",
         "Promo-floor leakage is potential discount leakage; benchmark gaps assume movement toward the benchmark."),
    ]
    html_cards([f"<div class='panel risk p-amber'><span class='ri'>⚠</span><h4>{_h(t)}</h4><p class='mutp'>{_h(d)}</p></div>"
                for t, d in risks], cols=4)


# ----------------------------------------------------------------------------------
# NAVIGATION + MAIN
# ----------------------------------------------------------------------------------
PAGES = {
    "Home": render_home,
    "Dashboard": render_dashboard,
    "Findings": render_findings,
    "COO Decision": render_coo,
}


PAGE_ICONS = {"Home": "⌂", "Dashboard": "▦", "Findings": "◎", "COO Decision": "★"}


def go_to(page: str) -> None:
    st.session_state["page"] = page


def render_sidebar() -> None:
    """Permanent left sidebar: branding, vertical navigation (one page at a time), audit stats."""
    with st.sidebar:
        st.markdown('<div class="sb-top"><span class="logo-mark"></span><div class="sb-brand">DARK STORE<br><span>DOWN</span></div></div>'
                    '<div class="sb-sub">Zipto Quick Commerce<br>Noida Cluster Review</div>'
                    '<div class="sb-label">NAVIGATION</div>', unsafe_allow_html=True)
        st.radio("Navigate", list(PAGES), key="page", label_visibility="collapsed",
                 format_func=lambda p: f"{PAGE_ICONS[p]}   {p}")
        st.markdown(f'<div class="sb-stats"><div class="sb-stat"><b>42-DAY</b><span>AUDIT</span></div>'
                    f'<div class="sb-stat"><b>10</b><span>STORES</span></div>'
                    f'<div class="sb-stat"><b>{fmt_int(ORDERS)}</b><span>ORDERS</span></div></div>',
                    unsafe_allow_html=True)


def render_footer() -> None:
    st.divider()
    f1, f2 = st.columns(2)
    f1.caption(f"**Zipto Quick Commerce — Noida Cluster Review**  \n42-day analytical review · 10 dark stores · "
               f"{fmt_int(ORDERS)} orders")
    f2.caption("SQL Analysis · Power Query Cleaning · Python · Streamlit · Plotly Dashboard  \n"
               "Source: Zipto Quick Commerce Hackathon datasets")


def main() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    if st.session_state.get("page") not in PAGES:
        st.session_state["page"] = "Home"
    render_sidebar()
    PAGES[st.session_state["page"]]()
    render_footer()


if __name__ == "__main__":
    main()