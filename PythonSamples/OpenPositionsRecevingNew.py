# The sample demonstrates how to request orders and open positions and observe changes on every price change
# Press Enter to interrupt the observing and stop the sample

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

# Events waiting time
TIMEOUT = 10


class OpenPositionsReceivingSampleNew(CELEnvironment.CELSinkBase):
    def __init__(self):
        self.eventGatewayIsUp = threading.Event()
        self.eventGatewayIsDown = threading.Event()
        self.eventAccountIsReady = threading.Event()
        self.eventOrdersQueryIsReady = threading.Event()

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

        Trace("Subscribe to open positions of all accounts")
        accounts = win32com.client.Dispatch(self.celEnvironment.cqgCEL.Accounts)
        for account in accounts:
            account.AutoSubscribeInstruments = True
            account.PositionSubcriptionLevel = constants.pslSnapshotAndUpdates
            Trace("GW Account id: {} name: {}".format(account.GWAccountID, account.GWAccountName))

        Trace("Select the first account")
        interestingAccount = win32com.client.Dispatch(accounts.ItemByIndex(0))

        Trace("Query orders in NotFinal state for account (gw id: {} name: {})".format(interestingAccount.GWAccountID,
                                                                                       interestingAccount.GWAccountName))
        ordersRequest = self.celEnvironment.cqgCEL.CreateOrdersRequest()
        ordersRequest.Account = interestingAccount
        ordersRequest.StatusFilter = constants.osfNotFinal
        ordersRequest.Date = datetime.now(timezone.utc)
        ordersRequest.Side = constants.osdUndefined

        self.orderQuery = self.celEnvironment.cqgCEL.RequestOrders(ordersRequest)

        Trace("Waiting for orders query completeness...")
        AssertMessage(self.eventOrdersQueryIsReady.wait(TIMEOUT), "Orders query timeout!")

        Trace("press Enter to stop..")
        input()

        Trace("Logoff from GW")
        self.eventGatewayIsDown.clear()
        self.celEnvironment.cqgCEL.GWLogoff()
        AssertMessage(self.eventGatewayIsDown.wait(TIMEOUT), "GW disconnection timeout!")

        Trace("Done!")

    def OnQueryProgress(self, cqgOrdersQuery, cqgError):
        if cqgError is not None:
            dispatchedCQGError = win32com.client.Dispatch(cqgError)
            Trace("OnQueryProgress - error: Code: {} Description: {}".format(dispatchedCQGError.Code,
                                                                             dispatchedCQGError.Description))
            self.eventOrdersQueryIsReady.set()
            return

        ordersQuery = win32com.client.Dispatch(cqgOrdersQuery)
        Trace("OnQueryProgress - account {} has {} order(s)".format(ordersQuery.Account.GWAccountName,
                                                                    ordersQuery.Orders.Count))

        for order in ordersQuery.Orders:
            Trace("     ORDER for instrument: {} limit price: {} stop price: {}".format(order.InstrumentName,
                                                                                        order.LimitPrice,
                                                                                        order.StopPrice))

        if ordersQuery.Orders.Count == 0 or ordersQuery.LastChunk:
            Trace("Orders query is completed!")
            self.eventOrdersQueryIsReady.set()

    def OnGWConnectionStatusChanged(self, connectionStatus):
        if connectionStatus == constants.csConnectionUp:
            Trace("GW connection is UP!")
            self.eventGatewayIsUp.set()
        if connectionStatus == constants.csConnectionDown:
            Trace("GW connection is DOWN!")
            self.eventGatewayIsDown.set()

    def OnAccountChanged(self, change, cqgAccount, cqgPosition):
        if change == constants.actPositionAdded:
            account = win32com.client.Dispatch(cqgAccount)
            position = win32com.client.Dispatch(cqgPosition)
            Trace("OnAccountChanged - open position is added for {} account - "
                  "instrument: {} average price: {} quantity: {} OTE: {} PL: {}".format(account.GWAccountName,
                                                                                        position.InstrumentName,
                                                                                        position.AveragePrice,
                                                                                        position.Quantity,
                                                                                        position.OTE,
                                                                                        position.ProfitLoss))

        if change == constants.actPositionChanged:
            account = win32com.client.Dispatch(cqgAccount)
            position = win32com.client.Dispatch(cqgPosition)
            Trace("OnAccountChanged - open position is changed for {} account - "
                  "instrument: {} average price: {} quantity: {} OTE: {} PL: {}".format(account.GWAccountName,
                                                                                        position.InstrumentName,
                                                                                        position.AveragePrice,
                                                                                        position.Quantity,
                                                                                        position.OTE,
                                                                                        position.ProfitLoss))

        if change == constants.actAccountsReloaded:
            Trace("OnAccountChanged - Accounts are ready!")
            self.eventAccountIsReady.set()


# If CQGCEL.APIConfiguration must be customized then do it in this function
def CustomAPIConfiguration(APIConfiguration):
    Trace("Set UTC time zone. All time values passed to (received from) CQG API should correspond to this setting. ")
    APIConfiguration.TimeZoneCode = constants.tzUTC
    # If you do not want to see positions change on each price change then comment the row below
    APIConfiguration.FireEventOnChangedPrices = True


CELEnvironment.StartSample(OpenPositionsReceivingSampleNew, CustomAPIConfiguration)
