# The sample requests ticks for a minute an hour ago and waits a response for 20 sec

import threading
import CELEnvironment
from CELEnvironment import Trace
import win32com.client
from datetime import datetime, timedelta, timezone
from win32com.client import constants

# Replace it with enabled symbol
SYMBOL = "DD"


class TicksRequestSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.eventDone = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def Start(self):
        Trace("Creating ticks request...")
        request = win32com.client.Dispatch(self.celEnvironment.cqgCEL.CreateTicksRequest())
        request.Symbol = SYMBOL
        request.Type = constants.trtTimeRange
        # If you need to set an exact date then set it as: datetime(2019, 4, 9, 10).replace(tzinfo=timezone.utc)
        request.RangeStart = datetime.now(timezone.utc) - timedelta(hours=1, minutes=1)
        request.RangeEnd = datetime.now(timezone.utc) - timedelta(hours=1)
        request.TickFilter = constants.tfAll
        request.SessionsFilter = 31
        request.Limit = 100

        Trace("Starting the request: {} - {} (an accuracy to the minute)...".format(request.RangeStart, request.RangeEnd))
        self.ticks = self.celEnvironment.cqgCEL.RequestTicks(request)

        self.eventDone.wait(20)

        Trace("Done!")

    def OnDataError(self, cqgError, errorDescription):
        if cqgError is not None:
            error = win32com.client.Dispatch(cqgError)
            Trace("OnDataError: Code: {} Description: {}".format(error.Code, error.Description))
        self.eventDone.set()

    def OnTicksResolved(self, cqgTicks, cqgError):
        if cqgError is not None:
            error = win32com.client.Dispatch(cqgError)
            Trace("OnTicksResolved: Code: {} Description: {}".format(error.Code,
                                                                     error.Description))
            self.eventDone.set()
        else:
            ticks = win32com.client.Dispatch(cqgTicks)
            Trace("OnTicksResolved: Ticks count: {}".format(ticks.Count))
            for tick in ticks:
                Trace(
                    "   Timestamp {} Volume {} Price {} PriceType {}".format(tick.Timestamp, tick.Volume, tick.Price,
                                                                             tick.PriceType))


# If CQGCEL.APIConfiguration must be customized then do it in this function
def CustomAPIConfiguration(APIConfiguration):
    Trace("Set UTC time zone. All time values passed to (received from) CQG API should correspond to this setting. ")
    APIConfiguration.TimeZoneCode = constants.tzUTC

CELEnvironment.StartSample(TicksRequestSample, CustomAPIConfiguration)
