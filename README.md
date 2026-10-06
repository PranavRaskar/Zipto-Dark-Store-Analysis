# DARK STORE DOWN — Zipto Quick Commerce

## Noida Cluster Review | Data Analytics Hackathon 2026

An end-to-end data analytics project answering one core business question:

> **Which two stores require deeper investigation, what is broken in each, and what is the potential monthly financial improvement?**

Built using **Excel / Power Query**, **MySQL**, and an **interactive HTML dashboard**.

---

## 📌 Business Problem

The analysis covers three areas:

* **Store Performance** — Which stores make money and which lose it?
* **Delivery & Fulfilment** — How do delivery time, lateness, returns, distance, and delivery cost vary by store?
* **Product & Promotions** — What are we selling, and what are promotions costing?

---

## 📊 Dataset Overview

| Metric                   |                          Value |
| ------------------------ | -----------------------------: |
| Analysis period          |                    **42 days** |
| Period                   | **18 May 2026 – 28 June 2026** |
| Stores                   |                         **10** |
| Total orders             |                     **52,133** |
| Delivered                |                     **48,510** |
| Returned                 |                      **2,556** |
| Cancelled                |                      **1,067** |
| Net amount               |                    **₹27.16M** |
| COGS                     |                    **₹21.12M** |
| Delivery cost            |                    **₹1.618M** |
| Contribution before rent |                    **₹3.026M** |

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
Initial Store Screening
   ↓
Operating-Day Adjustment
   ↓
S07 & S03 Investigation
   ↓
Delivery + Product + Promotion Analysis
   ↓
Validate Findings
   ↓
Potential ₹ / Month Opportunities
   ↓
