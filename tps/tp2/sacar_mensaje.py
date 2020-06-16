import argparse






if __name__ == "__main__":
    pass

    parser = argparse.ArgumentParser(usage="./esteganografia.py [-h] -s SIZE -f FILE -m FILE -f PIXELS -i PIXELS -o FILE2")
    parser.add_argument("-f", "--file", type=str, required=True, help="Archivo portador .ppm")
    parser.add_argument("-e", "--offset", type=int, default="1", help="Mensaje offset en pixels del inicio del raster")
    parser.add_argument("-i", "--interleave", type=str, default="1", help="Interleave de modificacion en pixel")
    parser.add_argument("-r", "--inicio", type=int, required=True, help="inicio del cuerpo")
    parser.add_argument("-x", "--tamaño", type=int, required=True, help="tamaño mensaje en bytes")
    args = parser.parse_args()

archivo = open(args.file,"rb")

archivo.seek(args.inicio)

lectura = archivo.read()
body_list = [int(x) for x in lectura]
lista=[]
inicio= args.offset * 3
fin =inicio + args.tamaño*(int(args.interleave)*3)
step = int(args.interleave)*3

for x in range(inicio,fin,step):
    print("rojo")
    lista.append()
