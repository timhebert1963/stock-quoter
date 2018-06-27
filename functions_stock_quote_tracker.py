import requests
import json
import sys
import time
import calendar

# holidays api -> from https://pypi.org/project/holidays/
import holidays

# get time from different timezones
import pytz
from pytz import timezone

from datetime import date
from datetime import timedelta
import datetime as dt

from Tim_common import *

from colorama import Fore, Back, Style, init
init(autoreset = True)

# **** END OF IMPORTS **** #


def get_symbol_list(symbol_list1, symbol_list2, count):

    # user has the option of pre-defining / assigning symbol_list1 and symbol_list2
    if len(symbol_list1) != 0 and len(symbol_list2) != 0:
        if count % 2 != 0:
            symbol_list = symbol_list1
        else:
            symbol_list = symbol_list2

    # user has the option of pre-defining / assigning symbol_list1 and not pre-defining symbol_list2
    # this situation should be rare but handling it here
    elif len(symbol_list1) != 0:
        symbol_list = symbol_list1

    # user has the option of pre-defining / assigning symbol_list2 and not pre-defining symbol_list1
    # this situation should be rare but handling it here
    elif len(symbol_list2) != 0:
        symbol_list = symbol_list2

    # none of the above conditions are True
    else:
        symbol_list = []

    return symbol_list

# **** End of get_symbol_list() **** #


def get_alpha_vantage_api_key(path):

    # open file c:\\users\\aaron\\python scripts\\Alpha Vantage APIKEY\\alpha_vantage_api_key.txt
    # readline 2 (which is actually line 3)
    # return key
    api_key = open(path,'r')
    lines   = api_key.readlines()
    key     = lines[2][:-1]

    return key

# **** End of get_alpha_vantage_api_key() **** #


def welcome_to_stock_quotes_banner():

    #first = 8
    #mid   = 15 * 5
    #last  = 30
    #center = first + mid + last
    line_len = 118

    # assign string to display in display_banner()
    first_string  = "Welcome to Stock Quoter"
    second_string = "Stock Quoter: displays stock performance stats"
    third_string  = "Alpha Vantage url: https://www.alphavantage.co/query used for Stock Queries"

    first_string  = pad_banner_string(first_string, line_len)
    second_string = pad_banner_string(second_string, line_len)
    third_string  = pad_banner_string(third_string, line_len)

    print(first_string)
    print('\n')
    print(second_string)
    print('\n')
    print(third_string)
    print('\n')
    print('\n')

# **** End of welcome_to_stock_quotes_banner() **** #


def stock_quotes_available_banner(second_string, est_time):

    line_len = 118

    time = what_is_string_time(est_time)

    # assign string to display in display_banner()
    first_string  = "Stock Quoter Results Available"
    third_string  = "Current time: {} EST".format(time)

    first_string   = pad_banner_string(first_string, line_len)
    second_string  = pad_banner_string(second_string, line_len)
    third_string   = pad_banner_string(third_string, line_len)

    print(first_string)
    print(second_string)
    print(third_string)
    print('\n')

# **** End of stock_quotes_available_banner() **** #


def thank_you_stock_quoter_banner():

    line_len = 118

    # assign string to display in display_banner()
    first_string  = "########################################"
    second_string = "#   Thank You for using Stock Quoter   #"
    third_string  = "########################################"

    first_string   = pad_banner_string(first_string, line_len)
    second_string  = pad_banner_string(second_string, line_len)
    third_string   = pad_banner_string(third_string, line_len)

    print('\n')
    print(first_string)
    print(second_string)
    print(third_string)
    print('\n')
    print('\n')


# **** End of thank_you_stock_quoter_banner() **** #


def pad_banner_string(string, line_len):

    # create spaces for front and back of first_string for display
    string_front = int((line_len - len(string)) / 2)
    string_back  = line_len - (string_front + len(string))

    front = ''
    back  = ''

    for i in range(string_front + 1):
        front = front + " "

    for i in range(string_back + 1):
        back = back + " "

    string = front + string + back

    return string

# **** End of function pad_banner_string() **** #


def do_you_want_to_track_symbols():
    no_y_or_n     = "You must answer 'y' or 'n'. Try again!"    
    track_symbols = ("Do you want to track stock symbols?")
    answer        = input(" {} Enter 'y' or 'n'.  ".format(track_symbols))

    # make sure answer is 'y' or 'n'
    while answer.lower() != 'y' and answer.lower() != 'n':
        print('\n')
        print(" {}".format(no_y_or_n))
        print('\n')
        answer = input(" {} Enter 'y' or 'n'.  ".format(track_symbols))

    if answer.lower() == 'n':
        return False
    else:
        return True

# **** End of function do_you_want_to_track_symbols() **** #


