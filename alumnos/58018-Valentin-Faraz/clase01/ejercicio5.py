def fibo(n,a=0,b=1):                #Este codigo muestra la serie de Fibonacci
   while n!=0:                      #Mientras n sea distinto de cero se ejecuta la secuencia
      return fibo(n-1,b,a+b)        #N disminuye en uno, 'a' toma el valor de 'b' y 'b' toma el valor de 'a+b'  
   return a                         #La funcion fibo returna el valor de 'a'

for i in range(0,10):               #Se imprimen los valores que returna la funcion fibo a medida que se le da valores a 'n'
   print(fibo(i))                   #'n' toma valores desde el 0 hasta el 10, se returna 'a' 11 veces
                                    #Cambiando los argumentos de range() podriamos obtener los elementos de Fibonacci que queramos