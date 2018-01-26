import numpy

class BotIndicators( object ):
	def __init__( self ):
		 pass

	def movingAverage( self, dataPoints, period ):
		if ( len( dataPoints ) > 1 ):
			return sum( dataPoints[-period:] ) / float( len( dataPoints[-period:] ) )

	def exponentialMovingAverage( self, dataPoints, period ):
		x = numpy.asarray( dataPoints )
		weights = None
		weights = numpy.exp( numpy.linspace( -1., 0., period ) )
		weights /= weights.sum( )

		a = numpy.convolve( x, weights, mode = 'full' )[:len( x )]
		a[:period] = a[period]
		return a

	def movingAverageConvergenceDivergence( self, dataPoints, nslow = 26, nfast = 12 ):
		emaslow = self.exponentialMovingAverage( dataPoints, nslow )
		emafast = self.exponentialMovingAverage( dataPoints, nfast )
		return emaslow, emafast, emafast - emaslow		

	def momentum( self, dataPoints, period = 14 ):
		if ( len( dataPoints ) > period - 1 ):
			return dataPoints[-1] * 100 / dataPoints[-period]

	def relativeStrangthIndex( self, dataPoints, period = 14 ):
		deltas = np.diff( dataPoints )
		seed = deltas[:period+1]
		up = seed[seed >= 0].sum( ) / period
		down = -seed[seed < 0].sum( ) / period
		rs = up / down
		rsi = np.zeros_like( dataPoints )
		rsi[:period] = 100. - 100./( 1. + rs )
 
		for i in range( period, len( dataPoints ) ):
 			delta = deltas[i - 1]  # cause the diff is 1 shorter
  			if delta > 0:
 				upval = delta
 				downval = 0.
 			else:
 				upval = 0.
 				downval = -delta
 
 			up = ( up * ( period - 1 ) + upval ) / period
 			down = ( down * ( period - 1 ) + downval ) / period
  			rs = up/down
 			rsi[i] = 100. - 100. / ( 1. + rs )
  		if len( dataPoints ) > period:
 			return rsi[-1]
 		else:
 			return 50 # output a neutral amount until enough data points in list to calculate RSI
