# -*- coding: utf-8 -*-
##La linea superior se encarga de poder hacer encoding con reconocimiento de tildes y enne

#CODIGO MASTER DEL SISTEMA DE AUTOMATIZACION DE PROYECTOS 
#Libreria para manejo de la fecha y el guardado de informacion segun la fecha
import datetime
#Libreria para manejar la lectura correcta de los archivos TXT
import glob
#Nos permite crear las carpetas en donde se guardara la informacion
import INFO_DIR_ACTUAL
#Libreria (necesario descargarla) para la creacion de los archivos de Excel
import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

#Libreria para ver tiempo que demora codigo en correr (util para mi, pero innecesario en version final)
import time
start = time.time()

#Esta clase es la encargada de todo el analisis de cada proyecto, con sus respectivas N etapas y 4 subetapas estandarizadas
class Proyecto:
    #Se inicializa con el nombre del proyecto y la cantidad de etapas, de tal forma que se puedan generar todas las...
    #respectivas subetapas de cada una de las etapas automaticamente.
    #Info de etapas esta en "self.vector_etapas"
    #Info de subetapas pertenece a cada etapa y esta en "self.vector_subetapas"
    def __init__(self, nombre_proyecto, cantidad_etapas,fecha_inicio_proyecto):
        self.nombre_proyecto = nombre_proyecto
        self.cantidad_etapas = int(cantidad_etapas)
        self.fecha_inicio_proyecto = fecha_inicio_proyecto
        self.fecha_fin_proyecto = "NO DEFINIDA"
        self.estado_proyecto = "EN PROGRESO"
        #Se inicializa el vector principal donde se almacene la informacion de cada una de las etapas, segun la cantidad de estas
        self.vector_etapas = []
        #Con el siguiente metodo, se generan automaticamente las etapas segun los parametros de entrada (cantidad de etapas y nombre del proyecto)
        self.crear_etapas_iniciales()


    def aumentar_etapa(self):
        #Se aumenta el numero de etapas en 1 (nueva etapa)
        self.cantidad_etapas = self.cantidad_etapas + 1
        #Se agrega rigurosamente nueva etapa al vector que las organiza
        self.vector_etapas.append( Etapa( "ETAPA {} {}".format( len(self.vector_etapas) +1, self.nombre_proyecto )) )
        posicion_ultima_etapa = len(self.vector_etapas) - 1

        for j in range(4):
            if j == 0:
                self.vector_etapas[ posicion_ultima_etapa ].agregar_subetapas( Subetapa( "IDEA BASICA {} {}".format( self.nombre_proyecto, self.vector_etapas[ posicion_ultima_etapa ].nombre_etapa  ), "NO DEFINIDA" ) )
            elif j == 1:
                self.vector_etapas[ posicion_ultima_etapa ].agregar_subetapas( Subetapa( "ANTEPROYECTO {} {}".format( self.nombre_proyecto, self.vector_etapas[ posicion_ultima_etapa ].nombre_etapa ),"NO DEFINIDA") )
            elif j == 2:
                self.vector_etapas[ posicion_ultima_etapa ].agregar_subetapas( Subetapa( "PROYECTO ARQUITECTÓNICO {} {}".format( self.nombre_proyecto, self.vector_etapas[ posicion_ultima_etapa ].nombre_etapa ), "NO DEFINIDA" ) )
                self.vector_etapas[ posicion_ultima_etapa ].vector_subetapas[j].estado_subetapa = "SIN COMENZAR"
            else:
                self.vector_etapas[ posicion_ultima_etapa ].agregar_subetapas( Subetapa( "COORDINACION ARQUITECTÓNICA {} {}".format( self.nombre_proyecto, self.vector_etapas[ posicion_ultima_etapa ].nombre_etapa ), "NO DEFINIDA" ) )
                self.vector_etapas[ posicion_ultima_etapa ].vector_subetapas[j].estado_subetapa = "SIN COMENZAR"





    #Se permite poder finalizar proyecto, con el animo de mostrar 
    def finalizar_proyecto(self, nombre_proyecto,fecha_finalizacion):
        self.estado_proyecto = "FINALIZADO"
        self.fecha_fin_proyecto = fecha_finalizacion
    #Metodo encargado de inicializar y almacenar la informacion valiosa de cada una de las etapas asociadas al proyecto
    #este metodo se corre unicamente al inicio de cada uno de los proyectos, para facilitar el manejo de las etapas y proyectos netos
    def crear_etapas_iniciales(self):
        for i in range( int(self.cantidad_etapas) ):
            #Se agregan tantas etapas como se hayan indicado en los parametros de creacion del proyecto
            self.vector_etapas.append(  Etapa( "ETAPA {} {}".format(str(i+1),self.nombre_proyecto) ) )
            #Se geran las respectivas 4 subetapas que son estandar (siempre las mismas)
            for j in range(4):
                if j == 0:
                    self.vector_etapas[i].agregar_subetapas( Subetapa( "IDEA BASICA {} {}".format( self.nombre_proyecto, self.vector_etapas[i].nombre_etapa  ), self.fecha_inicio_proyecto ) )
                elif j == 1:
                    self.vector_etapas[i].agregar_subetapas( Subetapa( "ANTEPROYECTO {} {}".format( self.nombre_proyecto, self.vector_etapas[i].nombre_etapa ),self.fecha_inicio_proyecto ) )
                elif j == 2:
                    self.vector_etapas[i].agregar_subetapas( Subetapa( "PROYECTO ARQUITECTÓNICO {} {}".format( self.nombre_proyecto, self.vector_etapas[i].nombre_etapa ), "NO DEFINIDA" ) )
                    self.vector_etapas[i].vector_subetapas[j].estado_subetapa = "SIN COMENZAR"
                else:
                    self.vector_etapas[i].agregar_subetapas( Subetapa( "COORDINACION ARQUITECTÓNICA {} {}".format( self.nombre_proyecto, self.vector_etapas[i].nombre_etapa ), "NO DEFINIDA" ) )
                    self.vector_etapas[i].vector_subetapas[j].estado_subetapa = "SIN COMENZAR"

    ####Mostrar info provicional mientras se crea el metodo oficial para mostrar los Excels
    def mostrar_etapas_y_subetapas(self):
        for i in range( len(self.vector_etapas) ):
            print("\n")
            print(self.vector_etapas[i].nombre_etapa)
            print(" ")
            for j in range(4):
                print(  self.vector_etapas[i].vector_subetapas[j].nombre_subetapa  )
                print(  "estado subetapa: " + self.vector_etapas[i].vector_subetapas[j].estado_subetapa )
                print(  "fecha inicio subetapa: " + self.vector_etapas[i].vector_subetapas[j].fecha_inicio )
                print(  "fecha fin subetapa: " + self.vector_etapas[i].vector_subetapas[j].fecha_fin )
                for m in range( len(self.vector_etapas[i].vector_subetapas[j].gastos) ):
                    print( "gasto: ",self.vector_etapas[i].vector_subetapas[j].gastos[m] )
                for m in range( len(self.vector_etapas[i].vector_subetapas[j].ingresos) ):
                    print( "ingreso: ",self.vector_etapas[i].vector_subetapas[j].ingresos[m] )





