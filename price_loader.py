import os
import pandas as pd
import yfinance as yf
from datetime import datetime, time
from pytz import timezone

# Enable local caching
yf.pdr_override()

DATA_FOLDER = './.data'


def is_market_open():
    current_time = datetime.now().astimezone(timezone('US/Eastern')).time()

    # Define NYSE trading hours
    nyse_open_time = time(9, 30)
    nyse_close_time = time(16, 0)

    # Check if current time is within NYSE trading hours
    return nyse_open_time <= current_time <= nyse_close_time


def get_end(latest_date):
    FRIDAY = 4
    now = pd.Timestamp(datetime.today())
    if is_market_open():
        return now
    d = pd.Timestamp(now.date())
    delta = d.day_of_week - FRIDAY if d.day_of_week > FRIDAY else 0
    return d - pd.Timedelta(days=delta)


def get_price(ticker_symbol, period='200D'):
    data_file = f'{DATA_FOLDER}/{ticker_symbol}.csv'
    if os.path.exists(data_file):
        local_data = pd.read_csv(data_file)
        local_data['Date'] = pd.to_datetime(local_data['Date'])
        local_data.set_index('Date', inplace=True)
        latest_date = local_data.index.max()
        end_date = get_end(latest_date)
        if latest_date < end_date:
            recent = yf.download(ticker_symbol, start=latest_date, end=end_date)
            union = pd.concat([local_data, recent])
            local_data = union.groupby(union.index).first()
            local_data.to_csv(data_file)
    else:
        local_data = yf.download(ticker_symbol, period=period)
        local_data.to_csv(data_file)

    ticker = yf.Ticker(ticker_symbol)
    divs = ticker.get_dividends()
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - pd.Timedelta(period)).strftime('%Y-%m-%d')
    divs = divs[(divs.index >= start_date) & (divs.index <= end_date)]

    d2 = pd.DataFrame({
        'Date': [d.tz_localize(None) for d in divs.keys()],
        'Dividend': divs.values
    })
    d2.set_index('Date', inplace=True)
    merged = pd.merge(local_data, d2, left_index=True, right_index=True, how='outer')
    return merged


if __name__ == "__main__":
    p = get_price('SVOL', '360D')
    print(p)
