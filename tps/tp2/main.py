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
from eleminar import eliminar_comentarios
from separar import separar
from bits import estego_mensaje



def modificar_rojo(b_mensaje):
    global body_list
    a = 0
    
    #print("HILO ROJO")
    #print(b_mensaje)


    inicio = 0 + (3*(int(args.offset)))
    fin = inicio+len(b_mensaje)*(int(args.interleave)*3)
    step = int(args.interleave)*9
    
    #print("rojo",inicio)

    for b in range(inicio,fin,step):
        
        candado.acquire()
        z=0
        
        #print("rojo:",b)
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
        
        a = a+3

    barrera.wait()

    new_image = open(""+args.output+".ppm", "ab")
    body = array.array('B', body_list)
    body.tofile(new_image)
    new_image.close()


def modificar_verde(b_mensaje):
    global body_list
    a = 1
    
    #print("HILO VERDE")
    #print(b_mensaje)

    inicio = 4 + (3*(int(args.offset)) + ((int(args.interleave)-1)*3))
    if int(args.interleave) == 1:
        inicio = 4 + (3*(int(args.offset)))
    fin = inicio+len(b_mensaje)*(int(args.interleave)*3)
    step = int(args.interleave)*9

    #print("verde:",inicio)

    if len(b_mensaje) %3 == 1:
        fin = fin - step
    
    for b in range(inicio,fin,step):
        candado.acquire()
        z=0
        
        #print("verde:",b)
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

    #print("HILO AZUL")
    #print(b_mensaje)

    inicio = 8 + (3*(int(args.offset)) + ((int(args.interleave)+int(args.interleave)-2)*3))
    if int(args.interleave) == 1:
        inicio = 8 + (3*(int(args.offset)))
    fin = inicio+len(b_mensaje)*(int(args.interleave)*3)
    step = int(args.interleave)*9

    #print("azul:",inicio)

    if len(b_mensaje) %3 == 1:
        fin = fin - step
    elif len(b_mensaje) %3 == 2:
        fin = fin - step

    for b in range(inicio,fin,step):
        candado.acquire()
        z=0
        
        #print("azul:",b)
        #print("a=",a)
        #print("bits=",b_mensaje[a])
        #print(body_list[b])
        
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
    parser.add_argument("-e", "--offset", type=str, help="Mensaje offset en pixels del inicio del raster")
    parser.add_argument("-i", "--interleave", type=str, help="Interleave de modificacion en pixel")
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


    archivo_mensaje = args.message

    b_mensaje,lista = estego_mensaje(archivo_mensaje)

    archivo = open(args.file,"rb")
    imagen_read = archivo.read(1024)
    imagen, ancho, alto = eliminar_comentarios(imagen_read)
    header = separar(imagen)
    
    #Verifico el tamaño de la imagen

    if ancho*alto < int(args.offset) + len(b_mensaje) * int(args.interleave):
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
    
    if hilo_rojo.is_alive()== False:
        print("Termino el Hilo Rojo...")

    if hilo_verde.is_alive()== False:
        print("Termino el hilo Verde...")

    if hilo_azul.is_alive()== False:
        print("Termino el Hilo Azul...")


    
    
    print("Se genero correctamente")
    print("--- %s segundos ---" % (time.time() - start_time))