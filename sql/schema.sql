-- =========================================
-- Schema: datadriven kundsegmentering B2B
-- =========================================

-- Tabell: companies
CREATE TABLE companies (
                           company_id INT PRIMARY KEY,
                           industry_code TEXT NOT NULL,         -- SNI2-kod, t.ex. '41', '62'
                           region TEXT NOT NULL,
                           size_class TEXT NOT NULL
                               CHECK (size_class IN ('small', 'medium', 'large')),
                           annual_revenue_msek NUMERIC
);

-- Tabell: engagement
CREATE TABLE engagement (
                            company_id INT PRIMARY KEY,
                            products_count INT,
                            interactions_per_year INT,
                            CONSTRAINT fk_engagement_company
                                FOREIGN KEY (company_id)
                                    REFERENCES companies(company_id)
);

-- Tabell: industry_growth
CREATE TABLE industry_growth (
                                 industry_code TEXT NOT NULL,          -- SNI2-kod
                                 year INT NOT NULL,
                                 growth_rate NUMERIC,
                                 CONSTRAINT pk_industry_growth
                                     PRIMARY KEY (industry_code, year)
);
