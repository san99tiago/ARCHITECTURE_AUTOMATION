#Repasos rapidos de la funcionalidad de la libreria Tkinter para crear GUIs(Graphical User Interfase)
#TUTORIAL:   https://www.youtube.com/watch?v=YXPyB4XeYLA&t=17312s
#Se deben importar tkinter (como base) y ttk (como apoyo a mejores funciones con mas ventajas que Tkinter)
import tkinter
from tkinter import ttk
#Es util-para indicar el path cuando trabajemos con "png", "jpg"y "ico"
import os
#Util para tamanno de iconos...
import math
#Es util para trabajar con imagenes....
#(OJO: se debe descargar libreria, recomndado descargarlas con: "pip install pillow" )
#Esta libreria es muy importante, porque es la manera mas sencilla de usar imagenes
from PIL import ImageTk, Image


#--------------------------------COMIENZA LA CREACION DE LA VENTANA DE TRABAJO----------------------------------

#Se crea la ventana principal en donde se guardara la info y se mostrara todo
root = tkinter.Tk()

#En esta parte hacemos que la ventana sea automaticamente FULL SIZE....
def FULL_SIZE_VENTANA():
    #Se crean variables globales(para hacer todos los widgets en terminos de porcentajes)
    global w
    global h
    #Se asignan estas variables al tamanno respectivo horizontal y vertical de la pantalla del PC
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    #Se modifica la geometria de la ventana para que sea del tamanno maximo posible
    root.geometry("%dx%d+0+0" % (w, h) )
    #Se evita que se pueda cambiar el tamanno, para evitar descuadres en los widgets
    root.resizable( 0,0)

#Se garantiza que el tamanno de la ventana sea el maximo posible ( con la funcion de arriba)
FULL_SIZE_VENTANA()

root.columnconfigure(0, uniform = 1)
root.rowconfigure(0, uniform = 1)

#Se agrega el titulo a la ventana de trabajo, para mostrar en la parte superior
root.title = "TEST 1 TKINTER SANTI"

#Se agrega el icono de la ventana de trabajo, el cual tambien se indica en la parte superior a la izquierda
#...se debe tener el icono en formato "ico" en la misma carpeta de trabajo (sino, indicar path absoluto)
root.iconbitmap( "{}\\ICON_1.ico".format( os.getcwd() ) )



#Agregar imagenes... (con libreria PIL)
#... se crea formato interno de imagen (path puede variar)
#OJO, proceso tambien incluye redimensionar la imagen a los pixeles deseados, en este caso a con redondeo del porcentaje total de la pantalla...(con Image.ANTIALIAS)
# img_1 = ImageTk.PhotoImage( Image.open("FOTO_1.jpg").resize( (math.floor(w*0.1),math.floor(h*0.2)),Image.ANTIALIAS ) )
img_1 = ImageTk.PhotoImage( Image.open("FOTO_1.jpg").resize( (100,100),Image.ANTIALIAS ) )

#Se crea la imagen sobre widget de Label, con parametro "image"
cuadro_img_1 = tkinter.Label( root, image = img_1 )
#Se agrega visualmente en el grid o lugar donde se desee mostrar
cuadro_img_1.grid( column = 0, row = 0,)



#Dropdown menus...
#Se debe crear variable asociada al menu respectivo...(para indicar elegido respectivo)
elegido_menu_1 = tkinter.StringVar(root)
elegido_menu_1.set("ELEGIR PROYECTO")
#Se crea el menu y luego se coloca en root...
#...OJO: CREAR MENU A PARTIR DE VECTOR:
VECTOR = []
for i in range( 50 ):
    VECTOR.append( str(i+1) + ". PROYECTO ALGO" )
#TRUCO: importar modulo ttk desde tkinter (ver al inicio), para tener un dropdownmenu mucho mejor y que tenga scrollbar (en caso de ser muchos proyectos)
menu_1 = ttk.Combobox( root, textvariable = elegido_menu_1, values = VECTOR )
menu_1.grid(row = 1, column = 3)



#Se ejecuta el "mainloop" que permite correr el codigo de la ventana correctamente
root.mainloop()
