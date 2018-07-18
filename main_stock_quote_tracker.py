from functions_stock_quote_tracker import *
from run_stock_quote_tracker import *
import time

# **** END OF IMPORTS *** #

###################################################################################################################
#
# This was developed and tested on Windows 8.1 and not tested on other Windows, Linux, etc. OS.
#
# Stock Quote Tracker will get latest trading price for stock symbols provided in the 
# symbol_list1 and symbols_list2 lists.
#
# 1. If the current day is a weekend or holdiay, the previous trading day data will be collected and displayed.
# 2. The latest data will be compared to previous latest data for each stock symbol and the percent change + or - 
#    wil be calculated and dispayed
#
# Again, this was developed and tested on Windows 8.1 and not tested on other Windows, Linux, etc. OS.
#
###################################################################################################################

##### **** IMPORTANT READ THIS **** ###### **** IMPORTANT READ THIS **** ###### **** IMPORTANT READ THIS **** #####
#
# The following packages need a pip install. Please visit url for any special instructions
# - colorama - https://pypi.org/project/colorama/
# - holidays - https://pypi.org/project/holidays/
#
# Real time stock quotes are obtained (get requests) from the Alpha Vantage api.
#
#
# Alpha Vantage
# #############
#
# An Alpha Vantage api_key is mandatory to run this script. You can obtain an api_key for free from
# https://www.alphavantage.co/
#
# After you obtain the api_key, create a text file named: alpha_vantage_api_key.txt 
# Cut and paste the 3 lines below and replace <your api_key number> with the api_key number you obtained from Alpha 
# Vantage. If you use the 3 lines below it will just work.
#
#    3 lines of your .txt file are as follows
#    ----------------------------------------
#    Alpha Vantage is a realtime Stock quote
#    Alpha Vantage apikey = <your api_key number>
#    <your api_key number>
#
#
# Next: you will need to provide the path to the alpha_vantage_api_key.txt.
# Example: av_path = 'c:\\users\\aaron\\python scripts\\Alpha Vantage APIKEY\\alpha_vantage_api_key.txt'
# the av_path is specified below. Please edit the path
#
##### **** IMPORTANT READ THIS **** ###### **** IMPORTANT READ THIS **** ###### **** IMPORTANT READ THIS **** #####
av_url = "https://www.alphavantage.co/query"
av_function = "TIME_SERIES_DAILY"
av_path = 'c:\\users\\aaron\\python scripts\\APIKEYS\\Alpha Vantage APIKEY\\alpha_vantage_api_key.txt'
av_api_key = get_alpha_vantage_api_key(av_path)

#################################################################################################
#
# User has options on how to provide stock symbols to track
#
# option1: user does NOT pre-define symbol_list1 or symbol_list2
# option2: user DOES pre-define symbol_list1 or symbol_list2
# option3: user DOES pre-define symbol_list1 and NOT symbol_list2 (NOT RECOMMENDED)
# option4: user DOES pre-define symbol_list2 and NOT symbol_list1 (NOT RECOMMENDED)
# option5: user DOES pre-define symbol_list1 = [] and symbol_list2 = [] (NOT RECOMMENDED)
#
# All options are handled
#
#################################################################################################

# option2: symbol_list1 and symbol_list2 can be edited with the stocks you choose to track.
# - user DOES pre-define symbol_list1 or symbol_list2
# Edit the list for the stock symbols you wish to track
symbol_list1 = ['SNAP', 'DQ', 'WYNN', 'VZ', 'SPOT', 'MSFT', 'CSCO', 'AAPL', 'AMZN', 'CBS']
symbol_list2 = ['NDAQ', 'FB', 'GOOGL', 'DIS', 'FOX', 'NFLX', 'PG', 'WMT', 'WM', 'AUDC']

# Begin
loop_continue = True
count = 1
max_count = 1001

# this script will loop through the stock symbols provided 1000 times
while loop_continue:

    try_symbol_list = True

    # Test the following
    # symbol_list1 != 0 and symbol_list2 != 0
    # symbol_list1 != 0 and symbol_list2 == 0
    # symbol_list1 == 0 and symbol_list2 != 0
    # symbol_list1 == 0 and symbol_list2 == 0

    # user has the option of pre-defining / assigning symbol_list1 and symbol_list2
    # this pre-defining happens above before while loop
    if try_symbol_list:

        try:
            symbol_list = get_symbol_list(symbol_list1, symbol_list2, count)

            if len(symbol_list) != 0:
                try_symbol_list = False

        except NameError:
            pass

    # user has the option of pre-defining / assigning symbol_list1 and not pre-defining symbol_list2
    # this situation should be rare but handling it here
    # this pre-defining happens above before while loop
    if try_symbol_list:

        try:
            fake_symbol_list = []
            symbol_list = get_symbol_list(symbol_list1, fake_symbol_list, count)

            if len(symbol_list) != 0:
                try_symbol_list = False

        except NameError:
            pass

    # user has the option of pre-defining / assigning symbol_list2 and not pre-defining symbol_list1
    # this situation should be rare but handling it here
    # this pre-defining happens above before while loop
    if try_symbol_list:

        try:
            fake_symbol_list = []
            symbol_list = get_symbol_list(fake_symbol_list, symbol_list2, count)

            if len(symbol_list) != 0:
                try_symbol_list = False

        except NameError:
            pass

    if try_symbol_list:
        symbol_list = []
        try_symbol_list = False


    # call run_stock_quotes()
    run_stock_quotes(av_url, av_function, av_api_key, symbol_list)

    # check if max_count has been reached.
    # if count == max_count then program will end
    if count == max_count:
        loop_continue = False
        print('\n')
        thank_you_stock_quoter_banner()

    else:
        count += 1



