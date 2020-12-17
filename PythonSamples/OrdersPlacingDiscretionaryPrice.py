# The sample demonstrates how to place an order with discretionary price.
import threading
import CELEnvironment
from CELEnvironment import Trace
from CELEnvironment import AssertMessage
import win32com.client
from win32com.client import constants

# Replace it with real login before run
LOGIN = "your_gw_login"
PASSWORD = "your_gw_password"

# Replace it with enabled symbol that supports discretionary prices
SYMBOL = "CUS10"

# Events waiting time
TIMEOUT = 10


class OrderPlacingDiscretionaryPriceSample(CELEnvironment.CELSinkBase):
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

        Trace("Select the first account (it should be authorized to trade {})".format(SYMBOL))
        accounts = win32com.client.Dispatch(self.celEnvironment.cqgCEL.Accounts)
        self.account = win32com.client.Dispatch(accounts.ItemByIndex(0))

        Trace("{} instrument requesting...".format(SYMBOL))
        self.celEnvironment.cqgCEL.NewInstrument(SYMBOL)
        Trace("{} instrument waiting...".format(SYMBOL))
        AssertMessage(self.eventInstrumentIsReady.wait(TIMEOUT), "Instrument resolution timeout!")
        instrument = win32com.client.Dispatch(self.instrument)

        offsetCount = instrument.DiscretionaryOffsetCount
        Trace("Symbol {} has {} discretionary offset count".format(instrument.FullName, offsetCount))

        AssertMessage(offsetCount != 0, "Symbol does not have discretionary prices. Select another one.")

        bestBid = instrument.Bid
        AssertMessage(bestBid.IsValid, "Error! Can't set an order price due to invalid BBA")

        Trace("Best bid value is {}".format(bestBid.Price))
        Trace("Calculating a price that below the market by 10 tick sizes")
        buyOrderPrice = bestBid.Price - 10 * instrument.TickSize
        Trace("It is {}".format(buyOrderPrice))
        Trace("Create Buy limit order")
        buyOrder = win32com.client.Dispatch(self.celEnvironment.cqgCEL.CreateOrder(constants.otLimit,
                                                                                   self.instrument, self.account, 1,
                                                                                   constants.osdUndefined,
                                                                                   buyOrderPrice))
        Trace("Set discretionary offset for the order price")
        buyOrder.DiscretionaryOffset = offsetCount - 1
        properties = win32com.client.Dispatch(buyOrder.Properties)
        executionInstructions = properties(constants.opExecutionInstructions)
        executionInstructions.Value = constants.oeiDiscretion

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

    def OnInstrumentResolved(self, symbol, cqgInstrument, cqgError):
        if cqgError is not None:
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace("OnInstrumentResolved error: Error code: {} Description: {}".format(dispatchedCQGError.Code,
                                                                                      dispatchedCQGError.Description))
            return

        self.instrument = cqgInstrument
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
        limitPrice = properties(constants.opLimitPrice)
        discretionaryPriceOffset = properties(constants.opDiscretionaryOffset)

        Trace("OnOrderChanged: change type: {}; GW status: {}; Quantity: {}; Instrument: {}; Price: {}; Offset: {}"
              .format(changeType, gwStatus, quantity, instrument, limitPrice, discretionaryPriceOffset))

        if changeType != constants.ctChanged:
            return

        if gwStatus.Value == constants.osInOrderBook:
            Trace("Order is placed!")
            self.eventOrderPlaced.set()


CELEnvironment.StartSample(OrderPlacingDiscretionaryPriceSample)
