# The sample demonstrates how to place a compound order with 2 legs, modify it by adding another leg and wait for the
#  order filling/canceling.

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


class CompoundOrdersPlacingSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.account = None
        self.instrument = None
        self.eventGatewayIsUp = threading.Event()
        self.eventGatewayIsDown = threading.Event()
        self.eventAccountIsReady = threading.Event()
        self.eventInstrumentIsReady = threading.Event()
        self.eventOrderPlaced = threading.Event()
        self.eventOrderFilled = threading.Event()
        self.eventOrderCanceled = threading.Event()
        self.expectedCanceledOrdersCount = 2  # both remained orders must be canceled by the filled one (it is OCO:
                                              # one cancels others)
        self.expectedPlacedOrdersCount = 2  # There are two orders should be placed before an OCO order modifying

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def createOrder(self, quantity, price):
        order = self.celEnvironment.cqgCEL.CreateOrder(constants.otLimit, self.instrument, self.account, quantity,
                                                       constants.osdUndefined, price)
        return win32com.client.Dispatch(order)

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

        Trace("{} instrument requesting...".format(SYMBOL))
        self.celEnvironment.cqgCEL.NewInstrument(SYMBOL)
        Trace("{} instrument waiting...".format(SYMBOL))
        AssertMessage(self.eventInstrumentIsReady.wait(TIMEOUT), "Instrument resolution timeout!")

        dispatchedInstrument = win32com.client.Dispatch(self.instrument)

        bestBid = dispatchedInstrument.Bid
        AssertMessage(bestBid.IsValid, "Error! Can't set an order price due to invalid BBA")

        Trace("Best bid value is {}".format(bestBid.Price))
        Trace("Calculating a price that below the market by 10 tick sizes...")
        buyOrderPrice = bestBid.Price - 10 * dispatchedInstrument.TickSize
        Trace("It is {}".format(buyOrderPrice))

        Trace("Creating two buy limit orders...")
        buyOrders = []
        buyOrders.append(self.createOrder(1, buyOrderPrice))
        buyOrders.append(self.createOrder(1, buyOrderPrice - 2 * dispatchedInstrument.TickSize))

        Trace("Creating an order chain for initial compound order...")
        orderChain = win32com.client.Dispatch(self.celEnvironment.cqgCEL.CreateOrderChain())
        orderChain.AddOrder(buyOrders[0])
        orderChain.AddOrder(buyOrders[1])

        Trace("Place the compound order")
        self.celEnvironment.cqgCEL.PlaceCompoundOrder(orderChain)
        Trace("Waiting for compound order legs placing...")
        AssertMessage(self.eventOrderPlaced.wait(TIMEOUT), "Order placing timeout!")

        sellOrderPrice = bestBid.Price
        Trace(
            "Create a sell limit order for the compound order extending. The order price is {}".format(sellOrderPrice))
        sellOrder = self.createOrder(-1, sellOrderPrice)

        Trace("Create an order chain for the compound order extending")
        newOrderChain = self.celEnvironment.cqgCEL.CreateOrderChain()
        newOrderChain.AddOrder(sellOrder)

        Trace("Modifying the compound order...")
        self.celEnvironment.cqgCEL.ModifyCompoundOrder(self.compoundOrderID, self.compoundOrderGUID, newOrderChain)

        Trace("Waiting for the order filling...")
        AssertMessage(self.eventOrderFilled.wait(TIMEOUT), "Order filling timeout!")
        Trace("Waiting for two orders canceling...")
        AssertMessage(self.eventOrderCanceled.wait(TIMEOUT), "Order canceling timeout!")

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
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace("OnOrderChanged error: Code: {} Description: {}".format(dispatchedCQGError.Code,
                                                                          dispatchedCQGError.Description))
            return

        dispatchedOrder = win32com.client.Dispatch(cqgOrder)
        properties = win32com.client.Dispatch(dispatchedOrder.Properties)
        gwStatus = properties(constants.opGWStatus)
        quantity = properties(constants.opQuantity)
        compoundOrderID = properties(constants.opCompoundOrderID)
        compoundOrderGUID = properties(constants.opCompoundOrderGUID)
        instrument = properties(constants.opInstrumentName)

        Trace("OnOrderChanged: compound order ID: {}; change type: {}; GW status: {}; Quantity: {}; Instrument: {}"
              .format(compoundOrderID, changeType, gwStatus, quantity, instrument))

        if changeType != constants.ctChanged:
            return

        if gwStatus.Value == constants.osInOrderBook:
            Trace("Compound order leg is placed!")
            self.compoundOrderID = compoundOrderID
            self.compoundOrderGUID = compoundOrderGUID
            self.expectedPlacedOrdersCount -= 1
            if (self.expectedPlacedOrdersCount == 0):
                self.eventOrderPlaced.set()
        if gwStatus.Value == constants.osFilled:
            Trace("Compound order leg is filled!")
            self.eventOrderFilled.set()
        if gwStatus.Value == constants.osCanceled:
            Trace("Another compound order leg is canceled!")
            self.expectedCanceledOrdersCount -= 1
            if (self.expectedCanceledOrdersCount == 0):
                self.eventOrderCanceled.set()


CELEnvironment.StartSample(CompoundOrdersPlacingSample)