def what_symbols_to_track(symbol_list):

    # input strings - enter_stock_symbol
    # questions     - additional_symbol
    # statement     - no_y_or_n
    enter_stock_symbol = " Enter stock symbol you want to track."
    additional_symbol  = " Do you want to track additional stock symbols? Enter 'y' or 'n'."
    no_y_or_n          = " You must answer 'y' or 'n'. Try again!"

    continue_loop = True

    while continue_loop:

        # get stock symbol
        symbol_list.append(input("{}   ".format(enter_stock_symbol)))

        # ask user if additional symbols will be entered
        answer = input("{}   ".format(additional_symbol))
        print('\n')

        # make sure answer is 'y' or 'n'
        while answer.lower() != 'y' and answer.lower() != 'n':
            print('\n')
            print("{}".format(no_y_or_n))
            print('\n')
            answer = input("{}   ".format(additional_symbol))

        if answer.lower() == 'n':

            # make sure all symbols are upper case
            for i in range(len(symbol_list)):
                symbol_list[i] = symbol_list[i].upper()

            return symbol_list

# **** End of what_symbols_to_track() **** #


def get_est_date():

    # US stock markets are on Eastern Standard Time

    tz = timezone('US/Eastern')
    eastern = dt.datetime.now(tz)

    # example of date format '2018-06-19'
    year  = str(eastern.year)

    # month needs to be 2 digits
    if eastern.month < 10:
        month = '0'+str(eastern.month)
    else:
    	month = str(eastern.month)

    # day needs to be 2 digits
    if eastern.day < 10:
        day = '0'+str(eastern.day)
    else:
    	day = str(eastern.day)

    return year + '-' + month + '-' + day

# **** End of get_est_date() **** #


def get_est_time():

    # US stock markets are on Eastern Standard Time

    tz = timezone('US/Eastern')
    eastern = dt.datetime.now(tz)

    hour = eastern.hour
    minute = eastern.minute
    time = (hour, minute)

    return time

# **** End of get_est_time() **** #


def get_est_day():

    # US stock markets are on Eastern Standard Time

    now = dt.datetime.now(pytz.timezone('US/Eastern'))
    weekday = now.weekday()
    return calendar.day_name[weekday]

# **** End of get_est_day() **** #


def is_US_holiday(est_date):

    # if not a holiday then holiday will be assigned NoneType
    # if it is a holiday then holiday will be assigned a US Holiday Name -> 'Independence Day'
    us_holidays = holidays.UnitedStates()
    holiday = us_holidays.get(est_date)

    # custom_holidays = holidays.HolidayBase()
    # usage append: custom_holidays.append({"2018-03-30": "Good Friday"})
    # usage get:    custom_holidays.get("2018-03-30")
    #
    # Good Friday needs to be added as a custom holiday.
    custom_holidays = holidays.HolidayBase()

    custom_holidays.append({'2017-04-14': 'Good Friday'})
    custom_holidays.append({'2018-03-30': 'Good Friday'})
    custom_holidays.append({'2019-04-19': 'Good Friday'})
    custom_holidays.append({'2020-04-10': 'Good Friday'})
    custom_holidays.append({'2021-04-02': 'Good Friday'})
    custom_holidays.append({'2022-04-15': 'Good Friday'})
    custom_holidays.append({'2023-04-07': 'Good Friday'})
    custom_holidays.append({'2024-03-29': 'Good Friday'})
    custom_holidays.append({'2025-04-18': 'Good Friday'})
    custom_holidays.append({'2026-04-03': 'Good Friday'})

    if holiday == None:
        holiday = custom_holidays.get(est_date)

    if holiday ==  None:
        holiday_result = ('not holiday')

    else:
        holiday_result = ('is holiday', holiday)

    return holiday_result

# **** End of is_US_holiday() **** #


