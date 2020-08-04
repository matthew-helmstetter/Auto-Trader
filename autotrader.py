from robinhood_crypto_api import RobinhoodCrypto
from login import *
import time

# TODO convert to OOP
def main ():
	try:
		robinhood_client = login()
	except:
		raise LoginException()
	amount_to_spend = 10
	upper_percentage = 1.0
	bitcoin_quantity = calculate_buy_quantity(robinhood_client,amount_to_spend)
	# sell_profit = calculate_sell_profit(robinhood_client)
	percentage_yield = round(calculate_percent_yield(robinhood_client)*100,0)
	counter = 0
	while percentage_yield < upper_percentage and counter < 5:
		print('still not true')
		counter += 1
		time.sleep(5)


def login():
	return RobinhoodCrypto(username, password)

# Returns quatity of bitcoin to buy. Done in cents only works with a min amount of 1.50
# TODO fix this later to work with lower denominations
def calculate_buy_quantity(robinhood_client, amount_to_spend):
	quote_info = robinhood_client.quotes()
	price = round(float(quote_info['mark_price']) * 1.005, 2)
	quantity = amount_to_spend/(price*100)
	return str(round(quantity, 8))

# Finds BTC then calculates total yield if sold
# TODO might not need this function, since calculate_percent_yield does this for us
# def calculate_sell_profit(robinhood_client):
# 	quote_info = robinhood_client.quotes()
# 	quote_price = round(float(quote_info['bid_price']), 2)
# 	holdings_info = robinhood_client.holdings()
# 	for asset in holdings_info:
# 		for cost_base in asset['cost_bases']:
# 			if cost_base['currency_id'] == '1072fc76-1862-41ab-82c2-485837590762':
# 				quantity = cost_base['direct_quantity']
# 				capital = cost_base['direct_cost_basis']
# 	return quote_price*float(quantity) - float(capital)

# Returns percentage yield from captial investment
# TODO make more efficient
def calculate_percent_yield(robinhood_client):
	quote_info = robinhood_client.quotes()
	quote_price = round(float(quote_info['bid_price']), 2)
	holdings_info = robinhood_client.holdings()
	for asset in holdings_info:
		for cost_base in asset['cost_bases']:
			if cost_base['currency_id'] == '1072fc76-1862-41ab-82c2-485837590762':
				quantity = cost_base['direct_quantity']
				capital = cost_base['direct_cost_basis']
	return calculate_sell_profit(robinhood_client)/float(capital) * 100

# TODO throw error if there is no BTC
def sell_all_bitcoin(robinhood_client):
	quote_info = robinhood_client.quotes()
	quote_price = round(float(quote_info['bid_price']), 2)
	holdings_info = robinhood_client.holdings()
	for asset in holdings_info:
		for cost_base in asset['cost_bases']:
			if cost_base['currency_id'] == '1072fc76-1862-41ab-82c2-485837590762':
				quantity = cost_base['direct_quantity']
	return quantity
	# market_order_info = robinhood_client.trade(
	#     'BTCUSD',
	#     price=quote_price,
	#     quantity=quantity,
	#     side="sell",
	#     time_in_force="gtc",
	#     type="market"
	# )
	
# Function used to sell set amount of bitcoin
def sell_bitcoin(robinhood_client, quantity):
	quote_info = robinhood_client.quotes()
	quote_price = round(float(quote_info['bid_price']), 2)
	market_order_info = robinhood_client.trade(
	    'BTCUSD',
	    price=quote_price,
	    quantity=quantity,
	    side="sell",
	    time_in_force="gtc",
	    type="market"
	)


# buy BTC but do not return true until it has actually bought
def buy_bitcoin(robinhood_client, quantity):
	quote_info = robinhood_client.quotes()
	pre_holdings_trade_count = len(robinhood_client.trade_history()['results'])
	market_order_info = robinhood_client.trade(
	    'BTCUSD',
	    price=round(float(quote_info['mark_price']) * 1.005, 2),
	    quantity=str(quantity),
	    side="buy",
	    time_in_force="gtc",
	    type="market"
	)
	while pre_holdings_trade_count == post_holdings_trade_count:
		post_holdings_trade_count = len(robinhood_client.trade_history()['results'])
		time.sleep(2)
	return market_order_info


def test_buy_bitcoin(robinhood_client):
	robinhood_client = login()
	quantity = calculate_buy_quantity(robinhood_client, 150)


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

