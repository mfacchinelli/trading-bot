import sys, getopt

from botchart import BotChart
from botstrategy import BotStrategy

def main(argv):
	chart = BotChart("poloniex","BTC_LTC",300)

	strategy = BotStrategy()

	for candlestick in chart.getPoints():
		strategy.tick(candlestick)

	netProfit = sum(strategy.profit)

	color = "\033[91m" # define color as red
	if (netProfit > 0):
		color = "\033[92m" # change color if positive profit
		

	strategy.output.log("Net profit: "+color+str(netProfit)+"\033[0m")

if __name__ == "__main__":
	main(sys.argv[1:])