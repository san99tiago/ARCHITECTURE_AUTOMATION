# -*- coding: utf-8 -*-
##La linea superior se encarga de poder hacer encoding con reconocimiento de tildes y enne


#Este codigo esta enfocado a eliminar TODAS las lineas de codigo de un proyecto especifico (eliminar proyecto)
#Libreria para manejar la lectura correcta de los archivos TXT
import glob

class ELIMINAR_PROYECTO:
    def __init__(self, nombre_proyecto_a_eliminar):
        #Obtenemos el nombre del archivo de los registros
        self.archivo = glob.glob("REGISTROS.txt")[0] 

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
                #Se separa linea por comas
                info = line.split(",")
                
                #Se compara nombre de los proyectos actuales, con los de cada linea y se efectua proceso para cambio
                if info[3] == nombre_proyecto_a_eliminar:
                    #Si la linea es la del proyecto a eliminar, se debe ELIMINAR (entonces NO hacemos nada)
                    pass

                #Si NO se llama igual al proyecto, entonces de debe permanecer la info de las lineas, pues son otros proyectos
                else:
                    NUEVO_TXT = NUEVO_TXT + line
            
            #Se evitan problemas de lectura y decodificacion, al emplear Try Except (ej: evitar problemas de lineas vacias)
            except:
                pass

        txt.close() 

        #---------AHORA SE ESCRIBE NUEVO TXT CON INFO ACTUALIZADA DE NOMBRE DE PROYECTOS---------------
        #Se abre archivo TXT en modo write, que contiene info de los proyectos y todos los registros
        txt = open( self.archivo, "w")
        txt.write(NUEVO_TXT)
        txt.close()

        
###-------------------------------------------------------------------------------------------------------------------------
##PRUEBAS DE ESCRITORIO
# CCC = ELIMINAR_PROYECTO("CAMIII")