def get_display_message(est_date, est_time, est_day, holiday_result):

    def when_is_black_friday(year):
        # Black Friday is the day after Thanksgiving and the US Stock Markets close
        # at 1pm EST the day after Thanksgiving to oberserve Thanksgiving.
        #
        # The same day is also known as Black Friday in US Retail.
        # return the date of black_friday in the format '2018-11-23'
        us_holidays = holidays.UnitedStates()

        str_year = str(year)

        for i in range(13, 31):
            str_i = str(i)
            date = str_year + '-' + '11' + '-' + str_i

            is_thanksgiving = us_holidays.get(date)

            if is_thanksgiving ==  None:
                pass
            else:
                # increment the 'day' of the date + 1 and this is black_friday
                black_friday = str_year + '-' + '11' + '-' + str(i+1)

                return black_friday

    # **** End of function when_is_black_friday() **** #

    # split the est_date passed in as argument
    # convert the indexes of split_date to int
    #
    # year will be used to determine what date of that year is 'Black Friday' which is day 
    # after Thanksgiving
    #
    # month and day will be used to determine if the date is July 3rd or Dec 24
    #
    # US Stock Markets close at 1pm EST on July 3rd, Black Friday (day after Thanksgiving)
    # and Dec 24th of every year
    split_date = est_date.split('-')
    year  = int(split_date[0])
    month = int(split_date[1])
    day   = int(split_date[2])

    black_friday = when_is_black_friday(year)

    current_est_time = what_is_string_time(est_time)

    message        = "US Stock Markets are Open"
    closed_message = "US Stock Markets are Closed"

    # US Stock Markets are closed on Saturday and Sunday
    if est_day == 'Saturday' or est_day == 'Sunday':
        day_message = " on '{}'".format(est_day)
        message = "{}{}".format(closed_message, day_message)

    # US Stock Markets are closed on Holidays
    elif holiday_result[0] == 'is holiday':
        holiday_message = " on '{}'".format(holiday_result[1])
        message = "{}{}".format(closed_message, holiday_message)

    ##########################################################################################
    # US Stock Markets close at 1pm EST on July 3rd, Day after Thanksgiving and Christmas Eve
    ##########################################################################################

    # July 3rd case - day before Independance Day
    #
    # US Stock Markets close at 1pm EST
    # (FYI) US Stock Markets close at 4pm EST if not a observed holiday
    elif (month == 7 and day == 3) and (est_time[0] >= 13 and est_time[0] < 16):
        at_1pm_message = " at 13:00 EST to observe 'Independence Day'"
        message = "{}{}".format(closed_message, at_1pm_message)

    # Dec 24th case - Christmas Eve
    #
    # US Stock Markets close at 1pm EST
    # (FYI) US Stock Markets close at 4pm EST if not a observed holiday
    elif (month == 12 and day == 24) and (est_time[0] >= 13 and est_time[0] < 16):
        at_1pm_message = " at 13:00 EST for 'Chistmas Eve'"
        message = "{}{}".format(closed_message, at_1pm_message)

    # Day after Thanksgiving case - aka Black Friday
    # call when_is_black_friday(year) and a date will be returned - example: '2018-11-23'
    #
    # US Stock Markets close at 1pm EST
    # (FYI) US Stock Markets close at 4pm EST if not a observed holiday
    elif est_date == black_friday and (est_time[0] >= 13 and est_time[0] < 16):
        at_1pm_message = " at 13:00 EST to observe 'Thanksgiving Day'"
        message = "{}{}".format(closed_message, at_1pm_message)


    # US stock markets (NYSE and NASDAQ) trading hours are from 9:30 EST to 16:00 EST (4pm EST)
    elif (est_time[0] < 9 or est_time[0] >= 16) or (est_time[0] == 9 and est_time[1] < 30):
        message = "{}".format(closed_message)
        
    return message

# **** End of get_display_message() **** #


def what_is_string_time(time):
    # convert int time to string time
    # int time = (12, 0) where 12 is hour and 0 is minute
    # string hour and string minute need to represent a 2 digit number
    if time[0] <= 9:
        hour = '0' + str(time[0])
    else:
        hour = str(time[0])

    if time[1] <= 9:
        minute = '0' + str(time[1])
    else:
        minute = str(time[1])

    str_time = hour + ':' + minute

    return str_time

# **** End of function what_is_string_time() **** #

def is_US_stock_exchange_open(est_date, est_time, est_day, holiday_result):

    # Args passed in -> examples
    # est_date '2018-06-19'
    # est_time (8, 1) -> 8:01am
    # est_day 'Tuesday'
    # holiday_result (False) if not holiday
    #                (True, 'holiday name') if is a holiday
    #
    # check for Holiday
    # check for Saturday and Sunday
    # if not Saturday, Sunday or Holiday return (True)
    # if Holiday return (False, <'Holiday Name'>)
    # if Saturday return (False, 'Saturday')
    # if Sunday return (False, 'Sunday')

    fpw_called = False    # fpw_called (find_previous_weekday_called) is set to False.
                          # fpw_called = True -> if holiday_result[0] == 'is holiday':
                          # fpw_called = True -> elif est_day == 'Saturday' or est_day == 'Sunday':
                          # fpw_called = True -> elif est_time[0] < 9 or (est_time[0] == 9 and est_time[1] < 30):

    if holiday_result[0] == 'is holiday':

        fpw_called = True

        # it is a holiday
        # call find_previous_weekday() and pass est_date amd est_day
        previous_weekday_date, previous_weekday_name = find_previous_weekday(est_date, est_day)

    elif est_day == 'Saturday' or est_day == 'Sunday':

        fpw_called = True

        # current est_day is Saturday or Sunday. Need to get previous weekday
        previous_weekday_date, previous_weekday_name = find_previous_weekday(est_date, est_day)
        holiday_result = is_US_holiday(previous_weekday_date)

        if holiday_result[0] == 'is holiday':
            previous_weekday_date, previous_weekday_name = find_previous_weekday(previous_weekday_date, previous_weekday_name)

    elif est_time[0] < 9 or (est_time[0] == 9 and est_time[1] < 30):

        fpw_called = True

        # current est_time is before 9:30am EST and US Stock Markets not open. 
        # Need to get previous weekday
        previous_weekday_date, previous_weekday_name = find_previous_weekday(est_date, est_day)
        holiday_result = is_US_holiday(previous_weekday_date)

        if holiday_result[0] == 'is holiday':
            previous_weekday_date, previous_weekday_name = find_previous_weekday(previous_weekday_date, previous_weekday_name)

    if fpw_called:
        return previous_weekday_date
    else:
        return est_date

# **** End of function is_US_stock_exchange_open() **** #


