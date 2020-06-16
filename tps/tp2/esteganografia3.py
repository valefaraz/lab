import time
import argparse
import matplotlib.pyplot as plt
import multiprocessing as mp
import os
import sys
import threading
import array
barrera = threading.Barrier(3)
candado = threading.Lock()
body_list = []



def eliminar_comentarios(imagen_read):
    inicio_comentario = 0
    fin_comentario = 0
    for n in range(imagen_read.count(b"\n#")):
        inicio_comentario = imagen_read.find(b"\n#")
        fin_comentario = imagen_read.find(b"\n", inicio_comentario + 1)
        imagen_read = imagen_read.replace(imagen_read[inicio_comentario:fin_comentario], b"")
    ancho= int(imagen_read[3:6].decode())
    alto = int(imagen_read[7:10].decode())
    return (imagen_read,ancho,alto)

def separar(image):
    global body_list
    return_1 = image.find(b"\n") + 1
    return_2 = image.find(b"\n", return_1) + 1
    header_end = image.find(b"\n", return_2) + 1
    header = image[:header_end].decode()
    #body = image[header_end:]
    #body = image.replace(header, b"")
    #header = header.decode()
    #header = header.replace("P6","P3")
    return(header)

def estego_mensaje(lista):
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
    return (b_mensaje)

def modificar_rojo(b_mensaje):
    global body_list
    a = 0
    #print("ROJO")
    #print(b_mensaje)

    inicio = (3*(int(args.offset)-1))
    #print(inicio)
    fin = inicio+len(b_mensaje)*(int(args.interleave)*3)
    step = int(args.interleave)*9

    
    for b in range(inicio,fin,step):
        candado.acquire()
        z=0
        print("rojo:",b)
        #print("b=",body_list[b])
        #print("a=",a)
        #print("bits=",b_mensaje[a])
        if body_list[b] %2 == 0 and b_mensaje[a] == 0 and z !=1:
            z=1
            pass

        elif body_list[b] %2 == 1 and b_mensaje[a] == 1 and z !=1:
            z=1
            pass
        
        elif body_list[b] %2 == 0 and b_mensaje[a] == 1 and z !=1:
            z=1
            body_list[b] = body_list[b] - 1
        
        elif body_list[b] %2 == 1 and b_mensaje[a] == 0 and z !=1:
            z=1
            body_list[b] = body_list[b] - 1
        
        candado.release()

        #print("new valor:",body_list[b])
        #print("----------------")
        #a = a+3
    barrera.wait()
    new_image = open(""+args.output+".ppm", "ab")
    body = array.array('B', body_list)
    body.tofile(new_image)
    new_image.close()


def modificar_verde(b_mensaje):
    global body_list
    a = 1
    #print("VERDE")

    #print(b_mensaje)

    inicio = (3*(int(args.offset))+1)
    fin = inicio+len(b_mensaje)*(int(args.interleave)*3)
    step = int(args.interleave)*9

    if len(b_mensaje) %3 == 1:
        fin = fin - step
    
    

    for b in range(inicio,fin,step):
        candado.acquire()
        z=0
        print("verde:",b)
        #print("b=",body_list[b])
        #print("a=",a)
        #print("bit=",b_mensaje[a])
        if body_list[b] %2 == 0 and b_mensaje[a] == 0 and z !=1:
            z=1
            pass

        elif body_list[b] %2 == 1 and b_mensaje[a] == 1 and z !=1:
            z=1
            pass
        
        elif body_list[b] %2 == 0 and b_mensaje[a] == 1 and z !=1:
            z=1
            body_list[b] = body_list[b] - 1

        elif body_list[b] %2 == 1 and b_mensaje[a] == 0 and z !=1:
            z=1
            body_list[b] = body_list[b] - 1
        candado.release()
        #print("new valor:",body_list[b])
        #print("----------------")
        a = a+3

    barrera.wait()

