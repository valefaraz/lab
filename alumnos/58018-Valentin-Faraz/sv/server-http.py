#!/usr/bin/python3
import socketserver
import os
import argparse

class Handler(socketserver.BaseRequestHandler):
    
    def handle(self):
        dic={"ico":"image/vnd.svf","txt":" text/plain","jpg":" image/jpeg",
            "ppm":" image/x-portable-pixmap","html":" text/html","pdf":" application/pdf"}
        
        self.data = self.request.recv(1024)
        encabezado = self.data.decode().splitlines()[0]
        #print(encabezado)
        archivo = "." + encabezado.split()[1]
        print(archivo)

        if archivo == './':
            archivo = './index.html'

        extension = archivo.split('.')[2]
        #print("Extension:",extension)
        print(self.client_address)
        print(self.data)

        #if os.path.isfile("index.html") == False: #si no esta el archivo
        #    archivo = './400error.html'
        
        if os.path.isfile(archivo) == False: #si no esta el archivo
            archivo = './400error.html'
        
        fd = os.open(archivo, os.O_RDONLY)
        body = os.read(fd, 50000)
        os.close(fd)

        header = bytearray("HTTP/1.1 200 OK\r\nContent-type:"+ dic[extension] 
                            +"\r\nContent-length:"+str(len(body))+"\r\n\r\n",'utf8')       
        
        self.request.sendall(header)
        self.request.sendall(body)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(usage="./server-http.py [-h] -p PORT -d DOCUMENT ROOT -s SIZE")
    parser.add_argument("-p", "--port", type=int, default=5000, help="Puerto")
    parser.add_argument("-s", "--size", type=int, default=1024, help="Bloque de lectura")
    parser.add_argument("-d", "--documentroot", type=str, default=os.getcwd(), help="/home/../..")
    args = parser.parse_args()

    ubicacion = args.documentroot
    os.chdir(ubicacion)
    #print(ubicacion)

    socketserver.TCPServer.allow_reuse_address = True
    server =  socketserver.ThreadingTCPServer(("0.0.0.0", args.port), Handler)
    server.serve_forever()

    
