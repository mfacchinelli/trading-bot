from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade

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
		self.output.log( "Price: " + str( candlestick.priceAverage ) + "\tMoving Average: " + str( average ) )

		self.evaluatePositions( )
		self.updateOpenTrades( )
		self.profit.append( sum( self.showPositions( ) ) )

	def evaluatePositions( self ):
		openTrades = []
		for trade in self.trades:
			if ( trade.status == "OPEN" ):
				openTrades.append( trade )

		if ( len( openTrades ) < self.numSimulTrades ):
			if ( self.currentPrice < self.indicators.movingAverage( self.prices, 15 ) ):
				self.trades.append( BotTrade( self.currentPrice, self.stopLoss ) )

		for trade in openTrades:
			if ( self.currentPrice > self.indicators.movingAverage( self.prices, 15 ) and trade.entryPrice < self.currentPrice ):
				trade.close( self.currentPrice )

	def updateOpenTrades( self ):
		for trade in self.trades:
			if ( trade.status == "OPEN" ):
				trade.tick( self.currentPrice )

	def showPositions( self ):
		profitList = []
		for trade in self.trades:
			profitList.append( trade.showTrade( ) )
		return profitList