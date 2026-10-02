-- =========================================================
-- ZIPTO QUICK COMMERCE - DATA ANALYSIS HACKATHON
-- =========================================================
-- Analysis Period: 42 Days
-- Main Decision: Identify 2 stores to fix first
-- Team Lanes:
-- 1. Store Performance
-- 2. Delivery & Fulfilment
-- 3. Product & Promotion

-- =========================================================
-- DATA EXPLORATION
-- Q1. Understand the overall dataset
-- =========================================================
SELECT
    COUNT(*) AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT store_id) AS total_stores,
    MIN(STR_TO_DATE(order_ts, '%d-%m-%Y %H.%i')) AS first_order,
    MAX(STR_TO_DATE(order_ts, '%d-%m-%Y %H.%i')) AS last_order,
    COUNT(DISTINCT DATE(STR_TO_DATE(order_ts, '%d-%m-%Y %H.%i'))) AS active_days
FROM orders_clean;

-- "First, I checked the size of the business, number of customers and stores, and the period covered by the data."

-- Q2. Understand order outcomes

SELECT order_status, COUNT(*) AS orders, 
ROUND( COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders_clean),2) AS percentage
FROM orders_clean
GROUP BY order_status
ORDER BY orders DESC;

-- "Then I checked how orders ended—delivered, returned or cancelled—because each status has different financial treatment."

-- Q3. Understand overall business economics

SELECT
    ROUND(SUM(net_amount), 2) AS net_amount,
    ROUND(SUM(cogs_amount), 2) AS cogs,
    ROUND(SUM(delivery_cost), 2) AS delivery_cost,
    ROUND(SUM(CASE
                WHEN order_status = 'delivered'
                    THEN net_amount - cogs_amount - delivery_cost
                WHEN order_status = 'returned'
                    THEN -(cogs_amount + delivery_cost)
                ELSE 0
            END),2) AS contribution
FROM orders_clean;

-- =========================================================
-- LANE 1 : STORE PERFORMANCE
-- Goal: Identify financially weak stores / which stores make/lose money
-- =========================================================
-- Business question: Which stores are profitable or loss-making?

-- Q4. Store Profit & Loss
--
-- Contribution:
-- Delivered = Net Amount - COGS - Delivery Cost
-- Returned  = -(COGS + Delivery Cost)
-- Cancelled = 0
--
-- P&L = Contribution - Rent
-- Analysis period = 42 days = 42/30 = 1.4 months

WITH store_contribution AS (
    SELECT store_id, SUM(CASE WHEN order_status = 'delivered'
                    THEN net_amount - cogs_amount - delivery_cost
                WHEN order_status = 'returned'
                    THEN -(cogs_amount + delivery_cost)
                ELSE 0
            END) AS contribution
    FROM orders_clean
    GROUP BY store_id
    )
SELECT sc.store_id, ROUND(sc.contribution, 2) AS contribution, d.monthly_rent,
    ROUND(sc.contribution - (d.monthly_rent * 1.4),2) AS store_pnl
FROM store_contribution sc
JOIN Dark_Stores d
    ON sc.store_id = d.store_id
ORDER BY store_pnl ASC;
-- insight
-- First I calculated contribution for each store using the given business rules. Then I deducted 1.4 months of rent to get store P&L.
-- S07 has the largest P&L loss, followed by S03 and S09. S07 and S03 therefore became the main stores for deeper investigation, while 
-- S09 needed to be checked for a possible low-volume explanation.


-- Q5 Is the store weak because each order is less profitable?
-- Q5. Contribution per Order
-- Formula:
-- Contribution per Order = Total Contribution / Total Orders

SELECT store_id, COUNT(*) AS orders,ROUND(SUM(CASE WHEN order_status = 'delivered'
                    THEN net_amount - cogs_amount - delivery_cost
                WHEN order_status = 'returned'
                    THEN -(cogs_amount + delivery_cost)
                ELSE 0
            END
        ) / COUNT(*),2) AS contribution_per_order
