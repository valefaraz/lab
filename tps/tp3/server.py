#!/usr/bin/python3
import socketserver
import os
import argparse
from concurrent import futures
import time
from math import ceil
from parceo import Parceo
from parceo_ppm import separar
import sys
intensidad = None
body_list = []
size=None

class Filtros_ppm():
    global body_list
    global size
    global intensidad
    
    def rojo(self,start):
        #print (float(intensidad[1]))
        for i in range(start,(start+size),3):
            body_list[i] = ceil(body_list[i] * float(intensidad[1]))
            if body_list[i] > 255 or body_list[i] < 0:
                body_list[i]= 255
            body_list[i+1] = 0
            body_list[i+2] = 0
    
    def verde(self,start):
        for i in range(start,(start+size-1),3):
            body_list[i+1]=ceil(body_list[i+1] * float(intensidad[1]))
            if body_list[i+2] > 255 or body_list[i] < 0:
                body_list[i+2]= 255
            body_list[i] = 0
            body_list[i+2] = 0

    def azul(self,start):
        for i in range(start,(start+size-2),3):
            body_list[i+2]=round(body_list[i+2] * float(intensidad[1]))
            if body_list[i+2] > 255 or body_list[i] < 0:
                body_list[i+2]= 255
            body_list[i] = 0
            body_list[i+1] = 0

    
    def black_white(self,start):
        print(start)
        for i in range(start,(start+size),3):
            promedio=ceil((int(body_list[i])+int(body_list[i+1])+int(body_list[i+2]))/3)* float(intensidad[1])
            #if promedio > 255 or promedio < 0:
                #promedio=255
            body_list[i] = int(promedio)
            body_list[i+1] = int(promedio)
            body_list[i+2] = int(promedio)

class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        global body_list
        global size
        global intensidad
        #global ruta_archivo
        #global query_list
        
        p=Parceo()
        f=Filtros_ppm()
        extension=[]
        ruta_archivo=""
        query_list=[]
        respuesta=""
        archivo=""


        ubicacion = args.documentroot
        os.chdir(ubicacion)
        dic={"ico":"image/vnd.svf","txt":" text/plain","jpg":" image/jpeg",
            "ppm":" image/x-portable-pixmap","html":" text/html","pdf":" application/pdf"}
        self.data = self.request.recv(1024)
        dato = self.data
        print(self.client_address)
        #print(dato)

        try:
            (ruta_archivo,query_list) = p.parcear(dato)
        except:
            pass

        for x in range(len(ruta_archivo)-1):
            if ruta_archivo[1+x] == '' and len(ruta_archivo) == 2:
                #print("cuando es /")
                archivo = 'index.html'
                respuesta= "200 OK"
                break

            if os.path.isfile(ruta_archivo[1+x]) == True:   #si existe el archivo
                archivo = ruta_archivo[1+x]
                respuesta="200 OK"
                #print("existe el archivo")
            
            if os.path.isfile(ruta_archivo[1+x]) == False:   #si no esta el archivo
                archivo = '400error.html'
                respuesta="404 Not Found"
                #print("no esta el archivo")

            if os.path.isdir(ruta_archivo[1+x]) == True:    #si existe el directorio
                os.chdir(ubicacion+"/"+ruta_archivo[1+x])
                archivo="index.html"
                #print("existe el directorio")

            if ruta_archivo[1+x] == '':
                #print("cuando es /")
                archivo = 'index.html'
                respuesta= "200 OK"
        try:
            extension = archivo.split('.')[1]
        except:
            pass
        if extension == "ppm" and query_list != "" and respuesta == "200 OK":
            print("querylist:",query_list)
            
            try:
                filtro=query_list[0].split("=")
            except:
                respuesta="500 Internal Server Error"

            try:
                intensidad=query_list[1].split("=")
            except:
                respuesta="500 Internal Server Error"
                intensidad=["",1]
            
            if intensidad[0] != "scale" or filtro[0] != "filter":
                respuesta = "500 Internal Server Error"

            fd = open(archivo,"rb")
            lectura=fd.read()
            header_ppm ,body = separar(lectura)
            #fd.seek(len(header_ppm))
            #body= fd.read()
            fd.close()
            
            body_list = [x for x in body]
            size=args.size
            while True:
                if size%3 !=0:
                    size += 1
                    if size%3 == 0:
                        break
            
            size_body_list=len(body_list)
            n_threads= ceil(size_body_list/size)
            #print(n_threads)
            hilos = futures.ThreadPoolExecutor(max_workers=n_threads)
            
            #resultado_a_futuro = hilos.map(f.rojo,range(0,size_body_list,size))
            if filtro[0] == "filter":
            
                if filtro[1] == "R" or filtro[1] == "r":
                    hilos.map(f.rojo,range(0,size_body_list,size))
                    #print(body_list)                    
                    #print("Imagen filtro rojo")
            
                if filtro[1] == "B" or filtro[1] == "b":
                    hilos.map(f.azul,range(0,size_body_list,size))
                    #print("Imagen filtro azul")
 
                if filtro[1] == "G" or filtro[1] == "g":
                    hilos.map(f.verde,range(0,size_body_list,size))
                    #print("Imagen filtro verde")
 
                if filtro[1] == "W" or filtro[1] == "w":
                    hilos.map(f.black_white,range(0,size_body_list,size))
                    #print("Imagen filtro black and white")

            body_ppm =""
            c=0
            for x in body_list:
                c += 1
                body_ppm += str(x) + " "
                if c%12 == 0:
                    body_ppm += "\n"

            header = bytearray("HTTP/1.1 "+respuesta+"\r\nContent-type:"+ dic[extension] 
                    +"\r\nContent-length:"+str(len(body_ppm)+len(header_ppm))+"\r\n\r\n",'utf8')   
            self.request.sendall(header)
            self.request.sendall(bytearray(header_ppm,"utf-8"))
            self.request.sendall(bytearray(body_ppm,"utf-8"))

        else:
            try:
                fd = os.open(archivo, os.O_RDONLY)
                body = os.read(fd,os.stat(archivo).st_size)
                os.close(fd)
                header = bytearray("HTTP/1.1 "+respuesta+"\r\nContent-type:"+ dic[extension] 
                                +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')       
                self.request.sendall(header)
                self.request.sendall(body)
            except FileNotFoundError:
                print("ERROR DOCUMENTROOt")
            
            


if __name__ == "__main__":

    parser = argparse.ArgumentParser(usage="./server-http.py [-h] -p PORT -d DOCUMENT ROOT -s SIZE")
    parser.add_argument("-p", "--port", type=int, default=5000, help="Puerto")
    parser.add_argument("-s", "--size", type=int, default=50000, help="Bloque de lectura")
    parser.add_argument("-d", "--documentroot", type=str, default=os.getcwd(), help="/home/../..")
    args = parser.parse_args()

    if args.port > 65535 or args.port < 1023 :
        print("No tiene permisos para ocupar este puerto o NO existe-->default puerto 5000")
        args.port=5000
    
    if args.size <= 0:
        print("El tamano de lectura [-s] no puede ser negativo")
        sys.exit()
    
    socketserver.TCPServer.allow_reuse_address = True
    server =  socketserver.ThreadingTCPServer(("0.0.0.0", args.port), Handler)
    server.serve_forever()