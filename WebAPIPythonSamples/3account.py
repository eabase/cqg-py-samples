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

# Request for a list of accounts this user is authorized to use and/ or monitor, empty message.
def resolve_account(msg_id=1, subscribe=None):
    client_msg = ClientMsg()
    information_request = client_msg.information_request.add()
    information_request.id = msg_id
    # send request with empty message by calling SetInParent()
    information_request.accounts_request.SetInParent()

    client.send_client_message(client_msg)
    server_msg = client.receive_server_message()


if __name__ == "__main__":
    client = webapi_client.WebApiClient()
    client.connect(host_name)
    logon(user_name, password)

    resolve_account()

    client.disconnect()
