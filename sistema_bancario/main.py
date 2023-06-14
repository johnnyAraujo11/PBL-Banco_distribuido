import l as lamp
from servers import SERVERS
import Socket_TPC
from web import API


#socket = Socket_TPC.Server_Bank(name="server2", host="localhost", port_TCP=60000)
#socket.connect()

API.run(name='server2', address='localhost', port=60000)