HTML Dashboard
```

---

## 🧹 Data Cleaning

Key cleaning steps included:

* Text and field standardisation
* Timestamp conversion
* Numeric data conversion
* Currency-symbol removal
* Hidden-character cleanup in delivery partner IDs
* Invalid / negative distance handling
* Legitimate `NULL` values retained
* Relationship and join validation
* Reconciliation of key totals
* `Order_Items` schema correction

A hidden `CHAR(13)` carriage return in delivery partner IDs was removed so delivery-partner relationships could be matched correctly.

> The previously reported **83% above 10 km** finding was revalidated and **excluded from the final analysis** because it was not supported by the validated distance data.

---

# 🔎 Initial Store Screening

The initial store-performance screening highlighted **S07, S03, and S09** as stores requiring further investigation based on store-level orders, contribution and P&L.

However, the stores did not all operate for the same number of days. Therefore, the initial result was **not used as the final store selection**.

The next step was to adjust store performance for actual operating days.

---

# 📐 Operating-Day Adjusted Store Comparison

### Final Store Selection

After adjusting contribution for the number of operating days:

| Store   | Operating days |    Orders | Adjusted monthly profit |
| ------- | -------------: | --------: | ----------------------: |
| **S07** |         **42** | **5,687** |        **−₹372,763.19** |
| **S03** |         **42** | **5,564** |        **−₹139,046.41** |
| **S09** |         **14** | **1,815** |        **+₹116,625.05** |

> **S07 and S03 are the only stores with negative adjusted monthly profit. S09 is profitable after accounting for its shorter operating period.**

This operating-day adjustment was used as the basis for the final investigation focus.

---

# 🔴 S07 — Largest Adjusted Loss

| Metric                       |            Value |
| ---------------------------- | ---------------: |
| **Adjusted monthly profit**  |     **−₹372.8K** |
| Contribution                 | **−₹202,668.46** |
| Contribution / order         |      **−₹35.64** |
| Orders / day                 |       **135.40** |
| Return rate                  |       **14.01%** |
| Delivery cost / order        |       **₹42.12** |
| Promo usage                  |       **28.68%** |
| Discount / delivered order   |       **₹48.69** |
| FRESH50 contribution / order |     **−₹205.48** |

### Main Findings

* Negative contribution per order
* Elevated return rate compared with the network
* Higher delivery cost per order
* High promotion and discount burden
* FRESH50 is associated with strongly negative average contribution per order
* Meat & Seafood has the lowest category margin at **6.51%** among the highlighted categories
* **19.03% of S07 trips have the same picked and delivered timestamp**
* **42.45% of S07 promotional orders are below the applicable minimum-order value**

---

# 🔵 S03 — Second-Largest Adjusted Loss

| Metric                       |          Value |
| ---------------------------- | -------------: |
| **Adjusted monthly profit**  |   **−₹139.0K** |
| Contribution                 | **₹79,735.03** |
| Contribution / order         |     **₹14.33** |
| Orders / day                 |     **132.48** |
| Return rate                  |      **7.94%** |
| Delivery cost / order        |     **₹41.98** |
| Promo usage                  |     **28.95%** |
| Discount / delivered order   |     **₹49.18** |
| FRESH50 contribution / order |   **−₹178.93** |

### Main Findings

* Very low contribution per order
* Elevated return rate compared with the network
* Higher delivery cost per order
* High promotion and discount burden
* FRESH50 is associated with strongly negative average contribution per order
* Meat & Seafood has the lowest category margin at **6.84%** among the highlighted categories
* **16.77% of S03 trips have the same picked and delivered timestamp**
* **41.78% of S03 promotional orders are below the applicable minimum-order value**

---

# 🚚 Delivery & Fulfilment Findings

## Standard Delivery Analysis

**Late delivery definition:**

```text
Pickup-to-delivery time > 10 minutes
```

| Metric                |          S03 |          S07 |
| --------------------- | -----------: | -----------: |
| Late rate             |   **72.33%** |   **72.10%** |
| Delivery cost / order |   **₹41.98** |   **₹42.12** |
| Avg. valid distance   | **~2.99 km** | **~3.02 km** |

These are supporting delivery-performance metrics.

Additional checks found:

* Distance does not meaningfully differentiate S03/S07 from the other stores.
* Gig vs Full-time partner type did not meaningfully explain the delivery-cost gap.
* The analysis does not establish that one delivery partner caused the issue.

---

## ⏱️ Same-Timestamp Delivery Scan Validation

A separate validation checked whether `picked_ts = delivered_ts`.

| Store group        | Same-timestamp share |
| ------------------ | -------------------: |
| **S07**            |           **19.03%** |
| **S03**            |           **16.77%** |
| **Other 8 stores** |            **0.00%** |

This pattern is concentrated at S07 and S03.

### Same-Timestamp Orders vs Normal Orders

| Scan type        |     Orders | Returned orders | Return rate |
| ---------------- | ---------: | --------------: | ----------: |
| Same timestamp   |  **2,015** |         **689** |  **34.19%** |
| Normal timestamp | **50,118** |       **1,867** |   **3.73%** |

> Same-timestamp orders show a much higher return rate. This is an **association, not proof of causation**.

---

# 🛒 Product & Promotion Findings

## Category Margins

| Category       |        S07 |        S03 |
| -------------- | ---------: | ---------: |
| Meat & Seafood |  **6.51%** |  **6.84%** |
| Dairy & Eggs   | **17.68%** | **17.48%** |
| Bakery         | **17.89%** | **18.34%** |

> Category margin analysis is treated as **secondary evidence**, not the primary root-cause finding.

---

## Promotion Burden

| Metric                     |        S07 |        S03 |
| -------------------------- | ---------: | ---------: |
| Promo usage                | **28.68%** | **28.95%** |
| Discount / delivered order | **₹48.69** | **₹49.18** |

---

## FRESH50

| Store   | Avg. contribution / order |
| ------- | ------------------------: |
| **S07** |              **−₹205.48** |
| **S03** |              **−₹178.93** |

> FRESH50 is associated with strongly negative average contribution per order at both stores.

---

# ✅ Promotion Rule Compliance

A **promo floor** is the minimum order value required to use a promotion.

For example:

```text
FRESH50 → Minimum order value = ₹800
```

Orders below the applicable minimum-order value should not receive the promotional discount.

### Validated Result

| Store   | Promo orders | Below applicable floor | Percentage |
| ------- | -----------: | ---------------------: | ---------: |
| **S03** |    **1,625** |                **679** | **41.78%** |
| **S07** |    **1,663** |                **706** | **42.45%** |

> Around **42% of promotional orders** at both stores were below the applicable minimum-order value.

---

# 💵 Verified Promotion Discount Leakage

The next analysis quantified the discount value given on promotional orders that were below the applicable minimum-order threshold.

| Store   | Below-floor orders | Leakage over 42 days | Potential leakage / month |
| ------- | -----------------: | -------------------: | ------------------------: |
| **S03** |            **679** |      **₹120,209.78** |            **₹85,864.13** |
| **S07** |            **706** |      **₹124,040.72** |            **₹88,600.51** |

### Combined Potential Exposure

> **S03 + S07 = ~₹174.5K/month**

> These are **potential promo-floor leakage amounts**, not guaranteed savings. Actual recovery depends on whether the promotional-rule exceptions are corrected.

---

# 💻 Key SQL Queries

## Initial / Supporting Analysis

* **Q7** — Initial Store Performance Screening
* **Q8** — Delivery Performance by Store
* **Q11** — Product Category Economics
* **Q13** — Promotion-Level Contribution
* **Q15** — Earlier Exploratory Evidence Table

## Final Validated Analysis

* **Q7A** — Operating-Day Adjusted Store Comparison
* **Q16** — Same-Timestamp Delivery Scan Analysis
* **Q17** — Same-Timestamp vs Return Rate Analysis
* **Q18** — Promotion Rule Compliance Analysis
* **Q19** — Promotion Discount Leakage Analysis

> Earlier exploratory queries are retained in the SQL file as part of the analysis trail. The final store-selection and root-cause story is based on the validated queries above.

---

# 🧭 Final Investigation Story

```text
Initial screening highlighted S07, S03 and S09
                    ↓
