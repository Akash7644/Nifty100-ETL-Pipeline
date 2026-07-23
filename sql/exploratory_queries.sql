-- =====================================
-- 1. Total Companies
-- =====================================

SELECT COUNT(*) AS total_companies
FROM companies;

-- =====================================
-- 2. Top 10 Companies by ROE
-- =====================================

SELECT
company_name,
roe_percentage
FROM companies
ORDER BY roe_percentage DESC
LIMIT 10;

-- =====================================
-- 3. Companies having more than 10 years of Balance Sheet data
-- =====================================

SELECT
company_id,
COUNT(DISTINCT year) AS total_years
FROM balancesheet
GROUP BY company_id
HAVING total_years > 10
ORDER BY total_years DESC;

-- =====================================
-- 4. Average Book Value
-- =====================================

SELECT
AVG(book_value) AS avg_book_value
FROM companies;

-- =====================================
-- 5. Highest Market Cap
-- =====================================

SELECT
company_id,
MAX(market_cap_crore) AS highest_market_cap
FROM market_cap
GROUP BY company_id
ORDER BY highest_market_cap DESC
LIMIT 10;

-- =====================================
-- 6. Latest Closing Price
-- =====================================

SELECT
company_id,
MAX(date),
close_price
FROM stock_prices
GROUP BY company_id;

-- =====================================
-- 7. Companies having negative Net Profit
-- =====================================

SELECT
company_id,
year,
net_profit
FROM profitandloss
WHERE net_profit < 0;

-- =====================================
-- 8. Total Documents
-- =====================================

SELECT COUNT(*)
FROM documents;

-- =====================================
-- 9. Number of Companies by Sector
-- =====================================

SELECT
broad_sector,
COUNT(*)
FROM sectors
GROUP BY broad_sector
ORDER BY COUNT(*) DESC;

-- =====================================
-- 10. Companies with highest Debt to Equity
-- =====================================

SELECT
company_id,
debt_to_equity
FROM financial_ratios
ORDER BY debt_to_equity DESC
LIMIT 10;