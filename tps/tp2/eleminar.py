

def eliminar_comentarios(imagen_read):
    inicio_comentario = 0
    fin_comentario = 0
    for n in range(imagen_read.count(b"\n#")):
        inicio_comentario = imagen_read.find(b"\n#")
        fin_comentario = imagen_read.find(b"\n", inicio_comentario + 1)
        imagen_read = imagen_read.replace(imagen_read[inicio_comentario:fin_comentario], b"")
    ancho= int(imagen_read[3:6].decode())
    alto = int(imagen_read[7:10].decode())
    return (imagen_read,ancho,alto)