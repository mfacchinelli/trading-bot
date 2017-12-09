from poloniex import poloniex
import urllib, json
import pprint
from botcandlestick import BotCandlestick

allowed = [ 300, 900, 1800, 7200, 14400, 86400 ]

class BotChart( object ):
	def __init__( self, exchange, pair, period, backtest = True ):
		self.pair = pair
		if ( int( period ) in allowed ):
			self.period = period
		else:
			print 'Periods should be in 300, 900, 1800, 7200, 14400, or 86400 second increments'
			sys.exit(2)

		self.startTime = 1512086400
		self.endTime = self.startTime + 7 * 86400

		self.data = []
		
		if ( exchange == "poloniex" ):
			self.conn = poloniex( 'I53E06MT-G40PI4S0-9ITBOEH8-HMMF10OA', 
				'b3b9a8fbdbfdf26d9bc7a2915cc39f62404a6ed2a2fce3f1867234342388e2f3783c3631c7de375b6d76e751f83eef7f901315b7af3e9474f294dc07d8cf767e' )

			if backtest:
				poloData = self.conn.api_query( "returnChartData" , {"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})
				for datum in poloData:
					if ( datum['open'] and datum['close'] and datum['high'] and datum['low'] ):
						self.data.append( BotCandlestick( self.period, datum['open'], datum['close'], 
							datum['high'], datum['low'], datum['weightedAverage'] ) )

		if ( exchange == "bittrex" ):
			if backtest:
				url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=" + self.pair + "&tickInterval=" + \
				+ self.period + "&_=" + str(self.startTime)
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
