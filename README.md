# DARK STORE DOWN — Zipto Quick Commerce

## Noida Cluster Review | Data Analytics Hackathon 2026

live website
https://pranavraskar.github.io/Zipto-Dark-Store-Analysis



An end-to-end data analytics project built to answer one core business question:

> **Which two stores should Zipto investigate first, what is broken in each, and what is the potential monthly financial improvement?**

The project combines **Excel / Power Query for data cleaning**, **MySQL for SQL-based analysis**, and an **interactive HTML dashboard** for presenting findings, evidence, and recommendations.

---

# 📌 Project Overview

Zipto operates multiple grocery dark stores across the Noida cluster.

Our analysis covers three business areas:

### 1. Store Performance
**Which stores make money and which lose it?**

### 2. Delivery & Fulfilment
**How do delivery time, late deliveries, returns, distance, and delivery cost vary by store?**

### 3. Product & Promotions
**What are we selling, what are the margins, and what are promotions costing the business?**

---

# 📊 Dataset & Scope

| Metric | Value |
|---|---:|
| Analysis period | **42 days** |
| Period covered | **18 May 2026 – 28 June 2026** |
| Stores analysed | **10** |
| Total orders | **52,133** |
| Delivered orders | **48,510** |
| Returned orders | **2,556** |
| Cancelled orders | **1,067** |
| Net amount | **₹27,161,486.00** |
| COGS | **₹21,120,588.37** |
| Delivery cost | **₹1,617,822.63** |
| Contribution before rent | **₹3,025,759.10** |

---

# 💰 Business Economics

The analysis follows the challenge's prescribed contribution and P&L definitions.

### Delivered Orders

```text
Contribution = Net Amount − COGS − Delivery Cost
```

### Returned Orders

```text
Contribution = −(COGS + Delivery Cost)
```

### Cancelled Orders

```text
Contribution = 0
```

### Store P&L

```text
Store P&L = Total Contribution − (Monthly Rent × Months in Data)
```

The analysis period is 42 days:

```text
42 / 30 = 1.4 months
```

Therefore:

```text
Store P&L = Contribution − (Monthly Rent × 1.4)
```

---

# 🔄 Analytical Workflow

```text
Raw CSV / Excel Files
        ↓
Excel / Power Query
Data Cleaning & Standardisation
        ↓
Data Validation
Data Types • IDs • Relationships • Reconciliation
        ↓
MySQL
Joins • KPIs • Store Economics • Root-Cause Analysis
        ↓
Lane 1 — Store Performance
Lane 2 — Delivery & Fulfilment
Lane 3 — Product & Promotions
        ↓
Benchmark Comparison
        ↓
S07 & S03 Investigation
        ↓
Potential Monthly Financial Opportunities
        ↓
Interactive HTML Dashboard
```

---

# 🧹 Data Preparation & Cleaning

The supplied datasets required cleaning and validation before analysis.

### Cleaning performed

- Standardised text fields
- Trimmed unnecessary spaces and characters
- Converted timestamps into valid date/time values
- Converted numeric fields into appropriate numeric data types
- Removed currency symbols where required
- Cleaned hidden characters from IDs
- Removed invalid / negative delivery distances from distance analysis
- Preserved legitimate `NULL` values
- Checked relationships and joins between datasets
- Reconciled key totals after cleaning
- Corrected the `Order_Items` schema and field types

### Order Items Structure

```text
Order_Item_ID
Order_ID
SKU
Unit_Price
Unit_Cost
Quantity
```

### Important Data Quality Finding

A hidden carriage-return character (`CHAR(13)`) was found in order-side delivery partner IDs.

After cleaning this hidden character, the S03/S07 orders matched the delivery partner data correctly.

### Distance Validation

The previously reported long-distance finding was revalidated against the raw Trip Logs.

The final analysis **does not use the unsupported claim that approximately 83% of S03/S07 deliveries were above 10 km**.

---

# 🔎 Store Screening

All 10 stores were compared using:

- Store P&L
- Contribution
- Contribution per order
- Order volume / orders per day

This identified **S07 and S03 for deeper investigation**.

---

# 🔴 S07 — Largest P&L Loss

## Store Metrics

| Metric | S07 |
|---|---:|
| **P&L** | **−₹521,868.46** |
| Contribution | **−₹202,668.46** |
| Contribution per order | **−₹35.64** |
| Orders per day | **135.40** |
| Return rate | **14.01%** |
| Delivery cost per order | **₹42.12** |
| Promo usage | **28.68%** |
| Discount per delivered order | **₹48.69** |
| FRESH50 contribution/order | **−₹205.48** |

### Key S07 Findings

**Weak unit economics**

S07 has the largest P&L loss and negative contribution per order.

**Elevated returns**

Return rate is **14.01%**, compared with the overall network return rate of **4.90%**.

**Higher delivery cost**

Delivery cost per order is **₹42.12**.

**High promotion burden**

