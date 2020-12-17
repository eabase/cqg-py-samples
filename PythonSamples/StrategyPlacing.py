# The sample demonstrates how to define a strategy and place a strategy order

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
STRATEGY = "SPREAD(CLE-DD)"

# Events waiting time
TIMEOUT = 10


class StrategyPlacingSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.account = None
        self.eventGatewayIsUp = threading.Event()
        self.eventGatewayIsDown = threading.Event()
        self.eventInstrumentIsReady = threading.Event()
        self.eventAccountIsReady = threading.Event()
        self.eventStrategyIsReady = threading.Event()
        self.eventOrderPlaced = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def createOrder(self, quantity, price):
        Trace("Creating a default execution pattern for limit orders...")
        executionPattern = win32com.client.Dispatch(
            self.celEnvironment.cqgCEL.CreateExecutionPattern(self.dispatchedStrategy, constants.otLimit))
        Trace("Creating a strategy order...")
        order = win32com.client.Dispatch(
            self.celEnvironment.cqgCEL.CreateStrategyOrder(constants.otLimit, self.dispatchedStrategy, self.account,
                                                           None,
                                                           quantity, constants.osdUndefined, price))
        Trace("Set an execution pattern order property...")
        properties = win32com.client.Dispatch(order.Properties)
        execPatternProperty = properties(constants.opExecutionPattern)
        execPatternProperty.Value = executionPattern.PatternString
        return order

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

        Trace("Define strategy...")
        definedStrategy = self.celEnvironment.cqgCEL.DefineStrategy(STRATEGY)

        Trace("Waiting for strategy resolution...")
        AssertMessage(self.eventStrategyIsReady.wait(TIMEOUT), "Strategy resolution timeout!")

        self.dispatchedStrategy = win32com.client.Dispatch(definedStrategy)

        Trace(
            "Subscribe to {} for a best ask value receiving. It will be used for an order placing...".format(STRATEGY))
        self.celEnvironment.cqgCEL.NewInstrument(STRATEGY)
        Trace("{} subscription waiting...".format(STRATEGY))
        AssertMessage(self.eventInstrumentIsReady.wait(TIMEOUT), "Instrument resolution timeout!")

        instrument = win32com.client.Dispatch(self.instrument)

        bestAsk = instrument.Ask
        AssertMessage(bestAsk.IsValid, "Error! Can't set an order price due to invalid BBA")

        Trace("Best ask value is {}".format(bestAsk.Price))
        Trace("Calculating a price that above the market by 10 tick sizes...")
        sellOrderPrice = bestAsk.Price + 10 * instrument.TickSize
        Trace("It is {}".format(sellOrderPrice))

        Trace("Starting a limit sell order creation procedure...")
        order = self.createOrder(-1, sellOrderPrice)

        Trace("Place the order...")
        order.Place()

        Trace("Waiting for order placing...")
        AssertMessage(self.eventOrderPlaced.wait(TIMEOUT), "Order placing timeout!")

        Trace("Logoff from GW")
        self.eventGatewayIsDown.clear()
        self.celEnvironment.cqgCEL.GWLogoff()
        AssertMessage(self.eventGatewayIsDown.wait(TIMEOUT), "GW disconnection timeout!")

        Trace("Done.")

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

    def OnStrategyDefinitionProgress(self, cqgDefinition, cqgError):
        if cqgError is not None:
            error = win32com.client.Dispatch(cqgError)
            Trace("OnStrategyDefinitionProgress error: Code: {} Description: {}".format(error.Code, error.Description))
            return

        dispatchedDefinition = win32com.client.Dispatch(cqgDefinition)
        Trace("OnStrategyDefinitionProgress: requested symbol: {} GW symbol: {} status: {}".format(
            dispatchedDefinition.RequestString, dispatchedDefinition.Symbol, dispatchedDefinition.Status))
        if dispatchedDefinition.Status == constants.srsSuccess:
            self.eventStrategyIsReady.set()

    def OnOrderChanged(self, changeType, cqgOrder, oldProperties, cqgFill, cqgError):
        if cqgError is not None:
            error = win32com.client.Dispatch(cqgError)
            Trace("OnOrderChanged error: Code: {} Description: {}".format(error.Code,
                                                                          error.Description))
            return

        dispatchedOrder = win32com.client.Dispatch(cqgOrder)
        properties = win32com.client.Dispatch(dispatchedOrder.Properties)
        gwStatus = properties(constants.opGWStatus)
        quantity = properties(constants.opQuantity)
        instrument = properties(constants.opInstrumentName)
        limitPrice = properties(constants.opLimitPrice)

        Trace("OnOrderChanged: change type: {}; GW status: {}; Quantity: {}; Instrument: {}; Price: {};"
              .format(changeType, gwStatus, quantity, instrument, limitPrice))

        if changeType != constants.ctChanged:
            return

        if gwStatus.Value == constants.osInOrderBook:
            Trace("Strategy order is placed!")
            self.eventOrderPlaced.set()

    def OnInstrumentResolved(self, symbol, instrument, cqgError):
        if cqgError is not None:
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace("OnInstrumentResolved error: Error code: {} Description: {}".format(dispatchedCQGError.Code,
                                                                                      dispatchedCQGError.Description))
            return

        self.instrument = instrument
        Trace("Instrument {} is resolved!".format(symbol))
        self.eventInstrumentIsReady.set()


CELEnvironment.StartSample(StrategyPlacingSample)
