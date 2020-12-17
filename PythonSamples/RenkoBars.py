# The sample makes Renko bars requests and waits for responses for 20 sec

import threading
import CELEnvironment
from CELEnvironment import Trace
import win32com.client

# Replace it with enabled symbol
SYMBOL = "DD"


class RenkoBarsSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.eventDone = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def Start(self):
        Trace("Create renko bars request")
        request = win32com.client.Dispatch(self.celEnvironment.cqgCEL.CreateRenkoBarsRequest())
        request.Symbol = SYMBOL
        request.RangeStart = 0
        request.RangeEnd = -3
        request.BrickUnit = win32com.client.constants.buTick
        request.BrickSize = 3
        request.Continuation = win32com.client.constants.tsctStandard
        request.SubscriptionLevel = win32com.client.constants.tslEachTick
        request.UpdatesEnabled = True
        request.SessionsFilter = 31

        Trace("Request renko bars")
        self.RenkoBars = self.celEnvironment.cqgCEL.RequestRenkoBars(request)

        Trace("Waiting results for 20 seconds...")
        self.eventDone.wait(20)

        Trace("Done!")

    def OnDataError(self, cqgError, errorDescription):
        if (cqgError is not None):
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace(
                "OnDataError: Code: {} Description: {}".format(dispatchedCQGError.Code, dispatchedCQGError.Description))
        self.eventDone.set()

    def OnRenkoBarsResolved(self, cqgRenkoBars, cqgError):
        if (cqgError is not None):
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace("OnRenkoBarsResolved: Code: {} Description: {}".format(dispatchedCQGError.Code,
                                                                         dispatchedCQGError.Description))
            self.eventDone.set()
        else:
            self.TraceBars(cqgRenkoBars, "-", "OnRenkoBarsResolved")

    def OnRenkoBarsAdded(self, cqgRenkoBars):
        self.TraceBars(cqgRenkoBars, "-", "OnRenkoBarsAdded")

    def OnRenkoBarsInserted(self, cqgRenkoBars, index):
        self.TraceBars(cqgRenkoBars, index, "OnRenkoBarsInserted")

    def OnRenkoBarsUpdated(self, cqgRenkoBars, index):
        self.TraceBars(cqgRenkoBars, index, "OnRenkoBarsUpdated")

    def OnRenkoBarsRemoved(self, cqgRenkoBars, index):
        self.TraceBars(cqgRenkoBars, index, "OnRenkoBarsRemoved")

    def TraceBars(self, cqgRenkoBars, index, methodName):
        renkoBars = win32com.client.Dispatch(cqgRenkoBars)
        Trace("{}: Bars count: {} index {}".format(methodName, renkoBars.Count, index))
        for renkoBar in renkoBars:
            Trace("  Bar: Timestamp {} RenkoHigh {} RenkoLow {} RenkoUp {} Open {} High {} Low {} Close {}".format(
                renkoBar.Timestamp, renkoBar.RenkoHigh, renkoBar.RenkoLow, renkoBar.RenkoUp, renkoBar.Open,
                renkoBar.High, renkoBar.Low, renkoBar.Close))


CELEnvironment.StartSample(RenkoBarsSample)
