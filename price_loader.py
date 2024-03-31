import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


session = CachedLimiterSession(
    limiter=Limiter(RequestRate(2, Duration.SECOND * 5)),  # max 2 requests per 5 seconds
    bucket_class=MemoryQueueBucket,
    backend=SQLiteCache("yfinance.cache"),
)
DATA_FOLDER = './.data'


def get_price(ticker_symbol, period='200D'):
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
        local_data = yf.download(ticker_symbol, period=period, session=session)
        local_data.to_csv(data_file)

    ticker = yf.Ticker(ticker_symbol, session=session)
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
