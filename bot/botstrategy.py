from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade

# Labels
openLabel = "OPEN"
closedLabel = "CLOSED"

# Profit margin for sell
profitMargin = 1.01

class BotStrategy( object ):
	def __init__( self ):
		self.output = BotLog( )
		self.prices = [ ]
		self.closes = [ ] # needed for momentum indicator
		self.trades = [ ]
		self.profit = [ ]
		self.stopLoss = 1e-5
		self.currentPrice = ""
		self.currentClose = ""
		self.numSimulTrades = 5
		self.indicators = BotIndicators( )

	def tick( self, candlestick ):
		self.currentPrice = float( candlestick.priceAverage )
		self.prices.append( self.currentPrice )
		# self.currentClose = float( candlestick['close'] )
		# self.closes.append( self.currentClose )

		average = self.indicators.movingAverage( self.prices, 15 )
		if ( average is None ):
			average = 0

		message = "Price: %.3f \tMoving Average: %.3f" % ( candlestick.priceAverage, average )
		self.output.log( "Price: " + str( candlestick.priceAverage ) + "\tMoving Average: " +  str( average ) )

		self.evaluatePositions( )
		self.profit.append( sum( self.updateTrades( ) ) )

	def evaluatePositions( self ):
		openTrades = []
		for trade in self.trades:
			if ( trade.status == openLabel ):
				openTrades.append( trade )

		if ( len( openTrades ) < self.numSimulTrades ):
			if ( self.currentPrice < self.indicators.movingAverage( self.prices, 15 ) ):
				self.trades.append( BotTrade( self.currentPrice, self.stopLoss ) )

		for trade in openTrades:
			if ( self.currentPrice > self.indicators.movingAverage( self.prices, 15 ) and profitMargin * trade.entryPrice < self.currentPrice ):
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
