import requests
import csv
import os
import glob
import re
import yfinance as yf
from datetime import datetime, timedelta

# ================= CONFIGURATION =================
CSV_URL = "https://www.cboe.com/available_weeklys/get_csv_download/"
ARCHIVE_DIR = "weeklys_archive"
# Set to True if you want to wait for real IV (slower), 
# or False to just use Beta (instant).
FETCH_REAL_IV = True 
# =================================================

def ensure_archive_dir():
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

def download_weeklys():
    headers = {'User-Agent': 'Mozilla/5.0'}
    print(f"Downloading CBOE Data from: {CSV_URL}...")
    try:
        response = requests.get(CSV_URL, headers=headers)
        response.raise_for_status()
        today_str = datetime.now().strftime("%Y-%m-%d")
        filepath = os.path.join(ARCHIVE_DIR, f"raw_weeklys_{today_str}.csv")
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
    except Exception as e:
        print(f"Error downloading: {e}")
        return None

def parse_csv_to_data(filepath):
    """Returns a dictionary: {TICKER: NAME}"""
    data_map = {}
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 2: continue
                col0, col1 = row[0].strip(), row[1].strip()
                if not col0 or not col1: continue
                if "Available Weeklys" in col0 or "Ticker" in col0: continue
                # Basic check to skip dates in the second column
                if re.search(r'\d{1,2}/\d{1,2}/\d{2,4}', col1): continue
                
                data_map[col0] = col1
    except Exception as e:
        print(f"Error parsing: {e}")
    return data_map

def get_iv_and_earnings(ticker_symbol):
    """
    Fetches extra data using yfinance. 
    Returns dict with Price, Sector, Earnings, and Volatility metrics.
    """
    try:
        # 1. Fetch Basic Info
        tick = yf.Ticker(ticker_symbol)
        
        # Fast Info (usually cached/quick)
        info = tick.info
        price = info.get('currentPrice', 0)
        sector = info.get('sector', 'N/A')
        beta = info.get('beta', 'N/A')
        
        # 2. Fetch Earnings Date
        # yfinance returns a table of dates; we want the next one
        earnings = "N/A"
        try:
            cal = tick.calendar
            if cal is not None and not cal.empty:
                # Calendar often has 'Earnings Date' or 'Earnings High' as index or column
                # Structure varies, but usually:
                dates = cal.get('Earnings Date', [])
                if dates:
                    earnings = dates[0].strftime('%Y-%m-%d')
        except:
            pass

        # 3. Fetch Real IV (Optional - SLOW)
        iv_display = "N/A"
        if FETCH_REAL_IV:
            try:
                # Get nearest expiration
                opts = tick.options
                if opts:
                    chain = tick.option_chain(opts[0])
                    # Get IV from At-The-Money Call (roughly)
                    calls = chain.calls
                    # Find strike closest to price
                    idx = (calls['strike'] - price).abs().idxmin()
                    iv_raw = calls.loc[idx, 'impliedVolatility']
                    iv_display = f"{iv_raw:.2%}"
            except:
                pass

        return {
            "Price": price,
            "Sector": sector,
            "Beta": beta,
            "Earnings": earnings,
            "IV": iv_display
        }
    except:
        return {"Price": 0, "Sector": "Error", "Beta": 0, "Earnings": "N/A", "IV": "N/A"}

def save_enriched_report(data_map, date_str):
    filename = f"enriched_weeklys_{date_str}.csv"
    filepath = os.path.join(ARCHIVE_DIR, filename)
    
    print(f"\nEnriching data for {len(data_map)} tickers (this may take a moment)...")
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ["Ticker", "Name", "Price", "Sector", "Earnings", "Beta", "IV"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        count = 0
        total = len(data_map)
        
        for ticker, name in sorted(data_map.items()):
            # Progress indicator
            count += 1
            if count % 10 == 0:
                print(f"Processing {count}/{total}...", end='\r')
            
            # Fetch Data
            extra = get_iv_and_earnings(ticker)
            
            row = {
                "Ticker": ticker,
                "Name": name,
                "Price": extra["Price"],
                "Sector": extra["Sector"],
                "Earnings": extra["Earnings"],
                "Beta": extra["Beta"],
                "IV": extra["IV"]
            }
            writer.writerow(row)
            
    print(f"\nDone! Enriched file saved to: {filepath}")

if __name__ == "__main__":
    ensure_archive_dir()
    
    # 1. Download
    raw_file = download_weeklys()
    
    if raw_file:
        date_str = os.path.basename(raw_file).replace('raw_weeklys_', '').replace('.csv', '')
        
        # 2. Parse
        data = parse_csv_to_data(raw_file)
        
        # 3. Enrich & Save
        save_enriched_report(data, date_str)
