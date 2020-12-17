# The sample makes Timed Bar request and waits for response and updates for 20 sec

import threading
import CELEnvironment
from CELEnvironment import Trace
import win32com.client

# Replace it with enabled symbol
SYMBOL = "DD"


class BarsRequestSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.eventDone = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def Start(self):
        Trace("Create timed bars request")
        request = win32com.client.Dispatch(self.celEnvironment.cqgCEL.CreateTimedBarsRequest())
        request.Symbol = SYMBOL
        request.RangeStart = 0
        request.RangeEnd = -10
        request.HistoricalPeriod = win32com.client.constants.hpDaily
        request.DailyBarClose = win32com.client.constants.dbcLastQuoteOrSettlement
        request.UpdatesEnabled = True
        request.IncludeOutput(win32com.client.constants.tbrContractVolume, True)
        request.IncludeOutput(win32com.client.constants.tbrCommodityVolume, True)
        request.SessionsFilter = 31

        Trace("Starting the request...")
        self.celEnvironment.cqgCEL.RequestTimedBars(request)

        self.eventDone.wait(20)

        Trace("Done!")

    def OnDataError(self, cqgError, errorDescription):
        if (cqgError is not None):
            error = win32com.client.Dispatch(cqgError)
            Trace("OnDataError: Code: {} Description: {}".format(error.Code, error.Description))
        self.eventDone.set()

    def OnTimedBarsResolved(self, cqgTimedBars, cqgError):
        if (cqgError is not None):
            error = win32com.client.Dispatch(cqgError)
            Trace("OnTimedBarsResolved: Code: {} Description: {}".format(error.Code,
                                                                         error.Description))
            self.eventDone.set()
        else:
            bars = win32com.client.Dispatch(cqgTimedBars)
            Trace("OnTimedBarsResolved: Bars count: {} Bars:".format(bars.Count))
            for i in range(0, bars.Count):
                self.dumpBar(win32com.client.Dispatch(bars.Item(i)), i)

    def OnTimedBarsAdded(self, cqgTimedBars):
        bars = win32com.client.Dispatch(cqgTimedBars)
        Trace("OnTimedBarsAdded: Bars count: {} Bars:".format(bars.Count))
        for i in range(0, bars.Count):
            self.dumpBar(win32com.client.Dispatch(bars.Item(i)), i)

    def OnTimedBarsUpdated(self, cqgTimedBars, index):
        Trace("OnTimedBarsUpdated: Updated bar index {}".format(index))
        bars = win32com.client.Dispatch(cqgTimedBars)
        self.dumpBar(win32com.client.Dispatch(bars.Item(index)), index)

    def OnTimedBarsRemoved(self, cqgTimedBars, index):
        bars = win32com.client.Dispatch(cqgTimedBars)
        Trace("OnTimedBarsRemoved: Bars count: {} : Removed bar index {}".format(bars.Count, index))
        for i in range(0, bars.Count):
            self.dumpBar(win32com.client.Dispatch(bars.Item(i)), i)

    def dumpBar(self, bar, index):
        Trace("   Bar index: {} Timestamp {} Open {} High {} Low {} Close {} "
              "ActualVolume {} CommodityVolume {} ContractVolume {} TickVolume {}".format(
            index, bar.Timestamp, bar.Open, bar.High, bar.Low, bar.Close,
            bar.ActualVolume, bar.CommodityVolume, bar.ContractVolume, bar.TickVolume))


CELEnvironment.StartSample(BarsRequestSample)