Operating periods were checked
                    ↓
S09 had only 14 operating days
                    ↓
Store economics were adjusted by operating days
                    ↓
S07 + S03 remained negative
                    ↓
Delivery scan validation found concentrated
same-timestamp patterns at S07 + S03
                    ↓
Same-timestamp orders showed much higher returns
                    ↓
Promotion validation found ~42% below-floor orders
                    ↓
Potential promo-floor leakage was quantified
```

---

# 🛠️ Technology Stack

* **Excel / Power Query** — Data cleaning and preprocessing
* **MySQL** — Data analysis and validation
* **HTML / CSS / JavaScript** — Interactive dashboard
* **GitHub** — Project hosting

---

# 🌐 Project Dashboard

[**Open Live Dashboard**](https://zipto-dark-store-analysis-kmr3joufedsiofqjfwiaea.streamlit.app/)

---

# 💻 GitHub Repository

[**View Repository**](https://github.com/PranavRaskar/Zipto-Dark-Store-Analysis)

---

# 🔗 LinkedIn

[**View LinkedIn Post**](https://lnkd.in/p/dbKiyRVc)

---

# ✅ Final Takeaway

The analysis identifies **S07 and S03 for deeper investigation** after adjusting store economics for different operating periods.

The strongest validated evidence is:

* **S07:** −₹372.8K adjusted monthly profit
* **S03:** −₹139.0K adjusted monthly profit
* Same-timestamp delivery scans: **19.03% at S07** and **16.77% at S03**
* Same-timestamp orders: **34.19% return rate vs 3.73% for normal-timestamp orders**
* Promo-floor violations: **42.45% at S07** and **41.78% at S03**
* Potential promo-floor leakage: **~₹88.6K/month at S07** and **~₹85.9K/month at S03**
* Combined potential promo-floor leakage: **~₹174.5K/month**

> **S07 and S03 are the only stores with negative adjusted monthly profit.**

The findings combine evidence from:

**Store Performance → Delivery & Fulfilment → Product & Promotions**

---

# ⚠️ Limitations

* Analysis covers **42 days** of data.
* S09 operated for only **14 days**, so operating-day adjustment is necessary for fair store comparison.
* Observed relationships do not establish causation.
* Same-timestamp delivery scans are treated as a validated anomaly pattern, not proof of fraud or a specific operational cause.
* Potential financial opportunities depend on the underlying assumptions and rule enforcement.
* Promo-floor leakage is a **potential financial exposure**, not guaranteed savings.
* Earlier benchmark-gap estimates for returns, delivery cost and discounts may overlap and should **not be summed** as a final financial opportunity.
* Some order-item rows have missing unit-cost values.
* Findings are limited to the supplied data and challenge definitions.

---

# 👥 Team

**Data Analytics Hackathon 2026 — Zipto Quick Commerce**

### Analysis Areas

**Store Performance • Delivery & Fulfilment • Product & Promotions**