def find_previous_weekday(est_date, est_day):


    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

    # need to find previous date. split est_date.
    #
    # est_date = '2018-06-19' and needs to be split to convert to int in order to use 
    # date(year, month, day) class.
    split_date = est_date.split('-')
    year  = int(split_date[0])
    month = int(split_date[1])
    day   = int(split_date[2])

    today = date(year, month, day)

    if est_day == 'Saturday':
        # previous is Friday. Subtract 1 day
        minus_days = timedelta(days=1)
        previous_weekday_name = 'Friday'

    elif est_day == 'Sunday':
        # previous is Friday. Subtract 2 days
        minus_days = timedelta(days=2)
        previous_weekday_name = 'Friday'

    elif est_day == 'Monday':
        # previous is Friday. Subtract 3 days
        minus_days = timedelta(days=3)
        previous_weekday_name = 'Friday'

    else:
        # Tuesday thru Friday. Subtract 1 day
        minus_days = timedelta(days=1)

        # get previous_weekday_name from weekday_names list
        for i in range(len(weekday_names)):
            if est_day == weekday_names[i]:
                previous_weekday_name = weekday_names[i-1]

    # subtract today - previous to get previous weekday
    previous_weekday_date = today - minus_days

    #################################################################
    # assemble the date back to a '2018-06-19' string format
    #################################################################
    year  = str(previous_weekday_date.year)

    # month needs to be 2 digit format
    if previous_weekday_date.month < 10:
        month = '0' + str(previous_weekday_date.month)
    else:
        month = str(previous_weekday_date.month)

    # day needs to be 2 digit format
    if previous_weekday_date.day < 10:
        day = '0' + str(previous_weekday_date.day)
    else:
        day = str(previous_weekday_date.day)

    # assemble the date
    previous_weekday_date = year + '-' + month + '-' + day

    return previous_weekday_date, previous_weekday_name

# **** End of function find_previous_weekday() **** #


def get_stock_quotes(url, function, api_key, current_date, symbol_list, pb):

    ###########################################################################################
    # pb has been passed in as an argument.
    #
    # pb = ProgressBar() and will update the pb object with progress of stock symbol queries
    # a progress bar will be displayed to the user
    ###########################################################################################

    quote_dict = {}

    # loop through symbol_list and create dictionary
    for i in range(len(symbol_list)):

        symbol = symbol_list[i]

        # assign data to the alpha vantage parameters needed to make the alpha vantage api call
        data = { "function": function, 
                 "symbol": symbol,
                 "apikey": api_key }

        # assign variable page the get requests data for the advantage url
        page = requests.get(url, params = data)

        # try_count will be used to determine the number of re-tries inside while loop: try: statement
        try_count = 1

        # assign alpha_vantage_get_data = True to execute while loop
        alpha_vantage_get_data = True

        while alpha_vantage_get_data:

            try:
                # sometimes there are Key Errors when retrieving and fetching data from alpha vantage.
                # url = "https://www.alphavantage.co/query"
                #
                # theory is, the site cannot always keep up with requests
                #
                # the while loop and try: except: creates a re-try mechanism

                ######################################################################################################
                # sleep for 1 second. This is done to slow down the number of get requests to Alpha Vantage site
                # to get the real-time stock quotes. The site recommends <= 200 requests per minute
                #
                # at times the queries will result in a key error and the theory is this is due to the rate of get
                # request. I have a question out to the Alpha Vantage site admins to see if the theory is correct.
                ######################################################################################################
                time.sleep(1)

                # if try_count == 2 then first attempt to get the data for current symbol did not receive a valid response
                # from Alpha Vantage. Typically a key error for 'Time Series (Daily)' key
                #
                # abort the current get request and assign av_query '00.00' values for each key in the av_query dictionary
                # 
                # for loop will move to next item in symbol_list
                # break to terminate while loop
                if try_count == 2:
                    av_query = {'1. open'  : '00.00',
                                '2. high'  : '00.00',
                                '3. low'   : '00.00',
                                '4. close' : '00.00',
                                '5. volume': '00.00'}

                    break

                else:
                    pass  # do nothing

                # increment try_count before query. If query fails -> except:   will execute pass
                # if try: succeeds the whil loop will terminate and try_count += 1 will not be evaluated
                try_count += 1
                
                #####################################################################################
                #
                # page.json()['Time Series (Daily)'][current_date]   will return a dictionary in the
                # following format.
                #
                # dictionary = {'1. open'  : value,
                #               '2. high'  : value,
                #               '3. low'   : value,
                #               '4. close' : value,
                #               '5. volume': value}
                #
                #####################################################################################             
                av_query = page.json()['Time Series (Daily)'][current_date]

                # assign alpha_vantage_get_data = False to terminate while loop
                alpha_vantage_get_data = False

            except Exception as e:
                # used for debugging
                #print("DEBUG: get_stock_quotes() page.json()['Time Series (Daily)'][current_date]")
                #print("DEBUG: *** symbol {:<6} : {} : {}".format(symbol, current_date, e))
                pass

        # get the company name for the stock symbol
        company_name = get_company_name(symbol)  # get company name from Yahoo! Finance API

        quote_dict[symbol] = {'open':   av_query['1. open'],
                              'high':   av_query['2. high'],
                              'low':    av_query['3. low'],
                              'close':  av_query['4. close'],
                              'volume': av_query['5. volume'],
                              'company_name': company_name}

        # a progress bar will be displayed to notify user of symbol query progress
        # increment pb.query_complete
        pb.query_complete += 1

        display_progress_bar(pb)

        # sleep after progress bar complete to give user a chance to view
        time.sleep(2)

    return quote_dict

