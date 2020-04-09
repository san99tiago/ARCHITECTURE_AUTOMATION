# -*- coding: utf-8 -*-

#VERSION BETA.
#EMPRESA PROPIETARIA: ALCUBO ARQUITECTOS.
#DESARROLLADOR:  SANTIAGO GARCIA ARANGO, (enero-marzo 2020)
#CREACION DE UN GUI MULTIPAGINAS CON AYUDA DE TKINTER CON MEJOR DISENNO VISUAL Y FUNCIONALIDAD
#    https://www.youtube.com/watch?v=A0gaXfM1UN0&list=PLQVvvaa0QuDclKx-QpC9wntnURXVJqLyk&index=2
#Este codigo es util para trabajar con muchos frames superpuestos y dar la ilusion de cambio de pagina o esquema...
#Su funcionalidad es a traves de un contenedor principal (ventana), que tiene todos los frames deseados...
#Luego con interaccion de algun tipo, se accede a colocar en primer plano el frame deseado, mostrando unicamente este.

#Se intenta correr en calidad visual mejorada:
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
#SE IMPORTAN OTROS ARCHIVOS DE PYTHON QUE TRABAJAN EN CONJUNTO:
import INFO_DIR_ACTUAL
import MASTER
import CAMBIAR_NOMBRE_PROYECTO
import CREAR_TXT_BACKUP
import ELIMINAR_PROYECTO
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell



#Se importa tkinter como herramienta para creacion de GUIs
import tkinter as tk
#Se importa otro modulo de tkinter similar a CSS, con algunas mejoras en el sentido grafico/visual de la app
from tkinter import ttk
from tkinter.messagebox import showinfo
#Es util para trabajar con imagenes:
#(OJO: se debe descargar libreria, recomndado descargarlas con: "pip install pillow" )
#Esta libreria es muy importante, porque es la manera mas sencilla de usar imagenes
from PIL import ImageTk, Image
import math
import glob
import datetime
import os




#Algunas FONTS empleadas en el codigo y que es importante que sean de facil acceso...
LARGE_FONT = ("Verdana",12,"bold")
SMALL_FONT = ("Verdana",10,"bold")


#Se crea la clase con el objetivo del manejo principal de la aplicacion. Es la encargada de procesar y acceder a todas las paginas.
#FUNDAMENTAL: heredar el objeto de tk.Tk, ya que con esto accedemos a manejo correcto de frames y funciones utiles importantes
#Tambien es necesario crear tantas clases, como paginas se deseen, cada clase lleva info de las otras pags
class APP(tk.Tk):
    #Por convencion, se inicializa con los "arguments" y "key words arguments"
    def __init__(self, *args, **kwargs):
        #Se inicializa a su vez funcionalidad de tkinter principal
        super().__init__(*args, **kwargs)

        #Se utilizar clase principal de MASTER para interpretar txt (OJO con nombre de archivo)
        self.M = MASTER.INTERPRETAR_TXT( glob.glob("REGISTROS.txt")[0] )
        
        #Se utiliza clase principal de CREAR_TXT_BACKUP para guardar los backups de txt en carpetas de excel
        self.BACKUP = CREAR_TXT_BACKUP.CREAR_TXT_BACKUP()
        self.BACKUP.nuevo_txt()

        #Se agrega ICO que ira en la parte superior izquiera (se puede indicar path, o si esta en carpeta, no es necesario)
        self.iconbitmap( self, "ICON_2.ico")

        #Se agrega el nombre de la ventana principal de trabajo, o nombre de la app
        self.title("PROYECTOS ALCUBO ARQUITECTOS")

        #Se agregan variables globales para el tamanno en pixeles de la pantalla empleada (para hacerlo independiente de la pantalla))
        global h
        global w
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()

        #Esto depende del tamanno de pantalla (SE DEBE CAMBIAR ESTAS LINEAS EN CASO DE SER NECESARIO)
        w = w/2
        h = h/2

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
        for F in (PaginaInicio , PaginaCrearProyecto,PaginaIniciarTerminarSubetapa,PaginaAgregarIngresoGasto, PaginaCambiarNombreEtapa, PaginaAgregarNombrePersonal,PaginaAgregarAreaEtapa, PaginaAgregarNuevaEtapa, PaginaCambiarNombreProyecto,PaginaEliminarProyecto):
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
        if controller == PaginaInicio:    
            print("pag inicio")
            frame.menu_1.focus()
            #SIEMPRE QUE ESTEMOS EN INICIO, SE ACTUALIZAN PROYECTOS Y SE CREAN REGISTROS, AL IGUAL QUE BACK UP EN CARPETA RESPECTIVA
            self.M.actualizar_todo()
            self.M.crear_excel_de_proyectos()
            self.BACKUP.nuevo_txt()

        elif controller == PaginaCrearProyecto:
            #Se actualiza que se vean los proyectos que se deseen mostrar (lista de proyectos despegables)
            proyectos_actualizados = self.M.get_nombre_proyectos()


        elif controller == PaginaAgregarIngresoGasto:
            #Se actualiza que se vean los proyectos que se deseen mostrar (lista de proyectos despegables)
            proyectos_actualizados = self.M.get_nombre_proyectos()
            frame.seleccion_proyecto.config(values = proyectos_actualizados)

        elif controller == PaginaIniciarTerminarSubetapa:
            #Se actualiza que se vean los proyectos que se deseen mostrar (lista de proyectos despegables)
            proyectos_actualizados = self.M.get_nombre_proyectos()
            frame.seleccion_proyecto.config(values = proyectos_actualizados)
        
        elif controller == PaginaCambiarNombreEtapa:
            #Se actualiza que se vean los proyectos que se deseen mostrar (lista de proyectos despegables)
            proyectos_actualizados = self.M.get_nombre_proyectos()
            frame.seleccion_proyecto.config(values = proyectos_actualizados)

        elif controller == PaginaAgregarNombrePersonal:
            #Se actualiza que se vean los proyectos que se deseen mostrar (lista de proyectos despegables)
            proyectos_actualizados = self.M.get_nombre_proyectos()
            frame.seleccion_proyecto.config(values = proyectos_actualizados)

        elif controller == PaginaAgregarAreaEtapa:
            #Se actualiza que se vean los proyectos que se deseen mostrar (lista de proyectos despegables)
            proyectos_actualizados = self.M.get_nombre_proyectos()
            frame.seleccion_proyecto.config(values = proyectos_actualizados)

        elif controller == PaginaAgregarNuevaEtapa:
            #Se actualiza que se vean los proyectos que se deseen mostrar (lista de proyectos despegables)
            proyectos_actualizados = self.M.get_nombre_proyectos()
            frame.seleccion_proyecto.config(values = proyectos_actualizados)

        elif controller == PaginaCambiarNombreProyecto:
            #Se actualiza que se vean los proyectos que se deseen mostrar (lista de proyectos despegables)
            proyectos_actualizados = self.M.get_nombre_proyectos()
            frame.seleccion_proyecto.config(values = proyectos_actualizados)

        elif controller == PaginaEliminarProyecto:
            #Se actualiza que se vean los proyectos que se deseen mostrar (lista de proyectos despegables)
            proyectos_actualizados = self.M.get_nombre_proyectos()
            frame.seleccion_proyecto.config(values = proyectos_actualizados)

        frame.tkraise()





#Se crean las paginas con la que se trabajaran los frames para tener multiples paginas funcionando sobre el contenedor 
#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
   
