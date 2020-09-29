#6 - Escriba un programa que acepte una serie de números separados por coma, 
#    y genere una lista de python ordenada de manera descendente.

#    ingresando los numeros 5,77,8,33,6,45,38 se debe obtener [77, 45, 33, 8, 6, 5, 3]

class Ejercicio6():

    def ingreso(self):
        numeros = input("Ingrese una serie de numeros\n")
        lista = numeros.split(sep=",")                      #trasforma un str en lista
        print (lista)
        return lista

    def ordenar_lista(self):
        lista = self.ingreso()
        for i in range(0,len(lista)):
            lista[i] = int(lista[i])
            print(i)
        lista_ordenada = sorted(lista)
        print (lista_ordenada[::-1])


if __name__ == "__main__":
    u = Ejercicio6()
    u.ordenar_lista()