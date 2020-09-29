#!/usr/bin/python3
'''2 - Realice un programa que utilice el módulo getopt o argparse para tomar argumentos, 
el programa deberá crear un hijo (usando fork()) que tome dichos argumentos y 
realice una potencia entre ellos. Adicionalmente debe tener la opción verbosa 
que muestre los argumentos ingresados y la opción help o ayuda que explique 
que argumentos espera el programa.

Argumentos necesarios
	-v verboso
	-h,--help ayuda
	-n base
	-m exponente'''

import argparse
import os
parser = argparse.ArgumentParser(usage="/fork_argumentos_getopt.py -v -n arg1 -m arg2",
                                 description="Los argumentos validos son -v (verboso) -n (base) -m (exponente)")

parser.add_argument("-v", "--verboso", action="store_true", default=False, help="Mostrar proceso")
parser.add_argument("-n", "--base", type=int, help="Numero base del exponente")
parser.add_argument("-m", "--exponente", type=int, help="Numero exponente")

args = parser.parse_args()

exp = args.base ** args.exponente

if args.verboso == True:
    print("...Modo verboso...\n")
    print("Argumentos ingresados: ", args._get_kwargs(), "\n")
    
pid = os.fork()
if pid == 0:
    print("PID padre:", os.getppid())
    print("PID hijo:", os.getpid(), "potencia:", exp, "por", os.getpid())