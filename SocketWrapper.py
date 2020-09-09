#Autor: Elias Lehnert
import socket
import json

class SocketWrapper:
    def __init__(self,port,hostname = socket.gethostname()):
        print("Hostname: ",hostname)
        self.__mSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__mSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__mHostName = hostname
        self.__mPort = port
        self.__pHostname = None
        self.__connectionEstablished = False
        self.__listening = False
        self.__dataLimit = 4096

    def waitForConnection(self):
        #Vor.: Keine
        #Eff.: Der Socket wartet auf eine eingehende Verbindung. Gab es bei der Verbindung Komplikationen, wird ein Fehler ausgegeben
        if not self.__connectionEstablished:
            self.__mSock.bind((self.__mHostName,self.__mPort))
            self.__mSock.listen(1)
            self.__mSock, self.__pHostname = self.__mSock.accept()
            self.__connectionEstablished = True
            self.__listening = True
        else:
            raise Exception("Error: Connection of single partner socket on port {} already established!".format(self.__mPort))

    def establishConnection(self,address):
        #Vor.:  address ist die Addresse oder der Hostname eines Rechners in Form eines Strings
        #Eff.:  Der Socket versucht mit der Addresse Verbindung aufzunehmen. Schlägt dies fehl, liefert er
        #       eine Fehlermeldung.
        if not self.__connectionEstablished:
            self.__mSock.connect((address,self.__mPort))
            self.__connectionEstablished = True
        else:
            raise Exception("Error: Connection for socket on {} on port {} already established!".format(self.__mHostName,self.__mPort))

    def breakConnection(self):
        #Vor.:  Der SocketWrapper befindet sich in einer Verbindung mit einem anderen Rechner
        #Eff.:  Die Verbindung wird getrennt
        self.__mSock.shutdown(socket.SHUT_RDWR)
        self.__mSock.close()
        del self

    def sendData(self,dictionairy):
        #Vor.:  'dictionairy' ist ein valides Python-Dictionairy.
        #Eff.:  Das dictionairy wird als JSON String enkodiert und über den Socket versendet
        if not self.__connectionEstablished:
            raise Exception("Socket for \"{}\" with port {}: No connection established; Unable to send data".format(self.__mHostName,self.__mPort))
        
        self.__mSock.send(bytes(json.dumps(dictionairy),'utf-8'))

    def recieveData(self):
        #Vor.: keine
        #Erg.: Wurde ein Datenpaket abgefangen, wurde es in Form eines dictonairy geliefert.
        #      Wurde kein Datenpaket abgefangen, wurde None geliefert.
        if not self.__connectionEstablished:
            raise Exception("Socket for \"{}\" with port {}: No connection established; Unable to recieve data".format(self.__mHostName,self.__mPort))
        
        byteData = self.__mSock.recv(self.__dataLimit)
    
        if(byteData == b""):
            return None
        dictionairy = json.loads(str(byteData,"utf-8"))
        return dictionairy
