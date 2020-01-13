#SANTIAGO GARCIA ARANGO, 13 enero 2020
#CREACION DE UN GUI MULTIPAGINAS CON AYUDA DE TKINTER...
#    https://www.youtube.com/watch?v=A0gaXfM1UN0&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=2
#Este codigo es util para trabajar con muchos frames superpuestos y dar la ilusion de cambio de pagina o esquema...
#Su funcionalidad es a traves de un contenedor principal (ventana), que tiene todos los frames deseados...
#Luego con interaccion de algun tipo, se accede a colocar en primer plano el frame deseado, mostrando unicamente este.


#Se importa tkinter como herramienta para creacion de GUIs
import tkinter as tk
#Algunas variables empleadas en el codigo y que es importante que sean de facil acceso...
LARGE_FONT = ("Verdana",12,"bold")


#Se crea la clase con el objetivo del manejo principal de la aplicacion. Es la encargada de procesar y acceder a todo
#FUNDAMENTAL: heredar el objeto de tk.Tk, ya que con esto accedemos a manejo correcto de frames y funciones utiles importantes
class APP(tk.Tk):
    #Por convencion, se inicializa con los "arguments" y "key words arguments"
    def __init__(self, *args, **kwargs):
        #Se inicializa a su vez funcionalidad de tkinter principal
        tk.Tk.__init__(self, *args, **kwargs)

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
        for F in (PaginaInicio , PaginaDos,PaginaTres):
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
        tk.Frame.__init__(self,parent)
        
        #Ahora se crea la info grafica/interactiva/estetica de la pagina de inicio
        INFO_1 = tk.Label(self, text = "PAGINA 1", font = LARGE_FONT)
        INFO_1.pack()

        #Se muestra un boton con funcionalidad de pasar de pagina. Ojo con  "command = lambda: controller.show_frame(PaginaDos)"...
        #... la razon es porque asi se pasan funciones con parametros en tkinter, de lo contrario no corre el loop correctamente.
        #Notar que la PaginaDos es la clase asociada a la nueva pagina a la que queremos ir
        boton_1 = tk.Button( self,text = "go to page 2",command = lambda : controller.show_frame(PaginaDos) )
        boton_1.pack()

#Se crea la info de la pagina 2, similar a la info de la pagina uno.. este proceso ya se vuelve muy estandar
#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaDos(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        INFO = tk.Label(self, text = "PAGINA 2", font = LARGE_FONT)
        INFO.pack()
        boton_1 = tk.Button( self,text = "go to page 1",command = lambda : controller.show_frame(PaginaInicio) )
        boton_1.pack()
        boton_2 = tk.Button( self,text = "go to page 3",command = lambda : controller.show_frame(PaginaTres) )
        boton_2.pack()

#Se crea la info de la pagina 3, similar a la info de la pagina uno y dos.. este proceso se vuelve muy estandar
#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaTres(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        INFO = tk.Label(self, text = "PAGINA 3", font = LARGE_FONT)
        INFO.pack()
        boton_2 = tk.Button( self,text = "go to page 2",command = lambda : controller.show_frame(PaginaDos) )
        boton_2.pack()








## Se crea la APP para mostrar el funcionamiento...
APP_SANTI = APP()
APP_SANTI.mainloop()