# **** End of get_stock_quotes() **** #


def progress_bar_scale():
    # create a progress bar
    blank = ' '
    print("{:>22}{}{:>24}{:>23}{:>23}{:>26}".format(blank, '0', '25%', '50%', '75%', '100%'))
    print(" Stock Query Progress", end="")

# **** End of progress_bar_scale() **** #


def display_progress_bar(pb):

    # pbar is the progress bar (colored bar)
    pbar = ''
    
    for i in range(pb.progress_units):
        pbar = pbar + (Back.GREEN + ' ' + Style.RESET_ALL)

    if pb.query_complete == 1:
        first = ' '
        pbar = first + pbar

    # check if pb.query_complete == pb.display_width
    # if True complete remainder of progress bar to 100%. All Queries done
    if pb.query_complete == pb.symbol_list_length:
        # complete remainder of progress_bar
        # force carriage return
        pbar_remaining = pb.display_width - (pb.query_complete * pb.progress_units)

        for i in range(pbar_remaining):
            pbar = pbar + (Back.GREEN + ' ' + Style.RESET_ALL)

        print(pbar)

    else:
        print(pbar, end="")

# **** End of display_progress_bar() **** #


def get_company_name(symbol):

    yahoo_url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)

    yahoo_get_company_name_data = True

    while yahoo_get_company_name_data:

        try:
            # sometimes there are Errors when retrieving and fetching data from
            # yahoo_url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(symbol)
            #
            # the while loop and try: except: creates a re-try mechanism
            result = requests.get(yahoo_url).json()

            for company in result['ResultSet']['Result']:
                if company['symbol'] == symbol:

                    yahoo_get_company_name_data = False

                    return company['name']

        except:
            pass   # do nothing

# **** End of get_company_name() **** #


def get_weekday_name(date):

    # arg date is passed date='2018-06-21'
    # split date
    # assign year as int, assign month as int, assign day as int
    split_date = date.split('-')
    year = int(split_date[0])
    month = int(split_date[1])
    day = int(split_date[2])

    my_date = dt.date(year, month, day)
    weekday_name = calendar.day_name[my_date.weekday()]

    return weekday_name
    
# **** End of function get_weekday_name() **** #


def is_quote_up_or_down(quote, previous_quote, symbol_list):

    def change_float_to_string(percent_change, pos_or_neg):

        # change to string with 2 decimals
        percent_change = "%.2f" % percent_change

        decimal = percent_change[-2:]
        integer = percent_change[:-3]

        # make sure integer string appears as a 2 digit number.
        # if integer appears as a 1 digit number lead with a '0'
        # 0.10 will change to 00.10
        if len(integer) == 1:
            integer = '0' + integer

        # if pos_or_neg == 'pos' lead the integer with a '+'
        # if pos_or_neg == 'neg' lead the integer with a '-'
        if pos_or_neg == 'pos':
            integer = '+' + integer
        elif pos_or_neg == 'neg':
            integer = '-' + integer

        # combine integer and decimal to appear as a decimal number and add % to end of string
        percent_change = integer + '.' + decimal + '%'

        return percent_change

    # **** End of function change_float_to_string() **** #


    for symbol in symbol_list:

        current_close  = float(quote[symbol]['close'])
        previous_close = float(previous_quote[symbol]['close'])

        if current_close == 0 or previous_close == 0:

            # this is a case where one of the queries for this stock symbol did not complete
            # for either current query or previous query and the data assigned to keys in the
            # dictionary are '00.00'
            #
            # the percent change will remain unknown and percent_change_str will be assign NA
            percent_change_str = '    NA%'

            change_symbol = '-'
            change_status = 'UNKNOWN'

        elif current_close == previous_close:
            percent_change_str = ' 00.00%'

            change_symbol = '-'    # 00.00% change. change_symbol = ' '
            change_status = 'flat'

        elif current_close > previous_close:
            diff = current_close - previous_close
            percent_change = float((diff / current_close) * 100)
            percent_change = round(percent_change, 2)

            # change float to string with a decimal number format
            # hange_float_to_string() will return a float 0.1 with a string 00.10
            percent_change_str = change_float_to_string(percent_change, 'pos')

            change_symbol = '*'
            change_status = 'up'

        elif current_close < previous_close:
            diff = previous_close - current_close
            percent_change = float((diff / previous_close) * 100)
            percent_change = round(percent_change, 2)

            # change float to string with a decimal number format
            # hange_float_to_string() will return a float 0.1 with a string 00.10
            percent_change_str = change_float_to_string(percent_change, 'neg')

            change_symbol = '*'
            change_status = 'down'

        quote[symbol]['percent_change'] = percent_change_str
        quote[symbol]['change_symbol']  = change_symbol
        quote[symbol]['change_status']  = change_status

    return quote

# **** End of function is_quote_up_or_down() **** #


