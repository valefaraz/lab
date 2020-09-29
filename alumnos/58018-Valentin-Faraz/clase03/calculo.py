#!/usr/bin/python3
import argparse

parser = argparse.ArgumentParser(usage="./calculo.py n1 [s|r|m|d] n2 -t tipo", description="Calculadora")
parser.add_argument("calculadora", type=float, help="Calculadora primitiva")
parser.add_argument("-s", "--suma", type=float, help="Sumar n1 y n2")
parser.add_argument("-r", "--resta", type=float, help="Restar n1 y n2")
parser.add_argument("-m", "--multiplicacion", type=float, help="Multiplicar n1 y n2")
parser.add_argument("-d", "--division", type=float, help="Dividir n1 y n2")
parser.add_argument("-t", "--tipo", help="Tipos: int o float")

args = parser.parse_args()

if args.tipo == "float":
        if args.suma != None:
            print(float(args.calculadora) + float(args.suma))
        elif args.resta != None:
            print(float(args.calculadora) - float(args.resta))
        elif args.multiplicacion != None:
            print(float(args.calculadora) * float(args.multiplicacion))
        elif args.division != None:
            print(float(args.calculadora) / float(args.division))

if args.tipo == "int":
    if args.suma != None:
        print(int(args.calculadora) + int(args.suma))
    elif args.resta != None:
        print(int(args.calculadora) - int(args.resta))
    elif args.multiplicacion != None:
        print(int(args.calculadora) * int(args.multiplicacion))
    elif args.division != None:
        print(int(args.calculadora) / int(args.division))