Promo usage is **28.68%**, with **₹48.69 discount per delivered order**.

**FRESH50**

FRESH50 is associated with **−₹205.48 average contribution per order**.

### S07 Category Margins

| Category | Margin |
|---|---:|
| Meat & Seafood | **6.51%** |
| Dairy & Eggs | **17.68%** |
| Bakery | **17.89%** |

Meat & Seafood has the weakest category margin at S07, but product-category performance is treated as a **secondary finding**, not the sole explanation for the store's weak economics.

---

# 🔵 S03 — Second-Largest P&L Loss

## Store Metrics

| Metric | S03 |
|---|---:|
| **P&L** | **−₹194,664.97** |
| Contribution | **₹79,735.03** |
| Contribution per order | **₹14.33** |
| Orders per day | **132.48** |
| Return rate | **7.94%** |
| Delivery cost per order | **₹41.98** |
| Promo usage | **28.95%** |
| Discount per delivered order | **₹49.18** |
| FRESH50 contribution/order | **−₹178.93** |

### Key S03 Findings

**Weak unit economics**

Contribution per order is only **₹14.33**.

**Elevated returns**

Return rate is **7.94%**, compared with the overall network return rate of **4.90%**.

**Higher delivery cost**

Delivery cost per order is **₹41.98**.

**High promotion burden**

Promo usage is **28.95%**, with **₹49.18 discount per delivered order**.

**FRESH50**

FRESH50 is associated with **−₹178.93 average contribution per order**.

### S03 Category Margins

| Category | Margin |
|---|---:|
| Meat & Seafood | **6.84%** |
| Dairy & Eggs | **17.48%** |
| Bakery | **18.34%** |

Meat & Seafood has the weakest category margin at S03, but product-category performance is treated as a **secondary finding**, not the primary explanation for the store's weak economics.

---

# 🟡 Why Not S09?

S09 is also loss-making, but its operating pattern is different.

| Metric | S09 |
|---|---:|
| Orders | **1,815** |
| Orders per day | **43.21** |
| Contribution per order | **₹74.21** |

S09 has much lower order volume and healthier contribution per order, indicating a different fixed-cost absorption pattern from S03 and S07.

---

# 🚚 Delivery & Fulfilment Findings

## Late Delivery Definition

```text
Late delivery = Pickup-to-delivery time > 10 minutes
```

### Validated Results

| Metric | S03 | S07 |
|---|---:|---:|
| Late rate | **72.33%** | **72.10%** |
| Delivery cost / order | **₹41.98** | **₹42.12** |
| Average valid distance | **~2.99 km** | **~3.02 km** |

### Additional Findings

- S03 and S07 have the highest late-delivery rates in the analysed store network.
- Average delivery distance is approximately **3 km** at both stores.
- Distance does not meaningfully differentiate S03/S07 from the other stores.
- Gig vs Full-time delivery partner type did not meaningfully explain the delivery-cost gap.
- The analysis does not establish that a single delivery partner caused the problem.
- The previously reported **83% above 10 km** finding was excluded after revalidation.

---

# 🛒 Product & Promotions Findings

## Product Category Economics

**Meat & Seafood** has the weakest margin at both S03 and S07.

This supports a product-economics finding, but the category results alone are not strong enough to identify product mix as the primary cause of the store losses.

---

## Promotion Burden

| Metric | S07 | S03 | Other Stores |
|---|---:|---:|---:|
| Promo usage | **28.68%** | **28.95%** | **~20–22%** |
| Discount / delivered order | **₹48.69** | **₹49.18** | **~₹22–26** |

---

## Promotion-Level Contribution

| Promotion | S07 | S03 |
|---|---:|---:|
| **FRESH50** | **−₹205.48** | **−₹178.93** |
| SAVE20 | **−₹24.69** | **−₹4.96** |
| No Promo | **₹82.87** | **₹101.71** |

> **FRESH50 is associated with strongly negative average contribution per order at both S07 and S03.**

This is an observed relationship and does not establish causation.

---

# 💵 Potential Monthly Financial Opportunity

These figures represent **separate potential improvement opportunities** if identified gaps are reduced toward benchmark levels.

## S07

| Opportunity Area | Potential / Month |
|---|---:|
| Return recovery | **~₹15.7K** |
| Excess delivery cost | **~₹57.4K** |
| Excess discount | **~₹82.6K** |

## S03

| Opportunity Area | Potential / Month |
|---|---:|
| Return recovery | **~₹10.3K** |
| Excess delivery cost | **~₹55.6K** |
| Excess discount | **~₹88.5K** |

### Important Financial Note

These figures are:

- **Potential**, not guaranteed savings
- Based on benchmark-gap assumptions
- Separate opportunity areas
- **Not additive**, because the same order may contribute to more than one gap

Therefore, the three opportunity values should **not** be summed into one guaranteed monthly saving.

---

# 🧠 Root-Cause Summary

## S07

