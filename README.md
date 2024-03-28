# High Dividend Strategy

## Summary

1. Create a portfolio of high dividend ETFs
2. Rebalance often according to trend, MACD and RSI. There is an element of timing in this.
3. Collect dividends

The portfolio of chosen securities must have these characteristics:

1. Stable or growing non-yield-adjusted close price
2. High dividend yield (> 9%)
3. Enough liquidity to trade, e.g. mean volume above 100K


## Risks

- Security prices often drop on the ex-dividend date, often by the amount of the dividend
- Short term capital gains or losses
- Timing mistakes
- Liquidity risks (can't buy or sell at the right time)
- Unaccounted factors (e.g. the strategy has not been tested)


## References
https://www.investopedia.com/terms/r/recorddate.asp


## Implementation

Securities:

### HYGH (y=8.9% trending up) or HYGW (y=13%) or TLTW (y=16% but beware of downtrend)
```
BUY DATES:    Mar  1, Apr  1, May  1, Jun  1, Jun 30, Jul 31, Sep  2, Sep 30, Oct 31, Nov 29, Dec 18
Ex-D dates:   Mar  4, Apr  2, May  2, Jun  4, Jul  2, Aug  2, Sep  4, Oct  2, Nov  4, Dec  3, Dec 20
Record dates: Mar  5, Apr  3, May  3, Jun  4, Jul  2, Aug  2, Sep  4, Oct  2, Nov  4, Dec  3, Dec 20
Pay dates:    Mar 10, Apr  8, May  8, Jun 10, Jul  9, Aug  8, Sep 10, Oct  8, Nov  9, Dec 27, Jan  3
```
From: https://www.ishares.com/us/literature/shareholder-letters/isharesandblackrocketfsdistributionschedule.pdf


### OARK (y=30% avg_vol=105k less risky)
* AMDY (y=70% avg_vol=180k check trend/technicals of underlying AMD)
* TSLY,NVDY,CONY,MSTY also viable
```
BUY DATES:    Mar  5, Apr  3, May  3, Jun  5, Jul  3, Aug  6, Sep  5, Oct  3, Nov  5, Dec  4
Ex-D dates:   Mar  6, Apr  4, May  6, Jun  6, Jul  5, Aug  7, Sep  6, Oct  4, Nov  6, Dec  5
Record dates: Mar  8, Apr  5, May  7, Jun  6, Jul  5, Aug  7, Sep  6, Oct  4, Nov  6, Dec  5
Pay dates:    Mar  9, Apr  8, May  8, Jun  7, Jul  8, Aug  8, Sep  9, Oct  7, Nov  7, Dec  6
```
From: https://www.yieldmaxetfs.com/distribution-schedule/

### YMAX (y=31%) or YMAG (y=30%) or ULTY (64%)
```
BUY DATES:    Mar 13, Apr 16, May 14, Jun 13, Jul 16, Jul 14, Sep 17, Oct 15, Nov 13, Dec 17
Ex-D dates:   Mar 14, Apr 17, May 15, Jun 14, Jul 17, Aug 15, Sep 18, Oct 16, Nov 14, Dec 18
Record dates: Mar 15, Apr 18, May 16, Jun 14, Jul 17, Aug 15, Sep 18, Oct 16, Nov 14, Dec 18
Pay dates:    Mar 18, Apr 19, May 17, Jun 17, Jul 18, Aug 16, Sep 19, Oct 17, Nov 15, Dec 19
```
From: https://www.yieldmaxetfs.com/distribution-schedule/

### SVOL (y=15%)
```
BUY DATES:    Mar 22, Apr 24, May 23, Jun 24, Jul 25, Aug 26, Sep 24, Oct 25, Nov 22, Dec 20
Ex-D dates:   Mar 25, Apr 25, May 24, Jun 25, Jul 26, Aug 27, Sep 25, Oct 28, Nov 25, Dec 23
Record dates: Mar 26, Apr 26, May 28, Jun 25, Jul 26, Aug 27, Sep 25, Oct 28, Nov 25, Dec 23
Pay dates:    Mar 28, Apr 30, May 31, Jul  1, Jul 31, Aug 30, Sep 30, Oct 31, Nov 29, Dec 31
```
From: https://www.simplify.us/sites/default/files/2024-01/Simplify-Distribution-Calendar-2024.pdf


## Log

```
2024-03-18 300xULTY dividend $319
2024-03-18 400xYMAX dividend $227
2024-03-18 300xYMAG dividend $177
```
