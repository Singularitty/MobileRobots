import socket
import sys
import signal
from time import sleep
from threading import Lock

from pyparsing import line

HOST = "192.168.30.217"  # The server's hostname or IP address -> "Default Gateway" of hotspot
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
        #print(line.decode())
        return line.decode()

def connect():
    while(1):
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("trying to connect")
            soc.connect((HOST, PORT))
            return soc
        except Exception as e:
            print("Connection not sucessfull")
            #print(e)
            sleep(1)


class detection:
    
    def __init__(self,object_number, picture_dimensions, obj_dimensions, relative_positions, categories_number, categories):
        self.object_number = object_number
        self.picture_dimensions = picture_dimensions
        self.obj_dimensions = obj_dimensions
        self.relative_positions = relative_positions
        self.categories_number = categories_number
        self.categories = categories
        
    def get_position_of_object(self, target_category):
        if self.categories is not None or len(self.categories) > 0:
            for i, (category, _) in enumerate(self.categories):
                if category == target_category:
                    x_left, x_right = self.obj_dimensions[i][1], self.obj_dimensions[i][3]
                    #relative_x, relative_y = self.relative_positions[i]
                    x = (float(x_left) + float(x_right)) / 2 # position of the middle of the detection box
                    return x, float(x_left), float(x_right)
        return None, None, None

def detect_objects(shared_mem: list[detection], mutex: Lock):
    
    while(1):
        soc = connect()
    
        print("sucessfully connected")
        while True:
            b = Buffer(soc)
            start = b.get_line()
            #print("Start", start)
            
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
                        
                    objs = detection(object_number, picture_dimensions, obj_dimensions, relative_position, categories_number, categories)            
                
                    #print("Number of objects:", object_number)
                    #print("Picture Dimensions", picture_dimensions)
                    #print("Object Dimensions",obj_dimensions)
                    #print("Relative dimensions", relative_position)
                    #print("Number of categories:", categories_number)
                    #print(objs.categories)
                    
                    #print("Picture Dimensions", picture_dimensions)
                    #print(objs.get_position_of_object("bottle"))
                    #print("error", (480//2 - 65) - objs.get_position_of_object("bottle"))
                    
                    
                    if not mutex.locked():
                        mutex.acquire()
                        shared_mem[0] = objs
                        mutex.release()
                    
            except Exception as ex:
                try: 
                    soc.close()
                except:
                    print("socket not closable")
                #print(ex)
                print("Connection error")
                break

#detect_objects(0,0)