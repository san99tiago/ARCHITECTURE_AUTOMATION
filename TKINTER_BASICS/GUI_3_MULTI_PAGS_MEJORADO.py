# -*- coding: utf-8 -*-

#SANTIAGO GARCIA ARANGO, 13 enero 2020
#CREACION DE UN GUI MULTIPAGINAS CON AYUDA DE TKINTER CON MEJOR DISENNO VISUAL Y FUNCIONALIDAD
#    https://www.youtube.com/watch?v=A0gaXfM1UN0&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=2
#Este codigo es util para trabajar con muchos frames superpuestos y dar la ilusion de cambio de pagina o esquema...
#Su funcionalidad es a traves de un contenedor principal (ventana), que tiene todos los frames deseados...
#Luego con interaccion de algun tipo, se accede a colocar en primer plano el frame deseado, mostrando unicamente este.


#Se importa tkinter como herramienta para creacion de GUIs
import tkinter as tk
#Se importa otro modulo de tkinter similar a CSS, con algunas mejoras en el sentido grafico/visual de la app
from tkinter import ttk
#Es util para trabajar con imagenes:
#(OJO: se debe descargar libreria, recomndado descargarlas con: "pip install pillow" )
#Esta libreria es muy importante, porque es la manera mas sencilla de usar imagenes
from PIL import ImageTk, Image


import math
#Algunas variables empleadas en el codigo y que es importante que sean de facil acceso...
LARGE_FONT = ("Verdana",12,"bold")


#Se crea la clase con el objetivo del manejo principal de la aplicacion. Es la encargada de procesar y acceder a todas las paginas.
#FUNDAMENTAL: heredar el objeto de tk.Tk, ya que con esto accedemos a manejo correcto de frames y funciones utiles importantes
#Tambien es necesario crear tantas clases, como paginas se deseen, cada clase lleva info de las otras pags
class APP(tk.Tk):
    #Por convencion, se inicializa con los "arguments" y "key words arguments"
    def __init__(self, *args, **kwargs):
        #Se inicializa a su vez funcionalidad de tkinter principal
        tk.Tk.__init__(self, *args, **kwargs)

        #Se agrega ICO que ira en la parte superior izquiera (se puede indicar path, o si esta en carpeta, no es necesario)
        tk.Tk.iconbitmap( self, "ICON_2.ico")

        #Se agrega el nombre de la ventana principal de trabajo, o nombre de la app
        tk.Tk.wm_title( self, "PROYECTOS ALCUBO ARQUITECTOS" )

        #Se obliga el tamanno de la ventana total a ser el maximo posible: 

        # #FORMA 1 (sin barra superior)
        # tk.Tk.attributes( self,"-fullscreen", True )

        # #FORMA 2 (con barra superior)... es similar a la primera forma, pero sin haber maximizado como tal
        # w, h = tk.Tk.winfo_screenwidth(self), tk.Tk.winfo_screenheight(self)
        # tk.Tk.geometry(self, "%dx%d+0+0" % (w, h))

        #Se agregan variables globales para el tamanno en pixeles de la pantalla empleada (para hacerlo independiente de la pantalla))
        global h
        global w
        w, h = tk.Tk.winfo_screenwidth(self), tk.Tk.winfo_screenheight(self)

        #FORMA 3 (ventana maximizada con barra superior) (yo prefiero esta)
        tk.Tk.state(self, "zoomed")

        #Se evita que se pueda cambiar el tamanno o dimension de la ventana, para evitar descuadres en los widgets
        tk.Tk.resizable(self, 0,0)


        #Se crea un contenedor principal para poder almacenar los frames y las ventanas deseadas
        contenedor = tk.Frame(self)
        #Posicionamos en totalidad de ventana, el contenedor que servira para agregar los frames necesitados
        #Ademas, se llena en totalidad, con los parametros internos, permitiendo expandir
        contenedor.pack( side = "top",fill = "both", expand = True )
        #Se da igual peso a las filas y columna del contenedor, con tamanno minimo posible igual a cero
        contenedor.grid_rowconfigure(0, weight = 1)
        contenedor.grid_columnconfigure(0, weight = 1) 

        #Se crea un diccionario en donde se guardaran todos los frames, para el manejo de las paginas diferentes correcto
        self.frames = {}

        #OJO: Agregar todas las clases a la tupla que recorremos, para luego poder recorrer paginas como se desee
        #Ahora debemos garantizar que TODOS los frames que queramos, se incluyan en el diccionario...
        #Es decir, se pasan TODAS las clases asociadas a las paginas con las que trabajaremos, y se agregan correctamente...
        for F in (PaginaInicio , PaginaCrearProyecto,PaginaIniciarTerminarSubetapa):
            #Se agregan los elementos respectivos de cada frame en la tupla que se recorre, asociada a las clases
            #Notar que el contenedor es el que llamamos "parent" porque aqui ira el frame, NO OLVIDAR EL "self"
            frame = F( contenedor,self )
            #Se agrega el frame respectivo, con el nombre de la clase al diccionario de frames 
            self.frames[F] = frame
            #Luego de crear frame y agregarla al diccionario, se posiciona visualmente en tkinter
            frame.grid(row = 0, column = 0, sticky = "nsew")
        
        #OJO: luego se debe llamar al metodo "show_frame", creado por nosotros, para mostrar un frame deseado...
        #...en esencia, permite traer al primer plano, un frame del vector "self.frames"
        self.show_frame( PaginaInicio )


    def show_frame(self,controller):
        #Se selecciona el frame requerido por el controller, desde el diccionario de frames ya creado anteriormente
        frame = self.frames[controller]
        #Ahora se llama a funcion de tkinter heredada desde clase APP, la cual permite traer frame indicada a primer plano
        frame.tkraise()




