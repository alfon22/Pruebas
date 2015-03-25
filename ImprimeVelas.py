# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 18:08:06 2015

@author: alf

Graficar un dataframe con datos del DAX de un para de años
"""

import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
     DayLocator, MONDAY
from matplotlib.finance import candlestick_ohlc
#from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
import pandas as pd
from matplotlib.dates import date2num

# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
#date1 = (2004, 2, 1)
#date2 = (2004, 4, 12)


#mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
#alldays = DayLocator()              # minor ticks on the days
#weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
#dayFormatter = DateFormatter('%d')      # e.g., 12

#quotes = quotes_historical_yahoo_ohlc('INTC', date1, date2)

#if len(quotes) == 0:
#    raise SystemExit

df = pd.read_csv('/home/alf/Pruebas/GOOG-TLV_INDX_S19.csv',parse_dates='Date',index_col='Date')
df['Date'] = [date2num(x) for x in df.index]
dt = df.reindex(columns=['Date','Open','High','Low','Close','Volume'])
#dt = dt.head(50)
tuples = [tuple(x) for x in dt.values ]

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.05)
#ax.xaxis.set_major_locator(mondays)
#ax.xaxis.set_minor_locator(alldays)
#ax.xaxis.set_major_formatter(weekFormatter)
#ax.xaxis.set_minor_formatter(dayFormatter)

#plot_day_summary(ax, quotes, ticksize=3)
candlestick_ohlc(ax, tuples, width=3,colorup=u'b', colordown=u'r')

#ax.xaxis_date()
ax.autoscale_view()
plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
plt.savefig('/home/alf/Pruebas/velas.png')
plt.show()
