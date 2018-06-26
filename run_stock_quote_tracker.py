import sys
from functions_stock_quote_tracker import *

# **** END OF IMPORTS **** #

def run_stock_quotes(av_url, av_function, av_api_key, symbol_list):

    ################################################################################
    #
    #     1. call welcome_to_stock_quotes_banner()
    #        - 2 carriage returns before and after banner display
    #        - call welcome_to_stock_quotes_banner()
    #
    ################################################################################
    clear_screen()
    welcome_to_stock_quotes_banner()
    continue_tracking = True

    ################################################################################
    #
    #     2. call what_symbols_to_track()
    #        - a symbol_list will be passed into main()
    #        - if len(symbol_list) == 0: call what_symbols_to_track()
    #            - user can enter infinite number of stock symbols to track
    #
    ################################################################################

    # if len(symbol_list) == 0: the symbol_list is empty
    #  - ask user if they want to track stock symbols or exit.
    #  - do_you_want_to_track_symbols() will return True or False
    #  - if answer == True user wants to continue; if False user wants to exit Stock Quoter
    #
    # if len(symbol_list) > 0: symbol_list has items and will pass through the try: except.
    if len(symbol_list) == 0:
        answer = do_you_want_to_track_symbols()

    # if answer == False, the user wants to exit.
    try:
        if not answer:
            continue_tracking = False
            return continue_tracking

        # call what_symbols_to_track()
        else:
            symbol_list = what_symbols_to_track(symbol_list)

    except:
        pass # do nothing

    # if above if statements are deleted go with original
    #if len(symbol_list) == 0:
        #symbol_list = what_symbols_to_track(symbol_list)

    ################################################################################
    #
    #     3. get est_date, est_time, est_day, holiday_result
    #
    #        Examples:
    #        - est_date = '2018-06-19'
    #        - est_time = (hour, minute) hour and minute are type int
    #        - est_day  = 'Tuesday'
    #        - holiday_result = ('is holiday', 'Independence Day')  if holiday
    #        - holiday_result = ('not holiday')  if not holiday
    #
    ################################################################################
    est_date = get_est_date()
    est_time = get_est_time()  # get_est_time will return tuple (hour, time)
    est_day  = get_est_day()
    holiday_result = is_US_holiday(est_date)

    # preserve est_date.
    # orig_est_date = est_date -> orig_est_date will be used in display_stock_quotes
    #                 if original est_date changes because of holidays, or weekend days
    orig_est_date = est_date

    ################################################################################
    #
    #     4. call get_display_message()
    #         - pass in est_time, est_day, holiday_result
    #         - will determine if orig_est_date is a day that the stock market is
    #            * open
    #            * closed (Holiday, Saturday, Sunday, or time of day when stock
    #              market is not open
    #         - will return a message with a string or a message with no string
    ################################################################################
    display_message = get_display_message(est_time, est_day, holiday_result)

    ################################################################################
    #
    #     5. call is_US_stock_exchange_open()
    #
    #            two def inside is_US_stock_exchange_open
    #            is_sat_or_sun()
    #                - NYSE and NASDAQ open Monday-Friday 9:30am and close 4:00pm
    #            is_holiday()
    #                - NYSE and NASDAQ recognise the same holidays
    #
    #  US Holidays:               Date                                     Date
    #  -------------------------|-------|--------------------------------|-------|
    #  New Years Day ........... (Jan 1)        Independence Day ........ (Jul 4)
    #  Martin Luther King Jr Day (-----)        Labor Day ............... (-----)
    #  Presidents Day .......... (-----)        Thanksgiving Day ........ (-----)
    #  Good Friday ............. (-----)        Christmas Day ........... (Dec 25)
    #  Memorial Day ............ (-----)
    #
    ################################################################################
    est_date = is_US_stock_exchange_open(est_date, est_time, est_day, holiday_result)

    ################################################################################
    # 
    #     6. PRINT HEADING OF PROGRESS BAR
    #        - a progress bar will be displayed to notify user of the stock query 
    #          progress
    #        - print the heading of the progress bar
    #        - create an instance of the class ProgressBar()
    #
    #        class ProgressBar() attributes are updated and evaluated during the 
    #        stock queries to determine progress of the queries.
    #
    ################################################################################
    progress_bar_scale()
    pb = ProgressBar(len(symbol_list))

    ################################################################################
    #
    #     7. GET STOCK QUOTE FOR TODAY or WHICHEVER DAY IS CURRENT 
    #        (WHICHEVER DAY IS CURRENT - in case of Holiday or weekend day)
    #
    #        - assign alpha_vantage_url, alpha_vantage_function
    #        - alpha_vantage_url = "https://www.alphavantage.co/query"
    #        - alpha_vantage_function = "TIME_SERIES_DAILY"
    #        - call get_alpha_vantage_api_key() to get the Alpha Vantage api_key
    #
    #        call get_stock_quotes()
    #        - api calls to Alpha Vantage to get stock quotes
    #        - get_stock_quotes() will return a dictionary. Format:
    #        - {'MSFT':{'open': <value>,
    #                   'high': <value>,
    #                   'low': <value>,
    #                   'close': <value>,
    #                   'volume': <value>},
    #             'DIS':{'open': <value>,
    #                   'high': <value>,
    #                   'low': <value>,
    #                   'close': <value>,
    #                   'volume': <value>}}
    #
    #      Note: Progress Bar will be displayed as each symbol query completes
    #            pb = ProgressBar() will keep track of query progress by using 
    #                 class ProgressBar()
    #
    ################################################################################
    quote = get_stock_quotes(av_url, av_function, av_api_key, est_date, symbol_list, pb)

    ################################################################################
    #
    #     8. GET STOCK QUOTE FOR PREVIOUS TRADING DAY
    #
    ################################################################################

    # step1
    previous_weekday_date_name = find_previous_weekday(est_date, est_day)
    previous_weekday_date = previous_weekday_date_name[0]
    previous_weekday_name = previous_weekday_date_name[1]

    # step2
    holiday_result = is_US_holiday(previous_weekday_date)

    # step3
    previous_weekday_name = get_weekday_name(previous_weekday_date)

    # step4
    #
    # actual time is not needed on the call to previous_weekday_date(), but time needs
    # to be passed as a parameter and time needs to be a time of day when the stock market
    # is trading.
    #
    # fake_time is set to a time of day when the stock market is open and trading
    # this is needed in order to get the immediate previous trading day
    #
    # a time before 9:30am would force is_US_stock_exchange_open() to go for the next previous trading day
    fake_time = (11, 30)

    # step5
    previous_weekday_date = is_US_stock_exchange_open(previous_weekday_date, fake_time, previous_weekday_name, holiday_result)

    previous_quote = get_stock_quotes(av_url, av_function, av_api_key, previous_weekday_date, symbol_list, pb)

    ################################################################################
    #
    #     9. ASSIGN pb.query_complete = 0
    #        - need to assign to 0 now that all queries are complete
    #        - this will allow Progress Bar to start at 0% for the next "new" set of
    #          stock queries. 
    #
    ################################################################################
    pb.query_complete = 0

    ################################################################################
    #
    #     10. IS QUOTE UP or DOWN
    #        - compare current trading day stock quote to previous trading day quote 
    #
    ################################################################################
    quote = is_quote_up_or_down(quote, previous_quote, symbol_list)

    ################################################################################
    #
    #     11. call display_stock_quotes()
    #         - before calling display_stock_quotes()
    #         - call clear_screen()
    #         - call stock_quotes_available_banner()
    #
    ################################################################################
    clear_screen()
    stock_quotes_available_banner(display_message)
    display_stock_quotes(est_date, orig_est_date, symbol_list, quote)

    return continue_tracking

# **** End of run_stock_quotes() **** #


class ProgressBar():

    ################################################################################
    # class ProgressBar(): designed to measure the progress of stock quote queries
    #
    # There will be 2 types of queries performed when getting stock quotes. 
    #    1. current_day  quote query 
    #    2. previous_day quote query
    #
    # def __init__() will assign the length of the symbol_list * 2 (1 for each type 
    # of query)
    #
    # length will be used to track the completion of each query (1 for each item in
    # symbol_list)
    ################################################################################

    def __init__(self, symbol_list_length):

        self.symbol_list_length = symbol_list_length * 2    # 2 queries performed against symbol_list
        self.query_complete = 0
        self.display_width  = 95   # number of characters in each row of display
        self.progress_units = int(self.display_width / self.symbol_list_length)

    # **** End of ProgressBar.__init__()

# **** End of class ProgressBar() **** #
