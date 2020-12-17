# The sample makes Ticks request and waits responses for 20 sec

import threading
import CELEnvironment
from CELEnvironment import Trace
import win32com.client
from win32com.client import constants

# Replace it with enabled symbol
SYMBOL = "DD"


class TicksRequestSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.eventDone = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def Start(self):
        request = win32com.client.Dispatch(self.celEnvironment.cqgCEL.CreateTicksRequest())
        request.Symbol = SYMBOL
        request.Type = constants.trtCurrentNotify
        request.TickFilter = constants.tfAll
        request.SessionsFilter = 31
        request.Limit = 10
        Trace("Limit: {}".format(request.Limit))

        self.ticks = self.celEnvironment.cqgCEL.RequestTicks(request)

        self.eventDone.wait(20)

        Trace("Done!")

    def OnDataError(self, cqgError, errorDescription):
        if cqgError is not None:
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace(
                "OnDataError: Code: {} Description: {}".format(dispatchedCQGError.Code, dispatchedCQGError.Description))
        self.eventDone.set()

    def OnTicksResolved(self, cqgTicks, cqgError):
        if cqgError is not None:
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace("OnTicksResolved: Code: {} Description: {}".format(dispatchedCQGError.Code,
                                                                     dispatchedCQGError.Description))
            self.eventDone.set()
        else:
            dispatchedCQGTicks = win32com.client.Dispatch(cqgTicks)
            Trace("OnTicksResolved: Ticks count: {}".format(dispatchedCQGTicks.Count))
            for tick in dispatchedCQGTicks:
                Trace(
                    "OnTicksResolved: Timestamp {} Volume {} Price {} PriceType {}".format(
                        tick.Timestamp, tick.Volume, tick.Price, tick.PriceType))

    def OnTicksAdded(self, cqgTicks, addedTicksCount):
        dispatchedCQGTicks = win32com.client.Dispatch(cqgTicks)
        Trace("OnTicksAdded: Ticks added count: {}".format(addedTicksCount))
        Trace("OnTicksAdded: Total ticks count: {}".format(dispatchedCQGTicks.Count))
        for i in range(dispatchedCQGTicks.Count - addedTicksCount, dispatchedCQGTicks.Count):
            tick = dispatchedCQGTicks.Item(i)
            Trace(
                "OnTicksAdded: Timestamp {} Volume {} Price {} PriceType {}".format(
                    tick.Timestamp, tick.Volume, tick.Price, tick.PriceType))

    def OnTicksRemoved(self, cqgTicks, removedTickIndex):
        dispatchedCQGTicks = win32com.client.Dispatch(cqgTicks)
        Trace("OnTicksRemoved: Removed tick index: {}".format(removedTickIndex))
        Trace("OnTicksRemoved: Total ticks count: {}".format(dispatchedCQGTicks.Count))


CELEnvironment.StartSample(TicksRequestSample)
