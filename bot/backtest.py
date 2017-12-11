import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy

# Colors
green = "\033[92m"
red = "\033[91m"
white = "\033[0m"

def main( argv ):
	chart = BotChart( "poloniex", "BTC_EMC2", 300 )

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