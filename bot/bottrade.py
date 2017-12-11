from botlog import BotLog

# Labels
openLabel = "OPEN"
closedLabel = "CLOSED"

# Overbuying and underselling coefficients
epsilon = 0.001
overCoefficient = float( 1 ) + epsilon
underCoefficient = float( 1 ) - epsilon

# Trading commission
commission = 0.995

# Colors
green = "\033[92m"
red = "\033[91m"
white = "\033[0m"

class BotTrade( object ):
	def __init__( self, currentPrice, stopLoss ):
		self.output = BotLog( )
		self.status = openLabel
		self.entryPrice = overCoefficient * currentPrice
		self.exitPrice = float( 0 )
		self.output.log( green + "Trade opened" + white )
		self.stopLoss = stopLoss
	
	def close( self, currentPrice ):
		self.status = closedLabel
		self.exitPrice = underCoefficient * currentPrice
		self.output.log( red + "Trade closed" + white )

	def tick( self, currentPrice ):
		if ( currentPrice < ( self.stopLoss * self.entryPrice ) ):
			self.close( currentPrice )

	def showTrade( self ):
		tradeStatus = "Entry Price: " + str( self.entryPrice ) + " Status: " + str( self.status )

		tradeStatus = tradeStatus + " Exit Price: " + str( self.exitPrice ) + " Profit: "
		if ( self.exitPrice > self.entryPrice ):
			tradeStatus = tradeStatus + green
		else:
			tradeStatus = tradeStatus + red

		profit = commission * ( self.exitPrice - self.entryPrice )
		tradeStatus = tradeStatus + str( profit ) + white 

		self.output.log( tradeStatus )
		return profit