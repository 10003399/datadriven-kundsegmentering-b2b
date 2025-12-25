WITH base AS (
    SELECT
        c.company_id,
        c.industry_code,
        c.annual_revenue_msek,
        e.products_count,
        e.interactions_per_year,
        g.growth_rate
    FROM companies c
             JOIN engagement e
                  ON e.company_id = c.company_id
             JOIN industry_growth g
                  ON g.industry_code = c.industry_code
),

     normalized AS (
         SELECT
             *,
             annual_revenue_msek / MAX(annual_revenue_msek) OVER ()     AS rev_norm,
             products_count / MAX(products_count) OVER ()               AS prod_norm,
             interactions_per_year / MAX(interactions_per_year) OVER () AS inter_norm,
             (growth_rate + 0.1) / MAX(growth_rate + 0.1) OVER ()        AS growth_norm
         FROM base
     )

SELECT
    company_id,
    industry_code,
    ROUND(
            0.4 * rev_norm +
            0.25 * prod_norm +
            0.15 * inter_norm +
            0.2 * growth_norm
        , 4) AS customer_score
FROM normalized
ORDER BY customer_score DESC;
