from poloniex import poloniex
import urllib, json
import pprint
from botcandlestick import BotCandlestick
from botconstants import exchange, allowed, fileName

class BotChart( object ):
	def __init__( self, pair, period, backtest = True ):
		self.pair = pair
		if exchange is "poloniex":
			if ( int( period ) in allowed ):
				self.period = period
			else:
				print 'Periods should be in 300, 900, 1800, 7200, 14400, or 86400 second increments'
				sys.exit(2)
		elif exchange is "bittrex":
			self.period = period

		self.startTime = 1512086400 + 0 * 86400 # start date is December 1st 2017
		self.endTime = self.startTime + 1 * 86400

		self.data = []
		
		if ( exchange == "poloniex" ):
			# Get credentials
			fileObject = open( fileName, 'r' )
			content = fileObject.readlines()
			key = content[0]
			code = content[1]
			fileObject.close()

			# API
			self.conn = poloniex( key, code )

			if backtest:
				poloData = self.conn.api_query( "returnChartData" , {"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
				for datum in poloData:
					if ( datum['open'] and datum['close'] and datum['high'] and datum['low'] ):
						self.data.append( BotCandlestick( self.period, datum['open'], datum['close'], 
							datum['high'], datum['low'], datum['weightedAverage'] ) )

		if ( exchange == "bittrex" ):
			if backtest:
				url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=" + self.pair + "&tickInterval=" + \
					self.period + "&_=" + str( self.startTime )
				response = urllib.urlopen( url )
				rawdata = json.loads( response.read( ) )

				self.data = rawdata["result"]

	def getPoints( self ):
		return self.data

	def getCurrentPrice( self ):
		currentValues = self.conn.api_query( "returnTicker" )
		lastPairPrice = {}
		lastPairPrice = currentValues[self.pair]["last"]
		return lastPairPrice