class Etapa:
    def __init__(self, nombre_etapa):
        self.nombre_etapa = nombre_etapa
        self.vector_subetapas = []
        self.area_etapa = "NO DEFINIDA"  
        self.director = "PENDIENTE POR ASIGNAR"
        self.coordinador = "PENDIENTE POR ASIGNAR"
        self.vector_arquitectos = []

    #Se permite agregar info del director de cada etapa
    def agregar_director(self,director):
        self.director = director
    
    #Se permite agregar coordinador de cada etapa
    def agregar_coordinador(self,coordinador):
        self.coordinador = coordinador
    
    #Se permite agregar arquitectos de cada etapa
    def agregar_arquitecto(self,arquitecto):
        self.vector_arquitectos.append( arquitecto )

    #Metodo util para cambiar el nombre de una etapa segun quiera el usuario
    def cambiar_nombre_etapa(self,nuevo_nombre_etapa):
        self.nombre_etapa = nuevo_nombre_etapa

    #Nos permite almacenar la info de las respectivas subetapas
    def agregar_subetapas(self, Subetapa):
        self.vector_subetapas.append( Subetapa )

    #Es fundamental poder modificar el area de las etapas a medida que vayan avanzando los proyectos
    def cambiar_area_etapa(self,area):
        try:
            self.area_etapa = float(area)
        except:
            self.area_etapa = area




