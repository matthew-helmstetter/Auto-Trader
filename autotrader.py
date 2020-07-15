from robinhood_crypto_api import RobinhoodCrypto
from login import *
def main ():
	try:
		robinhood_client = RobinhoodCrypto(username, password)
	except:
		raise LoginException()
	amount_to_spend = 10
	bitcoin_quantity = calculate_buy_quantity(robinhood_client,amount_to_spend)


def calculate_buy_quantity(robinhood_client, amount_to_spend):
	quote_info = robinhood_client.quotes()
	price = round(float(quote_info['ask_price']), 2)
	quantity = amount_to_spend/price
	return quantity

# you just need to know how much yield and then decide to sell
def calculate_sell_profit(robinhood_client, bitcoin_quantity):
	quote_info = robinhood_client.quotes()
	quote_price = round(float(quote_info['bid_price']), 2)
	holdings_info = robinhood_client.holdings()
	for asset in holdings_info:
		for cost_base in asset['cost_bases']:
			if cost_base['currency_id'] == '1072fc76-1862-41ab-82c2-485837590762':
				test
	return price
quantity*sell = amount

# if bought below ask_price won't sell instantly
# quote_info = robinhood_client.quotes()
# market_order_info = robinhood_client.trade(
#     'BTCUSD',
#     price=round(float(quote_info['bid_price']), 2),
#     quantity="0.00005",
#     side="buy",
#     time_in_force="gtc",
#     type="market"
# )
# order_id = market_order_info['id']
# print('market order {} status: {}'.format(order_id, robinhood_client.order_status(order_id)))

