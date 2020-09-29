import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1",5000))
s.listen(1)
c=0
while True:
    c = c+1
    s2,addr = s.accept() 
    print (addr)                            #datos de la conexion
    recibido = s2.recv(1024)                 #recibe lo que envia el cliente
    print("PEDIDO",c)
    print (recibido)                         #muestra lo recibido por el server
    respuesta = recibido.decode().upper()    #transforma lo recibido en mayuscula
    s2.send(respuesta.encode())             #envia al cliente la respuesta
    s2.close()