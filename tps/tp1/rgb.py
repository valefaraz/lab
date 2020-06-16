#!/usr/bin/python3
import argparse
import matplotlib.pyplot as plt
import multiprocessing as mp
import time
import os
import sys

def eliminar_comentarios(imagen_read):
    for n in range(imagen_read.count(b"\n#")):
        inicio_comentario = imagen_read.find(b"\n# ")
        fin_comentario = imagen_read.find(b"\n", inicio_comentario + 1)
        imagen_read = imagen_read.replace(imagen_read[inicio_comentario:fin_comentario], b"")
    return (imagen_read)

def separar(imagen_read):
    header = imagen_read[:15].decode()
    header = header.replace("P6","P3")
    body = imagen_read[15:]
    body_list = [x for x in body]
    return(body_list, header)

def rojo(q_red,qhistograma_rojo):
    a = b""
    while True:
        a += q_red.get()
        if q_red.empty():
            break 
    imagen_read = eliminar_comentarios(a)
    body_list, header = separar(imagen_read)
    histograma = []
    if args.red != 1:
        for i in range(0,(len(body_list)-3),3):
            histograma.append(body_list[i])
            body_list[i] = round(body_list[i] * args.red)
            body_list[i+1] = 0
            body_list[i+2] = 0
        qhistograma_rojo.put(histograma)
        body =""
        c=0
        for x in body_list:
            c += 1
            body += str(x) + " "
            if c%9 == 0:
                body += "\n"
        imagen = open("rojo.ppm", "w")
        imagen.write(header + "\n")
        imagen.write(body)
        #plt.hist(histograma, rwidth= 0.9, bins=10)
        #plt.title("Histograma rojo")
        #plt.show()

def verde(q_green,qhistograma_verde):
    a = b""
    while True:
        a += q_green.get()
        if q_green.empty():
            break 
    imagen_read = eliminar_comentarios(a)
    body_list, header = separar(imagen_read)
    histograma=[]
    if args.green != 1:
        for i in range(0,(len(body_list)-3),3):
            histograma.append(body_list[i+1])
            body_list[i+1]=round(body_list[i+1] * args.green)
            body_list[i] = 0
            body_list[i+2] = 0
        qhistograma_verde.put(histograma)
        body =""
        c=0
        for x in body_list:
            c += 1
            body += str(x) + " "
            if c%9 == 0:
                body += "\n"
        imagen = open("verde.ppm", "w")
        imagen.write(header + "\n")
        imagen.write(body)
        #plt.hist(histograma, rwidth= 0.9, bins=10)
        #plt.title("Histograma green")
        #plt.show()

def azul(q_blue,qhistograma_azul):
    a = b""
    while True:
        a += q_blue.get()
        if q_blue.empty():
            break 
    imagen_read = eliminar_comentarios(a)
    body_list, header = separar(imagen_read)
    histograma=[]
    if args.blue != 1:
        for i in range(0,(len(body_list)-3),3):
            histograma.append(body_list[i+2])
            body_list[i+2]=round(body_list[i+2] * args.blue)
            body_list[i] = 0
            body_list[i+1] = 0
        qhistograma_azul.put(histograma)
        body =""
        c=0
        for x in body_list:
            c += 1
            body += str(x) + " "
            if c%9 == 0:
                body += "\n"
        imagen = open("azul.ppm", "w")
        imagen.write(header + "\n")
        imagen.write(body)
        
if __name__ == "__main__":
   
    parser = argparse.ArgumentParser(usage="./procesador.py [-h] [-r RED] [-g GREEN] [-b BLUE] -s SIZE -f FILE", description="Filtro de imagen")
    parser.add_argument("-f", "--file", type=str, required=True, help="Archivo a procesar .ppm")
    parser.add_argument("-s", "--size", type=int, required=True, help="Bloque de lectura")
    parser.add_argument("-b", "--blue", type=float, default=1, help="Escala para azul")
    parser.add_argument("-g", "--green", type=float, default=1, help=" Escala para verde")
    parser.add_argument("-r", "--red", type=float, default=1, help="Escala para rojo")
    args = parser.parse_args()

    q_red = mp.Queue()
    q_green = mp.Queue()
    q_blue = mp.Queue()
    qhistograma_rojo =mp.Queue()
    qhistograma_azul =mp.Queue()
    qhistograma_verde =mp.Queue()

    hijo_red = mp.Process(target=rojo, args=(q_red,qhistograma_rojo))
    hijo_green = mp.Process(target=verde, args=(q_green,qhistograma_verde))
    hijo_blue = mp.Process(target=azul, args=(q_blue,qhistograma_azul))

    if args.size < 0:
        print("El tamaño de lectura [-s] no puede ser negativos ")
        sys.exit()
    if args.red < 0 or args.blue < 0 or args.green < 0:
        print("Las escala de color [-r -g -b] no puede ser negativas")
        sys.exit()
    try:
        archivo = open(args.file,"rb")
    except FileNotFoundError:
        print("Archivo no encontrado")
        sys.exit()

    name_file = len(args.file)
    if args.file[(name_file-3):name_file] != "ppm":
        print("El archivo debe ser .ppm")
        sys.exit()
    
    while True:
        texto = archivo.read(args.size + 15)
        q_red.put(texto)
        q_green.put(texto)
        q_blue.put(texto)
        if not texto:
            break
    
    archivo.close()
    time.sleep(1)
    print("Creando hijo 1....")    
    hijo_red.start()
    time.sleep(1)
    print("Creando hijo 2....")
    hijo_green.start()
    time.sleep(1)
    print("Crando hijo 3....")
    hijo_blue.start()

    histograma_rojo = qhistograma_rojo.get()
    histograma_verde = qhistograma_verde.get()
    histograma_azul = qhistograma_azul.get()

    hijo_red.join()
    hijo_green.join()                           #el padre espera a que los hijos terminen
    hijo_blue.join()

    plt.hist(histograma_rojo, rwidth= 10, bins=1000,color="red")
    plt.title("Histograma rojo")
    plt.xlabel("Valor de pixel rojo")
    plt.ylabel("Cantidad de pixels")
    plt.show()
    plt.hist(histograma_verde, rwidth= 10, bins=1000,color="green")
    plt.xlabel("Valor de pixel verde")
    plt.ylabel("Cantidad de pixels")
    plt.title("Histograma verde")
    plt.show()
    plt.hist(histograma_azul, rwidth= 10, bins=1000,color="blue")
    plt.xlabel("Valor de pixel azul")
    plt.ylabel("Cantidad de pixels")
    plt.title("Histograma azul")
    plt.show()
    
    print("Se crearon las imagenes correctamente en: "+ (os.path.abspath("")))