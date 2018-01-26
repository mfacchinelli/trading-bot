# Allowed values
allowed = [ 300, 900, 1800, 7200, 14400, 86400 ]

# File name for API
fileName = "credentials.txt"

# Labels
openLabel = "OPEN"
closedLabel = "CLOSED"

# Moving average
movingAveragePeriod = 10

# Buying and selling
exchange = "bittrex"
investment = 1e3 # amount of ALTCOIN to invest
epsilon = 0.001
overCoefficient = float( 1 ) + epsilon
underCoefficient = float( 1 ) - epsilon
profitMargin = 1.1
stopLoss = 0.1

# Trading commission
commission = 0.995

# Colors
green = "\033[92m"
red = "\033[91m"
white = "\033[0m"