import os
import pandas as pd
import pytz
import yfinance as yf
from datetime import datetime, timedelta

DATA_FOLDER = './.data'


def get_price(ticker_symbol, period='6mo'):
    data_file = f'{DATA_FOLDER}/{ticker_symbol}.csv'
    if os.path.exists(data_file):
        local_data = pd.read_csv(data_file)
        local_data['Date'] = pd.to_datetime(local_data['Date'])
        local_data.set_index('Date', inplace=True)
        latest_date = local_data.index.max()
        now = pd.Timestamp(datetime.now())
        if latest_date < now:
            recent = yf.download(ticker_symbol, start=latest_date, end=now)
            union = pd.concat([local_data, recent])
            local_data = union.groupby(union.index).first()
            local_data.to_csv(data_file)
    else:
        local_data = yf.download(ticker_symbol, period=period)
        local_data.to_csv(data_file)

    ticker = yf.Ticker(ticker_symbol)
    divs = ticker.get_dividends()
    d2 = pd.DataFrame({
        'Date': [d.tz_localize(None) for d in divs.keys()],
        'Dividend': divs.values
    })
    d2.set_index('Date', inplace=True)
    merged = pd.merge(local_data, d2, left_index=True, right_index=True, how='outer')
    return merged


if __name__ == "__main__":
    p = get_price('OARK')
    print(p)
