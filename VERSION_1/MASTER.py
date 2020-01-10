#CODIGO MASTER DEL SISTEMA DE AUTOMATIZACION DE PROYECTOS 
import datetime
# from MANEJO_TXT import ArchivoTexto
import glob

#Esta clase es la encargada de todo el analisis de cada proyecto, con sus respectivas N etapas y 4 subetapas estandarizadas
class Proyecto:
    #Se inicializa con el nombre del proyecto y la cantidad de etapas, de tal forma que se puedan generar todas las...
    #respectivas subetapas de cada una de las etapas automaticamente.
    #Info de etapas esta en "self.vector_etapas"
    #Info de subetapas pertenece a cada etapa y esta en "self.vector_subetapas"
    def __init__(self, nombre_proyecto, cantidad_etapas,fecha):
        self.nombre_proyecto = nombre_proyecto
        self.cantidad_etapas = cantidad_etapas
        self.fecha = fecha
        self.estado_proyecto = "EN PROGRESO"
        #Se inicializa el vector principal donde se almacene la informacion de cada una de las etapas, segun la cantidad de estas
        self.vector_etapas = []
        #Con el siguiente metodo, se generan automaticamente las etapas segun los parametros de entrada (cantidad de etapas y nombre del proyecto)
        self.crear_etapas_iniciales()

    def finalizar_proyecto(self, nombre_proyecto,fecha):
        self.estado_proyecto = "FINALIZADO"

    #Metodo encargado de inicializar y almacenar la informacion valiosa de cada una de las etapas asociadas al proyecto
    #este metodo se corre unicamente al inicio de cada uno de los proyectos, para facilitar el manejo de las etapas y proyectos netos
    def crear_etapas_iniciales(self):
        for i in range( int(self.cantidad_etapas) ):
            #Se agregan tantas etapas como se hayan indicado en los parametros de creacion del proyecto
            self.vector_etapas.append(  Etapa( "ETAPA {} {}".format(str(i+1),self.nombre_proyecto) ) )
            #Se geran las respectivas 4 subetapas que son estandar (siempre las mismas)
            for j in range(4):
                if j == 0:
                    self.vector_etapas[i].agregar_subetapas( Subetapa( "IDEA BASICA {} {}".format( self.nombre_proyecto, self.vector_etapas[i].nombre_etapa  ), self.fecha ) )
                elif j == 1:
                    self.vector_etapas[i].agregar_subetapas( Subetapa( "ANTEPROYECTO {} {}".format( self.nombre_proyecto, self.vector_etapas[i].nombre_etapa ),self.fecha ) )
                elif j == 2:
                    self.vector_etapas[i].agregar_subetapas( Subetapa( "PROYECTO ARQUITECTONICO {} {}".format( self.nombre_proyecto, self.vector_etapas[i].nombre_etapa ), "NO DEFINIDA" ) )
                    self.vector_etapas[i].vector_subetapas[j].estado_subetapa = "SIN COMENZAR"
                else:
                    self.vector_etapas[i].agregar_subetapas( Subetapa( "COORDINACION ARQUITECTONICA {} {}".format( self.nombre_proyecto, self.vector_etapas[i].nombre_etapa ), "NO DEFINIDA" ) )
                    self.vector_etapas[i].vector_subetapas[j].estado_subetapa = "SIN COMENZAR"

    def mostrar_etapas_y_subetapas(self):
        for i in range( int(self.cantidad_etapas) ):
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

    def agregar_subetapas(self, Subetapa):
        self.vector_subetapas.append( Subetapa )



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

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#Esta accion es encargada de interpretar cada linea de un archivo de texto en donde se dejen todos los registros...
#estos registros se deben interpretar linea a linea, por lo que esta clase se encarga de crear internamente los...
#objetos luego de leer las lineas, y permiten el funcionamiento correcto del programa.
# FECHA/ ACTIVO-INACTIVO / TIPO(GASTO PROYECTO, CREAR PROYECTO, etc) / info propia
#este diccionario guarda numeros segun el nombre del proyecto, los cuales se almacenaran en un vector de objetos(proyectos)
#ej> diccionario_proyectos = {"BOREAL":0, "CASA GUARNE":1, "ALEJANDRIA CASA": 2}
diccionario_posicion__en_vector_proyectos = {}
#este vector tendra cada uno de los proyectos agregados (en orden como lo diga el diccionario)
vector_proyectos= []
class INTERPRETAR_TXT:
    def __init__(self, ruta):
        self.ruta = ruta
        txt = open( self.ruta, "r")
        info_lineas = txt.readlines()
        for line in info_lineas:
            info = line.split(",")
            #LINEAS DE REGISTRO (CREACION PROYECTOS):  "fecha", "ACTIVO/INACTIVO","CREAR PROYECTO","NOMBRE PROYECTO","ETAPAS"
            if info[2] == "CREAR PROYECTO" and info[1] == "ACTIVO":
                #Recordemos que "info[3]" representa el nombre del proyecto, el cual tendra un numero unico asociado a este en el diccionario mostrado
                diccionario_posicion__en_vector_proyectos[ info[3] ] = len(vector_proyectos)
                vector_proyectos.append( Proyecto( info[3], info[4], info[0] ) )

            #LINEAS DE REGISTRO (INICIACION SUBETAPAS):  "fecha", "ACTIVO/INACTIVO","INICIAR SUBETAPA","NOMBRE PROYECTO","ETAPA","SUBETAPA"
            elif info[2] == "INICIAR SUBETAPA" and info[1] == "ACTIVO":
                for proy in vector_proyectos:
                    if proy.nombre_proyecto == info[3]:
                        etapa = int(info[4]) - 1
                        subetapa = int(info[5]) - 1
                        proy.vector_etapas[ etapa ].vector_subetapas[ subetapa ].iniciar_subetapa( info[0] )

            #LINEAS DE REGISTRO (TERMINACION SUBETAPAS):  "fecha", "ACTIVO/INACTIVO","TERMINAR SUBETAPA","NOMBRE PROYECTO","ETAPA","SUBETAPA"
            elif info[2] == "TERMINAR SUBETAPA" and info[1] == "ACTIVO":
                for proy in vector_proyectos:
                    if proy.nombre_proyecto == info[3]:
                        etapa = int(info[4]) - 1
                        subetapa = int(info[5]) - 1
                        proy.vector_etapas[ etapa ].vector_subetapas[ subetapa ].finalizar_subetapa( info[0] )

            #LINEAS DE REGISTRO (AGREGAR GASTOS DE SUBETAPAS):  "fecha", "ACTIVO/INACTIVO","GASTO","NOMBRE PROYECTO","ETAPA","SUBETAPA","CANTIDAD"
            elif info[2] == "GASTO" and info[1] == "ACTIVO":
                for proy in vector_proyectos:
                    if proy.nombre_proyecto == info[3]:
                        etapa = int(info[4]) - 1
                        subetapa = int(info[5]) - 1
                        proy.vector_etapas[ etapa ].vector_subetapas[subetapa].agregar_gasto( Gasto( info[6], info[7], info[0] ) )

            #LINEAS DE REGISTRO (AGREGAR INGRESOS DE SUBETAPAS):  "fecha", "ACTIVO/INACTIVO","INGRESO","NOMBRE PROYECTO","ETAPA","SUBETAPA","CANTIDAD"
            elif info[2] == "INGRESO" and info[1] == "ACTIVO":
                for proy in vector_proyectos:
                    if proy.nombre_proyecto == info[3]:
                        etapa = int(info[4]) - 1
                        subetapa = int(info[5]) - 1
                        proy.vector_etapas[ etapa ].vector_subetapas[subetapa].agregar_ingreso( Ingreso( info[6], info[7], info[0] ) )



        txt.close() 




##-----------------------------------------------------------------------------------------------------------------
##-----------------------------------------------------------------------------------------------------------------
##ZONA DE PRUEBAS DE ESCRITORIO

#Se crea clase para interpretar la info de txt (con ayuda de libreria glob.glob)
# print(diccionario_posicion__en_vector_proyectos)
# print(vector_proyectos)

recuperar_info = INTERPRETAR_TXT( glob.glob("REGISTROS.txt")[0] )


#mostramos proyectos, con sus etapas y subetapas e info de cada una de estas (mientras lo actualizamos en excel)
for proy in vector_proyectos:
    proy.mostrar_etapas_y_subetapas()
