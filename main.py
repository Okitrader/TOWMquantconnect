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
        self.nextEntryTime = self.Time #it will track the next entry time of self.spy position








