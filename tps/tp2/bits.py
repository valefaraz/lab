
def estego_mensaje(mensaje):
    
    hola = open(mensaje,"r")
    texto = hola.read()
    hola.close()
    lista=[]

    for letra in texto:
        lista.append(format(ord(letra), "b"))


    l_total=len(lista)
    b_mensaje= []
    for i in range(l_total):
        lista[i]=list(lista[i])        #crea una lista para cada byte
        c=0
        while True:
            if len(lista[i]) < 8:
                lista[i].insert(c,"0")
                c += 1
            else:
                break
        #print(lista[i])
        for x in lista[i]:
            b_mensaje.append(int(x))       #lista de todos los bits del mensaje
    return (b_mensaje,lista)
