from robinhood_crypto_api import RobinhoodCrypto
from login import *
import time

# TODO convert to OOP
# TOOD change the while True to break loop when certain time hits
def autotrader(robinhood_client):
	amount_to_spend = 1000
	upper_percentage = 1.0
	try:
		robinhood_client = login()
	except:
		raise LoginException()

	trade_history = robinhood_client.trade_history()
	if bitcoin_holdings(robinhood_client) > 0:
		# pulls most recent trade which would be the last buy order
		market_buy = trade_history['results'][0]
	else:
		# since there is no holdings buy more BTC
		print('BUY')
		bitcoin_quantity = calculate_buy_quantity(robinhood_client,amount_to_spend)
		market_buy = buy_bitcoin(robinhood_client, bitcoin_quantity)

	#TODO have it return price or some other metric when it does not sell
	while True:
		percentage_yield = calculate_percent_yield(robinhood_client)
		while percentage_yield < upper_percentage:
			print('DONT SELL')
			time.sleep(60)
			percentage_yield = round(calculate_percent_yield(robinhood_client),0)
		market_sell = sell_all_bitcoin(robinhood_client)
		print('SELL')
		# delete this once done testing
		break
		# wait until BTC drops in price then make a buy order
		while calculate_percent_change_from_original(robinhood_client, market_sell['id']) > 0:
			print('DONT BUY')
			time.sleep(60)
		bitcoin_quantity = calculate_buy_quantity(robinhood_client,amount_to_spend)
		market_buy = buy_bitcoin(robinhood_client, bitcoin_quantity)
		print('BUY')

def login():
	return RobinhoodCrypto(username, password)

def bitcoin_holdings(robinhood_client):
	holdings_info = robinhood_client.holdings()
	for asset in holdings_info:
		for cost_base in asset['cost_bases']:
			if cost_base['currency_id'] == '1072fc76-1862-41ab-82c2-485837590762':
				quantity = cost_base['direct_quantity']
	return float(quantity)
# Returns the percent of change from the previous buy order_id compared to the current price
def calculate_percent_change_from_original(robinhood_client, order_id):
	quote_info = robinhood_client.quotes()
	current_price = round(float(quote_info['mark_price']) * 1.005, 2)
	trade_history = robinhood_client.trade_history()['results']
	for trade in trade_history:
		if trade['id'] == order_id:
			previous_price = round(float(trade['price']),2)
	return previous_price/current_price*100-100


# Returns quatity of bitcoin to buy. Done in cents only works with a min amount of 1.50
# TODO fix this later to work with lower denominations
def calculate_buy_quantity(robinhood_client, amount_to_spend):
	quote_info = robinhood_client.quotes()
	price = round(float(quote_info['mark_price']) * 1.005, 2)
	quantity = amount_to_spend/(price*100)
	return str(round(quantity, 8))


# Returns percentage yield from captial investment
# TODO find bug where it might be using LTC
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
# TODO do not return until it is sold
# TODO test if it works
def sell_all_bitcoin(robinhood_client):
	quote_info = robinhood_client.quotes()
	quote_price = round(float(quote_info['bid_price']), 2)
	holdings_info = robinhood_client.holdings()
	for asset in holdings_info:
		for cost_base in asset['cost_bases']:
			if cost_base['currency_id'] == '1072fc76-1862-41ab-82c2-485837590762':
				quantity = cost_base['direct_quantity']
	market_order_info = robinhood_client.trade(
	    'BTCUSD',
	    price=quote_price,
	    quantity=quantity,
	    side="sell",
	    time_in_force="gtc",
	    type="market"
	)
	return market_order_info
	
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
	return market_order_info


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
	while robinhood_client.order_status(order_id)['state'] != 'filled':
		time.sleep(5)
	return market_order_info


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

