from AlgorithmImports import *
from datetime import timedelta


class TOWMhandlingData(QCAlgorithm):

    def Initialize(self):
        """The Initialize method is the entry point of your algorithm where you define a series
        of settings, including security subscriptions, starting cash balances, and warm-up periods.
         LEAN only calls the Initialize method one time, at the start of your algorithm."""

        self.SetStartDate(2013, 10, 7)  # Set Start Date
        self.SetEndDate(2013, 10, 11)  # Set End Date
        self.SetCash(100000)  # Set Strategy Cash

        spy = self.AddEquity("SPY", Resolution.Minute)
        # self.AddForex, self.AddFuture...

        spy.SetDataNormalizationMode(DataNormalizationMode.Raw) # Set DataNormalizationMode to Raw
        # raw is NO! modifications to the asset price at all. div paid in cash. split is 1:1. no adjustment to price.

        self.spy = spy.Symbol # Set Symbol object to make sure there is no ambiguity

        self.SetBenchmark("SPY") # Set Benchmark to SPY
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)
        # Set BrokerageModel to be specific for fee structure and margin requirements
        # cash account need to account for the t + 3 settlement period

        self.entryPrice = 0 #it will track the entry price of self.spy position
        self.period = timedelta(minutes=31) #it will track the period of the self.spy position; need to import timedelta from datetime
        self.nextEntryTime = self.Time #it will track the next entry time of self.spy position; intialized to current time

    def OnData(self, data):
        """OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
        Arguments:
            data: Slice object keyed by symbol containing the stock data in structured manner; properties include
            trade bars, splits, option chains, delistings, and more. These are dictionaries keyed by symbol.
            tick data, trade bar data OHLC, Quote Bar all asset types consolidating all exchange data for a given symbol
            mid point for OHLC for the bid and ask prices midpoints for the bid and ask.
        """
        if not self.spy in data:
            return # to check if data
        #price = data.Bars[self.spy].Close #get the close price of self.spy
        price = data[self.spy].Close #get the close price of self.spy
        #price = self.Securities[self.spy].Close #get the close price of self.spy

        if not self.Portfolio.Invested: # check to see if we have a position
            if self.nextEntryTime <= self.Time: # check to see if we are ready to enter a position based on time one month
                self.SetHoldings(self.spy, 1)
                # allcote 100% of our portfolio to self.spy; can change the second argument to be a fraction
                self.MarketOrder(self.spy, int(self.Portfolio.Cash / price)) # enter a position based on available cash
                self.Log("Purchased Stock at {0}".format(price))
                #self.Log("Purchased Stock at {0}".format(self.Securities[self.spy].Close))
                #self.Log("Buy SPY @" + str(price))
                self.entryPrice = price # the price we entered the position

            elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price: # check to see if position is 10% up or down
                self.Liquidate(self.spy) # liquidate the spy position; if we used no argument, it would liquidate all positions
                self.Log("Sold Stock at {0}".format(price))
                self.nextEntryTime= self.Time + self.period # set the next entry time to be one month from now










