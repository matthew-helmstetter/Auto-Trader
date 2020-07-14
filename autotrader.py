from robinhood_crypto_api import RobinhoodCrypto
from login import *
class AutoTraderException(Exception):
    pass
class LoginException (AutoTraderException):
	pass

def main ():
	try:
		robinhood_client = RobinhoodCrypto(username, password)
	except:
		raise LoginException()
	amount_to_spend = 10
	bitcoin_quantity = calculate_ten_dollars(robinhood_client,amount_to_spend)


def calculate_ten_dollars(client, amount_to_spend):
	quote_info = client.quotes()
	price = round(float(quote_info['mark_price']) * 1.005, 2)
	quantity = amount_to_spend/price
	return quantity

# market_order_info = r.trade(
#     'BTCUSD',
#     price=round(float(quote_info['mark_price']) * 1.005, 2),
#     quantity="0.00005",
#     side="buy",
#     time_in_force="gtc",
#     type="market"
# )
# order_id = market_order_info['id']
# print('market order {} status: {}'.format(order_id, r.order_status(order_id)))