def display_stock_quotes(est_date, orig_est_date, symbol_list, quote):

    def create_dashed_line(first, second, third, mid, mid_num, last):

        # assign dashed lines for the display format
        dashed_line_string = ' '

        # create first set of dashes and end with a |
        for i in range(first+1):
            if i == first:
                dashed_line_string = dashed_line_string + '|'
            else:
                dashed_line_string = dashed_line_string + '-'

        # create second set of dashes (do not end with |)
        for i in range(second):
            dashed_line_string = dashed_line_string + '-'

        # create third set of dashes and end with a |
        for i in range(third+1):
            if i == third:
                dashed_line_string = dashed_line_string + '|'
            else:
                dashed_line_string = dashed_line_string + '-'


        # create mid sets of dashes and end each mid with a |
        # the number of mid sets = mid_num
        count = 0
        while count < mid_num:

            for i in range(mid+1):
                if i == mid:
                    dashed_line_string = dashed_line_string + '|'
                else:
                    dashed_line_string = dashed_line_string + '-'

            count += 1

        # create last set of dashes
        for i in range(last):
            dashed_line_string = dashed_line_string + '-'

        return dashed_line_string

    # **** End of function create_dashed_line() **** #


    # set up the field sizes -> first section, mid section * mid_num, last section
    #
    #             second,
    #   first     third    .. mid section * mid_num ..    last section
    # 
    #  --------|----------|-------------|-------------|---------------------------

    first   = 8        # first set field size; first set dashed line -> number of dashes = first
    second  = 2        # second set field size; second set dashed line -> number of dashes = second
    third   = 8        # third set field size; third set dashed line -> number of dashes = third
    mid     = 13       # mid   set field size; mid   set dashed line -> number of dashes = mid
    mid_num = 5        # mid_num = number of mid sets used to print the number of mid sets dashes
    last    = 27       # last  set field size; last  set dashed line -> number of dashes = last

    ################################################################################################
    #
    # Pad the title variables with spacess for display positioning
    #
    # create
    #
    ################################################################################################

    # create titles of 2nd row of display output
    s_pad  = pad_with_spaces_dots('Symbol',         (first  - len('Symbol')),        'title')
    ch_pad = pad_with_spaces_dots('Change',         (second + third - len('Change')),'title')
    c_pad  = pad_with_spaces_dots('Current/Close',  (mid    - len('Current/Close')), 'title')
    h_pad  = pad_with_spaces_dots('High',           (mid    - len('High')),          'title')
    l_pad  = pad_with_spaces_dots('Low',            (mid    - len('Low')),           'title')
    o_pad  = pad_with_spaces_dots('Open',           (mid    - len('Open')),          'title')
    v_pad  = pad_with_spaces_dots('Volume',         (mid    - len('Volume')),        'title')
    cn_pad = pad_with_spaces_dots('Company Name',   (last   - len('Company Name')),  'title')

    # dashed_line_string is the 3rd row of display output
    dashed_line_string = create_dashed_line(first, second, third, mid, mid_num, last)

    ################################################################################################
    #
    # print 1st, 2nd, 3rd lines of display
    #
    ################################################################################################

    # print 1st line of display
    # display message is padded with spaces to be centered 
    if est_date == orig_est_date:
        print(" Date of Quote  : {}".format(est_date))
    else:
        print(" Date requested : {}".format(orig_est_date))
        print(" Date of Quote  : {}  (previous trading day)".format(est_date))

    print('\n')

    # print 2nd line of display
    print(" {}{}{}{}{}{}{}{}".format(s_pad, ch_pad, c_pad, h_pad, l_pad, o_pad, v_pad, cn_pad))

    # print 3rd line of display
    print(dashed_line_string)

    ################################################################################################
    #
    # Prepare the stock quote rows (stock ticker symbol) and all the attributes for display
    # - get length of all attributes for padding purposes
    # 
    ################################################################################################
    len_stock_symbol = len(symbol_list)

    # loop through symbol_list as it is in order of user input
    color_count = 0
    for i  in range(len(symbol_list)):

        ############################################################################################
        # preserve var symbol
        ############################################################################################
        symbol = symbol_list[i]

        ############################################################################################
        # assign a var for each attribute in quote dictionary
        ############################################################################################
        stock_symbol = symbol_list[i]
        stock_change_symbol  = quote[symbol]['change_symbol']
        stock_percent_change = quote[symbol]['percent_change']
        stock_close  = quote[symbol]['close']
        stock_high   = quote[symbol]['high']
        stock_low    = quote[symbol]['low']
        stock_open   = quote[symbol]['open']
        stock_volume = quote[symbol]['volume']

        ############################################################################################
        # check the length of company_name string
        # if company_name > last: truncate/slice company_name so the length of company_name == last
        ############################################################################################
        if len(quote[symbol]['company_name']) > last:
            #quote[symbol]['company_name'] = quote[symbol]['company_name'][:last]
            stock_company_name = quote[symbol]['company_name'][:last]

        ############################################################################################
        # check the length of company_name string
        # if company_name <= last: no need to truncate/slice company_name 
        ############################################################################################
        else:
            stock_company_name = quote[symbol]['company_name']

        ############################################################################################
        # need to add spaces padding to the variables for display because of colorama
        # colorama will add 13 bytes to original length
        #
        # get the length of each variable
        ############################################################################################
        stock_symbol_len           = first  - len(stock_symbol)
        stock_change_symbol_len    = second - len(quote[symbol]['change_symbol'])
        stock_percent_change_len   = third  - len(quote[symbol]['percent_change'])
        stock_close_len            = mid    - len(quote[symbol]['close'])
        stock_high_len             = mid    - len(quote[symbol]['high'])
        stock_low_len              = mid    - len(quote[symbol]['low'])
        stock_open_len             = mid    - len(quote[symbol]['open'])
        stock_volume_len           = mid    - len(quote[symbol]['volume'])
        stock_company_name_len     = last   - len(quote[symbol]['company_name'])

        ############################################################################################
        # add spaces or dots (padding) to each variable because of colorama
        ############################################################################################
        stock_symbol_pad         = pad_with_spaces_dots(stock_symbol, stock_symbol_len, 'dot')
        stock_change_symbol_pad  = pad_with_spaces_dots(stock_change_symbol, stock_change_symbol_len, 'space')
        stock_percent_change_pad = pad_with_spaces_dots(stock_percent_change, stock_percent_change_len, 'space_+_one')
        stock_close_pad          = pad_with_spaces_dots(stock_close, stock_close_len, 'dot')
        stock_high_pad           = pad_with_spaces_dots(stock_high, stock_high_len, 'dot')
        stock_low_pad            = pad_with_spaces_dots(stock_low, stock_low_len, 'dot')
        stock_open_pad           = pad_with_spaces_dots(stock_open, stock_open_len, 'dot')
        stock_volume_pad         = pad_with_spaces_dots(stock_volume, stock_volume_len, 'dot')
        stock_company_name_pad   = pad_with_spaces_dots(stock_company_name, stock_company_name_len, 'company')

        ############################################################################################
        # assign the colorama colors to text. Every other row with be a different color up to 4 rows
        # after 4 the color assignment will start again
        ############################################################################################
        if color_count == 0:
            TEXT_COLOR = Fore.YELLOW
            color_count += 1

        elif color_count == 1:
            TEXT_COLOR = Fore.CYAN
            color_count += 1

        elif color_count == 2:
            TEXT_COLOR = Fore.GREEN
            color_count += 1

        elif color_count == 3:
            TEXT_COLOR = Fore.WHITE
            color_count = 0

        # assign color to text
        stock_symbol         = (TEXT_COLOR + Style.BRIGHT + Back.BLACK + stock_symbol_pad         + Style.RESET_ALL)
        stock_percent_change = (TEXT_COLOR + Style.BRIGHT + Back.BLACK + stock_percent_change_pad + Style.RESET_ALL)
        stock_close          = (TEXT_COLOR + Style.BRIGHT + Back.BLACK + stock_close_pad          + Style.RESET_ALL)
        stock_high           = (TEXT_COLOR + Style.BRIGHT + Back.BLACK + stock_high_pad           + Style.RESET_ALL)
        stock_low            = (TEXT_COLOR + Style.BRIGHT + Back.BLACK + stock_low_pad            + Style.RESET_ALL)
        stock_open           = (TEXT_COLOR + Style.BRIGHT + Back.BLACK + stock_open_pad           + Style.RESET_ALL)
        stock_volume         = (TEXT_COLOR + Style.BRIGHT + Back.BLACK + stock_volume_pad         + Style.RESET_ALL)
        company_name         = (TEXT_COLOR + Style.BRIGHT + Back.BLACK + stock_company_name_pad   + Style.RESET_ALL)

        ############################################################################################
        # assign color to stock_change_symbol
        #
        # stock_change_symbol indicates whether stock price remained 'flat', went 'up', went 'down'
        # for change_status == 'flat'  the change_symbol value will be ' ' and color will be black
        # for change_status == 'up'    the change_symbol value will be '*' and color will be green
        # for change_status == 'down'  the change_symbol value will be '*' and color will be red
        ############################################################################################
        if quote[symbol]['change_status'] == 'flat':
            stock_change_symbol = (Fore.WHITE + Style.BRIGHT + Back.BLACK + stock_change_symbol_pad + Style.RESET_ALL)

        elif quote[symbol]['change_status'] == 'up':
            stock_change_symbol = (Fore.GREEN + Style.BRIGHT + Back.BLACK + stock_change_symbol_pad + Style.RESET_ALL)

        elif quote[symbol]['change_status'] == 'down':
            stock_change_symbol = (Fore.RED   + Style.BRIGHT + Back.BLACK + stock_change_symbol_pad + Style.RESET_ALL)

        elif quote[symbol]['change_status'] == 'UNKNOWN':
            stock_change_symbol = (Fore.RED   + Style.BRIGHT + Back.BLACK + stock_change_symbol_pad + Style.RESET_ALL)

        ############################################################################################
        # print row for stock_symbol and all attributes to be displayed
        ############################################################################################
        print(" {}{}{}{}{}{}{}{}{}".format(stock_symbol, \
                                           stock_change_symbol,  \
                                           stock_percent_change, \
        	                               stock_close,  \
        	                               stock_high,   \
                                           stock_low,    \
                                           stock_open,   \
                                           stock_volume, \
                                           company_name))

    print(dashed_line_string)

    # at time stock_percent_change will be assign NA%. Print a reason for user to understand
    print('\n')
    print(" NA% : if NA%  occurs then comparison data Not Available during query to Alpha Vantage url")
    print('\n')

