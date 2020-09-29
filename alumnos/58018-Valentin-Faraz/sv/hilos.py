import os
from itertools import islice
from concurrent import futures
import time
from math import ceil
intensidad = 1
body_list = []
size=0

class Filtros_ppm():
    def separar(self,imagen_read):
        header=""
        for i in imagen_read.splitlines():
            header += i.decode()+"\n"
            if i == b"255":
                break

        #print(header)
        #print(len(header))
        #header = imagen_read[:15].decode()
        header = header.replace("P6","P3")
        
        #body = imagen_read[len(header):]
        
        return(header)
    
    def rojo(self,start):
        #global intensidad
        #global body_list
        #print(start)
        for i in range(start,(start+size+3),3):
            body_list[i] = ceil(body_list[i] * intensidad)
            if body_list[i] > 255:
                body_list[i]= 255
            body_list[i+1] = 0
            body_list[i+2] = 0
        #print (body_ppm)
        #return(body_list)

if __name__ == "__main__":
    f=Filtros_ppm()
    fd = open("dog.ppm","rb")
    lectura=fd.read()
    
    header_ppm=f.separar(lectura)
    #print(header_ppm)
    fd.seek(len(header_ppm))
    
    #print(body_list)
    
     
    body= fd.read()
    fd.close()
    body_list = [x for x in body]
    size=100000

    while True:
        if size%3 !=0:
            size += 1
            if size%3 == 0:
                break
    
    #print(size)
    #file_size = os.stat("dog.ppm").st_size
    #print(file_size)
    size_body_list=len(body_list)
    #print(size_body_list)
    n_threads= ceil(size_body_list/size)
    print(n_threads)
    a=list(range(0,size_body_list,size))
    print(a)
    hilos = futures.ThreadPoolExecutor(max_workers=n_threads)
    resultado_a_futuro = hilos.map(f.rojo,a)
    #print ((resultado_a_futuro))
    
    
    #print(len(body_list))
    
    body_ppm =""
    c=0
    for x in body_list:
        c += 1
        body_ppm += str(x) + " "
        if c%9 == 0:
            body_ppm += "\n"
    imagen = open("rojelio.ppm", "w")
    imagen.write(header_ppm + "\n")
    imagen.write(body_ppm)
    
    
    #print(body_ppm)
    #print(cabecera_ppm)