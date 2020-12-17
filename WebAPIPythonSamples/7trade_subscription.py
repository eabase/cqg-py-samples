from WebAPI.webapi_1_pb2 import *
from WebAPI import webapi_client

host_name = 'wss://demoapi.cqg.com:443'
user_name = ''
password = ''

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

def request_trade_subscription():
    client_msg = ClientMsg()
    request = client_msg.trade_subscription.add()
    # user-defined ID of a request that should be unique to match with possible OrderRequestReject.
    request.id = 1
    request.subscribe = True
    # subscription_scope is an array, we use "append" to add subscription_scope
    request.subscription_scope.append(1) # 1 means order_status
    request.subscription_scope.append(2) # 2 means positions_status
    request.subscription_scope.append(3) # 3 means collateral_status
    client.send_client_message(client_msg)

    while True: 
        server_msg = client.receive_server_message()

if __name__ == "__main__":
    client = webapi_client.WebApiClient()
    client.connect(host_name)
    baseTime = logon(user_name, password)

    request_trade_subscription()

    client.disconnect()
