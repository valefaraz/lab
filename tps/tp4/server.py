import asyncio
import argparse
import sys
import os
from parceo import Parceo
from datetime import datetime

async def log(addr, ubicacion):
    f = open(str(ubicacion)+'/registro.txt', 'a')
    conexion ='cliente:' + str(addr) + '\t' + 'date:' + str(datetime.now()) + '\n'
    f.write(conexion)
    f.close()

async def handle_echo(reader, writer):
    p = Parceo()
    ubicacion = args.documentroot
    os.chdir(ubicacion)
    dic = {"ico": "image/vnd.svf", "txt": " text/plain", "jpg": " image/jpeg",
           "ppm": " image/x-portable-pixmap", "html": " text/html",
           "pdf": " application/pdf"}
    data = await reader.read(1000)
    addr = writer.get_extra_info('peername')
    try:
        ruta_archivo = p.parcear(data)    
    except Exception:
        pass
    
    print(ruta_archivo)
        
    for x in range(len(ruta_archivo)-1):
        if ruta_archivo[1+x] == '' and len(ruta_archivo) == 2:
            #print("cuando es /")
            archivo = 'index.html'
            respuesta = "200 OK"
            break
        if os.path.isfile(ruta_archivo[1+x]) == True:   #si existe el archivo
            archivo = ruta_archivo[1+x]
            respuesta = "200 OK"
            #print("existe el archivo")

        if os.path.isfile(ruta_archivo[1+x]) == False:   #si no esta el archivo
            archivo = '400error.html'
            respuesta = "404 Not Found"
            #print("no esta el archivo")
        if os.path.isdir(ruta_archivo[1+x]) == True:    #si existe el directorio
            os.chdir(ubicacion+"/"+ruta_archivo[1+x])
            archivo = "index.html"
            #print("existe el directorio")
        if ruta_archivo[1+x] == '':
            #print("cuando es /")
            archivo = 'index.html'
            respuesta = "200 OK"

    try:
        extension = archivo.split('.')[1]
        fd = os.open(archivo, os.O_RDONLY)
        body = os.read(fd,os.stat(archivo).st_size)
        os.close(fd)
        header = bytearray("HTTP/1.1 " + respuesta + "\r\nContent-type:" + dic[extension] 
                        +"\r\nContent-length:" + str(len(body)) + "\r\n\r\n",'utf8')       
        writer.write(header)
        writer.write(body)
        await writer.drain()
        writer.close()
    except FileNotFoundError:
        pass
    
    tarea = asyncio.create_task(log(addr,ubicacion))
    await tarea



async def main():
    server = await asyncio.start_server(
                    handle_echo,
                    ['127.0.0.1', '::1'], args.port)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='./server-http.py' +
                                           '[-h] -p PORT -d DOCUMENT ROOT' +
                                           '-s SIZE')

    parser.add_argument("-p", "--port", type=int, default=5000, help="Puerto")

    parser.add_argument("-s", "--size", type=int, default=50000,
                        help="Bloque de lectura")

    parser.add_argument("-d", "--documentroot", type=str, default=os.getcwd(),
                        help="/home/../..")

    args = parser.parse_args()

    if args.port > 65535 or args.port < 1023:
        print("No tiene permisos para ocupar este puerto o NO existe-->5000")
        args.port = 5000

    if args.size <= 0:
        print("El tamano de lectura [-s] no puede ser negativo")
        sys.exit()
    asyncio.run(main())
