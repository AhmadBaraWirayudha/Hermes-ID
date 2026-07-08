-- Latest values by item
SELECT item, region, category, MAX(date) AS latest_date, price, volume
FROM market_observations
GROUP BY item, region, category;

-- Daily aggregate by category
SELECT date, category, AVG(price) AS avg_price, SUM(volume) AS total_volume
FROM market_observations
GROUP BY date, category
ORDER BY date;

-- Price momentum over time
SELECT date, item, region, price,
       price - LAG(price) OVER (PARTITION BY item, region ORDER BY date) AS price_change
FROM market_observations
ORDER BY item, region, date;
