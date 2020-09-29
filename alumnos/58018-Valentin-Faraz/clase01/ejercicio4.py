from io import open

class Histograma():

    def lectura_de_archivo(self):
        archivo = open("archivo_ejercicio4.txt")
        lista = archivo.read()
        lista=list(lista.replace(" ", ""))
        return lista

    def crear_histograma(self):
        lista = self.lectura_de_archivo()
        print ("Sus datos son:", lista)
        print("")
        for x in lista:
            print("°" * int(x) )

if __name__ == "__main__":
    u = Histograma()
    u.crear_histograma()
