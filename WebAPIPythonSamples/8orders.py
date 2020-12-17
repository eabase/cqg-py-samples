from WebAPI.webapi_1_pb2 import *
from WebAPI import webapi_client

host_name = 'wss://demoapi.cqg.com:443'
user_name = ''
password = ''
resolveSymbolName = ''
trade_subscription_id = 1
request_id = 1

account_id = 16883045 # according to your account_id
contract_id = 1
cl_order_id = '1' # every order must have unique cl_order_id per trader per day
order_type = 1 # 1 means MKT 2 means LMT 3 means STP 4 means STL
duration = 1
side = 2 # 1 means buy and 2 means sell
uint32_qty = 1
is_manual = False

def logon(user_name, password, client_app_id='WebApiTest', client_version='python-client'):
    client_msg = ClientMsg()
    client_msg.logon.user_name = user_name
    client_msg.logon.password = password
    client_msg.logon.client_app_id = client_app_id
    client_msg.logon.client_version = client_version
    client.send_client_message(client_msg)
    server_msg = client.receive_server_message()
    if server_msg.logon_result.result_code == 0:
        return server_msg.logon_result.base_time
    else:
        raise Exception("Can't login: " + server_msg.logon_result.text_message)

def resolve_symbol(symbol_name, msg_id=1, subscribe=None):
    client_msg = ClientMsg()
    information_request = client_msg.information_request.add()
    information_request.id = msg_id
    if subscribe is not None:
        information_request.subscribe = subscribe
    information_request.symbol_resolution_request.symbol = symbol_name
    client.send_client_message(client_msg)

    server_msg = client.receive_server_message()
    return server_msg.information_report[0].symbol_resolution_report.contract_metadata

def request_trade_subscription(trade_subscription_id):
    client_msg = ClientMsg()
    request = client_msg.trade_subscription.add()
    request.id = trade_subscription_id
    request.subscribe = True
    request.subscription_scope.append(1) # 1 means order_status
    # request.subscription_scope.append(2) # 2 means positions_status
    # request.subscription_scope.append(3) # 3 means collateral_status
    client.send_client_message(client_msg)

    while True: 
        server_msg = client.receive_server_message()


def new_order_request(request_id, account_id, contract_id, cl_order_id, order_type, duration, side, uint32_qty, is_manual):
    client_msg = ClientMsg()
    order_request = client_msg.order_request.add()
    order_request.request_id = request_id
    order_request.new_order.order.account_id = account_id
    order_request.new_order.order.when_utc_time = 0
    order_request.new_order.order.contract_id = contract_id
    order_request.new_order.order.cl_order_id = cl_order_id
    order_request.new_order.order.order_type = order_type
    order_request.new_order.order.duration = duration
    order_request.new_order.order.side = side
    order_request.new_order.order.uint32_qty = uint32_qty
    order_request.new_order.order.is_manual = is_manual
    # add the limit_price when order_type is LIMIT
    # order_request.new_order.order.limit_price = 9150

    client.send_client_message(client_msg)
    while True:
        server_msg = client.receive_server_message()
        if server_msg.trade_snapshot_completion is not None:
            server_msg = client.receive_server_message()
            break


if __name__ == "__main__":
    client = webapi_client.WebApiClient()
    client.connect(host_name)
    baseTime = logon(user_name, password)
    contract_metadata = resolve_symbol(resolveSymbolName)

    request_trade_subscription(trade_subscription_id)

    new_order_request(request_id, account_id, contract_id, cl_order_id, order_type, duration, side, uint32_qty, is_manual)

    client.disconnect()