FROM orders_clean
GROUP BY store_id
ORDER BY contribution_per_order ASC;
-- insights 
-- S07 has negative contribution per order, while S03 generates only ₹14.33 per order compared with about ₹74–₹80 at most other stores.
-- I calculated contribution per order to make the stores comparable despite different order volumes. S07 is actually losing money at the
 -- contribution level, while S03 earns much less per order than the other stores.

-- Q6. Average Orders per Day
-- Formula:
-- Orders per Day = Total Orders / 42 days

SELECT store_id,COUNT(*) AS orders,ROUND(COUNT(*) / 42.0, 2) AS orders_per_day
FROM orders_clean
GROUP BY store_id
ORDER BY orders_per_day ASC;
-- insight
-- S03 and S07 have normal/high order volumes, so their losses cannot simply be explained by low demand. 
-- S09, however, has very low order volume, which may explain why its fixed rent is spread across fewer orders.


-- Q7. Store Performance Scorecard
-- Used to identify stores that need deeper investigation.

WITH store_metrics AS (
    SELECT store_id, COUNT(*) AS orders, SUM(CASE WHEN order_status = 'delivered'
                    THEN net_amount - cogs_amount - delivery_cost
                WHEN order_status = 'returned'
                    THEN -(cogs_amount + delivery_cost)
                ELSE 0
            END ) AS contribution
    FROM orders_clean
    GROUP BY store_id
)
SELECT sm.store_id,sm.orders,
    ROUND(sm.orders / 42.0, 2) AS orders_per_day,
    ROUND(sm.contribution, 2) AS contribution,
    ROUND(sm.contribution / sm.orders,2) AS contribution_per_order,
    ROUND(sm.contribution - (d.monthly_rent * 1.4),2) AS store_pnl
FROM store_metrics sm
JOIN Dark_Stores d
    ON sm.store_id = d.store_id
ORDER BY store_pnl ASC;

-- I combined store volume, contribution, contribution per order and P&L so that I could compare stores both financially and on a per-order basis."

-- conclusion: S07 and S03 became the two stores selected for deeper investigation because they combine negative P&L with unusually weak contribution economics.
 -- S09 is also loss-making, but its very low order volume makes its situation different.

/*  
"We first compared all 10 stores using contribution, P&L, contribution per order and order volume. S07 had the largest loss at about ₹5.22 lakh and negative
 contribution per order of ₹35.64. S03 had the second-largest loss at about ₹1.95 lakh and contribution of only ₹14.33 per order, far below the other stores.
 Both stores handle around 132–135 orders per day, so their poor performance cannot be explained simply by low order volume. Therefore, we selected S07 and S03 
 for deeper investigation into delivery, returns, products and promotions."
*/


-- =========================================================
-- LANE 2 : DELIVERY & FULFILMENT
-- Goal: Understand delivery performance and identify  operational issues at S03 and S07.
-- Are we delivering what we say we deliver?
-- =========================================================

-- Business question: Which stores have the highest late-delivery rates?

--  Q8. Delivery Performance by Store
-- Late delivery = delivery time greater than 10 minutes
-- because Zipto's service promise is 10 minutes.

WITH delivery_data AS (
    SELECT o.store_id, TIMESTAMPDIFF( MINUTE,
            STR_TO_DATE(t.Picked_TS, '%d-%m-%Y %H.%i'),
            STR_TO_DATE(t.Delivered_TS, '%d-%m-%Y %H.%i')) AS delivery_minutes
    FROM orders_clean o
    JOIN Trip_Logs t
        ON o.order_id = t.Order_ID
    WHERE o.order_status = 'delivered'
)
SELECT store_id, COUNT(*) AS delivered_orders,
    ROUND(AVG(delivery_minutes), 2) AS avg_delivery_minutes,
    ROUND(SUM(delivery_minutes > 10) * 100.0 / COUNT(*),2) AS late_rate
FROM delivery_data
GROUP BY store_id
ORDER BY late_rate DESC;
-- insights 
-- S03 and S07 have the highest late-delivery rates in the network, with around 72% of delivered orders taking more than 10 minutes.
-- We calculated actual delivery time from pickup to delivery and compared it with the 10-minute promise. S03 and S07 had the highest 
-- late-delivery rates, so delivery performance is a major operational concern at these stores.

