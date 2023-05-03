import socket
from time import sleep

adapter_addr = 'F8:AD:CB:04:D0:0D'
#adapter_addr = '00:00:00:00:00:00'
port = 10
buf_size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, 
socket.BTPROTO_RFCOMM)

try:
        s.connect((adapter_addr, port))
except Exception as e:
    print("Connection not sucessfull")
    print(e)
    sleep(1)


while(True):
    try:
        print("Trying to receive data")
        s.bind((socket.BDADDR_ANY, port))
        print("binding")
        s.listen(5)
        print("listening")
        data = s.recv(1024)
        print("received [%s]" % data)
    except Exception as ex:
        print(ex)
        print("Connecting to server")
        sleep(1)
       
## Endless loop for testing the connection
while(True):
    try:
        s.connect((adapter_addr, port))
    except Exception as e:
        print("Connection not sucessfull")
        print(e)
        sleep(1)
        break
