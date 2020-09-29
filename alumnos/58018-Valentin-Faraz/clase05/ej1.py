import argparse
import os
import time

parser = argparse.ArgumentParser(usage= "-f nombre.txt" )
parser.add_argument('-f', action="store", metavar='archivo', type=str,
                    required=True, help="Archivo a abrir")


args = parser.parse_args()
pipe_r, pipe_w = os.pipe()
hijo = os.fork()

if hijo == 0:

    os.close(pipe_w)
    print("Hijo iniciado\n")
    while True:
        leido = os.read(pipe_r, 15).decode()
        leido = leido.replace("\n", "")
        if leido == '':
            break
        print("Leyendo: " + leido[::-1].upper())
        

    exit()

else:
    archivo = open("/home/valentin/Escritorio/compu2/lab/alumnos/58018-Valentin-Faraz/clase05/" + str(args.f),"rb")
    #with open(args.f,"r") as archivo:
    print("\nEscribiendo...")
    for linea in archivo.readlines():
        #time.sleep(1)
        os.write(pipe_w, linea)
    archivo.close()

os.close(pipe_r)
os.close(pipe_w)
os.wait()