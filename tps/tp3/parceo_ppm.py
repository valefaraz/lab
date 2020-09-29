def separar(imagen_read):
    header=""
    for i in imagen_read.splitlines():
        header += i.decode()+"\n"
        if i == b"255":
            break
    header = header.replace("P6","P3")
    body = imagen_read[len(header):]
    return(header,body)