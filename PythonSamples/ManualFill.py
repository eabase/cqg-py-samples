# The sample demonstrates how to request all manual fills by account and to add a manual fill.

import threading
import CELEnvironment
from CELEnvironment import Trace
from CELEnvironment import AssertMessage
import win32com.client
from win32com.client import constants
from datetime import datetime, timezone

# Replace it with real login before run
LOGIN = "your_gw_login"
PASSWORD = "your_gw_password"

# Replace it with enabled symbol
SYMBOL = "DD"

# Events waiting time
TIMEOUT = 10


class ManualFillSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.account = None
        self.instrument = None
        self.eventGatewayIsUp = threading.Event()
        self.eventGatewayIsDown = threading.Event()
        self.eventAccountIsReady = threading.Event()
        self.eventInstrumentIsReady = threading.Event()
        self.eventManualFillUpdateResolved = threading.Event()
        self.eventManualFillsResolved = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def Start(self):
        Trace("Connecting to GW")
        self.celEnvironment.cqgCEL.GWLogon(LOGIN, PASSWORD)

        Trace("Waiting for GW connection...")
        AssertMessage(self.eventGatewayIsUp.wait(TIMEOUT), "GW connection timeout!")

        self.celEnvironment.cqgCEL.AccountSubscriptionLevel = constants.aslAccountUpdatesAndOrders
        Trace("Waiting for accounts coming...")
        AssertMessage(self.eventAccountIsReady.wait(TIMEOUT), "Accounts coming timeout!")

        Trace("Select the first account")
        accounts = win32com.client.Dispatch(self.celEnvironment.cqgCEL.Accounts)
        self.account = win32com.client.Dispatch(accounts.ItemByIndex(0))

        Trace("Requesting instrument {}".format(SYMBOL))
        self.celEnvironment.cqgCEL.NewInstrument(SYMBOL)
        Trace("Waiting for instrument {} ...".format(SYMBOL))
        AssertMessage(self.eventInstrumentIsReady.wait(TIMEOUT), "Instrument resolution timeout!")

        instrument = win32com.client.Dispatch(self.instrument)

        bestBid = instrument.Bid
        AssertMessage(bestBid.IsValid, "Error! Can't set a fill price due to invalid BBA")

        Trace("Best bid value is {}".format(bestBid.Price))
        Trace("Calculating a price that above the market by 10 tick sizes")
        buyOrderPrice = bestBid.Price - 10 * instrument.TickSize
        Trace("It is {}".format(buyOrderPrice))

        statementTime = datetime.now(timezone.utc)

        Trace("Creating a request for manual fill adding and fill it")
        manualFillRequest = win32com.client.Dispatch(
            self.celEnvironment.cqgCEL.CreateManualFillRequest(constants.mfutAdd, None))
        manualFillRequest.GWAccountID = self.account.GWAccountID
        manualFillRequest.InstrumentName = instrument.FullName
        manualFillRequest.Note = "Hi from API!"
        manualFillRequest.Price = buyOrderPrice
        manualFillRequest.Quantity = 1
        manualFillRequest.Side = constants.osdUndefined
        manualFillRequest.StatementDate = statementTime
        manualFillRequest.TradeTimestamp = statementTime
        manualFillRequest.SpeculationType = constants.sptSpeculation

        Trace("Invoking the request")
        self.celEnvironment.cqgCEL.RequestManualFillUpdate(manualFillRequest)

        Trace("Waiting for manual fill adding...")
        AssertMessage(self.eventManualFillUpdateResolved.wait(TIMEOUT), "Manual fill adding timeout!")

        Trace("Requesting manual fills for account {}".format(self.account.GWAccountID))
        self.celEnvironment.cqgCEL.RequestManualFills(self.account.GWAccountID, constants.mfdlSnapshot)

        Trace("Waiting for manual fills receiving...")
        AssertMessage(self.eventManualFillsResolved.wait(TIMEOUT), "Manual fills receiving timeout!")

        Trace("Logoff from GW")
        self.eventGatewayIsDown.clear()
        self.celEnvironment.cqgCEL.GWLogoff()
        AssertMessage(self.eventGatewayIsDown.wait(TIMEOUT), "GW disconnection timeout!")

        Trace("Done!")

    def OnDataError(self, cqgError, errorDescription):
        if cqgError is not None:
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace(
                "OnDataError: Code: {} Description: {}".format(dispatchedCQGError.Code, dispatchedCQGError.Description))

    def OnGWConnectionStatusChanged(self, connectionStatus):
        if connectionStatus == constants.csConnectionUp:
            Trace("GW connection is UP!")
            self.eventGatewayIsUp.set()
        if connectionStatus == constants.csConnectionDown:
            Trace("GW connection is DOWN!")
            self.eventGatewayIsDown.set()

    def OnAccountChanged(self, change, account, position):
        if change != constants.actAccountsReloaded:
            return

        Trace("Accounts are ready!")
        self.eventAccountIsReady.set()

    def OnInstrumentResolved(self, symbol, instrument, cqgError):
        if cqgError is not None:
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace("OnInstrumentResolved error: Error code: {} Description: {}".format(dispatchedCQGError.Code,
                                                                                      dispatchedCQGError.Description))
            return

        self.instrument = instrument
        Trace("Symbol {} is resolved!".format(symbol))
        self.eventInstrumentIsReady.set()

    def OnManualFillsResolved(self, cqgManualFills, cqgError):
        if cqgError is not None:
            error = win32com.client.Dispatch(cqgError)
            Trace("OnManualFillsResolved error: Code: {} Description: {}".format(error.Code, error.Description))
            return

        Trace("Manual fills are received!")

        manualFills = win32com.client.Dispatch(cqgManualFills)
        for manualFill in manualFills:
            Trace("Manual fill: instrument: {} GW account id: {} trade id: {} note: {} display price: {}".format(
                manualFill.InstrumentName, manualFill.GWAccountID, manualFill.TradeId, manualFill.Note,
                manualFill.DisplayPrice))

        self.eventManualFillsResolved.set()

    def OnManualFillUpdateResolved(self, cqgManualFillRequest, cqgError):
        if cqgError is not None:
            error = win32com.client.Dispatch(cqgError)
            Trace("OnManualFillUpdateResolved error: Code: {} Description: {}".format(error.Code, error.Description))
            return

        Trace("Manual fill is added!")
        self.eventManualFillUpdateResolved.set()


# If CQGCEL.APIConfiguration must be customized then do it in this function
def CustomAPIConfiguration(APIConfiguration):
    Trace("Set UTC time zone. All time values passed to (received from) CQG API should correspond to this setting. ")
    APIConfiguration.TimeZoneCode = constants.tzUTC


CELEnvironment.StartSample(ManualFillSample, CustomAPIConfiguration)
