#!/usr/bin/python3
import socketserver
import os
import argparse

class Handler(socketserver.BaseRequestHandler):
    
    def query(self):
    
    
    
    def handle(self):
        
        ubicacion = args.documentroot
        os.chdir(ubicacion)

        dic={"ico":"image/vnd.svf","txt":" text/plain","jpg":" image/jpeg",
            "ppm":" image/x-portable-pixmap","html":" text/html","pdf":" application/pdf"}
        
        self.data = self.request.recv(1024)

        encabezado = self.data.decode().splitlines()[0]
        #print(encabezado)
        ruta_archivo = encabezado.split()[1]
        #print(ruta_archivo)
        ruta_archivo= ruta_archivo.split("/")
        print(ruta_archivo)
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
                #break
            
            if os.path.isfile(ruta_archivo[1+x]) == False:   #si no esta el archivo
                archivo = '400error.html'
                respuesta="404 Not Found"
                #print("no esta el archivo")

            if os.path.isdir(ruta_archivo[1+x]) == True:    #si existe el directorio
                os.chdir(ubicacion+"/"+ruta_archivo[1+x])
                archivo="index.html"
                #print("existe el directorio")
                #break

            if ruta_archivo[1+x] == '':
                #print("cuando es /")
                archivo = 'index.html'
                respuesta= "200 OK"
            
            #if os.path.isdir(ruta_archivo[1+x]) ==False: #si no esta el directorio
                #print("no esta el dir")
                #archivo = '400error.html'
            
            
        extension = archivo.split('.')[1]
        #print("Extension:",extension)
        print(self.client_address)
        print(self.data)
            
        
        fd = os.open(archivo, os.O_RDONLY)
        body = os.read(fd, 50000)
        os.close(fd)
        header = bytearray("HTTP/1.1 "+respuesta+"\r\nContent-type:"+ dic[extension] 
                            +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')       
        
        self.request.sendall(header)
        self.request.sendall(body)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(usage="./server-http.py [-h] -p PORT -d DOCUMENT ROOT -s SIZE")
    parser.add_argument("-p", "--port", type=int, default=5000, help="Puerto")
    parser.add_argument("-s", "--size", type=int, default=1024, help="Bloque de lectura")
    parser.add_argument("-d", "--documentroot", type=str, default=os.getcwd(), help="/home/../..")
    args = parser.parse_args()

    
    #print(ubicacion)

    socketserver.TCPServer.allow_reuse_address = True
    server =  socketserver.ThreadingTCPServer(("0.0.0.0", args.port), Handler)
    server.serve_forever()

    
