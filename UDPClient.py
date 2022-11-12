from socket import *
import pickle
import os

class UDP:
    def __init__ (self):
        self.PAYLOAD_LENGTH = 0 # X length = payload length
        self.UDP_SYN_FLAG = 0
        self.UDP_ACK_FLAG = 0
        self.UDP_FIN_FLAG = 0
        self.HTTP_GET_REQUEST = 0
        self.HTTP_RESPONSE_STATUS_CODE = 0 
        self.HTTP_CLIENT_VERSION = 0
        self.HTTP_REQUEST_PATH = "" 
        self.TEXT = ""
        self.HTTP_INCLUDED_OBJECT = ""


serverName = 'localhost'
serverPort = 18111
clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_syn():
    dataObj = UDP()
    dataObj.UDP_SYN_FLAG = 1      # syn message
    dataObj.PAYLOAD_LENGTH = 1    # 1 for syn
    data_string = pickle.dumps(dataObj)
    clientSocket.sendto(data_string,(serverName, serverPort)) # sends udpclient class

def send_http_req(path,ver):
    dataObj = UDP()
    dataObj.HTTP_GET_REQUEST = 1
    dataObj.HTTP_REQUEST_PATH = path
    dataObj.HTTP_CLIENT_VERSION = ver
    data_string = pickle.dumps(dataObj)
    clientSocket.sendto(data_string,(serverName, serverPort)) # sends udpclient class

def send_ack():
    dataObj = UDP()
    dataObj.UDP_ACK_FLAG = 1      # ack message
    data_string = pickle.dumps(dataObj)
    clientSocket.sendto(data_string,(serverName, serverPort)) # sends udpclient class

def send_fin():
    dataObj = UDP()
    dataObj.UDP_FIN_FLAG = 1      # fin message
    data_string = pickle.dumps(dataObj)
    clientSocket.sendto(data_string,(serverName, serverPort)) # sends udpclient class

if __name__ == '__main__':
    
    while 1:
        clientVer = 0
        print("1.) Get file from server\n2.) Quit")
        message = input('select option: ')
        if(message == '2'): break
        elif(message != '1'):print("invalid option")
        else:
            os.system('cls')
            print("HTTP VERSION\n1.)HTTP 1.0\n2.)HTTP 1.1")
            message = input('select option: ')
            if(message != '1' and message != '2'): print("invalid option")
            else:
                if(message == '1'): clientVer = 1.0
                elif(message == '2'): clientVer = 1.1
                send_syn()
                print("sent SYN")
                dataGramE, serverAddress = clientSocket.recvfrom(2048)
                dataGram = pickle.loads(dataGramE)
                if(dataGram.UDP_SYN_FLAG ==  1 and dataGram.UDP_ACK_FLAG == 1):
                    print("recieved SYN and ACK")
                    send_ack()

                path = input("please enter path: ")
                while path:
                    send_http_req(path,clientVer)
                    print("sent http req")
                    dataGramE, serverAddress = clientSocket.recvfrom(2048)
                    dataGram = pickle.loads(dataGramE)
                    if(dataGram.HTTP_RESPONSE_STATUS_CODE == 404):
                        print("404 Page not found")
                        break
                    else:
                        if '\n' in dataGram.TEXT: print(f"202, {dataGram.TEXT}", end = "")
                        else: print(f"202, {dataGram.TEXT}")
                        if(not dataGram.HTTP_INCLUDED_OBJECT):
                          break
                        else:
                            if(dataGram.HTTP_CLIENT_VERSION == 1.1): path = dataGram.HTTP_INCLUDED_OBJECT
                            else:
                                path = dataGram.HTTP_INCLUDED_OBJECT
                                send_fin()
                                print("sent FIN")
                                dataGramE, serverAddress = clientSocket.recvfrom(2048)
                                dataGram = pickle.loads(dataGramE)
                                if(dataGram.UDP_FIN_FLAG ==  1 and dataGram.UDP_ACK_FLAG == 1):
                                    print("recieved FIN & ACK")
                                    send_ack()
                                    print("sent ACK")

                send_fin()
                print("sent FIN")
                dataGramE, serverAddress = clientSocket.recvfrom(2048)
                dataGram = pickle.loads(dataGramE)
                if(dataGram.UDP_FIN_FLAG ==  1 and dataGram.UDP_ACK_FLAG == 1):
                    print("recieved FIN & ACK")
                    send_ack()
                    print("sent ACK")
                    

            
            

            '''
            modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
            print (modifiedMessage.decode())
            '''
            #clientSocket.close()