def modificar_azul(b_mensaje):

    global body_list
    a = 2
    #print("AZUL")

    #print(b_mensaje)

    inicio = (3*(int(args.offset)+1)+2)
    fin = inicio+len(b_mensaje)*(int(args.interleave)*3)
    step = int(args.interleave)*9

    if len(b_mensaje) %3 == 1:
        fin = fin - step
    elif len(b_mensaje) %3 == 2:
        fin = fin - step
    
    
    
    for b in range(inicio,fin,step):
        candado.acquire()
        z=0
        print("azul:",b)

        #print(body_list[b])
        #print(a)
        if body_list[b] %2 == 0 and b_mensaje[a] == 0 and z !=1:
            z=1
            pass

        elif body_list[b] %2 == 1 and b_mensaje[a] == 1 and z !=1:
            z=1
            pass

        elif body_list[b] %2 == 0 and b_mensaje[a] == 1 and z !=1:
            z=1
            body_list[b] = body_list[b] + 1

        elif body_list[b] %2 == 1 and b_mensaje[a] == 0 and z !=1:
            z=1
            body_list[b] = body_list[b] - 1
        candado.release()
        #print("new valor:",body_list[b])
        #print("----------------")
        a = a+3
    barrera.wait()

if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(usage="./esteganografia.py [-h] -s SIZE -f FILE -m FILE -f PIXELS -i PIXELS -o FILE2")
    parser.add_argument("-f", "--file", type=str, required=True, help="Archivo portador .ppm")
    parser.add_argument("-s", "--size", type=int, default=1024, help="Bloque de lectura")
    parser.add_argument("-m", "--message", type=str, help="Mensaje esteganografico")
    parser.add_argument("-e", "--offset", type=str, default="1", help="Mensaje offset en pixels del inicio del raster")
    parser.add_argument("-i", "--interleave", type=str, default="1", help="Interleave de modificacion en pixel")
    parser.add_argument("-o", "--output", type=str, default="mensaje_oculto", help="Estego-mensaje")
    args = parser.parse_args()

    #Manejo de errores

    if args.size <= 0:
        print("El tamano de lectura [-s] no puede ser negativo")
        sys.exit()
    if int(args.offset) < 0 or int(args.interleave) < 0:
        print("El offset o interleave [-e -i] no puede ser negativos")
        sys.exit()
    try:
        archivo = open(args.file,"rb")
    except FileNotFoundError:
        print("Archivo no encontrado")
        sys.exit()

    name_file = len(args.file)
    if args.file[(name_file-3):name_file] != "ppm":
        print("El archivo -f debe ser .ppm")
        sys.exit()

    name_file3 = len(args.message)
    if args.message[(name_file3-3):name_file3] != "txt":
        print("El archivo -m debe ser .txt")
        sys.exit()

    hola = open(args.message,"r")
    texto = hola.read()
    hola.close()
    lista=[]

    for letra in texto:
        lista.append(format(ord(letra), "b"))

    b_mensaje = estego_mensaje(lista)


    archivo = open(args.file,"rb")
    imagen_read = archivo.read(1024)
    imagen, ancho, alto = eliminar_comentarios(imagen_read)
    header = separar(imagen)
    
    #Verifico el tamaño de la imagen

    if ancho*alto < int(args.offset)+len(b_mensaje)* int(args.interleave):
        print("La imagen no tiene la cantidad necesaria de pixels para ocultar su mensaje")
        sys.exit()

    #Coloco el puntero al inicio del cuerpo
    
    inicio_comentario = imagen_read.find(b"\n#")
    fin_comentario = imagen_read.find(b"\n", inicio_comentario + 1)
    tamano_comentario = fin_comentario - inicio_comentario
    inicio_body=len(header)+tamano_comentario
    archivo.seek(inicio_body)

    while True:
        lectura = archivo.read(args.size)
        for elemento in lectura:
            body_list.append(elemento)
        if not lectura:
            break

    new_image = open(""+args.output+".ppm", "w")
    compu = "#UMCOMPU2 " + args.offset + " " + args.interleave + " " + str(len(lista)) + "\n"
    new_image.write(header[:3])
    new_image.write(compu)
    new_image.write(header[3:])
    new_image.close()

    hilo_rojo = threading.Thread(target= modificar_rojo, args=(b_mensaje,))
    hilo_verde = threading.Thread(target= modificar_verde, args=(b_mensaje,))
    hilo_azul = threading.Thread(target= modificar_azul, args=(b_mensaje,))

    hilo_rojo.start()
    hilo_verde.start()
    hilo_azul.start()

    hilo_rojo.join()
    hilo_verde.join()
    hilo_azul.join()




    #new_image.close()
    #new_image = open(""+args.output+".ppm", "a")
    #new_image.write("#UMCOMPU2 " + args.offset + " " + args.interleave + " "+ str(len(lista)) + "\n")
    #new_image.close()



    print("--- %s seconds ---" % (time.time() - start_time))