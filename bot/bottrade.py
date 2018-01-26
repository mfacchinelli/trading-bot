from botlog import BotLog
from botconstants import openLabel, closedLabel, overCoefficient, underCoefficient, investment, commission, green, red, white

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

		profit = commission * investment * ( self.exitPrice - self.entryPrice )
		tradeStatus = tradeStatus + str( profit ) + white 

		self.output.log( tradeStatus )
		return profit