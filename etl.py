import pandas as pd

df = pd.read_csv("data/products.csv")
print(f"Before cleaning: {len(df)} rows")


df = df.drop_duplicates(subset=["product_name", "category"])
print(f"After dedup: {len(df)} rows")

df["price"] = df["price"].astype(str)
df["price"] = df["price"].str.replace("min-", "", regex=False)
df["price"] = df["price"].str.replace("-min-", "-", regex=False)


def extract_min_price(price):
    if price in ["Get Quote", "null", "nan", None]:
        return None
    try:
        if "-" in str(price):
            return float(str(price).split("-")[0])
        return float(price)
    except:
        return None

df["price_numeric"] = df["price"].apply(extract_min_price)


df["location"] = df["location"].replace(["India", "Made in India", ""], None)


df["has_price"] = df["price_numeric"].notna()


df.to_csv("data/products_clean.csv", index=False)
print(f"Final clean dataset: {len(df)} rows")
print(df.head())
print(df.info())