class Subetapa:
    def __init__(self, nombre_subetapa, fecha_inicio):
        #Cada subetapa se inicializa por defecto como False (es decir, NO acabada)
        self.nombre_subetapa = nombre_subetapa
        self.estado_subetapa = "EN PROGRESO"
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = "NO DEFINIDA"
        self.gastos = []
        self.ingresos = []
    
    def agregar_gasto(self, gasto):
        self.gastos.append( gasto )

    def agregar_ingreso(self, ingreso):
        self.ingresos.append( ingreso )
    
    #Esta es para las etapas que NO se inician instantaneamente (como el proyecto arquitectonico y la coordinacion arquitectonica)
    def iniciar_subetapa(self, fecha_inicio):
        self.fecha_inicio = fecha_inicio
        self.estado_subetapa = "EN PROGRESO"
    
    def finalizar_subetapa(self,fecha_fin):
        self.estado_subetapa = "SUBETAPA FINALIZADA"
        self.fecha_fin = fecha_fin


#Clases que se encargan de manejar los gastos asociados a los proyectos
#Estos gastos tienen a su vez, la informacion sobre el gasto ocurrido, la cantidad neta involucrada y la fecha (negativo)
class Gasto:
    def __init__(self, nombre_gasto, cantidad_gasto, fecha_gasto):
        self.nombre_gasto = nombre_gasto
        self.cantidad_gasto = -abs(float(cantidad_gasto))
        self.fecha_gasto = fecha_gasto

    def __str__(self):
        return("{},{},{}".format( self.nombre_gasto, self.cantidad_gasto, self.fecha_gasto ))


#Notar que los ingresos son practicamente iguales a los gastos, la unica diferencia es el nombre del registro y el valor (positivo)
class Ingreso:
    def __init__(self, nombre_ingreso, cantidad_ingreso,fecha_ingreso):
        self.nombre_ingreso = nombre_ingreso
        self.cantidad_ingreso = abs(float(cantidad_ingreso))
        self.fecha_ingreso = fecha_ingreso

    def __str__(self):
        return("{},{},{}".format( self.nombre_ingreso, self.cantidad_ingreso, self.fecha_ingreso ))



