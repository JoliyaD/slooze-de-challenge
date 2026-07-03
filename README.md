# B2B Textile Market Intelligence — Slooze Data Engineering Challenge

## Overview
An end-to-end data pipeline that collects, processes, and analyzes 
textile supplier data from ExportersIndia.com — a leading Indian B2B marketplace.

##  Architecture

ExportersIndia.com
       ↓
scraper.py (requests + BeautifulSoup)
       ↓
Groq AI (Llama 3) — intelligent data extraction
       ↓
etl.py — cleaning, deduplication, feature engineering
       ↓
eda.py — 6 charts + business insights
       ↓
products_clean.csv + products.json


## Why AI-Powered Extraction?
Instead of brittle HTML tag parsing, we use **Groq (Llama 3.1)** as an 
intelligent extraction layer. This means:
- Resilient to HTML structure changes
- Understands context (extracts meaning, not just tags)
- Handles inconsistent price formats automatically

##  Key Insights
1. Silk dominates premium pricing — avg ₹3000+, highest variance
2. 95.4% price transparency — most suppliers list fixed prices
3. Cotton is king — most frequent material across all categories
4. Low MOQ market — 95% of suppliers accept orders under 500 units
5. 6 categories scraped — textile, cotton, silk, khadi, chiffon, velvet

##  How to Run

### Install dependencies
bash
pip install requests beautifulsoup4 pandas matplotlib seaborn groq python-dotenv

### Setup
Create `.env` file:

GROQ_API_KEY=your_key_here


### Run pipeline
bash
# Step 1: Scrape data
python scraper.py

# Step 2: Clean data  
python etl.py

# Step 3: Generate EDA charts
python eda.py


##  Project Structure

DE_sloozechallenge/
├── scraper.py      # AI-powered web scraper
├── etl.py          # Data cleaning pipeline
├── eda.py          # Exploratory data analysis
├── data/
│   ├── products.csv        # Raw scraped data
│   └── products_clean.csv  # Cleaned data
├── charts/         # 6 EDA visualizations
└── README.md


##  Tech Stack
- Python — core language
- requests + BeautifulSoup — web scraping
- Groq (Llama 3.1) — AI extraction layer
- Pandas — data processing
- Matplotlib + Seaborn — visualization