import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import time

st.set_page_config(page_title='Momentum Screener', page_icon='🚀')

df = pd.read_csv('ind_niftytotalmarket_list.csv')

df = df.query("Series == 'EQ'")

df['Symbol'] = df['Symbol'] + '.NS'

newdf = df['Symbol'].tolist()

data = yf.download(newdf, period="1y", group_by="tickers")

annually = int(len(data))
sixmonthly = int(len(data) / 2)
quarterly = int(sixmonthly / 2)

screener = []

for ticker in newdf:
    try:

        return1yr = (data[ticker]['Close'][-1] / data[ticker]['Close'][0] - 1) * 100

        high52 = data[ticker]['Close'][-annually:].max()

        belowhigh52 = data[ticker]['Close'][-1] >= high52 * 0.75

        sma200 = data[ticker]['Close'].rolling(window=200).mean()

        abovesma200 = (((data[ticker]['Close'][-1] - sma200[-1])/data[ticker]['Close'][-1]) * 100).round(2)

        if (return1yr >= 6.5 and belowhigh52):

          return12m = ((data[ticker]['Close'][-1] / data[ticker]['Close'][0] - 1) * 100).round(2)
          return6m = ((data[ticker]['Close'][-1] / data[ticker]['Close'][-sixmonthly] - 1) * 100).round(2)
          return3m = ((data[ticker]['Close'][-1] / data[ticker]['Close'][-quarterly] - 1) * 100).round(2)

          dailyReturns = data[ticker]['Close'].pct_change()
          stddev = np.std(np.log1p(dailyReturns[1:])) * np.sqrt(252) * 100

          sharpe12m = ((return12m - 6.5)/stddev).round(2)
          sharpe6m = ((return6m - 3.25)/stddev).round(2)
          sharpe3m = ((return3m - 1.625)/stddev).round(2)

          avgsharpe = ((sharpe12m + sharpe6m + sharpe3m) / 3).round(2)

          awayfrom52whigh = (((high52 - data[ticker]['Close'][-1])/high52) * 100).round(2)

          lastclose = data[ticker]['Close'][-1].round(2)

          screener.append({
              'Ticker': ticker,
              '12M Return': return12m,
              '6M Return': return6m,
              '3M Return': return3m,
              '12M Sharpe': sharpe12m,
              '6M Sharpe': sharpe6m,
              '3M Sharpe': sharpe3m,
              'Avg Sharpe 12-6-3': avgsharpe,
              'Away from 52W High': awayfrom52whigh,
              'Above 200SMA': abovesma200,
              'CMP': lastclose
          })
    except KeyError:
        print(f"No data found for {ticker}")

df_screener = pd.DataFrame(screener)

df_screener = df_screener.sort_values('Avg Sharpe 12-6-3', ascending=False)

df_screener['Rank'] = df_screener['Avg Sharpe 12-6-3'].rank(ascending=False, method='first')

df_screener = df_screener.set_index('Rank')

df_screener[:30]

#df_screener.head(60).to_csv('Screener-rfr.csv')