#Se crean las paginas con la que se trabajaran los frames para tener multiples paginas funcionando sobre el contenedor 
#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
   
class PaginaInicio(tk.Frame):
    #Se inicializa con parent(Clase principal de la APP) y el controller(encar)
    def __init__(self,parent,controller):
        #Se inicializa el Frame de tkinter desde el parent
        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.config(self,bg = "black")
        #Agregar imagenes... (con libreria PIL)
        #... se crea formato interno de imagen (path puede variar)
        #OJO, proceso tambien incluye redimensionar la imagen a los pixeles deseados, en este caso a con redondeo del porcentaje total de la pantalla...(con Image.ANTIALIAS)
        # img_1 = ImageTk.PhotoImage( Image.open("FOTO_1.jpg").resize( (math.floor(w*0.1),math.floor(h*0.2)),Image.ANTIALIAS ) )
        #OJO: al agregar imagenes, se TIENE que agregar como "self", de lo contrario, NO aparece!
        self.img_1 = ImageTk.PhotoImage( Image.open("FOTO_1.jpg").resize( ( math.floor(0.1*w),math.floor(0.2*h) ),Image.ANTIALIAS ) )
        
        #Se crea la imagen sobre widget de Label, con parametro "image"
        cuadro_img_1 = tk.Label( self, image = self.img_1 )
        #Se posiciona esta imagen, con las condiciones deseadas
        cuadro_img_1.grid( column = 10, row = 10, columnspan = 2, rowspan = 2, sticky = 'se')

        #Ahora se crea la info grafica/interactiva/estetica de la pagina de inicio
        INFO_1 = tk.Label(self, text = "¡ Bienvenido al administrador de proyectos de Alcubo Arquitectos !", font = LARGE_FONT, bg = "black",fg = "yellow")
        INFO_1.grid(row = 0, column = 2, pady = math.floor(h*0.05), padx = math.floor(w*0.05))

        INFO_2 = tk.Label(self, text = "¿ Qué deseas hacer ?", font = LARGE_FONT, bg = "black",fg = "yellow")
        INFO_2.grid(row = 1, column = 2, sticky = "n")

        #Se muestra menu desplegable con las opciones a realizar:
        #Se debe crear variable asociada al menu respectivo...(para indicar elegido respectivo):
        elegido_menu_inicial = tk.StringVar(self)
        # elegido_menu_inicial.set("")
        #...OJO: CREAR MENU A PARTIR DE VECTOR:
        VECTOR = ["CREAR PROYECTO","INICIAR / TERMINAR SUBETAPA","AGREGAR INGRESO / GASTO","CAMBIAR NOMBRE ETAPA","AGREGAR PERSONAL ETAPA","ASIGNAR LABOR PERSONA","CULMINAR LABOR PERSONA","AGREGAR AREA ETAPA","AGREGAR NUEVA ETAPA"]
        #TRUCO: importar modulo ttk desde tkinter (ver al inicio), para tener un dropdownmenu mucho mejor y que tenga scrollbar (en caso de ser muchos proyectos)
        menu_1 = ttk.Combobox(self, textvariable = elegido_menu_inicial, values = VECTOR,width = math.floor(0.1*h)  )
        menu_1.grid(row = 3, column = 2,pady = math.floor(0.1*h) )

        #Se muestra un boton con funcionalidad de pasar de pagina. Ojo con  "command = lambda: controller.show_frame(PaginaDos)"...
        boton_ir = ttk.Button( self,text = "IR",command = lambda : self.accion_inicio(menu_1.get() ) )
        boton_ir.grid(row = 3,column =3)
    
    #Este metodo de la pagina principal, permite segun la opcion elegida, realizar una accion con el boton creado en el inicializador
    def accion_inicio(self,opcion_elegida):
        if opcion_elegida == "CREAR PROYECTO":
            self.controller.show_frame(PaginaCrearProyecto)
            print( opcion_elegida )
        elif opcion_elegida == "INICIAR / TERMINAR SUBETAPA":
            self.controller.show_frame(PaginaIniciarTerminarSubetapa)

#Se crea la info de la pagina 2, similar a la info de la pagina uno.. este proceso ya se vuelve muy estandar
#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaCrearProyecto(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        tk.Frame.config(self,bg = "black")
        INFO = tk.Label(self, text = "CREACIÓN DE PROYECTO NUEVO", font = LARGE_FONT, bg = "black",fg = "yellow")
        INFO.grid(row = 0, column = 0, pady = math.floor(0.01*h) , padx = math.floor(0.01*w))
        boton_retorno = ttk.Button( self,text = "go to page 1",command = lambda : controller.show_frame(PaginaInicio) )
        boton_retorno.grid(row = 3,column = 0, padx = math.floor(0.01*w), sticky = "w" )
        boton_agregar_proyecto = ttk.Button( self,text = "go to page 3",command = lambda : controller.show_frame(PaginaIniciarTerminarSubetapa) )
        # boton_agregar_proyecto.grid(column )

#Se crea la info de la pagina 3, similar a la info de la pagina uno y dos.. este proceso se vuelve muy estandar
#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaIniciarTerminarSubetapa(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        INFO = tk.Label(self, text = "PAGINA 3", font = LARGE_FONT)
        INFO.pack()
        boton_2 = ttk.Button( self,text = "go to page 2",command = lambda : controller.show_frame(PaginaCrearProyecto) )
        boton_2.pack()








## Se crea la APP para mostrar el funcionamiento...
APP_SANTI = APP()
APP_SANTI.mainloop()
print(w,h)