```text
Negative contribution per order
        +
High return rate
        +
Higher delivery cost per order
        +
High promotion & discount burden
        +
FRESH50 associated with negative contribution/order
        ↓
Weak store economics
```

## S03

```text
Very low contribution per order
        +
Elevated return rate
        +
Higher delivery cost per order
        +
High promotion & discount burden
        +
FRESH50 associated with negative contribution/order
        ↓
Weak store economics
```

These findings describe observed relationships and benchmark gaps; they do not establish causal relationships.

---

# 🧾 SQL Analysis

The SQL analysis was developed in stages, from business baseline to store screening and detailed investigation.

## Key Queries Used

### Q7 — Store Performance Scorecard

Used to compare:

- Orders
- Orders per day
- Contribution
- Contribution per order
- Store P&L

### Q8 — Delivery Performance by Store

Used to calculate:

- Average delivery time
- Late-delivery rate
- Store-level delivery performance

### Q11 — Product Category Economics

Used to calculate:

- Sales
- COGS
- Contribution
- Margin percentage
- Category economics

### Q13 — Promotion-Level Contribution

Used to compare:

- Promotion codes
- Discount levels
- Contribution per order
- FRESH50 performance

### Q15 — Final Evidence Table

Used to consolidate key evidence for S03 and S07 across:

- Store economics
- Returns
- Delivery
- Promotions

---

# 🌐 Interactive HTML Dashboard

The project includes an interactive HTML dashboard containing:

### Home
Business problem and executive snapshot.

### Store Performance
All-store comparison and S07/S03 investigation selection.

### Delivery & Fulfilment
Late rate, delivery time, delivery cost, distance, and comparison metrics.

### Product & Promotions
Category margins, promotion usage, discount burden, and promotion-level contribution.

### Findings
Data quality, validation, reconciliation, and methodology.

### COO Decision
S07/S03 investigation focus, potential monthly opportunities, actions, and limitations.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Excel / Power Query** | Data cleaning and transformation |
| **MySQL** | SQL analysis and business metrics |
| **HTML / CSS / JavaScript** | Interactive dashboard |
| **GitHub** | Version control and project hosting |

---

# 📁 Repository Structure

```text
dark-store-down-zipto/
│
├── README.md
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── sql/
│   └── zipto_analysis.sql
│
├── dashboard/
│   └── index.html
│
├── screenshots/
│   ├── q7_store_performance.png
│   ├── q8_delivery.png
│   ├── q11_product_category.png
│   ├── q13_promotions.png
│   └── q15_final_evidence.png
│
└── docs/
    ├── cleaning_log
    ├── finding_cards
    └── presentation
```

---

# ▶️ How to Run

## SQL Analysis

1. Import the cleaned datasets into MySQL.
2. Create or select the project database.
3. Run the SQL file from the `sql/` folder.
4. Review the results for each analysis lane.

## HTML Dashboard

1. Open `dashboard/index.html` in a browser, or
2. Deploy the HTML page using static hosting.
3. Use the dashboard navigation to explore the complete analysis.

---

# 🔗 Project Links

### 🌐 Live Project Website

[Open Project Dashboard](ADD_DEPLOYED_LINK_HERE)

### 💻 GitHub Repository

[View Source Code](ADD_GITHUB_REPOSITORY_LINK_HERE)

### 🔗 LinkedIn Post

[View LinkedIn Post](ADD_LINKEDIN_POST_LINK_HERE)

---

# ✅ Final Takeaway

The analysis identifies **S07 and S03 for priority investigation** based on their weak store-level economics and evidence across store, delivery, product, and promotion analysis.

### S07

- Largest P&L loss
- Negative contribution per order
- Elevated return rate
- Higher delivery cost per order
- High promotion and discount burden
- FRESH50 associated with strongly negative average contribution per order

### S03

- Second-largest P&L loss
- Very low contribution per order
- Elevated return rate
- Higher delivery cost per order
- High promotion and discount burden
- FRESH50 associated with strongly negative average contribution per order

The quantified monthly figures represent **separate potential benchmark-based improvement opportunities**, not guaranteed savings.

---

# ⚠️ Limitations

- The analysis covers **42 days** of data.
- Observed relationships do not establish causation.
- Potential monthly opportunities depend on the benchmark and assumptions used.
- Opportunity figures may overlap and should not be added together.
- Some product order lines have missing unit-cost values, which may affect product-margin calculations.
- The analysis is limited to the data and business definitions supplied in the challenge.

---

# 👥 Team

## Data Analytics Hackathon 2026 — Zipto Quick Commerce

**Analysis Areas**

- Store Performance
- Delivery & Fulfilment
- Product & Promotions

---

## ⭐ Project Objective

```text
CLEAN
  ↓
ANALYSE
  ↓
VALIDATE
  ↓
IDENTIFY
  ↓
QUANTIFY
  ↓
RECOMMEND
```

**From raw data to evidence-based business decisions.**
