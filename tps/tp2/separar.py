

def separar(image):
    #global body_list
    return_1 = image.find(b"\n") + 1
    return_2 = image.find(b"\n", return_1) + 1
    header_end = image.find(b"\n", return_2) + 1
    header = image[:header_end].decode()
    #header = header.replace("P6","P3")
    return(header)