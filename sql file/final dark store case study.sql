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

-- -- Initial 42-day screening identified S07, S03 and S09
-- as stores requiring further investigation.
-- Because stores do not have equal operating periods,
-- a normalized monthly comparison is required before
-- making the final store decision.


-- -- =========================================================
-- Q7A. NORMALIZED STORE PERFORMANCE
-- Final comparison after adjusting for operating days
-- -- Business Question:
-- Which stores are actually loss-making after normalizing
-- performance for different operating periods?
-- =========================================================

WITH store_metrics AS (
    SELECT store_id,COUNT(*) AS orders,COUNT(DISTINCT DATE(STR_TO_DATE(order_ts, '%d-%m-%Y %H.%i'))) AS operating_days,
        SUM(CASE WHEN order_status = 'delivered'
                    THEN net_amount - cogs_amount - delivery_cost
                WHEN order_status = 'returned'
                    THEN -(cogs_amount + delivery_cost)
                ELSE 0 END) AS contribution
    FROM orders_clean
    GROUP BY store_id
)
SELECT sm.store_id,sm.operating_days,sm.orders,
    ROUND(sm.contribution,2) AS contribution_42_days,
    ROUND(sm.contribution * 30.0 / sm.operating_days,2) AS normalized_monthly_contribution,
    d.monthly_rent,ROUND(sm.contribution * 30.0 / sm.operating_days- d.monthly_rent,2) AS normalized_profit_per_month
FROM store_metrics sm
JOIN Dark_Stores d
    ON sm.store_id = d.store_id
ORDER BY normalized_profit_per_month ASC;

/*
Insight:
- S07 and S03 are the only stores with negative normalized
  monthly profit.
- S09 operated for only 14 days, so raw totals are misleading.
- After normalization, S09 is profitable and should not be
  treated as one of the two problem stores.
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

 -- =========================================================
-- Q16. SAME-TIMESTAMP DELIVERY SCANS
-- =========================================================
-- Business Question:
-- Are there unusual delivery records where the picked
-- timestamp and delivered timestamp are identical?

WITH trip_check AS (
    SELECT o.store_id,o.order_id, o.order_status,o.delivery_partner_id, 
	CASE WHEN STR_TO_DATE(t.Picked_TS, '%d-%m-%Y %H.%i') = STR_TO_DATE(t.Delivered_TS, '%d-%m-%Y %H.%i')
            THEN 1  ELSE 0 END AS same_timestamp
    FROM orders_clean o
    JOIN Trip_Logs t ON o.order_id = t.Order_ID
)
SELECT store_id,COUNT(*) AS trips,
    SUM(same_timestamp) AS same_timestamp_trips, ROUND(SUM(same_timestamp) * 100.0 / COUNT(*),2)
    AS same_timestamp_pct
FROM trip_check
GROUP BY store_id
ORDER BY same_timestamp_pct DESC;

/*
Insight:
- Same-timestamp scans are concentrated at S07 and S03.
- S07: 19.03% of trips
- S03: 16.77% of trips
- Other stores: 0%
- This pattern is unique to the two problem stores,
  making it a strong delivery-process warning.
*/

-- Q16A. Drill-down: orders with same picked and delivered timestamp

SELECT o.store_id, o.order_id, t.trip_id, o.delivery_partner_id, t.Picked_TS, t.Delivered_TS, o.order_status
FROM orders_clean o
JOIN Trip_Logs t ON o.order_id = t.Order_ID
WHERE STR_TO_DATE(t.Picked_TS, '%d-%m-%Y %H.%i') = STR_TO_DATE(t.Delivered_TS, '%d-%m-%Y %H.%i') AND o.store_id IN ('S03','S07')
ORDER BY o.store_id, o.order_id
LIMIT 50;





-- =========================================================
-- Q17. SAME-TIMESTAMP SCANS VS RETURN RATE
-- Business Question:
-- Do orders with same-timestamp delivery scans have
-- a higher return rate than orders with normal timestamps?
-- =========================================================

WITH trip_check AS (
    SELECT o.store_id,o.order_status,
CASE WHEN STR_TO_DATE(t.Picked_TS, '%d-%m-%Y %H.%i') = STR_TO_DATE(t.Delivered_TS, '%d-%m-%Y %H.%i')
			THEN 'Same Timestamp'
            ELSE 'Normal Timestamp'
        END AS scan_type
    FROM orders_clean o
    JOIN Trip_Logs t ON o.order_id = t.Order_ID
)
SELECT scan_type,COUNT(*) AS orders, 
SUM(order_status = 'returned') AS returned_orders, ROUND(SUM(order_status = 'returned') * 100.0 / COUNT(*), 2 ) 
AS return_rate
FROM trip_check
GROUP BY scan_type
ORDER BY return_rate DESC;


