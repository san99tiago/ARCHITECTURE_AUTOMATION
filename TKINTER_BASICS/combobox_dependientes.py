#Santiago Garcia Arango, Enero 14 de 2020
#Codigo que permite mostrar info de segundo Combobox, a partir de la info del primero...
#... muy util al tener proyectos con dependencias multiples de los menus de eleccion

import tkinter as tk
from tkinter import ttk

#Se crea ventana principal de trabajo
root = tk.Tk()
root.config(bg = "black")
root.geometry("720x380")
#Funcion con el que se procesa el cambio de info en el segundo combobox (notar nombre variable), ojo con esto...
#... porque al trabajar con clase se debe cuidar de hacerlo global o en self, dependiendo de estructura
#OJO: "event" es el parametro asociado al VirtualEvent ejecutado en el momento de seleccionar algo en primer combobox (se debe dejar parametro)
def ACCION(event):
    #Se accede a posicion del combobox seleccionada (empiezan en cero...), es decir, posicion del vector asociado
    current = combobox.current()

    #Este print es para mostrar la ejecucion interna de los eventos al hacer click y su formato (curiosidad)
    print(current)
    print(event)

    #Si el texto del combobox inicial es diferente de las opciones, se accede...
    if current != -1:
        #Se accede al vector con la info de combobox inicial, y se devuelve la info asociada a este valor (numerico)
        value = values[current]

        #Se muestra la info asociada al vector inicial, el la posicion current (osea el texto con info seleccionada)
        print(value)

        #Se ejecuta un cambio en los vectores del segundo combobox, de tal forma que estas dependan del primero
        if value == "PYTHON":
            combobox2.config(values = ["P","1","2","3"])

        elif value == "JAVA":
            combobox2.config(values = ["J","alfa","beta","gamma"])

        elif value == "C++":
            combobox2.config(values = ["C","alfa","beta","gamma"])

        elif value == "RUBY":
            combobox2.config(values = ["R","alfa","beta","gamma"])


#CREACION DE COMBOBOXs....
#Valores asociados al primer combobox
values = ['PYTHON', 'JAVA', 'C++',"RUBY"]

#Se crea combobox inicial, con valores por defecto estandar 
combobox = ttk.Combobox(root, values=values)
#Se agrega bind, con el objetivo de que al seleccionar algo de este combobox, se ejecute la "ACCION", que luego se define arriba
combobox.bind('<<ComboboxSelected>>', ACCION)
combobox.pack()

#Se crea el segundo combobox, el cual inicialmente solo tiene una opcion obsoleta y luego...
#...sus opciones van a depender de lo seleccionado en el primer combobox a traves de "ACCION"
combobox2 = ttk.Combobox(root, values = [])
combobox2.config( values = ["nada de nada"] )
combobox2.pack()




#Se ejecuta ventana para el ejemplo
root.mainloop()