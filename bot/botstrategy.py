from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
from botconstants import exchange, openLabel, closedLabel, movingAveragePeriod, profitMargin, stopLoss

class BotStrategy( object ):
	def __init__( self ):
		self.output = BotLog( )
		self.prices = [ ]
		self.closes = [ ] # needed for momentum indicator
		self.trades = [ ]
		self.profit = [ ]
		self.currentPrice = ""
		self.currentClose = ""
		self.numSimulTrades = 5
		self.indicators = BotIndicators( )

	def tick( self, candlestick ):
		if exchange is "poloneix":
			self.currentPrice = float( candlestick.priceAverage )
		elif exchange is "bittrex":
			self.currentPrice = float( candlestick["C"] )
		self.prices.append( self.currentPrice )
		# self.currentClose = float( candlestick['close'] )
		# self.closes.append( self.currentClose )

		average = self.indicators.movingAverage( self.prices, movingAveragePeriod )
		if ( average is None ):
			average = 0
		if ( len( self.prices ) > 2 * movingAveragePeriod ):
			self.indicators.movingAverageConvergenceDivergence( self.prices, 2 * movingAveragePeriod, movingAveragePeriod )

		message = "Price: %.3e \tMoving Average: %.3e" % ( self.currentPrice, average )
		self.output.log( message )

		self.evaluatePositions( )
		self.profit.append( sum( self.updateTrades( ) ) )

	def evaluatePositions( self ):
		openTrades = []
		for trade in self.trades:
			if ( trade.status == openLabel ):
				openTrades.append( trade )

		if ( len( openTrades ) < self.numSimulTrades ):
			if ( self.currentPrice < self.indicators.movingAverage( self.prices, movingAveragePeriod ) ):
				self.trades.append( BotTrade( self.currentPrice, stopLoss ) )

		for trade in openTrades:
			if ( self.currentPrice > self.indicators.movingAverage( self.prices, movingAveragePeriod ) and profitMargin * trade.entryPrice < self.currentPrice ):
				trade.close( self.currentPrice )			

	def updateTrades( self ):
		i = 0
		profitList = []
		for trade in self.trades:
			if ( trade.status == openLabel ):
				trade.tick( self.currentPrice )
			elif ( trade.status == closedLabel ):
				profitList.append( trade.showTrade( ) )
				del self.trades[i]
			i += 1
		
		return profitList
