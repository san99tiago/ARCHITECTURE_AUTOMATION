# -*- coding: utf-8 -*-
##La linea superior se encarga de poder hacer encoding con reconocimiento de tildes y enne

#CODIGO PARA CREAR ARCHIVO TXT COMO BACKUP DE LOS REGISTROS EN LA CARPETA DONDE SE GUARDAN EXCELS

#Libreria para manejar la lectura correcta de los archivos TXT
import glob
import INFO_DIR_ACTUAL

class CREAR_TXT_BACKUP:
    def __init__(self):
        #Obtenemos el nombre del archivo de los registros
        self.archivo = glob.glob("REGISTROS.txt")[0] 
        self.nuevo_txt()

    def nuevo_txt(self):
        #NUEVO_TXT permite escribir los registros nuevos, con el cambio de nombre de dicho proyecto
        NUEVO_TXT = ""

        #Se abre archivo TXT en modo lectura, que contiene info de los proyectos y todos los registros
        txt = open( self.archivo, "r")
        #Se lee el txt segun cada linea (para filtrar info mejor)
        info_lineas = txt.readlines()
        #Se lee cada linea por separado y se analiza para hacer el cambio de nombre
        for line in info_lineas:

            #Try except (para evitar problemas si queda una linea con "enter", y trate de buscar vector en posicion que NO existe)
            try:
                NUEVO_TXT = NUEVO_TXT + line
            
            #Se evitan problemas de lectura y decodificacion, al emplear Try Except (ej: evitar problemas de lineas vacias)
            except:
                pass
            
            
        txt.close() 

        #---------AHORA SE ESCRIBE NUEVO TXT CON INFO ACTUALIZADA DE NOMBRE DE PROYECTOS---------------
        CARPETA_GUARDAR = INFO_DIR_ACTUAL.CREACION_CARPETA()
        path_guardar = CARPETA_GUARDAR.devolver_ruta_guardado() + "\\REGISTROS_BACKUP.txt"
        #Se abre archivo TXT con direccion de carpeta respectiva en modo write, que contiene info de los proyectos y todos los registros
        txt = open( path_guardar, "w")
        txt.write(NUEVO_TXT)
        txt.close()

#-----------------------------------------------------------------------------------------------------------------------------------
#PRUEBA DE ESCRITORIO
# TEST1 = CREAR_TXT_BACKUP()