#!/usr/bin/python3
import socketserver
import os
import argparse
from itertools import islice
from concurrent import futures
import time
from math import ceil
intensidad = None
body_list = []
size=None

class Filtros_ppm():
    global body_list
    global size
    global intensidad

    def separar(self,imagen_read):
        header=""
        for i in imagen_read.splitlines():
            header += i.decode()+"\n"
            if i == b"255":
                break
        header = header.replace("P6","P3")
        return(header)

    
    def rojo(self,start):
        for i in range(start,(start+size+3),3):
            body_list[i] = ceil(body_list[i] * int(intensidad[1]))
            if body_list[i] > 255:
                body_list[i]= 255
            body_list[i+1] = 0
            body_list[i+2] = 0

    def azul(self,start):
                        
        for i in range(start,(start+size+3),3):
            body_list[i+2]=round(body_list[i+2] * int(intensidad[1]))
            if body_list[i+2] > 255:
                body_list[i+2]= 255
            body_list[i] = 0
            body_list[i+1] = 0
        

    def verde(self,start):
        for i in range(start,(start+size+3),3):
            body_list[i+1]=ceil(body_list[i+1] * int(intensidad[1]))
            if body_list[i+2] > 255:
                body_list[i+2]= 255
            body_list[i] = 0
            body_list[i+2] = 0
    
    def black_white(self,start):
        for i in range(start,(start+size+3),3):
            promedio=ceil((body_list[i]+body_list[i+1]+body_list[i+2])/3)* int(intensidad[1])
            if promedio > 255:
                promedio=255
            body_list[i] = promedio
            body_list[i+1] = promedio
            body_list[i+2] = promedio

class Parceo():

     def parcear(self,dato):
        encabezado = dato.decode().splitlines()[0]
        pedido = encabezado.split()[1]
        print(encabezado)
        if pedido.count("?") == 1:
            pedido = pedido.split("?")
            ruta_archivo=pedido[0]
            query=pedido[1]
            query_list= query.split("&")
        else:
            ruta_archivo=pedido
            query_list=""
        ruta_archivo= ruta_archivo.split("/")
        return(ruta_archivo,query_list)


class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        global body_list
        global size
        global intensidad
        p=Parceo()
        f=Filtros_ppm()
        ubicacion = args.documentroot
        os.chdir(ubicacion)
        dic={"ico":"image/vnd.svf","txt":" text/plain","jpg":" image/jpeg",
            "ppm":" image/x-portable-pixmap","html":" text/html","pdf":" application/pdf"}

        self.data = self.request.recv(1024)
        dato = self.data
        print(self.client_address)
        (ruta_archivo,query_list) = p.parcear(dato)
        respuesta=""

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
        
        extension = archivo.split('.')[1]
        
        if extension == "ppm" and query_list != "" and respuesta == "200 OK":
            print("querylist:",query_list)
            
            try:
                filtro=query_list[0].split("=")
            except:
                pass

            try:
                intensidad=query_list[1].split("=")
            except:
                intensidad=1

            fd = open(archivo,"rb")
            #body = os.read(fd,os.stat(archivo).st_size)
            lectura=fd.read()
            header_ppm = f.separar(lectura)
            fd.seek(len(header_ppm))
            body= fd.read()
            fd.close()

            body_list = [x for x in body]
            #print(body_list)
            size=args.size
            while True:
                if size%3 !=0:
                    size += 1
                    if size%3 == 0:
                        break
            
            #(body_list,cabecera_ppm) =f.separar(f.eliminar_comentarios(body))
            size_body_list=len(body_list)
            n_threads= ceil(size_body_list/size)
            #print(n_threads)
            hilos = futures.ThreadPoolExecutor(max_workers=n_threads)
            
            #resultado_a_futuro = hilos.map(f.rojo,range(0,size_body_list,size))
            if filtro[0] == "filter":
            
                if filtro[1] == "R":
                    hilos.map(f.rojo,range(0,size_body_list,size))
                    #print(body_list)                    
                    #print("Imagen filtro rojo")
            
                if filtro[1] == "B":
                    hilos.map(f.azul,range(0,size_body_list,size))
                    #print("Imagen filtro azul")
 
                if filtro[1] == "G":
                    hilos.map(f.verde,range(0,size_body_list,size))
                    #print("Imagen filtro verde")
 
                if filtro[1] == "W":
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
            fd = os.open(archivo, os.O_RDONLY)
            body = os.read(fd,os.stat(archivo).st_size)
            os.close(fd)
            
            header = bytearray("HTTP/1.1 "+respuesta+"\r\nContent-type:"+ dic[extension] 
                                +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')       
            self.request.sendall(header)
            self.request.sendall(body)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(usage="./server-http.py [-h] -p PORT -d DOCUMENT ROOT -s SIZE")
    parser.add_argument("-p", "--port", type=int, default=5000, help="Puerto")
    parser.add_argument("-s", "--size", type=int, default=100000, help="Bloque de lectura")
    parser.add_argument("-d", "--documentroot", type=str, default=os.getcwd(), help="/home/../..")
    args = parser.parse_args()

    if args.port > 65535 or args.port < 1023 :
        print("No tiene permisos para ocupar este puerto o NO existe-->default puerto 5000")
        args.port=5000
    
    socketserver.TCPServer.allow_reuse_address = True
    server =  socketserver.TCPServer(("0.0.0.0", args.port), Handler)
    server.serve_forever()

    
