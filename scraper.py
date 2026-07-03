import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BASE_URL = "https://www.exportersindia.com/indian-suppliers/{category}.htm"
CATEGORIES = [
    "textile-fabric",
    "cotton-fabric",
    "silk-fabric", 
    "khadi-fabric",
    "georgette-fabric",
    "chiffon-fabric",
    "velvet-fabric",
    "lace-fabric",
    "denim-fabric",
    "polyester-fabric",
]

def get_page_html(url, page_number):
    full_url = f"{url}?page={page_number}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(full_url, headers=headers)
    time.sleep(2)
    return response.text


def extract_with_ai(raw_text):
    prompt = f"""
Extract ALL product listings from this B2B marketplace text.
Each listing has a product name, price, supplier/company name, and location/city.

Return ONLY a JSON array with these fields:
- product_name (the fabric/textile name)
- price (as string, e.g. "360-380" or "Get Quote")
- supplier_name (company name, look for words like "Textiles", "Industries", "Traders", "Handicrafts")
- location (Indian city or state, look for city names like Mumbai, Surat, Delhi, Gujarat etc)
- moq (minimum order quantity as number only, else null)
- category_type (what the fabric is used for, else null)

Text: {raw_text[:3000]}

CRITICAL RULES:
- Return ONLY raw JSON array, no markdown, no backticks
- price must be a string always
- Extract ALL products you can find, minimum 8 per response
- supplier_name and location are VERY important — look carefully
"""
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    
    return chat_completion.choices[0].message.content


def scrape_exportersindia(url, num_pages=1):
    all_products = []
    
    for page in range(1, num_pages + 1):
        print(f" Scraping page {page}...")
        html = get_page_html(url, page)
        soup = BeautifulSoup(html, "html.parser")
        
        product_cards = soup.find_all("div", class_="clsProDet")
        print(f"Found {len(product_cards)} cards on page {page}")
        
        raw_text = " ".join([card.get_text(separator=" ", strip=True) 
                            for card in product_cards])
        
        if not raw_text.strip():
            print(f" No data found on page {page}")
            continue
            
        print(f" Extracting with AI...")
        ai_response = extract_with_ai(raw_text)
        
        try:
            products = json.loads(ai_response)
            all_products.extend(products)
            print(f" Got {len(products)} products from page {page}")
        except:
            print(f" AI response parse failed on page {page}")
            print(f"Raw AI response: {ai_response[:200]}")
            
    return all_products

def save_data(products):
    df = pd.DataFrame(products)
    df.to_csv("data/products.csv", index=False)
    df.to_json("data/products.json", orient="records", indent=2)
    print(f" Saved {len(df)} products!")
    return df

if __name__ == "__main__":
    all_products = []
    
    for category in CATEGORIES:
        url = BASE_URL.format(category=category)
        print(f"\n Scraping: {category}")
        products = scrape_exportersindia(url, num_pages=1)
        
        for p in products:
            p['category'] = category
        
        all_products.extend(products)
    
    if all_products:
        df = save_data(all_products)
        print(f"\n Total: {len(df)} products")
