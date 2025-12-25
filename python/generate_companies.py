import os
import numpy as np
import pandas as pd

np.random.seed(42)
os.makedirs("data/processed", exist_ok=True)

# Läs branscher från SCB-deriverad tillväxt
growth = pd.read_csv("data/processed/industry_growth.csv")
industries = growth["industry_code"].unique()

# Parametrar
N_COMPANIES = 8000
regions = ["Stockholm", "Västra Götaland", "Skåne", "Övriga"]
size_classes = ["small", "medium", "large"]
size_probs = [0.65, 0.25, 0.10]

# Skapa companies
companies = pd.DataFrame({
    "company_id": range(1, N_COMPANIES + 1),
    "industry_code": np.random.choice(industries, N_COMPANIES),
    "region": np.random.choice(regions, N_COMPANIES, p=[0.35, 0.20, 0.15, 0.30]),
    "size_class": np.random.choice(size_classes, N_COMPANIES, p=size_probs),
})

# Omsättning (MSEK) – lognormal per storlek
def revenue_by_size(size, n):
    if size == "small":
        return np.random.lognormal(mean=2.2, sigma=0.6, size=n)  # ~5–50
    if size == "medium":
        return np.random.lognormal(mean=3.2, sigma=0.5, size=n)  # ~25–250
    return np.random.lognormal(mean=4.2, sigma=0.45, size=n)     # ~150–2000

companies["annual_revenue_msek"] = 0.0
for s in size_classes:
    idx = companies["size_class"] == s
    companies.loc[idx, "annual_revenue_msek"] = revenue_by_size(s, idx.sum())

companies["annual_revenue_msek"] = companies["annual_revenue_msek"].round(1)

# Skapa engagement (korrelerat med storlek)
engagement = companies[["company_id", "size_class"]].copy()
engagement["products_count"] = engagement["size_class"].map({
    "small": lambda: np.random.randint(1, 3),
    "medium": lambda: np.random.randint(2, 5),
    "large": lambda: np.random.randint(4, 8),
})
engagement["products_count"] = engagement["products_count"].apply(lambda f: f())

engagement["interactions_per_year"] = engagement["size_class"].map({
    "small": lambda: np.random.randint(2, 6),
    "medium": lambda: np.random.randint(6, 14),
    "large": lambda: np.random.randint(12, 30),
})
engagement["interactions_per_year"] = engagement["interactions_per_year"].apply(lambda f: f())

# Spara
companies.to_csv("data/processed/companies.csv", index=False)
engagement[["company_id", "products_count", "interactions_per_year"]] \
    .to_csv("data/processed/engagement.csv", index=False)

