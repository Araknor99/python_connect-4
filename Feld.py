#Autor: Elias Lehnert
from turtle import * 
from Spielstein import *
import math

class spielfeld:
    def __init__(self):
        sTurtle = Turtle()
        self.__steine=[]

        feldH=100
        feldB=100
        sTurtle.color("blue")
        sTurtle.speed(1000)
        sTurtle.begin_fill()

        for i in range(4):
            sTurtle.fd(700 - (i%2) * 100)
            sTurtle.left(90)
        sTurtle.end_fill()
        sTurtle.hideturtle()

        for y in range(7):
            zeile=[]
            for x in range(7):
                posX=feldB*x+feldB/2
                posY=feldH*y+feldH/2
                zeile.append(spielstein(posX,posY,y,x))
            self.__steine.append(zeile)

    def uberpruefeGewonnen(self,player):
        #Vor.: 'player' ist ein güliger Farbstring, der einem der im Spiel vorhandenen Spieler entspricht
        #Erg.:  Ist nach den Regeln des Spieles eine Reihe aus 4 Steinen der selben Farbe erbaut wurden, wurde
        #       die Farbe des Spielers geliefert. Ist ein Zustand erreicht wurden, in dem nicht mehr gespielt werden
        #       kann, wurde "NoPlay" geliefert. Ist weder ein Gewinnzustand noch ein unspielbarer Zustand erreicht wurden,
        #       wurde "ContinuePlaying" geliefert.
        for y in range(6):
            winconst = 0
            for x in range(7):
                addNumber = int(player == self.steinFuerPosition(x,y).gibFarbe())
                winconst = winconst * addNumber + addNumber
                if winconst >= 4:
                    return player

        for x in range(7):
            winconst = 0
            for y in range(6):
                addNumber = int(player == self.steinFuerPosition(x,y).gibFarbe())
                winconst = winconst * addNumber + addNumber
                if winconst >= 4:
                    return player

        xtemp = 3
        ytemp = 0
        for i in range(6):
            j = 0
            winconst = 0
            while xtemp-j >= 0 and ytemp+j <= 5:
                addNumber = int(player == self.steinFuerPosition(xtemp-j,ytemp+j).gibFarbe())
                winconst = winconst * addNumber + addNumber
                if winconst >= 4:
                    return player
                j += 1

            if xtemp > 5:
                ytemp += 1
            else:
                xtemp += 1

        xtemp = 3
        ytemp = 5
        for i in range(6):
            j = 0
            winconst = 0
            while xtemp-j >= 0 and ytemp-j >= 0:
                addNumber = int(player == self.steinFuerPosition(xtemp-j,ytemp-j).gibFarbe())
                winconst = winconst * addNumber + addNumber
                if winconst >= 4:
                    return player
                j+= 1

            if xtemp > 5:
                ytemp -= 1
            else:
                xtemp += 1
        

        filledFields = 0
        for zeile in self.__steine:
            for stein in zeile:
                if stein.gibFarbe() != "grey":
                    filledFields += 1

        if filledFields == 42:
            return "NoPlay"

        return "ContinuePlaying"

        
    
    def angeklickterStein(self,x,y):
        #Vor.:  x und y sind float-koordinaten
        #Erg.:  Wenn ein Stein an der Position liegt, ist dieser geliefert.
        #       Ansonsten ist None geliefert
        for zeile in self.__steine:
            for stein in zeile:
                posX,posY = stein.gibPosition()
                if math.sqrt((posX-x)**2 + (posY-y)**2) <= 43:
                    return stein
        return None

    def setzeSteinFarbe(self,x,y,farbe):
        #Vor.:  x und y sind valide Feldkoordinaten des Types int. 'farbe' ist ein valider Farbstring-
        #Eff.:  Der Stein an der entsprechenden Position wurde auf die Farbe gesetzt
        self.__steine[y][x].setzeFarbe(farbe)

    def pruefeEingaenge(self):
        #Vor.:  keine
        #Eff.:  Alle Eingänge, bei den noch Steine eingeworfen werden können, wurden auf grün gesetzt
        self.setzeEingaenge("white")
        for x in range(7):
            if self.__steine[5][x].gibFarbe() == "grey":
                self.__steine[6][x].setzeFarbe("green")

    def setzeEingaenge(self,farbe1):
        #Vor.:  farbe1 ist ein valider Farbstring
        #Eff.:  Alle Einänge wurden auf die angegebene Farbe gesetzt.
        for stein in self.__steine[6]:
            stein.setzeFarbe(farbe1)

    def bewegeStein(self,stein):
        #Vor.:  'stein' ist ein Stein aus dem Feld
        #Eff.:  Wenn sich unter dem Stein eine unbesetzte Stelle befand, wurde die Farbe des Steines auf die 
        #       des darunter übertragen. Der Stein selbst wurde grau.
        #Erg.:  befindet sich der Stein von nun an in einer Ruhe Position, in dem die Farbe nicht mehr nach unten
        #       gereicht werden kann, so wurde True geliefert. Ist er nicht in einem Ruhezustand angekommen, wurde False geliefert.
        #       Ansonsten ist an der Position liegt, ist dieser geliefert.
        if not stein.ruhe: 
            posx,posy = stein.gibFeldPosition()
            if self.__steine[posy-1][posx].gibFarbe() == "grey" and posy != 0:
                self.__steine[posy-1][posx].setzeFarbe(stein.gibFarbe())
                stein.setzeFarbe("grey")
            else:
                stein.ruhe = True
                return True
        return False

    def handleClick(self,x,y,player):
        #Vor.:  x und y sind float Koordinaten. 'player' ist ein valider Farbstring und einer der Spieler.
        #Eff.:  Wenn sich an der angeklickten Stelle ein Stein befindet und dieser grün ist, wird dieser auf die
        #       Spielerfarbe gesetzt.
        #Erg.:  Wurde erfolgreich ein Stein gefärbt, wurde True geliefert. Wurde kein Stein gefärbt. wurde False
        #       geliefert.
        stein = self.angeklickterStein(x,y)
        if stein != None and stein.gibFarbe() == "green":
            stein.setzeFarbe(player)
            return True
        return False

    def steinFuerPosition(self,x,y):
        #Vor.:  x und y sind valide Feldkoordinaten.
        #Erg.:  Der Stein an entsprechender Stelle wurde geliefert.
        return self.__steine[y][x] 
