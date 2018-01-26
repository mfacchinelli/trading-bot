import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy
from botconstants import exchange, green, red, white

def main( argv ):
	if exchange is "poloniex":
		chart = BotChart( "BTC_EMC2", 300 )
	elif exchange is "bittrex":
		chart = BotChart( "BTC-ADA", "fiveMin" )

	strategy = BotStrategy( )

	for candlestick in chart.getPoints( ):
		strategy.tick( candlestick )

	netProfit = sum( strategy.profit )

	color = red # define color as red
	if ( netProfit >= 0 ):
		color = green # change color if positive profit
		
	strategy.output.log( "Net profit: " + color + str( netProfit ) + white )

	print "Terminated."

if __name__ == "__main__":
	main( sys.argv[1:] )