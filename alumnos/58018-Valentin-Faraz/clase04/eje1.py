#!/usr/bin/python3

'''1 - realize un programa que al recibir una señal SIGUSR1, comienze a imprimir por pantalla el siguiente 
nro real cada 1 segundo.
Cada vez que se reciba una nueva señal SIGUSR1, 
el tiempo entre impresiones en pantalla se duplicará.
Si se recibe una señal SIGUSR2, se dejará de imprimir por pantalla el siguiente nro real.
En caso de recibir una segunda señal SIGUSR2, se continuará desde el nro real que estaba imprimiendo, 
con un intervalo de 1 segundo.'''
import time
import os
import signal

class Señal():
    def __init__(self):
        self.signal10=False
        self.signal12=False
        self.time = 1
        self.numero = 0

    def handler(self,signal_number,frame):
        if signal_number == 10:
            if self.signal10 == True:
                self.time = self.time * 2
            self.signal10 = True
            self.mostrar()
            
        if signal_number == 12:
            if self.signal12 == False:
                self.time = 1
                self.signal12 = True
                signal.pause()
            else:
                self.signal12 = False
                self.mostrar()

    def mostrar(self):

        while True:
            self.numero += 1
            print(self.numero)
            time.sleep(self.time)     

if __name__ == "__main__":

    u=Señal()

    def recibir_señal(signal_number,frame):
        u.handler(signal_number, frame)

    signal.signal(signal.SIGUSR1,recibir_señal)
    signal.signal(signal.SIGUSR2,recibir_señal)
    print(os.getpid())
    signal.pause()