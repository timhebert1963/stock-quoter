# stock-quoter

outputs latest stock quotes for stock symbols provided

Stock Quoter was developed and tested on Windows 8.1 and not tested on other Windows, Linux, etc. OS.

Stock Quote Tracker will get latest trading price for stock symbols provided in the 
symbol_list1 and symbols_list2 lists.

1. If the current day is a weekend or holdiay, the previous trading day data will be collected and displayed.
2. The latest data will be compared to previous latest data for each stock symbol and the percent change + or - 
   wil be calculated and dispayed

Again, this was developed and tested on Windows 8.1 and not tested on other Windows, Linux, etc. OS.

The following packages need a pip install. Please visit url for any special instructions
 - colorama - https://pypi.org/project/colorama/
 - holidays - https://pypi.org/project/holidays/

Real time stock quotes are obtained (get requests) from the Alpha Vantage api.

Alpha Vantage
#############

An Alpha Vantage api_key is mandatory to run this script. You can obtain an api_key for free from
https://www.alphavantage.co/

After you obtain the api_key, create a text file named: alpha_vantage_api_key.txt 
Cut and paste the 3 lines below and replace <your api_key number> with the api_key number you obtained from Alpha 
Vantage. If you use the 3 lines below it will just work.

   3 lines of your .txt file are as follows
   ----------------------------------------
   Alpha Vantage is a realtime Stock quote
   Alpha Vantage apikey = <your api_key number>
   <your api_key number>


Next: you will need to provide the path to the alpha_vantage_api_key.txt.
Example: av_path = 'c:\\users\\bla\\python scripts\\Alpha Vantage APIKEY\\alpha_vantage_api_key.txt'
