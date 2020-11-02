class Parceo():

    def parcear(self, dato):
        try:
            encabezado = dato.decode().splitlines()[0]
            pedido = encabezado.split()[1]
            ruta_archivo = pedido
            ruta_archivo = ruta_archivo.split("/")
            return(ruta_archivo)
        except SystemError:
            pass