/*
Insight:
- Same-timestamp orders have a 34.19% return rate.
- Normal-timestamp orders have a 3.73% return rate.
- The large difference suggests that the same-timestamp
  delivery pattern is associated with substantial return
  leakage.
- This is an association, not proof of causation.
*/

-- Q17A. Drill-down: same-timestamp orders that were returned

SELECT o.store_id, o.order_id, t.trip_id, o.delivery_partner_id, t.Picked_TS, t.Delivered_TS, o.order_status
FROM orders_clean o
JOIN Trip_Logs t ON o.order_id = t.Order_ID
WHERE STR_TO_DATE(t.Picked_TS, '%d-%m-%Y %H.%i') = STR_TO_DATE(t.Delivered_TS, '%d-%m-%Y %H.%i') AND o.order_status = 'returned' AND o.store_id IN ('S03','S07')
ORDER BY o.store_id, o.order_id
LIMIT 50;

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

SELECT o.store_id, p.category, ROUND(SUM(oi.quantity * oi.unit_price), 2) AS sales, 
	ROUND(SUM(oi.quantity * oi.unit_cost), 2) AS cogs,
    ROUND(SUM(oi.quantity * (oi.unit_price - oi.unit_cost)), 2) AS contribution,
    ROUND(SUM(oi.quantity * (oi.unit_price - oi.unit_cost)) * 100 / SUM(oi.quantity * oi.unit_price),2) 
    AS margin_pct
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
-- FRESH50 shows strongly negative average contribution
-- per order at both S03 and S07.
-- This is supporting evidence; it does not by itself
-- prove that FRESH50 caused the store losses.




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







-- =========================================================
-- Q18. PROMO FLOOR VALIDATION
-- Business Question:
-- Are promotional orders meeting the minimum order value
-- required by their respective promotion rules?
-- =========================================================

SELECT o.store_id,
COUNT(*) AS promo_orders,
    SUM(CASE WHEN o.gross_amount < p.min_order_value
            THEN 1 ELSE 0 END) AS below_floor_orders,
ROUND( SUM( CASE WHEN o.gross_amount < p.min_order_value
                THEN 1
                ELSE 0 END) * 100.0 / COUNT(*),2) AS below_floor_pct
FROM orders_clean o
JOIN Promo_Codes p ON TRIM(o.promo_code) = TRIM(p.promo_code)
WHERE o.store_id IN ('S03','S07') AND TRIM(o.promo_code) <> ''
GROUP BY o.store_id
ORDER BY o.store_id;

/*
Insight:
- S03: 41.78% of promotional orders were below
  the applicable minimum-order value.
- S07: 42.45% were below the applicable minimum.
- The results are approximately 42% at both stores,
  indicating a material promo-rule compliance issue.
*/


-- Q18A. Drill-down: promo orders below applicable minimum value

SELECT
    o.store_id,
    o.order_id,
    TRIM(o.promo_code) AS promo_code,
    ROUND(o.gross_amount, 2) AS gross_amount,
    p.min_order_value,
    ROUND(p.min_order_value - o.gross_amount, 2) AS amount_below_floor
FROM orders_clean o
JOIN Promo_Codes p
    ON TRIM(o.promo_code) = TRIM(p.promo_code)
WHERE o.store_id IN ('S03','S07')
  AND TRIM(o.promo_code) <> ''
  AND o.gross_amount < p.min_order_value
ORDER BY o.store_id, o.order_id
LIMIT 50;
-- =========================================================
-- Q19. VERIFIED PROMO FLOOR LEAKAGE
-- Business Question:
-- How much discount value was given on promotional orders
-- that did not meet the applicable minimum-order threshold?
-- =========================================================

SELECT o.store_id,COUNT(*) AS below_floor_orders,
    ROUND(SUM(o.discount_amount),2) AS leakage_42_days,
    ROUND(SUM(o.discount_amount) * 30.0 / 42,2) AS leakage_per_month
FROM orders_clean o
JOIN Promo_Codes p ON TRIM(o.promo_code) = TRIM(p.promo_code)
WHERE o.store_id IN ('S03','S07')AND TRIM(o.promo_code) <> ''AND o.gross_amount < p.min_order_value
GROUP BY o.store_id
ORDER BY o.store_id;

-- Q19A. Drill-down: discount leakage from below-floor orders

SELECT
    o.store_id,
    o.order_id,
    TRIM(o.promo_code) AS promo_code,
    ROUND(o.gross_amount, 2) AS gross_amount,
    p.min_order_value,
    ROUND(o.discount_amount, 2) AS discount_given
FROM orders_clean o
JOIN Promo_Codes p
    ON TRIM(o.promo_code) = TRIM(p.promo_code)
WHERE o.store_id IN ('S03','S07')
  AND TRIM(o.promo_code) <> ''
  AND o.gross_amount < p.min_order_value
ORDER BY o.store_id, o.order_id
LIMIT 50;