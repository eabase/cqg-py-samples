# The sample demonstrates DOM data receiving via instrument supscription

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
        self.celEnvironment.cqgCEL.NewInstrument(SYMBOL)

        self.eventDone.wait(10)

    def OnDataError(self, cqgError, errorDescription):
        if cqgError is not None:
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace(
                "OnDataError: Code: {} Description: {}".format(dispatchedCQGError.Code, dispatchedCQGError.Description))
        self.eventDone.set()

    def OnInstrumentResolved(self, symbol, cqgInstrument, cqgError):
        if cqgError is not None:
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace("OnInstrumentResolved error: Error code: {} Description: {}".format(dispatchedCQGError.Code,
                                                                                      dispatchedCQGError.Description))
            self.eventDone.set()
            return

        instrument = win32com.client.Dispatch(cqgInstrument)
        Trace("OnInstrumentResolved: Symbol: {} Instrument full name: {}".format(symbol, instrument.FullName))
        Trace("Set data subscription level for DOM data receiving")
        instrument.DataSubscriptionLevel = win32com.client.constants.dsQuotesAndDOM
        Trace("Set limit to DOM depth")
        instrument.DOMBookLimit = 10

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
    APIConfiguration.NewInstrumentMode = False
    APIConfiguration.DOMUpdatesMode = win32com.client.constants.domUMSnapshot
    APIConfiguration.DOMUpdatesPeriod = 1000


CELEnvironment.StartSample(DOMReceiving, CustomAPIConfiguration)
