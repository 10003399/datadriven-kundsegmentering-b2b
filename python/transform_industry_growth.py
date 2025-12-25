import os
import pandas as pd

os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv(
    "data/raw/scb_industry_full.csv",
    encoding="latin1",
    sep=",",
    quotechar='"'
)

df.columns = [c.lower().strip() for c in df.columns]

INDUSTRY_COL = "näringsgren sni 2007"
YEAR_COL = "år"
VALUE_COL = "basfakta företag enligt företagens ekonomi"

# 1. Ta bort aggregerade rader (A-, A-S etc.)
df = df[df[INDUSTRY_COL].str.match(r"^\d", na=False)]

# 2. Extrahera 2-siffer SNI
df["sni2"] = df[INDUSTRY_COL].str.extract(r"^(\d{2})")

# 3. Affärsrelevanta branscher
valid_sni2 = [
    "41","42","43",
    "45","46","47",
    "49","52",
    "62","63",
    "68","69","70","71","72",
    "77","78"
]

df = df[df["sni2"].isin(valid_sni2)]

# 4. Endast år 2022–2023
df = df[df[YEAR_COL].isin([2022, 2023])]

# 5. Säkerställ numeriska värden
df[VALUE_COL] = pd.to_numeric(df[VALUE_COL], errors="coerce")
df = df.dropna(subset=[VALUE_COL])

# 6. Aggregera till SNI2-nivå
agg = (
    df.groupby(["sni2", YEAR_COL])[VALUE_COL]
      .sum()
      .reset_index()
)

# 7. Beräkna tillväxt
agg = agg.sort_values(["sni2", YEAR_COL])
agg["growth_rate"] = agg.groupby("sni2")[VALUE_COL].pct_change()

# 8. Spara
out = agg.dropna()[["sni2", YEAR_COL, "growth_rate"]]
out.columns = ["industry_code", "year", "growth_rate"]

out.to_csv("data/processed/industry_growth.csv", index=False)
