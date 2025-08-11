import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from datetime import datetime
import os

URL = "https://stockcharts.com/freecharts/sctr.html"
DATA_DIR = "./data"

def fetch_sctr_page():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64; rv:141.0) Gecko/20100101 Firefox/141.0"
        )
    }
    resp = requests.get(URL, headers=headers)
    resp.raise_for_status()
    return resp.text


def parse_sctr(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", attrs={"id":"sctr"})
    rows = table.tbody.find_all("tr")
    records = []
    for row in rows:
        cols = [td.text.strip() for td in row.find_all("td")]
        # Adjust indices per actual page structure
        symbol, name, sector, industry, sctr, chg, last, volume, mktcap = cols[:9]
        records.append({
            "symbol": symbol,
            "name": name,
            "sector": sector,
            "industry": industry,
            "SCTR": float(sctr),
            "change": float(chg.strip('%')),
            "last": float(last.replace(',', '')),
            "volume": int(volume.replace(',', '')),
            "market_cap": float(mktcap.replace(',', '').strip('$'))
        })
    return pd.DataFrame(records)

def enrich_with_yf(df):
    info = []
    for sym in df["symbol"].tolist():
        ticker = yf.Ticker(sym)
        d = ticker.info
        info.append({
            "symbol": sym,
            "longName": d.get("longName"),
            "sector": d.get("sector"),
            "industry": d.get("industry"),
            "marketCap": d.get("marketCap")
        })
    df2 = pd.DataFrame(info).set_index("symbol")
    return df.set_index("symbol").combine_first(df2).reset_index()

def run_scan():
    html = fetch_sctr_page()
    df = parse_sctr(html)
    # sort high and low
    top = df.sort_values("SCTR", ascending=False).head(20)
    bottom = df.sort_values("SCTR", ascending=True).head(20)
    output = pd.concat([top.assign(bucket="top20"), bottom.assign(bucket="bot20")])
    output = output[output.volume >= 1_000_000]
    output = enrich_with_yf(output)
    today = datetime.utcnow().strftime("%Y%m%d")
    os.makedirs(DATA_DIR, exist_ok=True)
    fname = f"{DATA_DIR}/sctr-{today}.csv"
    output.to_csv(fname, index=False)
    print(f"Saved {len(output)} rows to {fname}")

if __name__ == "__main__":
    run_scan()
