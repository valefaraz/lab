
class Numero():

    def __init__(self):
        self.num = str(input("Ingrese un numero \n"))
        self.rep = int(input("ingrese un segundo numero \n"))
    
    def sumar(self):
        b=0
        for i in range(self.rep):
            a = (self.num * (i+1))
            #if a != '':
            b = b + int(a)
        print(b)

if __name__ == "__main__":
    u = Numero()
    u.sumar()