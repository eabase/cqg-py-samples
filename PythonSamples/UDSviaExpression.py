# The sample demonstrates how to place strategy order by expression

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
STRATEGY = "UDS(-C.US.CLE?1+C.US.CLE?2, CalC)"

# Events waiting time
TIMEOUT = 10


class UDSviaExpressionSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.account = None
        self.instrument = None
        self.eventGatewayIsUp = threading.Event()
        self.eventGatewayIsDown = threading.Event()
        self.eventAccountIsReady = threading.Event()
        self.eventUDSIsReady = threading.Event()
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

        accounts = win32com.client.Dispatch(self.celEnvironment.cqgCEL.Accounts)
        # Select an account that has enablement for UDS
        self.account = win32com.client.Dispatch(accounts.ItemByIndex(0))

        Trace("Creating a strategy order...")
        dispatchedOrder = win32com.client.Dispatch(
            self.celEnvironment.cqgCEL.CreateStrategyOrderByExpression(constants.otLimit, STRATEGY, self.account, None,
                                                                       -1, constants.osdUndefined, 3.30))
        Trace("Placing the strategy order...")
        dispatchedOrder.Place()

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

    def OnStrategyDefinitionProgress(self, cqgDefinition, cqgError):
        if cqgError is not None:
            error = win32com.client.Dispatch(cqgError)
            Trace("OnStrategyDefinitionProgress error: Code: {} Description: {}".format(error.Code, error.Description))
            return

        dispatchedDefinition = win32com.client.Dispatch(cqgDefinition)
        Trace("OnStrategyDefinitionProgress: requested symbol: {} GW symbol: {} status: {}".format(
            dispatchedDefinition.RequestString, dispatchedDefinition.Symbol, dispatchedDefinition.Status))
        if dispatchedDefinition.Status == constants.srsSuccess:
            self.eventUDSIsReady.set()

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

        Trace("OnOrderChanged: change type: {}; GW status: {}; Quantity: {}; Instrument: {}"
              .format(changeType, gwStatus, quantity, instrument))

        if changeType != constants.ctChanged:
            return

        if gwStatus.Value == constants.osInOrderBook:
            Trace("UDS order is placed!")
            self.eventOrderPlaced.set()


CELEnvironment.StartSample(UDSviaExpressionSample)
