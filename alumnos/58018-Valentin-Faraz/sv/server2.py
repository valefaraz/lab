#!/usr/bin/python3
import socketserver
import os
import argparse
class Filtros_ppm():
    def eliminar_comentarios(self,imagen_read):
        for n in range(imagen_read.count(b"\n#")):
            inicio_comentario = imagen_read.find(b"\n# ")
            fin_comentario = imagen_read.find(b"\n", inicio_comentario + 1)
            imagen_read = imagen_read.replace(imagen_read[inicio_comentario:fin_comentario], b"")
        return (imagen_read)

    def separar(self,imagen_read):
        header = imagen_read[:15].decode()
        header = header.replace("P6","P3")
        body = imagen_read[15:]
        body_list = [x for x in body]
        return(body_list, header)
    
    def rojo(self,body_list,intensidad):
        for i in range(0,(len(body_list)-3),3):
            body_list[i] = round(body_list[i] * int(intensidad[1]))
            body_list[i+1] = 0
            body_list[i+2] = 0
        body =""
        c=0
        for x in body_list:
            c += 1
            body += str(x) + " "
            if c%9 == 0:
                body += "\n"
        return(body)

    def azul(self,body_list,intensidad):
        for i in range(0,(len(body_list)-3),3):
            body_list[i+2]=round(body_list[i+2] * int(intensidad[1]))
            body_list[i] = 0
            body_list[i+1] = 0
        body =""
        c=0
        for x in body_list:
            c += 1
            body += str(x) + " "
            if c%9 == 0:
                body += "\n"
        return(body)

    def verde(self,body_list,intensidad):
        for i in range(0,(len(body_list)-3),3):

            body_list[i+1]=round(body_list[i+1] * int(intensidad[1]))
            body_list[i] = 0
            body_list[i+2] = 0
        body =""
        c=0
        for x in body_list:
            c += 1
            body += str(x) + " "
            if c%9 == 0:
                body += "\n"
        return(body)

class Parceo():
     def parcear(self,dato):
        
        encabezado = dato.decode().splitlines()[0]
        print(encabezado)
        pedido = encabezado.split()[1]
        if pedido.count("?") == 1:
            pedido = pedido.split("?")
            ruta_archivo=pedido[0]
            query=pedido[1]
            query_list= query.split("&")
        else:
            ruta_archivo=pedido
            query_list=""
        #print(pedido)
        #print("ruta de archivo=",ruta_archivo)
        #print("query",query)
        #print(query_list)
        ruta_archivo= ruta_archivo.split("/")

        return(ruta_archivo,query_list)


class Handler(socketserver.BaseRequestHandler):

    def handle(self):
        p=Parceo()
        f=Filtros_ppm()

        ubicacion = args.documentroot
        os.chdir(ubicacion)
        dic={"ico":"image/vnd.svf","txt":" text/plain","jpg":" image/jpeg",
            "ppm":" image/x-portable-pixmap","html":" text/html","pdf":" application/pdf"}

        self.data = self.request.recv(1024)
        dato = self.data

        (ruta_archivo,query_list) = p.parcear(dato)
        #print(query_list)
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
        
        extension = archivo.split('.')[1]
        #print("Extension:",extension)
        #print(self.client_address)
        #print(self.data)
        
        if extension == "ppm" and query_list != "" and respuesta == "200 OK":
            print("querylist:",query_list)
            try:
                filtro=query_list[0].split("=")
            except:
                pass

            try:
                intensidad=query_list[1].split("=")
            except:
                pass


            fd = os.open(archivo, os.O_RDONLY)
            
            body = os.read(fd,os.stat(archivo).st_size)
            
            os.close(fd)
            
            (body_list,cabecera_ppm) =f.separar(f.eliminar_comentarios(body))
            #print("filtro:",filtro)
            #print(body_list)

            if filtro[0] == "filter":
            
                if filtro[1] == "R":
                    body_ppm=(f.rojo(body_list,intensidad))
                    print("Imagen filtro rojo")
            
                if filtro[1] == "B":
                    body_ppm=(f.azul(body_list,intensidad))
                    print("Imagen filtro azul")
 
                if filtro[1] == "G":
                    body_ppm=(f.verde(body_list,intensidad))
                    print("Imagen filtro verde")
 
                #if filtro[1] == "W":
                #    print("Imagen filtro black and white")
            
            header = bytearray("HTTP/1.1 "+respuesta+"\r\nContent-type:"+ dic[extension] 
                    +"\r\nContent-length:"+str(len(body_ppm)+len(cabecera_ppm))+"\r\n\r\n",'utf8')     
        
            self.request.sendall(header)
            self.request.sendall(bytearray(cabecera_ppm,"utf-8"))
            self.request.sendall(bytearray(body_ppm,"utf-8"))
            
            #print(cabecera_ppm)
            #print(str(body_ppm))
            #imagen = open("rojo.ppm", "w")
            #imagen.write(str(cabecera_ppm) + "\n")
            #imagen.write(str(body_ppm))
        
        else:
        
            fd = os.open(archivo, os.O_RDONLY)
            body = os.read(fd, 500000)
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

    if args.port > 65535 or args.port < 1023 :
        print("No tiene permisos para ocupar este puerto o NO existe-->default puerto 5000")
        args.port=5000
    
    socketserver.TCPServer.allow_reuse_address = True
    server =  socketserver.ThreadingTCPServer(("0.0.0.0", args.port), Handler)
    server.serve_forever()

    
