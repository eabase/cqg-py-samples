Introduction
------------
There are 8 samples inside the package:
1logon 			Connect to API server and send client message with login credentials
2meta			1logon, and send client message to associate symbol with contract id, and get metadata
3account 		1logon, and send client message to receive account information associated with user id
4real_time 		1logon, 2meta, and send client message to subscribe to real time market data updates
5bar_time		1logon, 2meta, and send client message to request bar data starting at specific time
6time_and_sales		1logon, 2meta, and send client message to request time and sales data starting at a specific time
7trade_subscription 	1logon, 2meta, and send client message to subscribe to orders, position, or collateral updates
8orders			1logon, 2meta, and send client message to place or modify an order

How to use:
----------
Please follow the steps introduced below to test the samples:
1. In order to use the samples, a user needs to have python 3.x installed
	(http://www.python.org/)
2. In each sample, a user needs to modify the code according to his purpose
3. Open Commend Prompt, go to the sample's path, run the commend like:
	python 1logon.py
	python 4real_time.py

Package content:
---------------
\google           - part of Google Protocol Buffers library

\webapi
webapi_1_pb2.py   - protocol wrapper for Python, compiled from .proto
metadata_1_pb2.py
rules_1_pb2.py
webapi_client.py  - helper class for connection to WebAPI server
websocket.py      - WebSocket client library (https://pypi.python.org/pypi/websocket-client/)

\common
decimal_pb2.py    - protocol wrapper for Python, compiled from .proto
shared_1_pb2.py
timestamp_pb2.py

\proto
\proto\WebAPI
\proto\common
protocol files    - readable description of protocol messages in ProtoBuf format, version 1.134 last upgrade date: 12/20/2019
	            (https://partners.cqg.com/api-resources/web-api/documentation)
protoc.exe        - compiler to convert .proto files to _pb2.py, version 3.11.3 last upgrade date: 02/01/2020
generater.cmd 	  - double click to generate webapi_1_pb2.py in webapi folder compiled from protocol files

NOTICE:
-------------
When webapi_1.proto updates, a user may obtain more information from the server by using the updated protocol:

1. Go to this page and open the Production Protocol link:
   	(http://partners.cqg.com/api-resources/continuum-connect/documentation)
2. Save the protocol files into your proto folder
3. Follow the instruction in ReadMe.txt in proto folder

CONTACT:
-------------
If you have problems, questions, ideas or suggestions, please contact us:
continuum@cqg.com