-- Q9 Do S03 and S07 have unusually high exposure to deliveries above 10 km
-- Q9. Long-Distance Delivery Exposure
-- Long-distance delivery = distance greater than 10 km.

SELECT o.store_id, COUNT(*) AS delivered_orders, SUM(t.Distance_KM > 10) AS orders_over_10km,
    ROUND(SUM(t.Distance_KM > 10) * 100.0 / COUNT(*),2) AS over_10km_pct
FROM orders_clean o
JOIN Trip_Logs t
    ON o.order_id = t.Order_ID
WHERE o.order_status = 'delivered'
  AND t.Distance_KM > 0
GROUP BY o.store_id
ORDER BY over_10km_pct DESC;
-- insight
-- S03 and S07 have unusually high exposure to long-distance deliveries, which is associated with their high late-delivery rates.
-- “I checked distance exposure to see whether the high lateness at S03 and S07 was associated with longer delivery distances.
--  Both stores had around 83% of valid deliveries above 10 km, much higher than the other stores.”


-- Q10 Are late deliveries concentrated among a small number of partners at S03/S07?
-- Q10. Partner Delivery Performance
-- Used to identify partners with unusually high late rates.

SELECT
    o.store_id,REPLACE(o.delivery_partner_id, CHAR(13), '') AS partner_id,
    COUNT(*) AS delivered_orders,
    ROUND( AVG(TIMESTAMPDIFF(MINUTE,  STR_TO_DATE(t.Picked_TS, '%d-%m-%Y %H.%i'),
                STR_TO_DATE(t.Delivered_TS, '%d-%m-%Y %H.%i') )), 2) AS avg_delivery_minutes,
    ROUND(SUM(TIMESTAMPDIFF(MINUTE, STR_TO_DATE(t.Picked_TS, '%d-%m-%Y %H.%i'),
                STR_TO_DATE(t.Delivered_TS, '%d-%m-%Y %H.%i')) > 10) * 100.0 / COUNT(*),2) AS late_rate
FROM orders_clean o
JOIN Trip_Logs t
    ON o.order_id = t.Order_ID
WHERE o.order_status = 'delivered'AND o.store_id IN ('S03','S07')
GROUP BY o.store_id,
    REPLACE(o.delivery_partner_id, CHAR(13), '')
HAVING COUNT(*) >= 50
ORDER BY o.store_id, late_rate DESC;

-- Why REPLACE(...CHAR(13),'')?
-- We discovered the order-side partner ID had a hidden carriage-return character. We proved removing it makes all 11,251 S03/S07 orders match their partners.

-- Why HAVING COUNT(*) >= 50?
-- A partner with only 2 deliveries and 2 late deliveries would show 100% late, but that's not enough evidence.
-- We're only looking at partners with a reasonable number of deliveries.

-- insight  S03's delivery problem is not limited to one partner. Most high-volume partners shown have very high late rates, 
-- suggesting a broader fulfilment issue at S03 rather than a single underperforming partner.


-- lane 2 
/* We investigated whether S03 and S07 had a delivery problem. Both stores had the highest late-delivery rates, around 72%, 
and around 83% of their valid deliveries were above 10 km, compared with about 50% for most other stores. We also checked 
partner employment type, but Gig and Full-time delivery costs were very similar, so partner type did not explain the cost gap.”  */


-- =========================================================
-- LANE 3 : PRODUCT & PROMOTION
-- Goal: Understand product economics and promotion leakage
-- what we're selling and what discounts are costing
-- =========================================================

-- Business question : Which product categories have weaker margins at S03 and S07?

-- Q11. Product Category Economics
-- Sales = Quantity × Unit Price
-- COGS  = Quantity × Unit Cost
-- Product Contribution = Sales - COGS
-- Margin % = Contribution / Sales × 100

