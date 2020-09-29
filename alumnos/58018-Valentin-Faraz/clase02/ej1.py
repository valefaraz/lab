#!/usr/bin/python3
'''1 - realize un programa que lea todos los datos ingresados desde stdin, e invierta el orden de las letras en cada  palabra, enviandolo a stdout.

Ejemplo de funcionamiento

# echo -e  "hola mundo \n nos vemos" | ./invierte.py 

aloh odnum 
son somev '''

import sys

leido = sys.stdin.read()
leido = leido.split(sep="\n")

for x in range(len(leido)):

    print("")
    a = leido[x].split()
    for i in a:
        i = (" ")+ i
        sys.stdout.write(i[::-1])
