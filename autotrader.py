from Robinhood import Robinhood
from login import *
robinhood_client = Robinhood()
print(robinhood_client.login(username=username, password=password,qr_code=qr_code))
# stock_instrument = robinhood_client.instruments('MSFT')[0]

# # Get a stock's quote
# stock_quote = robinhood_client.quote_data('MSFT')

# # Market price
# print(stock_quote['last_trade_price'])