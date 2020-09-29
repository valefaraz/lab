#!/usr/bin/python3
import sys
class Numero():

    def ingreso_por_teclado(self):

        if ((len(sys.argv)) > 1):
            return (str(sys.argv[1]))
        else:
            print("Por defecto usa el numero 9")
            return (str(9))

    def sumar(self):
        num=self.ingreso_por_teclado()
        a = num
        b = (num*2)
        c = (num*3)
        print (int(a)+int(b)+int(c))

if __name__ == "__main__":
    u = Numero()
    u.sumar()


