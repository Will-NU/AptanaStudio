# Computational Investing Part I
# Homework 1
# Peng (Will) Chen

import pandas as pd
import numpy as np
import math
import copy
import QSTK.qstkutil.qsdateutil as du
import datetime as dt
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkstudy.EventProfiler as ep

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""


def find_events(ls_symbols, d_data):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
 
            # Event is found if the symbol price is below 5 today and
            # is above 5 yesterday
            if f_symprice_today < 5.0 and f_symprice_yest >= 5.0:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1

    return df_events

def find_events_by_daily_return(ls_symbols, d_data, f_lb = -1.0, f_ub = np.Inf):
    ''' Finding the event dataframe '''
    df_close = d_data['actual_close']

    print "Finding Events"

    # Creating an empty dataframe
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Time stamps for the event range
    ldt_timestamps = df_close.index

    for s_sym in ls_symbols:
        for i in range(1, len(ldt_timestamps)):
            f_symprice_today = df_close[s_sym].ix[ldt_timestamps[i]]
            f_symprice_yest = df_close[s_sym].ix[ldt_timestamps[i - 1]]
            f_symreturn_today = (f_symprice_today / f_symprice_yest) - 1
 
            # Event is found if the symbol return today is between f_lb and f_ub
            if f_symreturn_today > f_lb and f_symreturn_today < f_ub:
                df_events[s_sym].ix[ldt_timestamps[i]] = 1
                print s_sym
                print ldt_timestamps[i]

    return df_events

if __name__ == '__main__':
    dt_start = dt.datetime(2008, 1, 1)
    dt_end = dt.datetime(2009, 12, 31)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    
    # symbols from sp500 in 2012
#     ls_symbols = dataobj.get_symbols_from_list('sp5002012')
#     ls_symbols.append('SPY')
# 
#     ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
#     ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
#     d_data = dict(zip(ls_keys, ldf_data))
#  
#     for s_key in ls_keys:
#         d_data[s_key] = d_data[s_key].fillna(method='ffill')
#         d_data[s_key] = d_data[s_key].fillna(method='bfill')
#         d_data[s_key] = d_data[s_key].fillna(1.0)
#  
#     df_events = find_events(ls_symbols, d_data)
#     print "Creating Study"
#     ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
#                 s_filename='MyEventStudy2012.pdf', b_market_neutral=True, b_errorbars=True,
#                 s_market_sym='SPY')
# 
    # symbols from sp500 in 2008
    ls_symbols = dataobj.get_symbols_from_list('sp5002008')
    ls_symbols.append('SPY')
 
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
 
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
 
    #df_events = find_events(ls_symbols, d_data)
    df_events = find_events_by_daily_return(ls_symbols, d_data, f_ub = -0.5)
    print "Creating Study"
    ep.eventprofiler(df_events, d_data, i_lookback=20, i_lookforward=20,
                s_filename='MyEventStudy2008_drop50percent.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
    
    print 'done'