# **** End of display_stock_quotes() **** #


def pad_with_spaces_dots(var, length, space_or_dot):


    # colorama seems to add 13 to the length of a variable.
    # var = the colorama encoded var
    # length = original length of var before colorama encoding
    #
    # pad var with len_var number of spaces or dots
    if space_or_dot == 'company':

        for i in range(length):
            if i == 0:
                var = var + ' '
            else:
                var = var + '.'

    elif space_or_dot == 'dot':

        for i in range(length+1):
            if i == 0:
                var = var + ' '
            elif i != length:
                var = var + '.'
            else:
                var = var + ' '

    elif space_or_dot == 'title' or space_or_dot == 'space_+_one':

        for i in range(length+1):
            var = var + ' '

    elif space_or_dot == 'space':

        for i in range(length):
            var = var + ' '

    return var

# **** End of pad_with_spaces_dots() **** #


def spin_colors():

    ############################################################################################
    # assign chars of the spin wheel
    ############################################################################################
    a = '-'
    b = '\\'
    c = '|'
    d = '/'

    dot1 = ''
    dot2 = ''
    dot3 = ''
    dot4 = ''

    for i in range(27):
        dot1 = dot1 + '.'
    for i in range(29):
        dot2 = dot2 + '.'
    for i in range(28):
        dot3 = dot3 + '.'
        dot4 = dot4 + '.'

    spin_a = "{}{}{}{}{}{}{}{}{}".format(a,dot1,a,dot2,a,dot3,a,dot4,a)
    spin_b = "{}{}{}{}{}{}{}{}{}".format(b,dot1,b,dot2,b,dot3,b,dot4,b)
    spin_c = "{}{}{}{}{}{}{}{}{}".format(c,dot1,c,dot2,c,dot3,c,dot4,c)
    spin_d = "{}{}{}{}{}{}{}{}{}".format(d,dot1,d,dot2,d,dot3,d,dot4,d)

    ############################################################################################
    # The spinning wheel will rotate/loop through 4 different colors
    # - CYAN, RED, GREEN, YELLOW
    # - Colorama will set the colors
    ############################################################################################
    color_count = 1
    while color_count != 5:

        if color_count == 1:
            TEXT_COLOR = Fore.CYAN
        elif color_count == 2:
            TEXT_COLOR = Fore.RED
        elif color_count == 3:
            TEXT_COLOR = Fore.GREEN
        elif color_count == 4:
            TEXT_COLOR = Fore.YELLOW

        spin1 = (TEXT_COLOR + Style.BRIGHT + spin_a + Style.RESET_ALL)
        spin2 = (TEXT_COLOR + Style.BRIGHT + spin_b + Style.RESET_ALL)
        spin3 = (TEXT_COLOR + Style.BRIGHT + spin_c + Style.RESET_ALL)
        spin4 = (TEXT_COLOR + Style.BRIGHT + spin_d + Style.RESET_ALL)

        if color_count == 1:
            spinner1 = [spin1, spin2, spin3, spin4]
        elif color_count == 2:
            spinner2 = [spin1, spin2, spin3, spin4]
        elif color_count == 3:
            spinner3 = [spin1, spin2, spin3, spin4]
        elif color_count == 4:
            spinner4 = [spin1, spin2, spin3, spin4]

        color_count += 1       

    return spinner1, spinner2, spinner3, spinner4

