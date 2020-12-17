# The sample makes a Constant Volume Bar (CVB) request and waits for response and updates for 20 sec

import threading
import CELEnvironment
from CELEnvironment import Trace
import win32com.client

# Replace it with enabled symbol
SYMBOL = "DD"


class ConstantVolumeBarsSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.eventDone = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def Start(self):
        request = win32com.client.Dispatch(self.celEnvironment.cqgCEL.CreateConstantVolumeBarsRequest())
        request.Symbol = SYMBOL
        request.RangeStart = 0
        request.RangeEnd = -10
        request.VolumeLevel = 100
        request.VolumeType = win32com.client.constants.cvbvtActual
        request.Continuation = win32com.client.constants.tsctStandard
        request.SubscriptionLevel = win32com.client.constants.tslEachTick
        request.UpdatesEnabled = True

        self.celEnvironment.cqgCEL.RequestConstantVolumeBars(request)

        self.eventDone.wait(20)

    def OnDataError(self, cqgError, errorDescription):
        if cqgError is not None:
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace(
                "OnDataError: Code: {} Description: {}".format(dispatchedCQGError.Code, dispatchedCQGError.Description))
        self.eventDone.set()

    def OnConstantVolumeBarsResolved(self, cqgConstantVolumeBars, cqgError):
        if cqgError is not None:
            error = win32com.client.Dispatch(cqgError)
            Trace("OnConstantVolumeBarsResolved: Code: {} Description: {}".format(error.Code, error.Description))
            self.eventDone.set()
        else:
            bars = win32com.client.Dispatch(cqgConstantVolumeBars)
            Trace("OnConstantVolumeBarsResolved: Bars count: {} Bars:".format(bars.Count))
            for i in range(0, bars.Count):
                self.dumpBar(win32com.client.Dispatch(bars.Item(i)), i)

    def OnConstantVolumeBarsAdded(self, cqgConstantVolumeBars):
        bars = win32com.client.Dispatch(cqgConstantVolumeBars)
        Trace("OnConstantVolumeBarsAdded: Bars count: {} Bars:".format(bars.Count))
        for i in range(0, bars.Count):
            self.dumpBar(win32com.client.Dispatch(bars.Item(i)), i)

    def OnConstantVolumeBarsUpdated(self, cqgConstantVolumeBars, index):
        Trace("OnConstantVolumeBarsUpdated: Updated bar index {}".format(index))
        bars = win32com.client.Dispatch(cqgConstantVolumeBars)
        self.dumpBar(win32com.client.Dispatch(bars.Item(index)), index)

    def dumpBar(self, bar, index):
        Trace("   Bar index: {} Timestamp {} Open {} High {} Low {} Close {} "
              "ActualVolume {} TickVolume {}".format(index, bar.Timestamp, bar.Open, bar.High, bar.Low, bar.Close,
                                                     bar.ActualVolume, bar.TickVolume))


CELEnvironment.StartSample(ConstantVolumeBarsSample)
