#Rescriba un programa que cree un histograma de una lista de enteros ingresados por teclado. 
class Histograma():

    def ingresar_numeros(self):
        lista=[]
        cantidad=int(input("Ingrese la cantidad de datos del histrograma\n"))
        for x in range(cantidad):
            a = int(input("ingrese el dato n°" + " " + str(x+1) + "\t"))
            lista.append(a)
        return lista

    def crear_histograma(self):
        lista = self.ingresar_numeros()
        print ("Sus datos son:", lista)
        print("")
        for x in lista:
            print("°" * x )

if __name__ == "__main__":
    u = Histograma()
    u.crear_histograma()


