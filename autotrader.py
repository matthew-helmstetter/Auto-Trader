from robinhood_crypto_api import RobinhoodCrypto
from login import *
import time

# TODO convert to OOP
# TOOD implement trading
def autotrader():
	try:
		robinhood_client = login()
	except:
		raise LoginException()
	amount_to_spend = 10
	upper_percentage = 1.0
	bitcoin_quantity = calculate_buy_quantity(robinhood_client,amount_to_spend)
	percentage_yield = round(calculate_percent_yield(robinhood_client)*100,0)
	counter = 0
	while percentage_yield < upper_percentage and counter < 5:
		time.sleep(5)
		print('False')
		percentage_yield = round(calculate_percent_yield(robinhood_client)*100,0)

def login():
	return RobinhoodCrypto(username, password)

# This will calculate the cost at which the original purchase of BTC was
# It will be used to help determine when to buy next
# TODO get the original buy amount
def calculate_percent_change_from_original(robinhood_client):
	quote_info = robinhood_client.quotes()
	# quote_price = round(float(quote_info['bid_price']), 2)
	# holdings_info = robinhood_client.holdings()
	# for asset in holdings_info:
	# 	for cost_base in asset['cost_bases']:
	# 		if cost_base['currency_id'] == '1072fc76-1862-41ab-82c2-485837590762':
	# 			quantity = cost_base['direct_quantity']
	# 			capital = cost_base['direct_cost_basis']
	# return (quote_price*float(quantity) - float(capital))/float(capital) * 100


# Returns quatity of bitcoin to buy. Done in cents only works with a min amount of 1.50
# TODO fix this later to work with lower denominations
def calculate_buy_quantity(robinhood_client, amount_to_spend):
	quote_info = robinhood_client.quotes()
	price = round(float(quote_info['mark_price']) * 1.005, 2)
	quantity = amount_to_spend/(price*100)
	return str(round(quantity, 8))


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
	return (quote_price*float(quantity) - float(capital))/float(capital) * 100

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
	market_order_info = robinhood_client.trade(
	    'BTCUSD',
	    price=round(float(quote_info['mark_price']) * 1.005, 2),
	    quantity=str(quantity),
	    side="buy",
	    time_in_force="gtc",
	    type="market"
	)
	order_id = market_order_info['id']
	while robinhood_client.order_status('4d4014c9-e0df-4ea1-b1a2-6e71233ea3a2') != 'filled':
		time.sleep(5)
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

