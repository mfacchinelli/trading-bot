from botlog import BotLog

# Labels
openLabel = "OPEN"
closedLabel = "CLOSED"

# Overbuying and underselling coefficients
epsilon = 0.001
overCoefficient = float( 1 ) + epsilon
underCoefficient = float( 1 ) - epsilon

class BotTrade( object ):
	def __init__( self, currentPrice, stopLoss ):
		self.output = BotLog( )
		self.status = openLabel
		self.entryPrice = overCoefficient * currentPrice
		self.exitPrice = float( 0 )
		self.output.log( "Trade opened" )
		self.stopLoss = stopLoss
	
	def close( self, currentPrice ):
		self.status = closedLabel
		self.exitPrice = underCoefficient * currentPrice
		self.output.log( "Trade closed" )

	def tick( self, currentPrice ):
		if ( currentPrice < self.stopLoss ):
			self.close( currentPrice )

	def showTrade( self ):
		tradeStatus = "Entry Price: " + str( self.entryPrice ) + " Status: " + str( self.status )
		profit = float( 0 )

		if ( self.status == closedLabel ):
			tradeStatus = tradeStatus + " Exit Price: " + str( self.exitPrice ) + " Profit: "
			if ( self.exitPrice > self.entryPrice ):
				tradeStatus = tradeStatus + "\033[92m"
			else:
				tradeStatus = tradeStatus + "\033[91m"

			profit = self.exitPrice - self.entryPrice
			tradeStatus = tradeStatus + str( profit ) + "\033[0m"

		self.output.log( tradeStatus )
		return profit