SELECT o.store_id, p.category, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS sales, ROUND(SUM(oi.quantity * oi.unit_cost), 2) AS cogs,
    ROUND(SUM(oi.quantity * (oi.unit_price - oi.unit_cost)), 2) AS contribution,
    ROUND(SUM(oi.quantity * (oi.unit_price - oi.unit_cost)) * 100 / SUM(oi.quantity * oi.unit_price),2) AS margin_pct
FROM orders_clean o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN Products p ON oi.sku = p.sku
WHERE o.order_status = 'delivered' AND o.store_id IN ('S03','S07')
GROUP BY o.store_id, p.category
ORDER BY o.store_id, margin_pct ASC;

-- insights 
-- Meat & Seafood has the weakest margin at both candidate stores, but overall product mix is not strong enough to call it the primary reason for the store losses.


-- Q12. Promotion Usage and Discount Burden
-- Blank promo_code = No Promo
-- Discount per Order = Total Discount / Delivered Orders

SELECT store_id, COUNT(*) AS delivered_orders, SUM(NULLIF(TRIM(promo_code), '') IS NOT NULL) AS promo_orders,
ROUND(SUM(NULLIF(TRIM(promo_code), '') IS NOT NULL)* 100.0 / COUNT(*),2) AS promo_usage_pct,
ROUND(SUM(discount_amount) / COUNT(*),2) AS discount_per_order
FROM orders_clean
WHERE order_status = 'delivered'
GROUP BY store_id
ORDER BY discount_per_order DESC;

/*
S03:
- Promo usage = 28.95%
- Discount/order = ₹49.18
S07:
- Promo usage = 28.68%
- Discount/order = ₹48.69
Other stores:
- Promo usage = roughly 20–22%
- Discount/order = roughly ₹22–26

Insight:
S03 and S07 have roughly double the discount burden of the other stores,
making promotion leakage a major contributor to weak economics.
*/

-- Q13. Promotion-level Contribution
-- Which specific promotion is associated with the weakest contribution?
-- Contribution per Order =  Net Amount - COGS - Delivery Cost

SELECT store_id, COALESCE( NULLIF(TRIM(promo_code), ''),'No Promo') AS promo_code,
    COUNT(*) AS orders, ROUND(AVG(discount_amount),2) AS avg_discount,
    ROUND(AVG(net_amount - cogs_amount - delivery_cost),2) AS contribution_per_order
FROM orders_clean
WHERE order_status = 'delivered' AND store_id IN ('S03','S07')
GROUP BY store_id, promo_code
ORDER BY store_id, contribution_per_order ASC;
/*  S03:
- FRESH50 = −₹178.93/order
- SAVE20 = −₹4.96/order
- No Promo = ₹101.71/order

S07:
- FRESH50 = −₹205.48/order
- SAVE20 = −₹24.69/order
- No Promo = ₹82.87/order

 insight:
FRESH50 is the strongest promotion-level warning at both stores, with negative contribution per order, while non-promo orders generate positive contribution.
*/



-- lane 3 We first looked at product categories to understand COGS and margins. Meat & Seafood had the lowest margin at both S03 and S07,
-- but product mix did not fully explain the store problem. We then looked at promotions and found that S03 and S07 have much higher discount
-- burden than the other stores. Finally, we drilled into individual promotions and found FRESH50 was associated with strongly negative contribution
-- per order at both stores.”


-- =========================================================
-- final ₹ impact.
-- =========================================================
-- =========================================================
-- Q14. Potential Monthly Opportunity
--
-- All opportunities are separate and should NOT be added
-- directly because some cost leakages may overlap.
--
-- Monthly value = 42-day value × 30 / 42
-- =========================================================

SELECT'S03' AS store_id,
    ROUND(199235.08 * 30 / 42, 2) AS current_return_loss_monthly,
    ROUND(77808.32 * 30 / 42, 2) AS excess_delivery_cost_monthly,
    ROUND(123840.73 * 30 / 42, 2) AS excess_discount_monthly

UNION ALL

SELECT'S07',
    ROUND(374494.32 * 30 / 42, 2),
    ROUND(80291.15 * 30 / 42, 2),
    ROUND(115619.17 * 30 / 42, 2);
    
