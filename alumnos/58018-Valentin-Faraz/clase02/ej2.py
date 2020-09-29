#!/usr/bin/python3
'''2 - Escriba un programa que pida que se ingrese por teclado un nombre de archivo origen 
y luego uno destino. Debe abrir ambos archivos, leer el primero y escribirlo en el segundo. 
(use las funciones disponibles en el modulo os)

./copia.py
ingrese archivo origen: prueba.txt
ingrese archivo destino: otro.txt

# diff prueba.txt otro.txt
#                                               '''
import shutil, os

ruta = os.path.dirname(os.path.abspath(__file__)) + os.sep

while True:
        ingreso1 = input("Ingrese archivo origen (.txt)\n")
        if os.path.isfile(ruta + ingreso1) is True:
            break
        else:
            print("El archivo no existe, intente nuevamente: \n")

ingreso2 =input("Ingrese archivo destino (.txt)\n")

origen = ruta + ingreso1
destino = ruta + ingreso2

archivo_origen = open(origen,"rb")
archivo_destino = open(destino,"wb")

shutil.copyfileobj(archivo_origen, archivo_destino)

if archivo_destino == archivo_destino:
    print("...OK...")