# The sample demonstrates how to make a request for quoutes (RFQ)

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
EXPRESSION = "UDS(-C.US.EP?1+C.US.EP?2, CalC)"

# Events waiting time
TIMEOUT = 30


class RFQSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.account = None
        self.dispatchedRFQ = None
        self.eventGatewayIsUp = threading.Event()
        self.eventGatewayIsDown = threading.Event()
        self.eventAccountIsReady = threading.Event()
        self.eventRFQIsReady = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def Start(self):
        Trace("Connecting to GW")
        self.celEnvironment.cqgCEL.GWLogon(LOGIN, PASSWORD)

        Trace("Waiting for GW connection...")
        AssertMessage(self.eventGatewayIsUp.wait(TIMEOUT), "GW connection timeout!")

        self.celEnvironment.cqgCEL.AccountSubscriptionLevel = constants.aslAccountsOnly
        Trace("Waiting for accounts coming...")
        AssertMessage(self.eventAccountIsReady.wait(TIMEOUT), "Accounts coming timeout!")

        accounts = win32com.client.Dispatch(self.celEnvironment.cqgCEL.Accounts)
        # Select an account that has enablement for UDS
        self.account = win32com.client.Dispatch(accounts.ItemByIndex(0))

        Trace("Define RFQ...")
        self.dispatchedRFQ = win32com.client.Dispatch(
            self.celEnvironment.cqgCEL.CreateStrategyQuoteRequest(self.account, EXPRESSION))
        self.dispatchedRFQ.Side = constants.osdUndefined
        self.dispatchedRFQ.Size = -1
        self.dispatchedRFQ.AlgorithmID = 100
        self.dispatchedRFQ.AlgorithmDescription = "My-Algo"

        Trace("Invoke RFQ...")
        self.celEnvironment.cqgCEL.InvokeStrategyQuoteRequest(self.dispatchedRFQ)

        Trace("Waiting for RFQ result...")
        AssertMessage(self.eventRFQIsReady.wait(TIMEOUT), "RFQ result waiting timeout!")

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

    def OnStrategyQuoteRequestResolved(self, cqgRFQ, isProcessed, cqgError):
        Trace("OnStrategyQuoteRequestResolved!")

        if cqgError is not None:
            error = win32com.client.Dispatch(cqgError)
            Trace("OnStrategyQuoteRequestResolved error: Code: {} Description: {}".format(error.Code,
                                                                                          error.Description))
            self.eventRFQIsReady.set()
            return

        rfq = win32com.client.Dispatch(cqgRFQ)
        Trace("OnStrategyQuoteRequestResolved: requested symbol: {} isProcessed: {}".format(rfq.Symbol, isProcessed))
        self.eventRFQIsReady.set()


CELEnvironment.StartSample(RFQSample)
