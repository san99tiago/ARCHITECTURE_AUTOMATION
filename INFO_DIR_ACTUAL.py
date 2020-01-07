#Este codigo se encarga de llevar la info de MASTER del proyecto, a archivos organizados con carpetas y los datos en excel.
#Es importante poder crear las subcarpetas con la info del dia del registro realizado
import os
import datetime
class CREACION_CARPETA:
    def __init__(self):
        #Se establece la informacion de la fecha actual, para crear las subcarpetas deseadas y luego los registros
        info_actual = datetime.datetime.now()

        #Estos se encargan de guardar info para el manejo de las carpetas en donde se guarde la info
        self.anno_registro = info_actual.strftime( "%Y" )
        self.mes_registro = info_actual.strftime( "%B" )
        self.dia_registro = info_actual.strftime( "%d %B %Y" )

        #Se obtiene info del directorio actual en el que estamos... (get current work directory)
        self.current_directory = os.getcwd()

        #Se crea el directorio final de info a guardar con base en el directorio en el que nos encontremos (independiente de donde sea)
        self.final_directory = os.path.join(self.current_directory, r"{}\\{}\\{}\\{}".format("PROYECTOS",self.anno_registro,self.mes_registro,self.dia_registro) )
        #Se garantiza NO crear repetidos innecesarios
        if not os.path.exists(self.final_directory):
            os.makedirs(self.final_directory)
    
    #Con este metodo, se permite retornar un str con el path absoluto hasta la carpeta del dia de trabajo...
    #Se debe ingresar esta info, justo antes del path de crear el archivo de excel con la info neta
    def devolver_ruta_guardado(self):
        return( self.final_directory )


#PRUEBAS DE ESCRITORIO
#------------------------------------------------------
# TEST = CREACION_CARPETA()
# print("ESTAAA")
# print( TEST.devolver_ruta_guardado() )