import socket
import sys
import os
import datetime
import signal
from time import sleep
from matplotlib import category

from pyparsing import line

HOST = "192.168.43.236"  # The server's hostname or IP address -> "Default Gateway" of hotspot
PORT = 8888

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Buffer:

    def __init__(self,sock):
        self.sock = sock
        self.buffer = b''

    def get_line(self):
        while b':' not in self.buffer:
            data = self.sock.recv(1024)
            if not data: # socket closed
                return None
            self.buffer += data
        line,sep,self.buffer = self.buffer.partition(b':')
        print(line.decode())
        return line.decode()

def interrupt_handler(signal, frame):
    print("Stopping data acquisition")
    sys.exit(0)

def connect():
    while(1):
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("trying to connect")
            soc.connect((HOST, PORT))
            return soc
        except Exception as e:
            print("Connection not sucessfull")
            print(e)
            sleep(1)

def main():
    print("start")
    
    while(1):
        soc = connect()
    
        print("sucessfully connected")
        while True:
            b = Buffer(soc)
            start = b.get_line()
            print("Start", start)
            
            try:
                if(int(start) == 12):
                    picture_dimensions = []
                    picture_dimensions.append(b.get_line())
                    picture_dimensions.append(b.get_line())
                    
                    obj_dimensions = []
                    categories = []
                    relative_position = []
                    object_number = b.get_line()
                    for i in range(int(object_number)):
                    
                        obj_dimensions.append([b.get_line(), b.get_line(), b.get_line(), b.get_line()])

                        categories_number = int(b.get_line())
                       # for j in range(categories_number):
                        categories.append([b.get_line(), b.get_line()])

                        relative_position.append([b.get_line(),b.get_line()])                    
                
                    print("Number of objects:", object_number)
                    print("Picture Dimensions", picture_dimensions)
                    print("Object Dimensions",obj_dimensions)
                    print("Relative dimensions", relative_position)
                    print("Number of categories:", categories_number)
                    print(categories)
            except Exception as ex:
                try: 
                    soc.close()
                except:
                    print("socket not closable")
                print(ex)
                print("Connection error")
                break
                    
   

if __name__ == "__main__":
    signal.signal(signal.SIGINT, interrupt_handler)
    main()
