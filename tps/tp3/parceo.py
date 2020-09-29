class Parceo():
     def parcear(self,dato):
        try:
            encabezado = dato.decode().splitlines()[0]
            pedido = encabezado.split()[1]
        except:
            pass
        
        try:
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
        except:
            pass
        
