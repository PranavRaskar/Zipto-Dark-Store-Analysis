# DARK STORE DOWN — Zipto Quick Commerce

## Noida Cluster Review | Data Analytics Hackathon 2026

An end-to-end data analytics project answering one core business question:

> **Which two stores should Zipto investigate first, what is broken in each, and what is the potential monthly financial improvement?**

Built using **Excel / Power Query**, **MySQL**, and an **interactive HTML dashboard**.

---

## 📌 Business Problem

The analysis covers three areas:

- **Store Performance** — Which stores make money and which lose it?
- **Delivery & Fulfilment** — How do delivery time, lateness, returns, distance, and delivery cost vary by store?
- **Product & Promotions** — What are we selling, and what are promotions costing?

---

## 📊 Dataset Overview

| Metric | Value |
|---|---:|
| Analysis period | **42 days** |
| Period | **18 May 2026 – 28 June 2026** |
| Stores | **10** |
| Total orders | **52,133** |
| Delivered | **48,510** |
| Returned | **2,556** |
| Cancelled | **1,067** |
| Net amount | **₹27.16M** |
| COGS | **₹21.12M** |
| Delivery cost | **₹1.618M** |
| Contribution before rent | **₹3.026M** |

---

## 🔄 Analysis Workflow

```text
Raw Data
   ↓
Excel / Power Query
   ↓
Data Cleaning & Validation
   ↓
MySQL Analysis
   ↓
Store Screening
   ↓
S07 & S03 Investigation
   ↓
Delivery + Product + Promotion Analysis
   ↓
Benchmark Comparison
   ↓
Potential ₹ / Month Opportunities
   ↓
HTML Dashboard
```

---

## 🧹 Data Cleaning

Key cleaning steps included:

- Text and field standardisation
- Timestamp conversion
- Numeric data conversion
- Currency-symbol removal
- Hidden-character cleanup in delivery partner IDs
- Invalid / negative distance handling
- Legitimate `NULL` values retained
- Relationship and join validation
- Reconciliation of key totals
- `Order_Items` schema correction

A hidden `CHAR(13)` carriage return in delivery partner IDs was removed so the S03/S07 delivery-partner relationships matched correctly.

The previously reported **83% above 10 km** finding was revalidated and **excluded from the final analysis**.

---

# 🔴 S07 — Largest P&L Loss

| Metric | Value |
|---|---:|
| **P&L** | **−₹521,868.46** |
| Contribution | **−₹202,668.46** |
| Contribution / order | **−₹35.64** |
| Orders / day | **135.40** |
| Return rate | **14.01%** |
| Delivery cost / order | **₹42.12** |
| Promo usage | **28.68%** |
| Discount / delivered order | **₹48.69** |
| FRESH50 contribution / order | **−₹205.48** |

### Main Findings

- Negative contribution per order
- Elevated return rate
- Higher delivery cost per order
- High promotion and discount burden
- FRESH50 associated with strongly negative average contribution per order
- Meat & Seafood has the weakest category margin at **6.51%**

---

# 🔵 S03 — Second-Largest P&L Loss

| Metric | Value |
|---|---:|
| **P&L** | **−₹194,664.97** |
| Contribution | **₹79,735.03** |
| Contribution / order | **₹14.33** |
| Orders / day | **132.48** |
| Return rate | **7.94%** |
| Delivery cost / order | **₹41.98** |
| Promo usage | **28.95%** |
| Discount / delivered order | **₹49.18** |
| FRESH50 contribution / order | **−₹178.93** |

### Main Findings

- Very low contribution per order
- Elevated return rate
- Higher delivery cost per order
- High promotion and discount burden
- FRESH50 associated with strongly negative average contribution per order
- Meat & Seafood has the weakest category margin at **6.84%**

---

## 🚚 Delivery Findings

**Late delivery definition:**

```text
Pickup-to-delivery time > 10 minutes
```

| Metric | S03 | S07 |
|---|---:|---:|
| Late rate | **72.33%** | **72.10%** |
| Delivery cost / order | **₹41.98** | **₹42.12** |
| Avg. valid distance | **~2.99 km** | **~3.02 km** |

Additional checks found that:

- Distance does not meaningfully differentiate S03/S07 from the other stores.
- Gig vs Full-time partner type did not meaningfully explain the delivery-cost gap.
- The analysis does not establish that one delivery partner caused the issue.

---

## 🛒 Product & Promotion Findings

### Category Margins

| Category | S07 | S03 |
|---|---:|---:|
| Meat & Seafood | **6.51%** | **6.84%** |
| Dairy & Eggs | **17.68%** | **17.48%** |
| Bakery | **17.89%** | **18.34%** |

### Promotion Burden

| Metric | S07 | S03 |
|---|---:|---:|
| Promo usage | **28.68%** | **28.95%** |
| Discount / delivered order | **₹48.69** | **₹49.18** |

### FRESH50

| Store | Avg. contribution / order |
|---|---:|
| **S07** | **−₹205.48** |
| **S03** | **−₹178.93** |

> FRESH50 is associated with strongly negative average contribution per order at both stores.

---

# 💵 Potential Monthly Financial Opportunity

These are **separate potential improvement opportunities**, not guaranteed savings.

### S07

- Return recovery: **~₹15.7K/month**
- Excess delivery cost: **~₹57.4K/month**
- Excess discount: **~₹82.6K/month**

### S03

- Return recovery: **~₹10.3K/month**
- Excess delivery cost: **~₹55.6K/month**
- Excess discount: **~₹88.5K/month**

> **The opportunity figures should not be added together because they may overlap.**

---

## 🧾 Key SQL Queries

- **Q7** — Store Performance Scorecard
- **Q8** — Delivery Performance by Store
- **Q11** — Product Category Economics
- **Q13** — Promotion-Level Contribution
- **Q15** — Final Evidence Table

---

## 🛠️ Technology Stack

- **Excel / Power Query** — Data cleaning
- **MySQL** — Data analysis
- **HTML / CSS / JavaScript** — Interactive dashboard
- **GitHub** — Project hosting

---

## 🌐 Project Dashboard

**[Open Live Dashboard](https://pranavraskar.github.io/Zipto-Dark-Store-Analysis)**

## 💻 GitHub Repository

**[View Repository](https://github.com/PranavRaskar/Zipto-Dark-Store-Analysis)**

## 🔗 LinkedIn

**[View LinkedIn Post](ADD_LINKEDIN_POST_LINK_HERE)**

---

## ✅ Final Takeaway

The analysis identifies **S07 and S03 for deeper investigation** based on their weak store-level economics and supporting evidence across:

**Store Performance → Delivery & Fulfilment → Product & Promotions**

The monthly figures represent **potential benchmark-based improvement opportunities** and are **not additive or guaranteed savings**.

---

## ⚠️ Limitations

- Analysis covers **42 days** of data.
- Observed relationships do not establish causation.
- Potential financial opportunities depend on benchmark assumptions.
- Opportunity figures may overlap.
- Some order-item rows have missing unit-cost values.
- Findings are limited to the supplied data and challenge definitions.

---

## 👥 Team

**Data Analytics Hackathon 2026 — Zipto Quick Commerce**

**Analysis Areas:**

Store Performance • Delivery & Fulfilment • Product & Promotions