#Esta accion (INTERPRETAR_TXT) es encargada de interpretar cada linea de un archivo de texto en donde se dejen todos los registros...
#...estos registros se deben interpretar linea a linea, por lo que esta clase se encarga de crear internamente los...
#...objetos luego de leer las lineas, y permiten el funcionamiento correcto del programa.
# FECHA/ ACTIVO-INACTIVO / TIPO(GASTO PROYECTO, CREAR PROYECTO, etc) / INFO PROPIA SEGUN TIPO DE ACCION
#Es importante tener en cuenta que esta clase tendra toda la info de todos los proyectos mientras corre el codigo de crear los excels
class INTERPRETAR_TXT:
    def __init__(self,ruta):
        self.ruta = ruta
        self.actualizar_todo()

    def actualizar_todo(self):
        # print("ACTUALIZADO")
        #este diccionario guarda numeros segun el nombre del proyecto, los cuales se almacenaran en un vector de objetos(proyectos)
        #ej> diccionario_proyectos = {"BOREAL":0, "CASA GUARNE":1, "ALEJANDRIA CASA": 2}
        self.diccionario_posicion__en_vector_proyectos = {}
        #este vector tendra cada uno de los proyectos agregados (en orden como lo diga el diccionario)
        self.vector_proyectos= []
        txt = open( self.ruta, "r")
        info_lineas = txt.readlines()
        for line in info_lineas:
            #Try except (para evitar problemas si queda una linea con "enter", y trate de buscar vector en posicion que NO existe)
            try:
                info = line.split(",")
                #LINEAS DE REGISTRO (CREACION PROYECTOS):  "fecha", "ACTIVO/INACTIVO","CREAR PROYECTO","NOMBRE PROYECTO","ETAPAS"
                if info[2] == "CREAR PROYECTO" and info[1] == "ACTIVO":
                    #Recordemos que "info[3]" representa el nombre del proyecto, el cual tendra un numero unico asociado a este en el diccionario mostrado
                    self.diccionario_posicion__en_vector_proyectos[ info[3] ] = len(self.vector_proyectos)
                    self.vector_proyectos.append( Proyecto( info[3], info[4], info[0] ) )

                #LINEAS DE REGISTRO (INICIACION SUBETAPAS):  "fecha", "ACTIVO/INACTIVO","INICIAR SUBETAPA","NOMBRE PROYECTO","ETAPA","SUBETAPA"
                elif info[2] == "INICIAR SUBETAPA" and info[1] == "ACTIVO":
                    for proy in self.vector_proyectos:
                        if proy.nombre_proyecto == info[3]:
                            etapa = int(info[4]) - 1
                            subetapa = int(info[5]) - 1
                            proy.vector_etapas[ etapa ].vector_subetapas[ subetapa ].iniciar_subetapa( info[0] )

                #LINEAS DE REGISTRO (TERMINACION SUBETAPAS):  "fecha", "ACTIVO/INACTIVO","TERMINAR SUBETAPA","NOMBRE PROYECTO","ETAPA","SUBETAPA"
                elif info[2] == "TERMINAR SUBETAPA" and info[1] == "ACTIVO":
                    for proy in self.vector_proyectos:
                        if proy.nombre_proyecto == info[3]:
                            etapa = int(info[4]) - 1
                            subetapa = int(info[5]) - 1
                            proy.vector_etapas[ etapa ].vector_subetapas[ subetapa ].finalizar_subetapa( info[0] )

                #LINEAS DE REGISTRO (AGREGAR GASTOS DE SUBETAPAS):  "fecha", "ACTIVO/INACTIVO","GASTO","NOMBRE PROYECTO","ETAPA","SUBETAPA","CANTIDAD"
                elif info[2] == "GASTO" and info[1] == "ACTIVO":
                    for proy in self.vector_proyectos:
                        if proy.nombre_proyecto == info[3]:
                            etapa = int(info[4]) - 1
                            subetapa = int(info[5]) - 1
                            proy.vector_etapas[ etapa ].vector_subetapas[subetapa].agregar_gasto( Gasto( info[6], info[7], info[0] ) )

                #LINEAS DE REGISTRO (AGREGAR INGRESOS DE SUBETAPAS):  "fecha", "ACTIVO/INACTIVO","INGRESO","NOMBRE PROYECTO","ETAPA","SUBETAPA","CANTIDAD"
                elif info[2] == "INGRESO" and info[1] == "ACTIVO":
                    for proy in self.vector_proyectos:
                        if proy.nombre_proyecto == info[3]:
                            etapa = int(info[4]) - 1
                            subetapa = int(info[5]) - 1
                            proy.vector_etapas[ etapa ].vector_subetapas[subetapa].agregar_ingreso( Ingreso( info[6], info[7], info[0] ) )       
                
                #LINEAS DE REGISTRO (CAMBIAR NOMBRE ETAPA): "fecha","ACTIVO/INACTIVO","CAMBIAR NOMBRE ETAPA","NOMBRE PROYECTO","ETAPA","NUEVO NOMBRE ETAPA"
                elif info[2] == "CAMBIAR NOMBRE ETAPA" and info[1] == "ACTIVO":
                    for proy in self.vector_proyectos:
                        if proy.nombre_proyecto == info[3]:
                            etapa = int(info[4]) - 1
                            proy.vector_etapas[etapa].cambiar_nombre_etapa( info[5] )
                
                #LINEAS DE REGISTRO (AGREGAR DIRECTOR ETAPA): "fecha","ACTIVO/INACTIVO","AGREGAR DIRECTOR","NOMBRE PROYECTO","ETAPA","NOMBRE DIRECTOR"
                elif info[2] == "AGREGAR DIRECTOR" and info[1] == "ACTIVO":
                    for proy in self.vector_proyectos:
                        if proy.nombre_proyecto == info[3]:
                            etapa = int(info[4]) - 1
                            proy.vector_etapas[etapa].agregar_director( info[5] )

                #LINEAS DE REGISTRO (AGREGAR COORDINADOR ETAPA): "fecha","ACTIVO/INACTIVO","AGREGAR COORDINADOR","NOMBRE PROYECTO","ETAPA","NOMBRE COORDINADOR"
                elif info[2] == "AGREGAR COORDINADOR" and info[1] == "ACTIVO":
                    for proy in self.vector_proyectos:
                        if proy.nombre_proyecto == info[3]:
                            etapa = int(info[4]) - 1
                            proy.vector_etapas[etapa].agregar_coordinador( info[5] )

                #LINEAS DE REGISTRO (AGREGAR ARQUITECTO ETAPA): "fecha","ACTIVO/INACTIVO","AGREGAR ARQUITECTO","NOMBRE PROYECTO","ETAPA","NOMBRE ARQUITECTO"
                elif info[2] == "AGREGAR ARQUITECTO" and info[1] == "ACTIVO":
                    for proy in self.vector_proyectos:
                        if proy.nombre_proyecto == info[3]:
                            etapa = int(info[4]) - 1
                            proy.vector_etapas[etapa].agregar_arquitecto( info[5] )

                #LINEAS DE REGISTRO (AGREGAR AREA ETAPA): "fecha","ACTIVO/INACTIVO","AGREGAR AREA ETAPA","NOMBRE PROYECTO","ETAPA","AREA"
                elif info[2] == "AGREGAR AREA ETAPA" and info[1] == "ACTIVO":
                    for proy in self.vector_proyectos:
                        if proy.nombre_proyecto == info[3]:
                            etapa = int(info[4]) - 1
                            proy.vector_etapas[etapa].cambiar_area_etapa( info[5] )

                #LINEAS DE REGISTRO (AGREGAR NUEVA ETAPA): "fecha","ACTIVO/INACTIVO","AGREGAR NUEVA ETAPA","NOMBRE PROYECTO"
                elif info[2] == "AGREGAR NUEVA ETAPA" and info[1] == "ACTIVO":
                    for proy in self.vector_proyectos:
                        if proy.nombre_proyecto == info[3]:
                            proy.aumentar_etapa()






            except:
                pass



                


        txt.close() 

    #METODO PARA GUI (mostrar proyectos actuales)
    def get_nombre_proyectos(self):
        vector_nombre_proyectos = []
        for proy in range( len(self.vector_proyectos) ):
            vector_nombre_proyectos.append( self.vector_proyectos[proy].nombre_proyecto )
        return (vector_nombre_proyectos)

    #METODO PARA GUI (mostrar etapas segun el proyecto indicado)
    def get_nombre_etapas(self,index_proyecto):
        vector_nombre_etapas = []
        for etap in range( len(self.vector_proyectos[index_proyecto].vector_etapas)):
            vector_nombre_etapas.append( self.vector_proyectos[index_proyecto].vector_etapas[etap].nombre_etapa )
        return(vector_nombre_etapas)


    def guardar_info(self):
        #mostramos proyectos, con sus etapas y subetapas e info de cada una de estas (mientras lo actualizamos en excel)
        
        for proy in self.vector_proyectos:
            proy.mostrar_etapas_y_subetapas()
    
    def crear_excel_de_proyectos(self):
        #Se crea la carpeta donde se guarda la informacion de los proyectos
        path_carpeta = INFO_DIR_ACTUAL.CREACION_CARPETA()
        #Se utiliza la libreria de creacion de excels para crear un archivo xlsx con todos los proyectos y su info
        PROYECTOS_EXCEL = xlsxwriter.Workbook( "{}\\{}".format( path_carpeta.devolver_ruta_guardado() ,'{}.xlsx'.format("PROYECTOS")  ) )
        
        #Formatos utiles para mostrar informacion organizada
        bold = PROYECTOS_EXCEL.add_format({'bold': True})
        bold_border = PROYECTOS_EXCEL.add_format({"bold":True,"border":True})
        bold_border_gris = PROYECTOS_EXCEL.add_format({"bold":True,"border":True,"align":"center","bg_color":"#C8C8C8"})
        normal_border = PROYECTOS_EXCEL.add_format({"border":True})
        currency_border = PROYECTOS_EXCEL.add_format({"num_format":'$#,##0.00',"border":True})
        currency_border_bold  = PROYECTOS_EXCEL.add_format({"num_format":'$#,##0.00',"border":True,"bold":True})
        txt_rojo_bold = PROYECTOS_EXCEL.add_format({'bold': True, 'font_color':"red"})
        txt_verde_bold = PROYECTOS_EXCEL.add_format({"bold":True, "font_color":"green"})
        fondo_gris_bold = PROYECTOS_EXCEL.add_format({"bold":True,"bg_color":"#C0C0C0","border":True})
        fondo_azul_bold_merge_1 = PROYECTOS_EXCEL.add_format({"bold":True,"bg_color":"#66B2FF","align":"center","border":True})
        fondo_azul_bold_merge_2 = PROYECTOS_EXCEL.add_format({"bold":True,"bg_color":"#CFE2F5","align":"left","border":True,"font_color":"black"})


        
        #Creamos vector respectivas hojas de excel para cada uno de los proyectos (una por cada proyecto)
        vector_hojas_excel = []

        #Accedemos a cada proyecto...
        for proy in range( len(self.vector_proyectos) ):
            #Creamos variables encargadas del manejo de filas y columnas en el archivo de excel para cada hoja de cada proyecto
            fila = 5
            columna = 0 

            #Agregamos tantos proyectos como sean necesarios en un vector asociados a las hojas de excel (con su nombre)
            vector_hojas_excel.append( PROYECTOS_EXCEL.add_worksheet("{}".format( self.vector_proyectos[proy].nombre_proyecto ) )  )
            


            #Dejamos el nombre del proyecto respectivo en la primera celda, junto con la info basica
            vector_hojas_excel[proy].write( 0,0, "{}".format( "NOMBRE PROYECTO:" ), fondo_gris_bold )
            vector_hojas_excel[proy].write( 0,1, "{}".format( self.vector_proyectos[proy].nombre_proyecto ), fondo_gris_bold )
            vector_hojas_excel[proy].write( 1,0, "{}".format( "FECHA INICIO:" ), fondo_gris_bold )
            vector_hojas_excel[proy].write( 1,1, "{}".format( self.vector_proyectos[proy].fecha_inicio_proyecto ), fondo_gris_bold)
            vector_hojas_excel[proy].write( 2,0, "{}".format( "FECHA FIN:" ), fondo_gris_bold )
            vector_hojas_excel[proy].write( 2,1, "{}".format( self.vector_proyectos[proy].fecha_fin_proyecto),fondo_gris_bold )
            vector_hojas_excel[proy].write( 3,0, "{}".format( "CANTIDAD ETAPAS:" ), fondo_gris_bold )
            try:
                vector_hojas_excel[proy].write( 3,1, int(self.vector_proyectos[proy].cantidad_etapas), fondo_gris_bold )
            except:
                vector_hojas_excel[proy].write( 3,1,self.vector_proyectos[proy].cantidad_etapas, fondo_gris_bold )




            #Accedemos a cada etapa...
            for etap in range( len( self.vector_proyectos[proy].vector_etapas) ):
                #Cada etapa tendra las filas de un tamanno horizontal optimo (mejorar visualizacion y separacion entre ellas) 
                vector_hojas_excel[proy].set_column('{}:{}'.format( xl_rowcol_to_cell(fila,columna) , xl_rowcol_to_cell(fila,columna + 3) ), 30)
                
                #Mostramos titulo de cada etapa del proyecto
                vector_hojas_excel[proy].merge_range( fila,columna,fila,columna + 3, "{}".format( str(self.vector_proyectos[proy].vector_etapas[etap].nombre_etapa)  ), fondo_azul_bold_merge_1 )
                fila = fila + 1
                
                #Mostramos personal de trabajo de la etapa (director, coordinador y arquitectos)
                vector_hojas_excel[proy].write( fila, columna, "DIRECTOR ETAPA:",bold )
                vector_hojas_excel[proy].write( fila, columna + 1 , "{}".format( self.vector_proyectos[proy].vector_etapas[etap].director ),bold )
                vector_hojas_excel[proy].write( fila + 1, columna, "COORDINADOR ETAPA:",bold )
                vector_hojas_excel[proy].write( fila + 1, columna + 1 , "{}".format( self.vector_proyectos[proy].vector_etapas[etap].coordinador ),bold )
                fila = fila + 2

                #Mostramos arquitectos, segun los que hayan...
                if len( self.vector_proyectos[proy].vector_etapas[etap].vector_arquitectos ) == 0:
                    vector_hojas_excel[proy].write( fila, columna, "ARQUITECTOS:",bold )
                    vector_hojas_excel[proy].write( fila, columna + 1, "PENDIENTE POR ASIGNAR",bold )
                    fila = fila + 1

                else:
                    vector_hojas_excel[proy].write( fila, columna, "ARQUITECTOS:",bold )
                    for arq in range( len( self.vector_proyectos[proy].vector_etapas[etap].vector_arquitectos ) ):
                        vector_hojas_excel[proy].write( fila, columna + 1, "{}".format( self.vector_proyectos[proy].vector_etapas[etap].vector_arquitectos[arq] ) ,bold )
                        fila = fila + 1
                vector_hojas_excel[proy].write( fila + 1, columna,"ÁREA ETAPA:",bold )
                try:
                    vector_hojas_excel[proy].write( fila + 1, columna + 1,float( self.vector_proyectos[proy].vector_etapas[etap].area_etapa)  ,bold )
                except:
                    vector_hojas_excel[proy].write( fila + 1, columna + 1,self.vector_proyectos[proy].vector_etapas[etap].area_etapa,bold )

                fila = fila + 4
                #Recorremos cada subetapa (siempre son las mismas 4)
                for subetapa in range(4):
                    #Con esto comenzamos a mostrar la info de cada subetapa (su nombre)
                    vector_hojas_excel[proy].merge_range( fila,columna, fila, columna + 3,"{}".format( self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].nombre_subetapa ),fondo_azul_bold_merge_2 )                    
                    fila = fila +1
                    vector_hojas_excel[proy].write( fila,columna,"{}".format( "ESTADO ACTUAL" ),bold )
                    vector_hojas_excel[proy].write( fila,columna + 1,"{}".format( self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].estado_subetapa ),bold )
                    fila = fila +1
                    vector_hojas_excel[proy].write( fila,columna,"{}".format( "FECHA INICIO" ),bold )
                    vector_hojas_excel[proy].write( fila,columna + 1,"{}".format( self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].fecha_inicio ),bold )
                    fila = fila +1
                    vector_hojas_excel[proy].write( fila,columna,"{}".format( "FECHA FINALIZACIÓN" ),bold )
                    vector_hojas_excel[proy].write( fila,columna + 1,"{}".format( self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].fecha_fin ),bold )
                    fila = fila +3
                    
                    #Comenzamos a mostrar la info de los gastos
                    vector_hojas_excel[proy].write( fila,columna,"{}".format( "GASTOS:" ),txt_rojo_bold )
                    fila = fila +1

                    #Condicional para mostrar gastos (o en su defecto, mostrar que no hay)
                    if len( self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].gastos ) == 0:
                        #Mostramos que no hay gastos, si el vector de gastos esta vacio
                        vector_hojas_excel[proy].write( fila,columna,"{}".format( "No hay gastos registrados" ) )
                        fila = fila +1
                    else:
                        #Si SI hay gastos, se muestra el encabezado para la fecha, el nombre del gasto y el valor asociado
                        vector_hojas_excel[proy].write( fila,columna,"{}".format("Fecha"),bold_border_gris)
                        vector_hojas_excel[proy].write( fila,columna + 1,"{}".format("Nombre Gasto"),bold_border_gris)
                        vector_hojas_excel[proy].write( fila,columna + 2,"{}".format("Cantidad"),bold_border_gris)
                        fila = fila + 1

                        #Se crea string con las CELDAS que ALMACENAN LA CANTIDAD DE LOS GASTOS (para ingresar formula del total)
                        string_celdas_gastos = "="
                        #Se recorren los gastos, con ayuda del vector que los almacena y se muestra su info importante
                        for gasto in range( len(self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].gastos) ):
                            vector_hojas_excel[proy].write( fila, columna,"{}".format( self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].gastos[gasto].fecha_gasto ), normal_border )
                            vector_hojas_excel[proy].write( fila, columna + 1,"{}".format( self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].gastos[gasto].nombre_gasto ),normal_border )
                            vector_hojas_excel[proy].write( fila, columna + 2, float(self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].gastos[gasto].cantidad_gasto ),currency_border )

                            #Se almacenan las celdas de los gastos estrategicos
                            if gasto == ( len(self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].gastos) - 1 ):
                                string_celdas_gastos = string_celdas_gastos + xl_rowcol_to_cell(fila,columna+2)
                            else:
                                string_celdas_gastos = string_celdas_gastos + xl_rowcol_to_cell(fila,columna+2) + "+"

                            #Se aumenta la fila para continuar debido proceso
                            fila = fila + 1


                        # # print(string_celdas_gastos)
                        vector_hojas_excel[proy].write( fila,columna + 1,"{}".format("total gastos") , bold_border )
                        vector_hojas_excel[proy].write( fila,columna + 2, string_celdas_gastos, currency_border_bold)
                        fila = fila + 1


                    #Ahora se muestran los Ingresos
                    fila = fila + 1
                    vector_hojas_excel[proy].write( fila,columna,"{}".format( "INGRESOS:" ),txt_verde_bold )
                    fila = fila + 1
                    #Condicional para mostrar ingresos (o en su defecto, mostrar que NO hay)
                    if len( self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].ingresos ) == 0:
                        #Mostramos que no hay ingresos, si el vector de ingresos esta vacio
                        vector_hojas_excel[proy].write( fila,columna,"{}".format( "No hay ingresos registrados" ) )
                        fila = fila +1
                    else:
                        #Si SI hay ingresos, se muestra el encabezado para la fecha, el nombre del ingreso y el valor asociado
                        vector_hojas_excel[proy].write( fila,columna,"{}".format("Fecha"),bold_border_gris)
                        vector_hojas_excel[proy].write( fila,columna + 1,"{}".format("Nombre Ingreso"),bold_border_gris)
                        vector_hojas_excel[proy].write( fila,columna + 2,"{}".format("Cantidad"),bold_border_gris)
                        fila = fila + 1

                        #Se recorren los ingresos, con ayuda del vector que los almacena y se muestra su info importante
                        #OJO: se debe crear un string que logre almacenar las celdas que llevan cantidad de ingreso (para formula posterior)
                        string_celdas_ingresos = "="
                        for ingreso in range( len(self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].ingresos) ):
                            vector_hojas_excel[proy].write( fila, columna,"{}".format( self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].ingresos[ingreso].fecha_ingreso ), normal_border )
                            vector_hojas_excel[proy].write( fila, columna + 1,"{}".format( self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].ingresos[ingreso].nombre_ingreso ),normal_border )
                            vector_hojas_excel[proy].write( fila, columna + 2, float(self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].ingresos[ingreso].cantidad_ingreso ),currency_border )

                            #Se almacenan las celdas de los gastos estrategicos
                            if ingreso == ( len(self.vector_proyectos[proy].vector_etapas[etap].vector_subetapas[subetapa].ingresos) - 1 ):
                                string_celdas_ingresos = string_celdas_ingresos + xl_rowcol_to_cell(fila,columna+2)
                            else:
                                string_celdas_ingresos = string_celdas_ingresos + xl_rowcol_to_cell(fila,columna+2) + "+"

                            #Se aumenta la fila para continuar debido proceso
                            fila = fila + 1


                        # # print(string_celdas_gastos)
                        vector_hojas_excel[proy].write( fila,columna + 1,"{}".format("total ingresos") , bold_border )
                        vector_hojas_excel[proy].write( fila,columna + 2, string_celdas_ingresos, currency_border_bold)
                        fila = fila + 1


                    #Dejamos un espacio de 3 entre cada subetapa (para ser mas organizados)
                    fila = fila + 3



                columna = columna + 5
                fila = 5

                
                            
        PROYECTOS_EXCEL.close()
            
##-----------------------------------------------------------------------------------------------------------------
##-----------------------------------------------------------------------------------------------------------------
##ZONA DE PRUEBAS DE ESCRITORIO

# recuperar_info = INTERPRETAR_TXT( glob.glob("REGISTROS.txt")[0] )
# recuperar_info.guardar_info()
# recuperar_info.crear_excel_de_proyectos()


# #Para ver tiempo de correr codigo
# print ("\nTIEMPO CODIGO: ", str( time.time() - start ), "segundos.")