# **** End of function spin_colors() **** #


def spinning_wheel():

    ############################################################################################
    # spinning wheel to show activity instead of using time.sleep()
    #
    # spin_colors() will return lists and each list has spin wheel chars set to differnt color
    #
    ############################################################################################
    spinner1, spinner2, spinner3, spinner4 = spin_colors()

    spinner_count = 1

    # indent cursor 1 space
    sys.stdout.write(' ')
    sys.stdout.flush()

    count = 1
    while count != 241:

        ############################################################################################
        #
        # each color will cycle through the spinning wheel 10 times before switching to next color
        #
        ############################################################################################
        if spinner_count == 1:
            spinner = spinner1
        elif spinner_count == 11:
            spinner = spinner2
        elif spinner_count == 21:
            spinner = spinner3
        elif spinner_count == 31:
            spinner = spinner4
        elif spinner_count == 41:
            spinner_count = 1

        spinner_count += 1

        for i in range(len(spinner)):

            ############################################################################################
            # display each char on the spinner list
            ############################################################################################
            sys.stdout.write(spinner[i])   # write the next character
            sys.stdout.flush()             # flush stdout buffer (actual character display)
            time.sleep(0.001)              # sleep n seconds 1.0 = seconds, 0.1 milliseconds, 0.01 micro

            for i in range(117):
                sys.stdout.write('\b')     # erase the last written char

        count += 1

    # spinning wheel is done. need to enter one last back space to bring cursur to far left.
    sys.stdout.write('\b')

# **** End of function spinning_wheel() **** #