class PaginaInicio(tk.Frame):
    #Se inicializa con parent(Clase principal de la APP) y el controller(encar)
    def __init__(self,parent,controller):
        #Se inicializa el Frame de tkinter desde el parent
        self.controller = controller
        super().__init__(parent )
        self.configure(background = "black")
        #Agregar imagenes... (con libreria PIL)
        #... se crea formato interno de imagen (path puede variar)
        #OJO, proceso tambien incluye redimensionar la imagen a los pixeles deseados, en este caso a con redondeo del porcentaje total de la pantalla...(con Image.ANTIALIAS)
        # img_1 = ImageTk.PhotoImage( Image.open("FOTO_1.jpg").resize( (math.floor(w*0.1),math.floor(h*0.2)),Image.ANTIALIAS ) )
        #OJO: al agregar imagenes, se TIENE que agregar como "self", de lo contrario, NO aparece!
        self.img_1 = ImageTk.PhotoImage( Image.open("FOTO_1.jpg").resize( ( math.floor(0.1*w),math.floor(0.2*h) ),Image.ANTIALIAS ) )
        
        #Se crea la imagen sobre widget de Label, con parametro "image"
        cuadro_img_1 = tk.Label( self, image = self.img_1 )
        #Se posiciona esta imagen, con las condiciones deseadas
        cuadro_img_1.grid( column = 5, row = 10, columnspan = 2, rowspan = 3, sticky = 'se', padx = (math.floor(0.02*w),0 ),pady = (math.floor(0.05*h),0) )

        #Ahora se crea la info grafica/interactiva/estetica de la pagina de inicio
        INFO_1 = tk.Label(self, text = "¡ Bienvenido al administrador de proyectos de Alcubo Arquitectos !", font = LARGE_FONT, bg = "black",fg = "yellow")
        INFO_1.grid(row = 0, column = 1, pady = math.floor(h*0.05), padx = math.floor(w*0.05))

        INFO_2 = tk.Label(self, text = "¿ Qué deseas hacer ?", font = LARGE_FONT, bg = "black",fg = "yellow")
        INFO_2.grid(row = 1, column = 1, sticky = "n")

        #Se muestra menu desplegable con las opciones a realizar:
        #Se debe crear variable asociada al menu respectivo...(para indicar elegido respectivo):
        self.elegido_menu_inicial = tk.StringVar(self)
        # elegido_menu_inicial.set("")
        #...OJO: CREAR MENU A PARTIR DE VECTOR:
        VECTOR = ["CREAR PROYECTO","INICIAR / TERMINAR SUBETAPA","AGREGAR INGRESO / GASTO","CAMBIAR NOMBRE ETAPA","AGREGAR PERSONAL ETAPA","AGREGAR AREA ETAPA","AGREGAR NUEVA ETAPA","CAMBIAR NOMBRE PROYECTO","ELIMINAR PROYECTO"]
        #TRUCO: importar modulo ttk desde tkinter (ver al inicio), para tener un dropdownmenu mucho mejor y que tenga scrollbar (en caso de ser muchos proyectos)
        self.menu_1 = ttk.Combobox(self, textvariable = self.elegido_menu_inicial, values = VECTOR, state = "readonly",width = math.floor(0.03*w)  )
        self.menu_1.grid(row = 3, column = 0, columnspan = 2, sticky = "ew", padx = (math.floor(0.02*w) , math.floor(0.02*w)), pady = math.floor(0.05*h)  )

        #Se muestra un boton con funcionalidad de pasar de pagina. Ojo con  "command = lambda: controller.show_frame(PaginaDos)"...
        boton_ir = ttk.Button( self,text = "IR",command = lambda : self.accion_inicio(self.menu_1.get() ) )
        boton_ir.grid(row = 3,column =2, sticky = "e")
    
    #Este metodo de la pagina principal, permite segun la opcion elegida, realizar una accion con el boton creado en el inicializador
    def accion_inicio(self,opcion_elegida):
        if opcion_elegida == "CREAR PROYECTO":
            self.controller.show_frame(PaginaCrearProyecto)

        elif opcion_elegida == "INICIAR / TERMINAR SUBETAPA":
            self.controller.show_frame(PaginaIniciarTerminarSubetapa)

        elif opcion_elegida == "AGREGAR INGRESO / GASTO":
            self.controller.show_frame(PaginaAgregarIngresoGasto)
        
        elif opcion_elegida == "CAMBIAR NOMBRE ETAPA":
            self.controller.show_frame(PaginaCambiarNombreEtapa)
        
        elif opcion_elegida == "AGREGAR PERSONAL ETAPA":
            self.controller.show_frame(PaginaAgregarNombrePersonal)

        elif opcion_elegida == "AGREGAR AREA ETAPA":
            self.controller.show_frame(PaginaAgregarAreaEtapa)

        elif opcion_elegida == "AGREGAR NUEVA ETAPA":
            self.controller.show_frame(PaginaAgregarNuevaEtapa)

        elif opcion_elegida == "CAMBIAR NOMBRE PROYECTO":
            self.controller.show_frame(PaginaCambiarNombreProyecto)

        elif opcion_elegida == "ELIMINAR PROYECTO":
            self.controller.show_frame(PaginaEliminarProyecto)


