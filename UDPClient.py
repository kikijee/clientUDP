from socket import *
import pickle
import os

class UDP:
    def __init__ (self):
        self.PAYLOAD_LENGTH = 0
        self.UDP_SYN_FLAG = 0
        self.UDP_ACK_FLAG = 0
        self.UDP_FIN_FLAG = 0
        self.HTTP_GET_REQUEST = 0
        self.HTTP_RESPONSE_STATUS_CODE = 0 
        self.HTTP_CLIENT_VERSION = 0
        self.HTTP_REQUEST_PATH = "" # X length = payload length
        self.HTTP_INCLUDED_OBJECT = 0

serverName = 'localhost'
serverPort = 18111
clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_syn(dataObj):
    dataObj.UDP_SYN_FLAG = 1      # syn message
    dataObj.PAYLOAD_LENGTH = 1    # 1 for syn
    data_string = pickle.dumps(dataObj)
    clientSocket.sendto(data_string,(serverName, serverPort)) # sends udpclient class

if __name__ == '__main__':
    while 1:
        print("1.) Get file from server\n2.) Quit")
        message = input('select option: ')
        if(message == '2'): break
        elif(message != '1'):print("invalid option")
        else:
            clientDatagram = UDP()
            os.system('cls')
            print("HTTP VERSION\n1.)HTTP 1.0\n2.)HTTP 1.1")
            message = input('select option: ')
            if(message != '1' and message != '2'): print("invalid option")
            else:
                if(message == '1'): clientDatagram.HTTP_CLIENT_VERSION = 1.0
                elif(message == '2'): clientDatagram.HTTP_CLIENT_VERSION = 1.1
                send_syn(clientDatagram)
                print("sent SYN")
                dataGramE, serverAddress = clientSocket.recvfrom(2048)
                dataGram = pickle.loads(dataGramE)
                print("recieved ACK")
            
            

            '''
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            print (modifiedMessage.decode())
            '''
            #clientSocket.close()
