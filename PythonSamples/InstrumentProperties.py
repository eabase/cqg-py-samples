# The sample demonstrates how to get instrument properties

import threading
import CELEnvironment
from CELEnvironment import Trace
import win32com.client

# Replace it with enabled symbol
SYMBOL = "DD"


class InstrumentProperties(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.eventDone = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def Start(self):
        Trace("Request instrument properties for {}".format(SYMBOL))
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
        Trace("OnInstrumentResolved: Symbol: {}".format(symbol))
        properties = win32com.client.Dispatch(instrument.Properties)
        for property in properties:
            Trace("   Property name: {} Value: {}".format(property.Name, property.Value))
        self.eventDone.set()


CELEnvironment.StartSample(InstrumentProperties)
