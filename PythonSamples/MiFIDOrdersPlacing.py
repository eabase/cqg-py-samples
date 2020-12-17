# The sample demonstrates how to place an order with MiFID algo id.
import threading
import CELEnvironment
from CELEnvironment import Trace
from CELEnvironment import AssertMessage
import win32com.client
from win32com.client import constants

# Replace it with real login before run
LOGIN = "your_gw_login"
PASSWORD = "your_gw_password"

# Replace it with enabled symbol
SYMBOL = "DD"

# Events waiting time
TIMEOUT = 10


class OrderPlacingSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.account = None
        self.instrument = None
        self.eventGatewayIsUp = threading.Event()
        self.eventGatewayIsDown = threading.Event()
        self.eventAccountIsReady = threading.Event()
        self.eventInstrumentIsReady = threading.Event()
        self.eventOrderPlaced = threading.Event()

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

        Trace("Select the first account...")
        accounts = win32com.client.Dispatch(self.celEnvironment.cqgCEL.Accounts)
        self.account = win32com.client.Dispatch(accounts.ItemByIndex(0))

        Trace("{} instrument requesting...".format(SYMBOL))
        self.celEnvironment.cqgCEL.NewInstrument(SYMBOL)
        Trace("{} instrument waiting...".format(SYMBOL))
        AssertMessage(self.eventInstrumentIsReady.wait(TIMEOUT), "Instrument resolution timeout!")

        dispatchedInstrument = win32com.client.Dispatch(self.instrument)

        bestBid = dispatchedInstrument.Bid
        offsetFromBestBid = 10
        AssertMessage(bestBid.IsValid, "Error! Can't set an order price due to invalid BBA")

        Trace("Create Buy limit order")
        buyOrderPrice = bestBid.Price - offsetFromBestBid * dispatchedInstrument.TickSize
        buyOrder = win32com.client.Dispatch(
            self.celEnvironment.cqgCEL.CreateOrder(constants.otLimit, self.instrument, self.account, 1,
                                                   constants.osdUndefined, buyOrderPrice))

        buyOrder.MiFIDAlgorithmID = "My-Own-MiFID-Algo-ID"
        Trace("Set MiFID algorithm ID to {}".format(buyOrder.MiFIDAlgorithmID))

        Trace("Place order")
        buyOrder.Place()
        Trace("Waiting for order placing...")
        AssertMessage(self.eventOrderPlaced.wait(TIMEOUT), "Order placing timeout!")

        Trace("Logoff from GW")
        self.eventGatewayIsDown.clear()
        self.celEnvironment.cqgCEL.GWLogoff()
        AssertMessage(self.eventGatewayIsDown.wait(TIMEOUT), "GW disconnection timeout!")

        Trace("Done!")

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

    def OnOrderChanged(self, changeType, cqgOrder, oldProperties, cqgFill, cqgError):
        if cqgError is not None:
            error = win32com.client.Dispatch(cqgError)
            Trace("OnOrderChanged error: Code: {} Description: {}".format(error.Code, error.Description))
            return

        dispatchedOrder = win32com.client.Dispatch(cqgOrder)
        properties = win32com.client.Dispatch(dispatchedOrder.Properties)
        gwStatus = properties(constants.opGWStatus)
        quantity = properties(constants.opQuantity)
        instrument = properties(constants.opInstrumentName)
        mifidId = properties(constants.opMiFIDAlgorithmID)

        Trace("OnOrderChanged: change type: {}; GW status: {}; Quantity: {}; Instrument: {} MiFID Algo ID: {}"
              .format(changeType, gwStatus, quantity, instrument, mifidId))

        if changeType != constants.ctChanged:
            return

        if gwStatus.Value == constants.osInOrderBook:
            Trace("Order is placed!")
            self.eventOrderPlaced.set()


CELEnvironment.StartSample(OrderPlacingSample)
