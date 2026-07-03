import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re
import os


os.makedirs("charts", exist_ok=True)


df = pd.read_csv("data/products_clean.csv")
print(f"Dataset: {len(df)} products, {df['category'].nunique()} categories")
print(df['category'].value_counts())

# CHART 1: Products per Category 
plt.figure(figsize=(10, 5))
category_counts = df['category'].value_counts()
sns.barplot(x=category_counts.index, y=category_counts.values, palette="RdPu")
plt.title("Number of Products per Textile Category", fontsize=14, fontweight='bold')
plt.xlabel("Category")
plt.ylabel("Product Count")
plt.xticks(rotation=15)
for i, v in enumerate(category_counts.values):
    plt.text(i, v + 0.1, str(v), ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig("charts/01_products_per_category.png", dpi=150)
plt.close()
print(" Chart 1 saved")

# CHART 2: Price Distribution per Category
plt.figure(figsize=(12, 6))
df_priced = df[df['price_numeric'].notna()]
sns.boxplot(data=df_priced, x='category', y='price_numeric', palette="RdPu")
plt.title("Price Distribution per Textile Category (₹)", fontsize=14, fontweight='bold')
plt.xlabel("Category")
plt.ylabel("Price (₹)")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig("charts/02_price_distribution.png", dpi=150)
plt.close()
print(" Chart 2 saved")

#  CHART 3: Price Availability 
plt.figure(figsize=(8, 5))
price_availability = df['has_price'].value_counts()
labels = ['Fixed Price', 'Get Quote']
colors = ['#FF4D8B', "#DFDFDF"]
plt.pie(price_availability.values, labels=labels, colors=colors,
        autopct='%1.1f%%', startangle=90,
        textprops={'fontsize': 12, 'fontweight': 'bold', 'color': 'white'})
plt.title("Price Transparency in B2B Textile Market", 
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig("charts/03_price_availability.png", dpi=150)
plt.close()
print("Chart 3 saved")

#  CHART 4: Average Price per Category 
plt.figure(figsize=(10, 5))
avg_price = df.groupby('category')['price_numeric'].mean().sort_values(ascending=False)
sns.barplot(x=avg_price.index, y=avg_price.values, palette="RdPu")
plt.title("Average Price per Textile Category (₹)", fontsize=14, fontweight='bold')
plt.xlabel("Category")
plt.ylabel("Average Price (₹)")
plt.xticks(rotation=15)
for i, v in enumerate(avg_price.values):
    plt.text(i, v + 50, f"₹{v:.0f}", ha='center', fontweight='bold', fontsize=9)
plt.tight_layout()
plt.savefig("charts/04_avg_price_category.png", dpi=150)
plt.close()
print(" Chart 4 saved")

# CHART 5: Top Keywords in Product Names 
from collections import Counter
import re

all_words = " ".join(df['product_name'].str.lower()).split()
stopwords = ['fabric', 'for', 'and', 'the', 'of', 'in', 'a', 'an', 
             'with', 'to', 'by', 'at', 'from', 'type', 'plain', 'printed']
filtered = [w for w in all_words if w not in stopwords and len(w) > 3]
word_freq = Counter(filtered).most_common(15)

words, counts = zip(*word_freq)
plt.figure(figsize=(12, 5))
sns.barplot(x=list(words), y=list(counts), palette="RdPu")
plt.title("Top 15 Keywords in Textile Product Names", fontsize=14, fontweight='bold')
plt.xlabel("Keyword")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("charts/05_top_keywords.png", dpi=150)
plt.close()
print(" Chart 5 saved")

#  CHART 6: MOQ Distribution 
plt.figure(figsize=(10, 5))
df_moq = df[df['moq'].notna()].copy()
df_moq['moq_numeric'] = pd.to_numeric(df_moq['moq'], errors='coerce')
df_moq = df_moq[df_moq['moq_numeric'].notna()]

sns.histplot(data=df_moq, x='moq_numeric', bins=10, color='#FF4D8B')
plt.title("Minimum Order Quantity Distribution", fontsize=14, fontweight='bold')
plt.xlabel("MOQ (Units/Meters)")
plt.ylabel("Number of Suppliers")
plt.tight_layout()
plt.savefig("charts/06_moq_distribution.png", dpi=150)
plt.close()
print(" Chart 6 saved")