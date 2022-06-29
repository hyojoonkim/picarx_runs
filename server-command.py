#!/usr/bin/python3           # This is server.py file
import socket                                         


HOST = '0.0.0.0'
PORT = 9999                                           

def main():
    # create a socket object
    serversocket = socket.socket(
    	        socket.AF_INET, socket.SOCK_STREAM) 
    
    # get local machine name
    #host = socket.gethostname()                           
    
    
    # bind to the port
    #serversocket.bind((host, port))                                  
    serversocket.bind((HOST, PORT))                                  
    
    # queue up to 5 requests
    serversocket.listen(5)                                           
    
    while True:

        print("Waiting for a client to connect....\n")

        # establish a connection
        clientsocket,addr = serversocket.accept()      
     
        print("Got a connection from %s" % str(addr))
         
        msg = 'Thank you for connecting'+ "\r\n"
        clientsocket.send(msg.encode('ascii'))
    
        # INPUT cycle
        while True:
            command = input("Enter command (f <duration>, b <duration>, speed <amount>, linetrack <duration>, exit): ")
            msg = command
            clientsocket.send(msg.encode('ascii'))

            if command == 'exit':
                print("Disconnecting client: {}\n".format(str(addr)))
                break
    
        clientsocket.close()

if __name__ == '__main__':
    main()
