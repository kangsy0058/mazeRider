from bluetooth import *

class BLU:

    def __init__(self, st):
        client_socket = BluetoothSocket( RFCOMM )
        client_socket.connect(("98:D3:11:FD:35:46", 1))
        client_socket.send(st)
        print("Finished")
        client_socket.close()


