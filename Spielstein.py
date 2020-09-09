#Autor: Elias Lehnert
from turtle import *

class spielstein:
    def __init__(self,x,y,fieldX,fieldY):
        self.__stein=Turtle()
        self.__stein.hideturtle()
        self.__farbe="grey"
        self.__fieldX = fieldX
        self.__fieldY = fieldY
        self.ruhe = True

        self.__stein.shape('circle')
        self.__stein.color(self.__farbe)
        self.__stein.penup()
        self.__stein.speed(1000)
        self.__stein.goto(x,y)
        self.__stein.showturtle()

    def gibFarbe(self):
        #Vor.:  keine
        #Erg.:  Der Farbstring des Steines wurde geliefert.
        return self.__farbe

    def setzeFarbe(self, color):
        #Vor.:  color ist ein valider Farbstring
        #Eff.:  Der Stein hat die Farbe angenommen und befindet sich nicht mehr im Ruhezustand
        self.__farbe = color
        self.__stein.color(self.__farbe)
        self.ruhe = False

    def gibPosition(self):
        #Vor.:  keine
        #Erg.:  Die Position des Steines wurde in float-Koordinaten geliefert.
        return self.__stein.pos()

    def gibFeldPosition(self):
        #Vor.:  keine
        #Erg.:  Die Feldposition des Steines wurde geliefert.
        return (self.__fieldY,self.__fieldX)
