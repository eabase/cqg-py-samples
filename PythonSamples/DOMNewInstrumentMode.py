# The sample demonstrates DOM data receiving via new instrument mode

import threading
import CELEnvironment
from CELEnvironment import Trace
import win32com.client

# Replace it with enabled symbol
SYMBOL = "DD"


class DOMReceiving(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.eventDone = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def Start(self):
        Trace("Request DOM for {}".format(SYMBOL))
        request = win32com.client.Dispatch(self.celEnvironment.cqgCEL.CreateInstrumentRequest())
        request.Symbol = SYMBOL
        request.QuoteLevel = win32com.client.constants.qsNone
        request.PropertyLevel = win32com.client.constants.psNone
        request.DOMBBAType = win32com.client.constants.dbtCombined
        request.DOMStatus = True

        self.celEnvironment.cqgCEL.SubscribeNewInstrument(request)

        self.eventDone.wait(10)

    def OnDataError(self, cqgError, errorDescription):
        if cqgError is not None:
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace(
                "OnDataError: Code: {} Description: {}".format(dispatchedCQGError.Code, dispatchedCQGError.Description))
        self.eventDone.set()

    def OnInstrumentDOMChanged(self, cqgInstrument, cqgPrevAsks, cqgPrevBids):
        instrument = win32com.client.Dispatch(cqgInstrument)
        for ask in instrument.DOMAsks:
            if ask.IsValid:
                Trace("{} Price: {} Volume {}".format("ASK", ask.Price, ask.Volume))
        for bid in instrument.DOMBids:
            if bid.IsValid:
                Trace("     {} Price: {} Volume {}".format("BID", bid.Price, bid.Volume))


# If CQGCEL.APIConfiguration must be customized then do it in this function
def CustomAPIConfiguration(APIConfiguration):
    APIConfiguration.NewInstrumentMode = True
    APIConfiguration.DOMUpdatesMode = win32com.client.constants.domUMSnapshot
    APIConfiguration.DOMUpdatesPeriod = 1000


CELEnvironment.StartSample(DOMReceiving, CustomAPIConfiguration)