/*
These columns mean different things:
- Return loss/month = current return-related loss converted to monthly.
- Excess delivery cost/month = estimated extra delivery cost vs benchmark.
- Excess discount/month = estimated extra discount vs benchmark.
*/

/*
============================================================
POTENTIAL MONTHLY FINANCIAL OPPORTUNITY
============================================================
S03
- Return recovery opportunity: ~₹10.3K/month
- Excess delivery cost: ~₹55.6K/month
- Excess discount: ~₹88.5K/month

S07
- Return recovery opportunity: ~₹15.7K/month
- Excess delivery cost: ~₹57.4K/month
- Excess discount: ~₹82.6K/month
:
"These numbers show the potential monthly financial improvement
if we reduce these gaps toward the performance of the other stores."
============================================================
*/


/*
============================================================
Q15. FINAL EVIDENCE TABLE
============================================================
This brings the main evidence for S03 and S07 into one table.
Store performance:
- P&L
- Contribution per order
- Orders per day
Delivery:
- Return rate
- Late delivery rate
- Long-distance exposure
Promotion:
- Promo usage
- Discount per delivered order
This is the final evidence table for the presentation.
============================================================
*/
WITH store_metrics AS (
    SELECT o.store_id,COUNT(*) AS orders,
        ROUND(COUNT(*) / 42.0,2) AS orders_per_day,
        ROUND(SUM(CASE WHEN order_status = 'delivered' THEN net_amount - cogs_amount - delivery_cost
                    WHEN order_status = 'returned' THEN -(cogs_amount + delivery_cost)
                    ELSE 0 END) / COUNT(*),2) AS contribution_per_order,
        ROUND(SUM(order_status = 'returned') * 100.0 / COUNT(*),2) AS return_rate,
        ROUND(SUM(CASE WHEN order_status = 'delivered' AND NULLIF(TRIM(promo_code),'') IS NOT NULL THEN 1 ELSE 0 END)
            * 100.0 / SUM(order_status = 'delivered'),2) AS promo_usage_pct,
        ROUND(SUM(CASE WHEN order_status = 'delivered' THEN discount_amount ELSE 0 END)
            / SUM(order_status = 'delivered'),2) AS discount_per_order,
        ROUND(SUM(CASE WHEN order_status = 'delivered' THEN net_amount - cogs_amount - delivery_cost
                    WHEN order_status = 'returned' THEN -(cogs_amount + delivery_cost)
                    ELSE 0 END) - d.monthly_rent * 1.4,2) AS pnl
    FROM orders_clean o
    JOIN Dark_Stores d ON o.store_id = d.store_id
    WHERE o.store_id IN ('S03','S07')
    GROUP BY o.store_id,d.monthly_rent
),
delivery_metrics AS (
    SELECT o.store_id,
        ROUND(SUM(TIMESTAMPDIFF(MINUTE,STR_TO_DATE(t.Picked_TS,'%d-%m-%Y %H.%i'),
            STR_TO_DATE(t.Delivered_TS,'%d-%m-%Y %H.%i')) > 10) * 100.0 / COUNT(*),2) AS late_rate,
        ROUND(SUM(CASE WHEN t.Distance_KM > 0 AND t.Distance_KM > 10 THEN 1 ELSE 0 END) * 100.0
            / SUM(CASE WHEN t.Distance_KM > 0 THEN 1 ELSE 0 END),2) AS long_distance_pct
    FROM orders_clean o
    JOIN Trip_Logs t ON o.order_id = t.Order_ID
    WHERE o.order_status = 'delivered'
      AND o.store_id IN ('S03','S07')
    GROUP BY o.store_id
)
SELECT s.store_id,s.orders,s.orders_per_day,s.pnl,s.contribution_per_order,s.return_rate,
       d.late_rate,d.long_distance_pct,s.promo_usage_pct,s.discount_per_order
FROM store_metrics s
JOIN delivery_metrics d ON s.store_id = d.store_id
ORDER BY s.pnl ASC;