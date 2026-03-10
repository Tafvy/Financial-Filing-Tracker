import requests
import json
import time

# --- CONFIGURATION ---
# Replace these with your actual tickers or a mechanism to read your TV export
TICKERS = ["AAOI", "AXTI", "LITE", "CHOR"] 
HEADERS = {'User-Agent': 'Taufiqur tauf2772@gmail.com'} 

def get_filings():
    # 1. Get Ticker-to-CIK mapping from SEC
    mapping_url = "https://www.sec.gov/files/company_tickers.json"
    mapping_data = requests.get(mapping_url, headers=HEADERS).json()
    
    ticker_to_cik = {v['ticker']: str(v['cik_str']).zfill(10) for k, v in mapping_data.items()}
    
    results = []

    for ticker in TICKERS:
        cik = ticker_to_cik.get(ticker.upper())
        if not cik: continue
        
        # 2. Fetch recent filings for this CIK
        sec_url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        try:
            data = requests.get(sec_url, headers=HEADERS).json()
            filings = data['filings']['recent']
            
            # Grab the last 5 filings
            for i in range(5):
                results.append({
                    "ticker": ticker,
                    "form": filings['form'][i],
                    "date": filings['filingDate'][i],
                    "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{filings['accessionNumber'][i].replace('-', '')}/{filings['primaryDocument'][i]}"
                })
            time.sleep(0.1) # Respect SEC rate limits (10 requests/sec)
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    # 3. Save to a JSON file for the front-end
    with open('data.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    get_filings()
