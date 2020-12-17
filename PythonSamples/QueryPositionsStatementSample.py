# The sample demonstrates how to request open positions statement for a date. CQG IC must be logged to GW first.

import threading
import CELEnvironment
import time
from CELEnvironment import Trace
from CELEnvironment import AssertMessage
import win32com.client
from win32com.client import constants
from datetime import datetime, timedelta, timezone

# Replace it with real login before run
LOGIN = "your_gw_login"
PASSWORD = "your_gw_password"

# Events waiting time
TIMEOUT = 10


class QueryPositionsStatementSample(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.eventGatewayIsUp = threading.Event()
        self.eventGatewayIsDown = threading.Event()
        self.account = None
        self.eventAccountIsReady = threading.Event()
        self.eventPositionsStatementReady = threading.Event()

    def Init(self, celEnvironment):
        self.celEnvironment = celEnvironment

    def Start(self):
        Trace("Connecting to GW")
        self.celEnvironment.cqgCEL.GWLogon(LOGIN, PASSWORD)

        Trace("Waiting for GW connection...")
        AssertMessage(self.eventGatewayIsUp.wait(TIMEOUT), "GW connection timeout!")

        self.celEnvironment.cqgCEL.AccountSubscriptionLevel = constants.aslNone
        self.celEnvironment.cqgCEL.AccountSubscriptionLevel = constants.aslAccountsOnly
        Trace("Waiting for accounts coming...")
        AssertMessage(self.eventAccountIsReady.wait(TIMEOUT), "Accounts coming timeout!")

        accounts = win32com.client.Dispatch(self.celEnvironment.cqgCEL.Accounts)
        self.account = win32com.client.Dispatch(accounts.ItemByIndex(0))
        for account in accounts:
            Trace("GW Account id: {} name: {}".format(account.GWAccountID, account.GWAccountName))

        statementDate = datetime.now(timezone.utc) - timedelta(days=1)

        Trace("Request positions statement for GW account ID = {} for date: {}".format(self.account.GWAccountID,
                                                                                       statementDate))

        self.celEnvironment.cqgCEL.QueryPositionsStatement(self.account.GWAccountID, statementDate)

        Trace("Waiting for positions statement coming...")
        AssertMessage(self.eventPositionsStatementReady.wait(TIMEOUT), "Positions statement coming timeout!")

        Trace("Logoff from GW")
        self.eventGatewayIsDown.clear()
        self.celEnvironment.cqgCEL.GWLogoff()
        AssertMessage(self.eventGatewayIsDown.wait(TIMEOUT), "GW disconnection timeout!")

        Trace("Done!")

    def OnGWConnectionStatusChanged(self, connectionStatus):
        if (connectionStatus == constants.csConnectionUp):
            Trace("GW connection is UP!")
            self.eventGatewayIsUp.set()
        if (connectionStatus == constants.csConnectionDown):
            Trace("GW connection is DOWN!")
            self.eventGatewayIsDown.set()

    def OnAccountChanged(self, change, account, position):
        if (change != constants.actAccountsReloaded):
            return

        Trace("Accounts are ready!")
        self.eventAccountIsReady.set()

    def OnPositionsStatementResolved(self, cqgPositionsStatement, cqgError):
        if (cqgError is not None):
            error = win32com.client.Dispatch(cqgError)
            Trace("OnPositionsStatementResolved error: Code: {} Description: {}".format(error.Code, error.Description))
            self.eventPositionsStatementReady.set()
            return

        positionsStatement = win32com.client.Dispatch(cqgPositionsStatement)
        Trace("Positions statement for account: {} for date: {} received".format(positionsStatement.GWAccountID,
                                                                                 positionsStatement.StatementDate))

        for position in positionsStatement.Positions:
            Trace("  open position for instrument: {} with average price: {} quantity: {} OTE: {} PL: {}".format(
                position.InstrumentName, position.AveragePrice, position.Quantity, position.OTE, position.ProfitLoss))

        self.eventPositionsStatementReady.set()


# If CQGCEL.APIConfiguration must be customized then do it in this function
def CustomAPIConfiguration(APIConfiguration):
    Trace("Set UTC time zone. All time values passed to (received from) CQG API should correspond to this setting. ")
    APIConfiguration.TimeZoneCode = constants.tzUTC


CELEnvironment.StartSample(QueryPositionsStatementSample, CustomAPIConfiguration)
