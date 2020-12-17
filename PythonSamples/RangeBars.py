# The sample makes historical RangeBars requests and waits for responses for 20 sec

import threading
import CELEnvironment
from CELEnvironment import Trace
import win32com.client
from win32com.client import constants
from datetime import datetime, timedelta, timezone

# Replace it with enabled symbol
SYMBOL = "DD"


class RangeBarsSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.eventDone = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def Start(self):
        Trace("Create range bars request")
        request = win32com.client.Dispatch(self.celEnvironment.cqgCEL.CreateRangeBarsRequest())
        request.Symbol = SYMBOL
        request.RangeStart = datetime.now(timezone.utc) - timedelta(hours=2)
        request.RangeEnd = datetime.now(timezone.utc) - timedelta(hours=1)
        request.RangeUnit = win32com.client.constants.ruTick
        request.Range = 5
        request.SessionsFilter = 31

        Trace("Request range bars ({} - {})".format(request.RangeStart, request.RangeEnd))
        self.RangeBars = self.celEnvironment.cqgCEL.RequestRangeBars(request)

        Trace("Waiting results for 20 seconds...")
        self.eventDone.wait(20)

        Trace("Done!")

    def OnDataError(self, cqgError, errorDescription):
        if (cqgError is not None):
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace(
                "OnDataError: Code: {} Description: {}".format(dispatchedCQGError.Code, dispatchedCQGError.Description))
        self.eventDone.set()

    def OnRangeBarsResolved(self, cqgRangeBars, cqgError):
        if (cqgError is not None):
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace("OnRangeBarsResolved: Code: {} Description: {}".format(dispatchedCQGError.Code,
                                                                         dispatchedCQGError.Description))
            self.eventDone.set()
        else:
            self.TraceBars(cqgRangeBars, "OnRangeBarsResolved")

    def TraceBars(self, cqgRangeBars, methodName):
        rangeBars = win32com.client.Dispatch(cqgRangeBars)
        Trace("{}: Bars count: {}".format(methodName, rangeBars.Count))
        for rangeBar in rangeBars:
            Trace(
                "  Bar: Timestamp {} Open {} High {} Low {} Close {} Mid {} HLC3 {} Avg {} Range {} ActualVolume {} "
                "TickVolume {}".format(
                    rangeBar.Timestamp, rangeBar.Open, rangeBar.High, rangeBar.Low, rangeBar.Close, rangeBar.Mid,
                    rangeBar.HLC3, rangeBar.Avg, rangeBar.Range, rangeBar.ActualVolume, rangeBar.TickVolume))


# If CQGCEL.APIConfiguration must be customized then do it in this function
def CustomAPIConfiguration(APIConfiguration):
    Trace("Set UTC time zone. All time values passed to (received from) CQG API should correspond to this setting. ")
    APIConfiguration.TimeZoneCode = constants.tzUTC

CELEnvironment.StartSample(RangeBarsSample, CustomAPIConfiguration)
