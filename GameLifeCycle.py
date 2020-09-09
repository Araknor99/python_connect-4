#Autor: Elias Lehnert
from SocketWrapper import SocketWrapper
from Feld import *
from turtle import *

import random as r
import math
import time
import threading
import sys

class LifeCycle:
    def __init__(self):
        self.__sock = SocketWrapper(8008)
        self.__player = "None"
        self.__currentPlayer = None
        self.__players = ["red","yellow"]
        self.__turnNumber = 0
        self.__won = False
        self.__canPlay = True
        self.__mFeld = spielfeld()
        self.__waitForConnection = False
        self.__mFeld.setzeEingaenge("white")
        self.__stonefalling = False

    def findPartner(self):
        #Vor.:  keine
        #Eff.:  In einem Text-Prompt in der Kommandozeile wurde erfragt, ob man sich 'verbinden', oder auf eine Verbindung 'warten' will.
        #       Wählte man 'warten wird auf einen Verbindungsaufbau unebschränkt lange gewartet.
        #       Wählte man 'verbinden' fragte das Programm in einem weiteren Prompt die Addresse/den Hostnamen.
        #       Bei Eingabe hat das Programm versucht, sich mit dem Host zu verbinden.
        #       Wählte man weder die eine, noch die andere Option, wurde die Auswahl erneut erfragt.
        #       Des Weiteren wurde die Spielstein Farbe des Spielers auf rot gesetzt wenn er sich verbinden will,
        #       ansonsten auf gelb.
        while True:
            userInput = input("Mit einem Partner verbinden oder warten? (verbinden|warten)\n>>>")
            if userInput == "verbinden":
                self.__player = "red"
                userInput = input("Mit welcher Addresse willst du dich verbinden?\n>>>")
                trialCount = 0
                while True:
                    try:
                        self.__sock.establishConnection(userInput)
                        break
                    except:
                        if trialCount == 10:
                            raise Exception("Fehler: verbinden mit Addresse nicht gelungen")
                        trialCount += 1
                        time.sleep(0.5)
                break
            elif userInput == "warten":
                self.__player = "yellow"
                self.__waitForConnection = True
                self.__sock.waitForConnection()
                break
            else:
                print("Bitte gebe 'verbinden' oder 'warten' ein.")

    def startGame(self):
        #Vor.:  keine
        #Eff.:  Der Spieler der anfängt wurde von dem Programm, was den Verbindungsaufbau wählte ausgewählt und an den anderen gesendet.
        #       Ist man die Person, die wartete, empfing man dies und die eigenen Zustände wurden danach ausgerichtet.
        #       Ist man der Spieler, der anfängt, so wurden die Eingänge auf grün gesetzt.
        #       Des Weiteren wurden die Farben des Spielers und die des Spielers der anfängt ausgegeben.
        if self.__waitForConnection:
            r.seed()
            self.__currentPlayer = r.choice(self.__players)
            dict = {"currentPlayer":self.__currentPlayer}
            self.__sock.sendData(dict)
            
        else:
            while True:
                dict = self.__sock.recieveData()
                if dict != None:
                    self.__currentPlayer = dict["currentPlayer"]
                    break

        if self.__currentPlayer == "yellow":
                self.__players.reverse()

        if self.__currentPlayer == self.__player:
            self.__mFeld.setzeEingaenge("green")
        else:
            thread = threading.Thread(target=self.waitForAnswer,args=())
            thread.daemon = True
            thread.start()

        print("Du bist Farbe {}!".format(self.__player))
        print("{} fängt an!".format(self.__currentPlayer))

    def waitForAnswer(self):
        #Vor.:  keine
        #Eff.:  Das Programm wartet unbeschränkt lange auf ein Datenpaket des anderen Programmes in entsprechender Form.
        #       Bei Annahme eines Datenpaketes wird der entsprechende Stein gefärbt und 
        while True:
            data = self.__sock.recieveData()
            
            if data != None:
                self.__currentPlayer = data["currentPlayer"]
                self.__turnNumber = data["turnNumber"]
                x = data["stoneFieldX"]
                y = data["stoneFieldY"]
                stoneColor = data["stoneColor"]
                self.__stonefalling = True
                self.__mFeld.setzeSteinFarbe(x,y,stoneColor)
                thread = threading.Thread(target=self.moveStoneDown,args=[self.__mFeld.steinFuerPosition(x,y)])
                thread.start()
                break
    
    def moveStoneDown(self,stone):
        #Vor.:  stone ist ein Stein des Feldes.
        #Eff.:  Der Stein wurde bis erreichen einer Ruheposition alle viertel Sekunde eine Stelle nach unten bewegt.
        #       Das Programm erreichte bis zu dem Erreichen dieser Position in einen Zustand gesetzt, indem der Spieler nicht mit dem Feld agieren kann.
        #       Bei Erreichen dieser Position wurde überprüft, ob einer der Spieler gewonnen hat, oder ob das weitere Spielen noch möglich ist.
        #       Hat ein Spieler gewonnen, so wurde das in der Kommandozeile ausgegeben.
        #       Kann nicht mehr weiter gespielt werden, ist 'Unentschieden!' ausgegeben wurden.
        #       Die Eingänge der Person, die nun dran ist, wurden überprüft und die Zugnummer wurde für die Person angegeben.
        #       Die Eingänge der Person, die dran war, wurden auf weiß gesetzt. Des Weiteren konnte dieser nun nicht mehr mit dem Feld agieren, bis der
        #       andere Spieler ein Stein setzte.
        cStone = stone

        while not self.__mFeld.bewegeStein(cStone):
            posx,posy = cStone.gibFeldPosition()
            cStone = self.__mFeld.steinFuerPosition(posx,posy-1)
            time.sleep(0.25)
        self.__stonefalling = False

        
        for player in self.__players:
            ret = self.__mFeld.uberpruefeGewonnen(player)
            if ret == player:
                print("Spieler {} hat gewonnen!".format(player))
                self.__won = True
                return
            elif ret == "NoPlay":
                self.__canPlay = False
                print("Unentschieden!")
                return
        
        if self.__currentPlayer == self.__player:
            self.__mFeld.pruefeEingaenge()
            print("\nZug nr. {}\nDu bist dran!".format(self.__turnNumber+1))
        else:
            self.__mFeld.setzeEingaenge("white")
            thread = threading.Thread(target=self.waitForAnswer,args=())
            thread.daemon = True
            thread.start()
            


    def handleClick(self,x,y):
        #Vor.:  x und y sind float-Koordinaten
        #Eff.:  Ist der Zustand des Spieles richtig und ist der Spieler dran, wurde überprüft ob der Spieler auf einen grünen Stein geklickt hat.
        #       Ist das der Fall so wird dieser auf die Spielerfarbe gesetzt und die Veränderung wird der anderen Person übermittelt.
        #       Das Programm versetzte sich nun in einen Zustand, wo der Spieler nicht mehr mit dem Feld interagieren konnte, bis der eingefügte
        #       Stein eine Ruheposition erreichte und der andere Spieler einen Stein setzt.
        if self.__currentPlayer == self.__player and not self.__stonefalling and not self.__won and self.__canPlay:
            if self.__mFeld.handleClick(x,y,self.__currentPlayer):
                stein = self.__mFeld.angeklickterStein(x,y)
                posX,posY = stein.gibFeldPosition()
                self.__turnNumber += 1
                self.__currentPlayer = self.__players[self.__turnNumber % 2]

                dict = {"turnNumber":self.__turnNumber, "currentPlayer":self.__currentPlayer,
                        "stoneFieldX":posX, "stoneFieldY":posY, "stoneColor":stein.gibFarbe()}
                self.__sock.sendData(dict)

                self.__stonefalling = True

                thread = threading.Thread(target=self.moveStoneDown,args=[self.__mFeld.steinFuerPosition(posX,posY)])
                thread.daemon = True
                thread.start()

if __name__ == "__main__":
    setworldcoordinates(10,10,700,700)
    points = ()

    for i in range(16):
        points = points + (
            (math.cos(math.radians(360/16*i)) * 45,
            math.sin(math.radians(360/16*i)) * 45),
        )

    screen = getscreen()
    screen.register_shape("circle",points)

    cycle = LifeCycle()

    screen.onclick(cycle.handleClick,1)

    cycle.findPartner()
    cycle.startGame()
    mainloop()