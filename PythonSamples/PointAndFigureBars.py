# The sample makes Point and Figure request and waits for response and updates for 20 sec

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
        request = win32com.client.Dispatch(self.celEnvironment.cqgCEL.CreatePointAndFigureBarsRequest())
        request.Symbol = SYMBOL
        request.RangeStart = 0
        request.RangeEnd = -10
        request.BoxSize = 3
        request.BoxUnits = win32com.client.constants.pfbuTicks
        request.Reversal = 3
        request.DataSource = win32com.client.constants.pfds1Min
        request.Continuation = win32com.client.constants.tsctStandard
        request.SubscriptionLevel = win32com.client.constants.tslEachTick
        request.UpdatesEnabled = True

        self.celEnvironment.cqgCEL.RequestPointAndFigureBars(request)

        self.eventDone.wait(20)

    def OnDataError(self, cqgError, errorDescription):
        if (cqgError is not None):
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace(
                "OnDataError: Code: {} Description: {}".format(dispatchedCQGError.Code, dispatchedCQGError.Description))
        self.eventDone.set()

    def OnPointAndFigureBarsResolved(self, cqgPointAndFigureBars, cqgError):
        if (cqgError is not None):
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace("OnPointAndFigureBarsResolved: Code: {} Description: {}".format(dispatchedCQGError.Code,
                                                                                  dispatchedCQGError.Description))
            self.eventDone.set()
        else:
            bars = win32com.client.Dispatch(cqgPointAndFigureBars)
            Trace("OnPointAndFigureBarsResolved: Bars count: {} Bars:".format(bars.Count))
            for i in range(0, bars.Count):
                self.dumpBar(win32com.client.Dispatch(bars.Item(i)), i)

    def OnPointAndFigureBarsAdded(self, cqgPointAndFigureBars):
        bars = win32com.client.Dispatch(cqgPointAndFigureBars)
        Trace("OnPointAndFigureBarsAdded: Bars count: {} Bars:".format(bars.Count))
        for i in range(0, bars.Count):
            self.dumpBar(win32com.client.Dispatch(bars.Item(i)), i)

    def OnPointAndFigureBarsUpdated(self, cqgPointAndFigureBars, index):
        Trace("OnPointAndFigureBarsUpdated: Updated bar index {}".format(index))
        bars = win32com.client.Dispatch(cqgPointAndFigureBars)
        self.dumpBar(win32com.client.Dispatch(bars.Item(index)), index)

    def dumpBar(self, bar, index):
        Trace("   Bar index: {} Timestamp {} PFHigh {} PFLow {} Up {} ".format(index, bar.Timestamp, bar.PFHigh,
                                                                               bar.PFLow, bar.Up))


CELEnvironment.StartSample(BarsRequestSample)