#Se crea la info de la pagina 2, similar a la info de la pagina uno.. este proceso ya se vuelve muy estandar
#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaCrearProyecto(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        tk.Frame.__init__(self,parent)
        tk.Frame.config(self,bg = "black")
        #TITULO PRINCIPAL DE VENTANA ACTUAL
        self.INFO_1 = tk.Label(self, text = "CREACIÓN DE PROYECTO NUEVO", font = LARGE_FONT, bg = "black",fg = "yellow")
        self.INFO_1.grid(row = 0, column = 0, columnspan = 4, pady = math.floor(0.02*h) , padx = math.floor(0.01*w))

        #CREACION PARA INGRESAR LA FECHA ACTUAL
        INFO_DIA = tk.Label(self, text = "Ingrese día:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_DIA.grid(row = 1, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_MES = tk.Label(self, text = "Ingrese mes:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_MES.grid(row = 2, column = 1, sticky = "w", pady = math.floor(0.01*h)) 
        INFO_ANNO = tk.Label(self, text = "Ingrese año:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_ANNO.grid(row = 3, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_NOMBRE_PROYECTO = tk.Label(self, text = "Nombre Proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_NOMBRE_PROYECTO.grid(row = 4, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_ETAPAS_PROYECTO = tk.Label(self, text = "Numero Etapas Proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_ETAPAS_PROYECTO.grid(row = 5, column = 1, sticky = "w", pady = math.floor(0.01*h))

        vector_dias = []
        for i in range(31):
            vector_dias.append( str(i+1) )

        #Variable fundamental para manejo de opcion elegida en entry de anno y reseteo de esta
        self.elegido_entry_anno = tk.StringVar()
        self.elegido_nombre_proyecto = tk.StringVar()
        self.elegido_etapas = tk.StringVar()

        #Se crean "Comboboxes" necesarias para manejo de fechas
        self.seleccion_dia = ttk.Combobox( self, values = vector_dias , state = "readonly")
        self.seleccion_dia.grid( row = 1, column = 2, padx = math.floor(0.01*w) )

        vector_meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.seleccion_mes = ttk.Combobox( self, values = vector_meses , state = "readonly")
        self.seleccion_mes.grid( row = 2, column = 2, padx = math.floor(0.01*w) )

        self.seleccion_anno = ttk.Entry( self, textvariable = self.elegido_entry_anno )
        self.seleccion_anno.grid( row = 3, column = 2, padx = math.floor(0.01*w), sticky = "ew")
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )

        self.seleccion_proyecto = ttk.Entry( self, textvariable = self.elegido_nombre_proyecto )
        self.seleccion_proyecto.grid( row = 4, column = 2, padx = math.floor(0.01*w), sticky = "ew")

        self.seleccion_etapas = ttk.Entry( self, textvariable = self.elegido_etapas )
        self.seleccion_etapas.grid( row = 5, column = 2, padx = math.floor(0.01*w), sticky = "ew")

        #BOTON PARA REGRESAR A PAGINA INICIO
        self.boton_retorno = ttk.Button( self,text = "Volver",command = self.volver )
        self.boton_retorno.grid(row = 6,column = 0, padx = math.floor(0.01*w), sticky = "w" )

        boton_agregar_proyecto = ttk.Button( self,text = "AGREGAR PROYECTO",command = self.creacion_proyecto )
        boton_agregar_proyecto.grid(row = 6,column =3, padx = (math.floor(0.01*w),math.floor(0.02*w)) )


    def creacion_proyecto(self):
        try:
            test_validar_etapas = int(self.elegido_etapas.get())
        except:
            test_validar_etapas = False
        #Se valida ingreso de datos correctos, de lo contrario, mostrar "error"...
        if len(self.elegido_entry_anno.get() ) != 4 or self.seleccion_mes.current() == -1 or self.seleccion_dia.current() == -1 or self.elegido_nombre_proyecto.get() == "" or self.elegido_etapas.get() == "" or test_validar_etapas == False:
            showinfo( "ERROR DE DATOS", "Ingrese datos correctamente" )

        else:
            if  self.seleccion_mes.current()  < 9:
                REGISTRO = self.seleccion_dia.get() + "/0" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO,CREAR PROYECTO," + self.elegido_nombre_proyecto.get() + "," + self.elegido_etapas.get()
            else:  
                REGISTRO = self.seleccion_dia.get() + "/" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO,CREAR PROYECTO," + self.elegido_nombre_proyecto.get() + "," + self.elegido_etapas.get()
            
            RUTA = os.getcwd()
            txt = open("{}\\REGISTROS.txt".format(RUTA), "a")
            txt.write( "\n{}".format( REGISTRO))
            txt.close()
            self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )
            self.seleccion_dia.set("")
            self.seleccion_mes.set("")
            self.elegido_nombre_proyecto.set("")
            self.elegido_etapas.set("")
            self.controller.show_frame(PaginaInicio)

    def volver(self):
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )
        self.seleccion_dia.set("")
        self.seleccion_mes.set("")
        self.elegido_nombre_proyecto.set("")
        self.elegido_etapas.set("")
        self.controller.show_frame(PaginaInicio)

        
#Se crea la info de la pagina 3, similar a la info de la pagina uno y dos.. este proceso se vuelve muy estandar
#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaIniciarTerminarSubetapa(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(  bg = "black" )
        INFO_1 = tk.Label(self, text = "MANEJO FECHAS SUBETAPAS", font = LARGE_FONT, bg = "black", fg = "yellow")
        INFO_1.grid(row = 0, column = 0, columnspan = 3)


        #CREACION PARA INGRESAR LA FECHA ACTUAL
        INFO_DIA = tk.Label(self, text = "Ingrese día:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_DIA.grid(row = 1, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_MES = tk.Label(self, text = "Ingrese mes:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_MES.grid(row = 2, column = 1, sticky = "w", pady = math.floor(0.01*h)) 
        INFO_ANNO = tk.Label(self, text = "Ingrese año:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_ANNO.grid(row = 3, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_ACCION = tk.Label(self, text = "Seleccione accion:" , font = SMALL_FONT, bg = "black", fg = "white")
        INFO_ACCION.grid(row = 4, column = 1, sticky = "w", pady = math.floor(0.01*h)) 
        INFO_PROYECTO = tk.Label(self, text = "Seleccione proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_PROYECTO.grid(row = 5, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_ETAPA = tk.Label(self, text = "Seleccione etapa de proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_ETAPA.grid(row = 6, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_SUBETAPA = tk.Label(self, text = "Seleccione Subetapa de proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_SUBETAPA.grid(row = 7, column = 1, sticky = "w", pady = math.floor(0.01*h) )


        vector_dias = []
        for i in range(31):
            vector_dias.append( str(i+1) )

        self.elegido_entry_anno = tk.StringVar()
        self.elegido_subetapa = tk.StringVar()


        self.seleccion_dia = ttk.Combobox( self, values = vector_dias , state = "readonly")
        self.seleccion_dia.grid( row = 1, column = 2, padx = math.floor(0.01*w) , sticky = "ew")

        vector_meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.seleccion_mes = ttk.Combobox( self, values = vector_meses,state = "readonly")
        self.seleccion_mes.grid( row = 2, column = 2, padx = math.floor(0.01*w), sticky = "ew" )

        self.seleccion_anno = ttk.Entry( self, textvariable = self.elegido_entry_anno )
        self.seleccion_anno.grid( row = 3, column = 2, padx = math.floor(0.01*w), sticky = "ew")
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )


        self.seleccion_accion = ttk.Combobox( self, values = ["INICIAR SUBETAPA", "TERMINAR SUBETAPA"], state = "readonly" )
        self.seleccion_accion.grid(row = 4, column = 2, padx =  math.floor(0.01*w), sticky = "ew")

        #Se accede a info actualizada de proyectos (los proyectos que existan en el momento...)
        #esta info sera utilizada para mostrar el campo de los proyectos a elegir
        proyectos_actualizados = controller.M.get_nombre_proyectos()

        self.seleccion_proyecto = ttk.Combobox(self, values = proyectos_actualizados, state = "readonly", width = math.floor(0.02*w))
        self.seleccion_proyecto.grid(row = 5, column =2, padx = math.floor(0.01*w), sticky = "ew")
        #OJO: "bind" para que al seleccionar algo, me lleve  metodo de mostrar etapas
        self.seleccion_proyecto.bind( "<<ComboboxSelected>>",self.mostrar_etapas )

        self.seleccion_etapa = ttk.Combobox(self, values = [], state = "readonly")
        self.seleccion_etapa.grid(row = 6, column =2, padx = math.floor(0.01*w), sticky = "ew")        

        self.seleccion_subetapa = ttk.Combobox(self, values = ["IDEA BASICA","ANTEPROYECTO","PROYECTO ARQUITECTÓNICO","COORDINACION ARQUITECTÓNICA"], state = "readonly")
        self.seleccion_subetapa.grid(row = 7, column =2, padx = math.floor(0.01*w), sticky = "ew") 

        #BOTON PARA REGRESAR A PAGINA INICIO
        boton_retorno = ttk.Button( self,text = "Volver",command = self.volver )
        boton_retorno.grid(row = 8,column = 0, padx = math.floor(0.01*w), sticky = "w" )

        #BOTON PARA REALIZAR ACCION
        boton_agregar_proyecto = ttk.Button( self,text = "AGREGAR",command = self.agregar_accion_subetapa )
        boton_agregar_proyecto.grid(row = 8,column =3, padx = (math.floor(0.01*w),math.floor(0.02*w)) )

    #Metodo para limpiar completamente todos los campos de entrada o seleccion de ventana
    def limpiar_campos(self):
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )
        self.seleccion_dia.set("")
        self.seleccion_mes.set("")
        self.seleccion_accion.set("")
        self.seleccion_proyecto.set("")
        self.seleccion_etapa.set("")
        self.seleccion_subetapa.set("")        

    def volver(self):
        self.limpiar_campos()
        self.controller.show_frame(PaginaInicio)

    #Metodo para cambiar etapas a seleccionar, segun el proyecto
    def mostrar_etapas(self,event):
        #Se obtiene posicion del proyecto dentro del vector de poryectos actuales...
        index_seleccion_proyecto = int(self.seleccion_proyecto.current() ) 
        print(index_seleccion_proyecto)
        etapas_segun_proyecto = self.controller.M.get_nombre_etapas( index_seleccion_proyecto )
        self.seleccion_etapa.config(values = etapas_segun_proyecto)
        self.seleccion_etapa.set("")
    
    def agregar_accion_subetapa(self):
        #Se valida ingreso de datos correctos, de lo contrario, mostrar "error"...

        if len(self.elegido_entry_anno.get() ) != 4 or self.seleccion_mes.current() == -1 or self.seleccion_dia.current() == -1 or self.seleccion_proyecto.current() == -1 or self.seleccion_etapa.current() == -1 or self.seleccion_subetapa.current() == -1:
            showinfo( "ERROR DE DATOS", "Ingrese datos correctamente" )

        else:
            if  self.seleccion_mes.current()  < 9:
                REGISTRO = self.seleccion_dia.get() + "/0" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO," + self.seleccion_accion.get() + ","
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + "," + str( int(self.seleccion_etapa.current() ) +1 ) + "," + str( int(self.seleccion_subetapa.current() ) + 1 )
            else:  
                REGISTRO = self.seleccion_dia.get() + "/" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO," + self.seleccion_accion.get() + ","
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + "," + str( int(self.seleccion_etapa.current() ) +1 ) + "," + str( int(self.seleccion_subetapa.current() ) + 1 )          
            
            RUTA = os.getcwd()
            txt = open("{}\\REGISTROS.txt".format(RUTA), "a")
            txt.write( "\n{}".format( REGISTRO))
            txt.close()

            self.limpiar_campos()
            self.controller.show_frame(PaginaInicio)




class PaginaAgregarIngresoGasto(tk.Frame):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent)
        self.configure(background = "black")
        #TITULO PRINCIPAL DE VENTANA ACTUAL
        self.INFO_1 = tk.Label(self, text = "AGREGAR INGRESO O GASTO", font = LARGE_FONT, bg = "black",fg = "yellow")
        self.INFO_1.grid(row = 0, column = 0, columnspan = 4, pady = math.floor(0.02*h) , padx = math.floor(0.01*w))

        #CREACION PARA INGRESAR LA FECHA ACTUAL
        INFO_DIA = tk.Label(self, text = "Ingrese día:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_DIA.grid(row = 1, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_MES = tk.Label(self, text = "Ingrese mes:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_MES.grid(row = 2, column = 1, sticky = "w", pady = math.floor(0.01*h)) 
        INFO_ANNO = tk.Label(self, text = "Ingrese año:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_ANNO.grid(row = 3, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_INGRESO_O_GASTO = tk.Label(self, text = "Seleccione acción:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_INGRESO_O_GASTO.grid(row = 4, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_NOMBRE_ACCION = tk.Label(self, text = "Nombre acción:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_NOMBRE_ACCION.grid(row = 5, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_CANTIDAD = tk.Label(self, text = "Ingrese cantidad:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_CANTIDAD.grid(row = 6, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_PROYECTO = tk.Label(self, text = "Seleccione proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_PROYECTO.grid(row = 7, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_ETAPA = tk.Label(self, text = "Seleccione etapa de proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_ETAPA.grid(row = 8, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_SUBETAPA = tk.Label(self, text = "Seleccione Subetapa de proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_SUBETAPA.grid(row = 9, column = 1, sticky = "w", pady = math.floor(0.01*h) )


        vector_dias = []
        for i in range(31):
            vector_dias.append( str(i+1) )

        #Variable fundamental para manejo de opcion elegida en entry de anno y reseteo de esta
        self.elegido_entry_anno = tk.StringVar()
        self.elegido_nombre_accion = tk.StringVar()
        self.elegido_cantidad = tk.StringVar()
        self.elegido_subetapa = tk.StringVar()


        #Se crean "Comboboxes" necesarias para manejo de fechas
        self.seleccion_dia = ttk.Combobox( self, values = vector_dias , state = "readonly")
        self.seleccion_dia.grid( row = 1, column = 2, padx = math.floor(0.01*w), sticky = "ew")

        vector_meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.seleccion_mes = ttk.Combobox( self, values = vector_meses , state = "readonly")
        self.seleccion_mes.grid( row = 2, column = 2, padx = math.floor(0.01*w), sticky = "ew" )

        self.seleccion_anno = ttk.Entry( self, textvariable = self.elegido_entry_anno )
        self.seleccion_anno.grid( row = 3, column = 2, padx = math.floor(0.01*w), sticky = "ew")
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )


        self.seleccion_accion = ttk.Combobox( self, values = ["INGRESO", "GASTO"], state = "readonly" )
        self.seleccion_accion.grid(row = 4, column = 2, padx =  math.floor(0.01*w), sticky = "ew")

        self.seleccion_nombre_accion = ttk.Entry( self, textvariable = self.elegido_nombre_accion )
        self.seleccion_nombre_accion.grid( row = 5, column = 2, padx = math.floor(0.01*w), sticky = "ew")

        self.seleccion_cantidad = ttk.Entry( self, textvariable = self.elegido_cantidad )
        self.seleccion_cantidad.grid( row = 6, column = 2, padx = math.floor(0.01*w), sticky = "ew")

        #Se accede a info actualizada de proyectos (los proyectos que existan en el momento...)
        #esta info sera utilizada para mostrar el campo de los proyectos a elegir
        proyectos_actualizados = controller.M.get_nombre_proyectos()

        self.seleccion_proyecto = ttk.Combobox(self, values = proyectos_actualizados, state = "readonly", width = math.floor(0.02*w))
        self.seleccion_proyecto.grid(row = 7, column =2, padx = math.floor(0.01*w), sticky = "ew")
        #OJO: "bind" para que al seleccionar algo, me lleve  metodo de mostrar etapas
        self.seleccion_proyecto.bind( "<<ComboboxSelected>>",self.mostrar_etapas )


        self.seleccion_etapa = ttk.Combobox(self, values = [], state = "readonly")
        self.seleccion_etapa.grid(row = 8, column =2, padx = math.floor(0.01*w), sticky = "ew")        

        self.seleccion_subetapa = ttk.Combobox(self, values = ["IDEA BASICA","ANTEPROYECTO","PROYECTO ARQUITECTÓNICO","COORDINACION ARQUITECTÓNICA"], state = "readonly")
        self.seleccion_subetapa.grid(row = 9, column =2, padx = math.floor(0.01*w), sticky = "ew") 

        #BOTON PARA REGRESAR A PAGINA INICIO
        self.boton_retorno = ttk.Button( self,text = "Volver",command = self.volver )
        self.boton_retorno.grid(row = 10,column = 0, padx = math.floor(0.01*w), sticky = "w" )

        boton_agregar_proyecto = ttk.Button( self,text = "AGREGAR",command = self.agregar_ingreso_gasto )
        boton_agregar_proyecto.grid(row = 9,column =3, padx = (math.floor(0.01*w),math.floor(0.02*w)) )


    def volver(self):
        self.limpiar_campos()
        self.controller.show_frame(PaginaInicio)

    #Metodo para cambiar etapas a seleccionar, segun el proyecto
    def mostrar_etapas(self,event):
        #Se obtiene posicion del proyecto dentro del vector de poryectos actuales...
        index_seleccion_proyecto = int(self.seleccion_proyecto.current() ) 
        print(index_seleccion_proyecto)
        etapas_segun_proyecto = self.controller.M.get_nombre_etapas( index_seleccion_proyecto )
        self.seleccion_etapa.config(values = etapas_segun_proyecto)
        self.seleccion_etapa.set("")
    
    #Metodo para limpiar completamente todos los campos de entrada o seleccion de ventana
    def limpiar_campos(self):
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )
        self.seleccion_dia.set("")
        self.seleccion_mes.set("")
        self.seleccion_accion.set("")
        self.elegido_nombre_accion.set("")
        self.elegido_cantidad.set("")
        self.seleccion_proyecto.set("")
        self.seleccion_etapa.set("")
        self.seleccion_subetapa.set("")


    def agregar_ingreso_gasto(self):
        #Se valida ingreso de datos correctos, de lo contrario, mostrar "error"...
        try:
            validar_cantidad = float( self.seleccion_cantidad.get() )
        except:
            validar_cantidad = False

        if len(self.elegido_entry_anno.get() ) != 4 or self.seleccion_mes.current() == -1 or self.seleccion_dia.current() == -1 or validar_cantidad ==False :
            showinfo( "ERROR DE DATOS", "Ingrese datos correctamente" )

        else:
            if  self.seleccion_mes.current()  < 9:
                REGISTRO = self.seleccion_dia.get() + "/0" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO," + self.seleccion_accion.get() + ","
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + "," + str( int(self.seleccion_etapa.current() ) +1 ) + "," + str( int(self.seleccion_subetapa.current() ) + 1 ) + ","
                REGISTRO = REGISTRO + self.seleccion_nombre_accion.get() + "," + self.seleccion_cantidad.get()
            else:  
                REGISTRO = self.seleccion_dia.get() + "/" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO," + self.seleccion_accion.get() + ","
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + "," + str( int(self.seleccion_etapa.current() ) +1 ) + "," + str( int(self.seleccion_subetapa.current() ) + 1 ) + ","
                REGISTRO = REGISTRO + self.seleccion_nombre_accion.get() + "," + self.seleccion_cantidad.get()            
            
            RUTA = os.getcwd()
            txt = open("{}\\REGISTROS.txt".format(RUTA), "a")
            txt.write( "\n{}".format( REGISTRO))
            txt.close()
            self.limpiar_campos()
            self.controller.show_frame(PaginaInicio)


#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaCambiarNombreEtapa(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(  bg = "black" )
        INFO_1 = tk.Label(self, text = "CAMBIO NOMBRE ETAPA", font = LARGE_FONT, bg = "black", fg = "yellow")
        INFO_1.grid(row = 0, column = 0, columnspan = 3)


        #CREACION PARA INGRESAR LA FECHA ACTUAL
        INFO_DIA = tk.Label(self, text = "Ingrese día:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_DIA.grid(row = 1, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_MES = tk.Label(self, text = "Ingrese mes:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_MES.grid(row = 2, column = 1, sticky = "w", pady = math.floor(0.01*h)) 
        INFO_ANNO = tk.Label(self, text = "Ingrese año:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_ANNO.grid(row = 3, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_PROYECTO = tk.Label(self, text = "Seleccione proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_PROYECTO.grid(row = 4, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_ETAPA = tk.Label(self, text = "Seleccione etapa de proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_ETAPA.grid(row = 5, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_SUBETAPA = tk.Label(self, text = "Ingrese nuevo nombre etapa:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_SUBETAPA.grid(row = 6, column = 1, sticky = "w", pady = math.floor(0.01*h) )


        vector_dias = []
        for i in range(31):
            vector_dias.append( str(i+1) )

        self.elegido_entry_anno = tk.StringVar()
        self.elegido_nombre_etapa = tk.StringVar()


        self.seleccion_dia = ttk.Combobox( self, values = vector_dias , state = "readonly")
        self.seleccion_dia.grid( row = 1, column = 2, padx = math.floor(0.01*w) , sticky = "ew")

        vector_meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.seleccion_mes = ttk.Combobox( self, values = vector_meses,state = "readonly")
        self.seleccion_mes.grid( row = 2, column = 2, padx = math.floor(0.01*w) , sticky = "ew")

        self.seleccion_anno = ttk.Entry( self, textvariable = self.elegido_entry_anno )
        self.seleccion_anno.grid( row = 3, column = 2, padx = math.floor(0.01*w), sticky = "ew")
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )


        #Se accede a info actualizada de proyectos (los proyectos que existan en el momento...)
        #esta info sera utilizada para mostrar el campo de los proyectos a elegir
        proyectos_actualizados = controller.M.get_nombre_proyectos()

        self.seleccion_proyecto = ttk.Combobox(self, values = proyectos_actualizados, state = "readonly",  width = math.floor(0.02*w))
        self.seleccion_proyecto.grid(row = 4, column =2, padx = math.floor(0.01*w), sticky = "ew")
        #OJO: "bind" para que al seleccionar algo, me lleve  metodo de mostrar etapas
        self.seleccion_proyecto.bind( "<<ComboboxSelected>>",self.mostrar_etapas )

        self.seleccion_etapa = ttk.Combobox(self, values = [], state = "readonly")
        self.seleccion_etapa.grid(row = 5, column =2, padx = math.floor(0.01*w), sticky = "ew")        

        self.seleccion_nombre_etapa = ttk.Entry( self, textvariable = self.elegido_nombre_etapa )
        self.seleccion_nombre_etapa.grid( row = 6, column = 2, padx = math.floor(0.01*w), sticky = "ew")
        
        #BOTON PARA REGRESAR A PAGINA INICIO
        boton_retorno = ttk.Button( self,text = "Volver",command = self.volver )
        boton_retorno.grid(row = 7,column = 0, padx = math.floor(0.01*w), sticky = "w" )

        #BOTON PARA REALIZAR ACCION
        boton_agregar_proyecto = ttk.Button( self,text = "AGREGAR",command = self.agregar_cambio_nombre )
        boton_agregar_proyecto.grid(row = 7,column =3, padx = (math.floor(0.01*w),math.floor(0.02*w)) )

    #Metodo para limpiar completamente todos los campos de entrada o seleccion de ventana
    def limpiar_campos(self):
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )
        self.seleccion_dia.set("")
        self.seleccion_mes.set("")
        self.seleccion_proyecto.set("")
        self.seleccion_etapa.set("")
        self.elegido_nombre_etapa.set("")

    def volver(self):
        self.limpiar_campos()
        self.controller.show_frame(PaginaInicio)

    #Metodo para cambiar etapas a seleccionar, segun el proyecto
    def mostrar_etapas(self,event):
        #Se obtiene posicion del proyecto dentro del vector de poryectos actuales...
        index_seleccion_proyecto = int(self.seleccion_proyecto.current() ) 
        print(index_seleccion_proyecto)
        etapas_segun_proyecto = self.controller.M.get_nombre_etapas( index_seleccion_proyecto )
        self.seleccion_etapa.config(values = etapas_segun_proyecto)
        self.seleccion_etapa.set("")
    
    def agregar_cambio_nombre(self):
        #Se valida ingreso de datos correctos, de lo contrario, mostrar "error"...

        if len(self.elegido_entry_anno.get() ) != 4 or self.seleccion_mes.current() == -1 or self.seleccion_dia.current() == -1 or self.seleccion_proyecto.current() == -1 or self.seleccion_etapa.current() == -1:
            showinfo( "ERROR DE DATOS", "Ingrese datos correctamente" )

        else:
            if  self.seleccion_mes.current()  < 9:
                REGISTRO = self.seleccion_dia.get() + "/0" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO,CAMBIAR NOMBRE ETAPA,"
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + "," + str( int(self.seleccion_etapa.current() ) +1 ) + "," + self.elegido_nombre_etapa.get()
            else:  
                REGISTRO = self.seleccion_dia.get() + "/" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO,CAMBIAR NOMBRE ETAPA,"
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + "," + str( int(self.seleccion_etapa.current() ) +1 ) + "," + self.elegido_nombre_etapa.get() 
            
            RUTA = os.getcwd()
            txt = open("{}\\REGISTROS.txt".format(RUTA), "a")
            txt.write( "\n{}".format( REGISTRO))
            txt.close()

            self.limpiar_campos()
            self.controller.show_frame(PaginaInicio)



#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaAgregarNombrePersonal(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(  bg = "black" )
        INFO_1 = tk.Label(self, text = "AGREGAR PERSONAL", font = LARGE_FONT, bg = "black", fg = "yellow")
        INFO_1.grid(row = 0, column = 0, columnspan = 3)


        #CREACION PARA INGRESAR LA FECHA ACTUAL
        INFO_DIA = tk.Label(self, text = "Ingrese día:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_DIA.grid(row = 1, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_MES = tk.Label(self, text = "Ingrese mes:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_MES.grid(row = 2, column = 1, sticky = "w", pady = math.floor(0.01*h)) 
        INFO_ANNO = tk.Label(self, text = "Ingrese año:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_ANNO.grid(row = 3, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_ACCION = tk.Label(self, text = "Seleccione personal a agregar:" , font = SMALL_FONT, bg = "black", fg = "white")
        INFO_ACCION.grid(row = 4, column = 1, sticky = "w", pady = math.floor(0.01*h)) 
        INFO_PROYECTO = tk.Label(self, text = "Seleccione proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_PROYECTO.grid(row = 5, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_ETAPA = tk.Label(self, text = "Seleccione etapa de proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_ETAPA.grid(row = 6, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_SUBETAPA = tk.Label(self, text = "Ingrese nombre de la persona:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_SUBETAPA.grid(row = 7, column = 1, sticky = "w", pady = math.floor(0.01*h) )


        vector_dias = []
        for i in range(31):
            vector_dias.append( str(i+1) )

        self.elegido_entry_anno = tk.StringVar()
        self.elegido_nombre_persona = tk.StringVar()


        self.seleccion_dia = ttk.Combobox( self, values = vector_dias , state = "readonly")
        self.seleccion_dia.grid( row = 1, column = 2, padx = math.floor(0.01*w) , sticky = "ew")

        vector_meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.seleccion_mes = ttk.Combobox( self, values = vector_meses,state = "readonly")
        self.seleccion_mes.grid( row = 2, column = 2, padx = math.floor(0.01*w) , sticky = "ew" )

        self.seleccion_anno = ttk.Entry( self, textvariable = self.elegido_entry_anno )
        self.seleccion_anno.grid( row = 3, column = 2, padx = math.floor(0.01*w), sticky = "ew")
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )

        self.seleccion_tipo_personal = ttk.Combobox( self, values = ["DIRECTOR","COORDINADOR","ARQUITECTO"], state = "readonly" )
        self.seleccion_tipo_personal.grid(row = 4, column = 2, padx =  math.floor(0.01*w), sticky = "ew")

        #Se accede a info actualizada de proyectos (los proyectos que existan en el momento...)
        #esta info sera utilizada para mostrar el campo de los proyectos a elegir
        proyectos_actualizados = controller.M.get_nombre_proyectos()

        self.seleccion_proyecto = ttk.Combobox(self, values = proyectos_actualizados, state = "readonly",  width = math.floor(0.02*w))
        self.seleccion_proyecto.grid(row = 5, column =2, padx = math.floor(0.01*w), sticky = "ew")
        #OJO: "bind" para que al seleccionar algo, me lleve  metodo de mostrar etapas
        self.seleccion_proyecto.bind( "<<ComboboxSelected>>",self.mostrar_etapas )

        self.seleccion_etapa = ttk.Combobox(self, values = [], state = "readonly")
        self.seleccion_etapa.grid(row = 6, column =2, padx = math.floor(0.01*w), sticky = "ew") 

        self.seleccion_nombre_persona = ttk.Entry( self, textvariable = self.elegido_nombre_persona )
        self.seleccion_nombre_persona.grid( row = 7, column = 2, padx = math.floor(0.01*w), sticky = "ew")       


        #BOTON PARA REGRESAR A PAGINA INICIO
        boton_retorno = ttk.Button( self,text = "Volver",command = self.volver )
        boton_retorno.grid(row = 8,column = 0, padx = math.floor(0.01*w), sticky = "w" )

        #BOTON PARA REALIZAR ACCION
        boton_agregar_proyecto = ttk.Button( self,text = "AGREGAR",command = self.agregar_accion_subetapa )
        boton_agregar_proyecto.grid(row = 8,column =3, padx = (math.floor(0.01*w),math.floor(0.02*w)) )

    #Metodo para limpiar completamente todos los campos de entrada o seleccion de ventana
    def limpiar_campos(self):
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )
        self.seleccion_dia.set("")
        self.seleccion_mes.set("")
        self.seleccion_tipo_personal.set("")
        self.seleccion_proyecto.set("")
        self.seleccion_etapa.set("")
        self.elegido_nombre_persona.set("")        

    def volver(self):
        self.limpiar_campos()
        self.controller.show_frame(PaginaInicio)

    #Metodo para cambiar etapas a seleccionar, segun el proyecto
    def mostrar_etapas(self,event):
        #Se obtiene posicion del proyecto dentro del vector de poryectos actuales...
        index_seleccion_proyecto = int(self.seleccion_proyecto.current() ) 
        print(index_seleccion_proyecto)
        etapas_segun_proyecto = self.controller.M.get_nombre_etapas( index_seleccion_proyecto )
        self.seleccion_etapa.config(values = etapas_segun_proyecto)
        self.seleccion_etapa.set("")
    
    def agregar_accion_subetapa(self):
        #Se valida ingreso de datos correctos, de lo contrario, mostrar "error"...

        if len(self.elegido_entry_anno.get() ) != 4 or self.seleccion_mes.current() == -1 or self.seleccion_dia.current() == -1 or self.seleccion_proyecto.current() == -1 or self.seleccion_etapa.current() == -1 or self.elegido_nombre_persona.get() == "":
            showinfo( "ERROR DE DATOS", "Ingrese datos correctamente" )

        else:
            if  self.seleccion_mes.current()  < 9:
                REGISTRO = self.seleccion_dia.get() + "/0" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO,AGREGAR " + self.seleccion_tipo_personal.get() + ","
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + "," + str( int(self.seleccion_etapa.current() ) +1 ) + "," + self.elegido_nombre_persona.get()
            else:  
                REGISTRO = self.seleccion_dia.get() + "/" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO,AGREGAR " + self.seleccion_tipo_personal.get() + ","
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + "," + str( int(self.seleccion_etapa.current() ) +1 ) + "," + self.elegido_nombre_persona.get()         
            
            RUTA = os.getcwd()
            txt = open("{}\\REGISTROS.txt".format(RUTA), "a")
            txt.write( "\n{}".format( REGISTRO))
            txt.close()

            self.limpiar_campos()
            self.controller.show_frame(PaginaInicio)


#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaAgregarAreaEtapa(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(  bg = "black" )
        INFO_1 = tk.Label(self, text = "AGREGAR ÁREA ETAPA", font = LARGE_FONT, bg = "black", fg = "yellow")
        INFO_1.grid(row = 0, column = 0, columnspan = 3)


        #CREACION PARA INGRESAR LA FECHA ACTUAL
        INFO_DIA = tk.Label(self, text = "Ingrese día:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_DIA.grid(row = 1, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_MES = tk.Label(self, text = "Ingrese mes:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_MES.grid(row = 2, column = 1, sticky = "w", pady = math.floor(0.01*h)) 
        INFO_ANNO = tk.Label(self, text = "Ingrese año:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_ANNO.grid(row = 3, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_PROYECTO = tk.Label(self, text = "Seleccione proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_PROYECTO.grid(row = 4, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_ETAPA = tk.Label(self, text = "Seleccione etapa de proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_ETAPA.grid(row = 5, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_SUBETAPA = tk.Label(self, text = "Ingrese área de la etapa:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_SUBETAPA.grid(row = 6, column = 1, sticky = "w", pady = math.floor(0.01*h) )


        vector_dias = []
        for i in range(31):
            vector_dias.append( str(i+1) )

        self.elegido_entry_anno = tk.StringVar()
        self.elegido_area_etapa = tk.StringVar()


        self.seleccion_dia = ttk.Combobox( self, values = vector_dias , state = "readonly")
        self.seleccion_dia.grid( row = 1, column = 2, padx = math.floor(0.01*w) , sticky = "ew")

        vector_meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.seleccion_mes = ttk.Combobox( self, values = vector_meses,state = "readonly")
        self.seleccion_mes.grid( row = 2, column = 2, padx = math.floor(0.01*w) , sticky = "ew")

        self.seleccion_anno = ttk.Entry( self, textvariable = self.elegido_entry_anno )
        self.seleccion_anno.grid( row = 3, column = 2, padx = math.floor(0.01*w), sticky = "ew")
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )


        #Se accede a info actualizada de proyectos (los proyectos que existan en el momento...)
        #esta info sera utilizada para mostrar el campo de los proyectos a elegir
        proyectos_actualizados = controller.M.get_nombre_proyectos()

        self.seleccion_proyecto = ttk.Combobox(self, values = proyectos_actualizados, state = "readonly",  width = math.floor(0.02*w) )
        self.seleccion_proyecto.grid(row = 4, column =2, padx = math.floor(0.01*w), sticky = "ew")
        #OJO: "bind" para que al seleccionar algo, me lleve  metodo de mostrar etapas
        self.seleccion_proyecto.bind( "<<ComboboxSelected>>",self.mostrar_etapas )

        self.seleccion_etapa = ttk.Combobox(self, values = [], state = "readonly")
        self.seleccion_etapa.grid(row = 5, column =2, padx = math.floor(0.01*w), sticky = "ew") 

        self.seleccion_area_etapa = ttk.Entry( self, textvariable = self.elegido_area_etapa )
        self.seleccion_area_etapa.grid( row = 6, column = 2, padx = math.floor(0.01*w), sticky = "ew")       


        #BOTON PARA REGRESAR A PAGINA INICIO
        boton_retorno = ttk.Button( self,text = "Volver",command = self.volver )
        boton_retorno.grid(row = 7,column = 0, padx = math.floor(0.01*w), sticky = "w" )

        #BOTON PARA REALIZAR ACCION
        boton_agregar_proyecto = ttk.Button( self,text = "AGREGAR",command = self.agregar_area_etapa )
        boton_agregar_proyecto.grid(row = 7,column =3, padx = (math.floor(0.01*w),math.floor(0.02*w)) )

    #Metodo para limpiar completamente todos los campos de entrada o seleccion de ventana
    def limpiar_campos(self):
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )
        self.seleccion_dia.set("")
        self.seleccion_mes.set("")
        self.seleccion_proyecto.set("")
        self.seleccion_etapa.set("")
        self.elegido_area_etapa.set("")        

    def volver(self):
        self.limpiar_campos()
        self.controller.show_frame(PaginaInicio)

    #Metodo para cambiar etapas a seleccionar, segun el proyecto
    def mostrar_etapas(self,event):
        #Se obtiene posicion del proyecto dentro del vector de poryectos actuales...
        index_seleccion_proyecto = int(self.seleccion_proyecto.current() ) 
        print(index_seleccion_proyecto)
        etapas_segun_proyecto = self.controller.M.get_nombre_etapas( index_seleccion_proyecto )
        self.seleccion_etapa.config(values = etapas_segun_proyecto)
        self.seleccion_etapa.set("")
    
    def agregar_area_etapa(self):
        #Se valida ingreso de datos correctos, de lo contrario, mostrar "error"...

        if len(self.elegido_entry_anno.get() ) != 4 or self.seleccion_mes.current() == -1 or self.seleccion_dia.current() == -1 or self.seleccion_proyecto.current() == -1 or self.seleccion_etapa.current() == -1 or self.elegido_area_etapa.get() == "":
            showinfo( "ERROR DE DATOS", "Ingrese datos correctamente" )

        else:
            if  self.seleccion_mes.current()  < 9:
                REGISTRO = self.seleccion_dia.get() + "/0" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO,AGREGAR AREA ETAPA,"
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + "," + str( int(self.seleccion_etapa.current() ) +1 ) + "," + self.elegido_area_etapa.get()
            else:  
                REGISTRO = self.seleccion_dia.get() + "/" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO,AGREGAR AREA ETAPA,"
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + "," + str( int(self.seleccion_etapa.current() ) +1 ) + "," + self.elegido_area_etapa.get()         
            
            RUTA = os.getcwd()
            txt = open("{}\\REGISTROS.txt".format(RUTA), "a")
            txt.write( "\n{}".format( REGISTRO))
            txt.close()

            self.limpiar_campos()
            self.controller.show_frame(PaginaInicio)


#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaAgregarNuevaEtapa(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(  bg = "black" )
        INFO_1 = tk.Label(self, text = "AGREGAR NUEVA ETAPA", font = LARGE_FONT, bg = "black", fg = "yellow")
        INFO_1.grid(row = 0, column = 0, columnspan = 3)


        #CREACION PARA INGRESAR LA FECHA ACTUAL
        INFO_DIA = tk.Label(self, text = "Ingrese día:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_DIA.grid(row = 1, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_MES = tk.Label(self, text = "Ingrese mes:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_MES.grid(row = 2, column = 1, sticky = "w", pady = math.floor(0.01*h)) 
        INFO_ANNO = tk.Label(self, text = "Ingrese año:", font = SMALL_FONT, bg = "black",fg = "white")
        INFO_ANNO.grid(row = 3, column = 1, sticky = "w", pady = math.floor(0.01*h))
        INFO_PROYECTO = tk.Label(self, text = "Seleccione proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_PROYECTO.grid(row = 4, column = 1, sticky = "w", pady = math.floor(0.01*h) )


        vector_dias = []
        for i in range(31):
            vector_dias.append( str(i+1) )

        self.elegido_entry_anno = tk.StringVar()


        self.seleccion_dia = ttk.Combobox( self, values = vector_dias , state = "readonly")
        self.seleccion_dia.grid( row = 1, column = 2, padx = math.floor(0.01*w) , sticky = "ew")

        vector_meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
        self.seleccion_mes = ttk.Combobox( self, values = vector_meses,state = "readonly")
        self.seleccion_mes.grid( row = 2, column = 2, padx = math.floor(0.01*w) , sticky = "ew")

        self.seleccion_anno = ttk.Entry( self, textvariable = self.elegido_entry_anno )
        self.seleccion_anno.grid( row = 3, column = 2, padx = math.floor(0.01*w), sticky = "ew")
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )


        #Se accede a info actualizada de proyectos (los proyectos que existan en el momento...)
        #esta info sera utilizada para mostrar el campo de los proyectos a elegir
        proyectos_actualizados = controller.M.get_nombre_proyectos()

        self.seleccion_proyecto = ttk.Combobox(self, values = proyectos_actualizados, state = "readonly",  width = math.floor(0.02*w))
        self.seleccion_proyecto.grid(row = 4, column =2, padx = math.floor(0.01*w), sticky = "ew")   

        #BOTON PARA REGRESAR A PAGINA INICIO
        boton_retorno = ttk.Button( self,text = "Volver",command = self.volver )
        boton_retorno.grid(row = 7,column = 0, padx = math.floor(0.01*w), sticky = "w" )

        #BOTON PARA REALIZAR ACCION
        boton_agregar_proyecto = ttk.Button( self,text = "AGREGAR",command = self.agregar_nueva_etapa )
        boton_agregar_proyecto.grid(row = 7,column =3, padx = (math.floor(0.01*w),math.floor(0.02*w)) )

    #Metodo para limpiar completamente todos los campos de entrada o seleccion de ventana
    def limpiar_campos(self):
        self.elegido_entry_anno.set( datetime.datetime.now().strftime("%Y") )
        self.seleccion_dia.set("")
        self.seleccion_mes.set("")
        self.seleccion_proyecto.set("")       

    def volver(self):
        self.limpiar_campos()
        self.controller.show_frame(PaginaInicio)
    
    def agregar_nueva_etapa(self):
        #Se valida ingreso de datos correctos, de lo contrario, mostrar "error"...

        if len(self.elegido_entry_anno.get() ) != 4 or self.seleccion_mes.current() == -1 or self.seleccion_dia.current() == -1 or self.seleccion_proyecto.current() == -1:
            showinfo( "ERROR DE DATOS", "Ingrese datos correctamente" )

        else:
            if  self.seleccion_mes.current()  < 9:
                REGISTRO = self.seleccion_dia.get() + "/0" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO,AGREGAR NUEVA ETAPA,"
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + ","
            else:  
                REGISTRO = self.seleccion_dia.get() + "/" + str(self.seleccion_mes.current() + 1 ) + "/" + self.elegido_entry_anno.get() + ",ACTIVO,AGREGAR NUEVA ETAPA,"
                REGISTRO = REGISTRO + self.seleccion_proyecto.get() + ","   
            
            RUTA = os.getcwd()
            txt = open("{}\\REGISTROS.txt".format(RUTA), "a")
            txt.write( "\n{}".format( REGISTRO))
            txt.close()

            self.limpiar_campos()
            self.controller.show_frame(PaginaInicio)


#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaCambiarNombreProyecto(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(  bg = "black" )
        INFO_1 = tk.Label(self, text = "CAMBIAR NOMBRE DE PROYECTO EXISTENTE", font = LARGE_FONT, bg = "black", fg = "yellow")
        INFO_1.grid(row = 0, column = 0, columnspan = 3)

        INFO_PROYECTO = tk.Label(self, text = "Seleccione proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_PROYECTO.grid(row = 1, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_NOMBRE_PROYECTO = tk.Label(self, text = "Ingrese nuevo nombre proyecto:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_NOMBRE_PROYECTO.grid(row = 2, column = 1, sticky = "w", pady = math.floor(0.01*h) )

        #Se accede a info actualizada de proyectos (los proyectos que existan en el momento...)
        #esta info sera utilizada para mostrar el campo de los proyectos a elegir
        proyectos_actualizados = controller.M.get_nombre_proyectos()

        self.seleccion_proyecto = ttk.Combobox(self, values = proyectos_actualizados, state = "readonly",  width = math.floor(0.02*w))
        self.seleccion_proyecto.grid(row = 1, column =2, padx = math.floor(0.01*w), sticky = "ew")  


        #Variables para eleccion nombre proyecto
        self.elegido_nombre_proyecto = tk.StringVar()

        self.seleccion_nombre_proyecto = ttk.Entry( self, textvariable = self.elegido_nombre_proyecto )
        self.seleccion_nombre_proyecto.grid( row = 2, column = 2, padx = math.floor(0.01*w), sticky = "ew") 

        #BOTON PARA REGRESAR A PAGINA INICIO
        boton_retorno = ttk.Button( self,text = "Volver",command = self.volver )
        boton_retorno.grid(row = 3,column = 0, padx = math.floor(0.01*w), sticky = "w" )

        #BOTON PARA REALIZAR ACCION
        boton_cambiar_nombre = ttk.Button( self,text = "CAMBIAR",command = self.cambiar_nombre_proyecto )
        boton_cambiar_nombre.grid(row = 3,column =3, padx = (math.floor(0.01*w),math.floor(0.02*w)) )

    #Metodo para limpiar completamente todos los campos de entrada o seleccion de ventana
    def limpiar_campos(self):
        self.seleccion_proyecto.set("")      
        self.elegido_nombre_proyecto.set("") 

    def volver(self):
        self.limpiar_campos()
        self.controller.show_frame(PaginaInicio)
    
    def cambiar_nombre_proyecto(self):
        #Se valida ingreso de datos correctos, de lo contrario, mostrar "error"...

        if (self.seleccion_proyecto.current() == -1 or self.elegido_nombre_proyecto.get() == ""):
            showinfo( "ERROR DE DATOS", "Ingrese datos correctamente" )

        else:

            CAMBIAR_NOMBRE_PROYECTO.CAMBIAR_NOMBRE_PROYECTO( self.seleccion_proyecto.get() , self.elegido_nombre_proyecto.get() )

            
            self.limpiar_campos()
            self.controller.show_frame(PaginaInicio)


#Recordar agregar esta pagina al diccionario de Frames en la inicializacion de la APP(para navegar sin errores)
class PaginaEliminarProyecto(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.config(  bg = "black" )
        INFO_1 = tk.Label(self, text = "ELIMINAR PROYECTO EXISTENTE", font = LARGE_FONT, bg = "black", fg = "yellow")
        INFO_1.grid(row = 0, column = 0, columnspan = 3)

        INFO_PROYECTO = tk.Label(self, text = "Seleccione proyecto a ELIMINAR:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_PROYECTO.grid(row = 1, column = 1, sticky = "w", pady = math.floor(0.01*h) )
        INFO_SEGURIDAD = tk.Label(self, text = "¿Está seguro?:", font = SMALL_FONT, bg = "black", fg = "white")
        INFO_SEGURIDAD.grid(row = 2, column = 1, sticky = "w", pady = math.floor(0.01*h) )

        #Se accede a info actualizada de proyectos (los proyectos que existan en el momento...)
        #esta info sera utilizada para mostrar el campo de los proyectos a elegir
        proyectos_actualizados = controller.M.get_nombre_proyectos()

        self.seleccion_proyecto = ttk.Combobox(self, values = proyectos_actualizados, state = "readonly",  width = math.floor(0.02*w))
        self.seleccion_proyecto.grid(row = 1, column =2, padx = math.floor(0.01*w), sticky = "ew")  

        self.seleccion_seguridad_confirmar = ttk.Combobox( self, values = ["SI"] , state = "readonly")
        self.seleccion_seguridad_confirmar.grid( row = 2, column = 2, padx = math.floor(0.01*w), sticky = "ew") 

        #BOTON PARA REGRESAR A PAGINA INICIO
        boton_retorno = ttk.Button( self,text = "Volver",command = self.volver )
        boton_retorno.grid(row = 3,column = 0, padx = math.floor(0.01*w), sticky = "w" )

        #BOTON PARA REALIZAR ACCION
        boton_cambiar_nombre = ttk.Button( self,text = "ELIMINAR PROYECTO",command = self.eliminar_proyecto )
        boton_cambiar_nombre.grid(row = 3,column =3, padx = (math.floor(0.01*w),math.floor(0.02*w)) )

    #Metodo para limpiar completamente todos los campos de entrada o seleccion de ventana
    def limpiar_campos(self):
        self.seleccion_proyecto.set("")      
        self.seleccion_seguridad_confirmar.set("") 

    def volver(self):
        self.limpiar_campos()
        self.controller.show_frame(PaginaInicio)
    
    def eliminar_proyecto(self):
        #Se valida ingreso de datos correctos, de lo contrario, mostrar "error"...

        if (self.seleccion_proyecto.current() == -1 or self.seleccion_seguridad_confirmar.current() == -1):
            showinfo( "ERROR PARA CONFIRMAR", "Seleccione opciones correctamente" )

        else:
            #SE ELIMINA proyecto elegido en combobox
            ELIMINAR_PROYECTO.ELIMINAR_PROYECTO( self.seleccion_proyecto.get() )
            
            self.limpiar_campos()
            self.controller.show_frame(PaginaInicio)

## Se crea la APP para mostrar el funcionamiento...
APP_SANTI = APP()
APP_SANTI.mainloop()
