# logging on is a prerequisite to accomplishing anything using the Web API.
# All other samples require a successful logon to work.
# The first step to logon is to build connection with the WebAPi Server.
# Second, logon message is built with valid credentials and sent as a client message.
# Success code in WebAPI when logon_result.result_code = 0.

from WebAPI.webapi_1_pb2 import *
from WebAPI import webapi_client

# the host_name is the stage server url we will connect to in demo environment.
host_name = 'wss://demoapi.cqg.com:443'
# user_name and password are two of four required parameters we need to send to the server
# however, different users can use same client_app_id and client_version, so we initialize
# these two parameters inside the logon() function.
user_name = ''
password = ''

def logon(user_name, password, client_app_id='WebApiTest', client_version='python-client'):
    # create a client_msg based on the protocol.
    client_msg = ClientMsg()
    # initialize the logon message, there are four required parameters.
    client_msg.logon.user_name = user_name
    client_msg.logon.password = password
    client_msg.logon.client_app_id = client_app_id
    client_msg.logon.client_version = client_version
    # see send_client_message() function in webapi_client.py in line 23.
    client.send_client_message(client_msg)
    # see receive_server_message() function in webapi_client.py in line 33.
    server_msg = client.receive_server_message()
    if server_msg.logon_result.result_code == 0:
        # in later samples, we will need to use base_time to complete the from_utc_time.
        # in the time_and_sales_request sample and the time_bar_request sample.
        return server_msg.logon_result.base_time
    else:
        # the text_message contains the reason why user cannot login.
        raise Exception("Can't login: " + server_msg.logon_result.text_message)

if __name__ == "__main__":
    # see WebApiClient() class in webapi_client.py in line 5.
    client = webapi_client.WebApiClient()
    # see connect() function in webapi_client.py in line 16.
    client.connect(host_name)
    logon(user_name, password)
    # see disconnect() function in webapi_client.py in line 19.
    client.disconnect()
