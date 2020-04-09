# -*- coding: utf-8 -*-
##La linea superior se encarga de poder hacer encoding con reconocimiento de tildes y enne


#Este codigo esta enfocado a cambiar nombre de 1 proyecto en el TXT de registros
#Libreria para manejar la lectura correcta de los archivos TXT
import glob


class CAMBIAR_NOMBRE_PROYECTO:
    def __init__(self, nombre_actual_proyecto, nombre_nuevo_proyecto):
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
                if info[3] == nombre_actual_proyecto:
                    #Se genera string para almacenar info de la linea nueva, segun cambio (o no) de nombres proyectos
                    linea_nueva = ""

                    #OJO: como no todos tienen igual cantidad de info (algunos tienen 6 posiciones, otros 7, otros 8, etcc...)
                    #...entonces recorro segun cantidad de separaciones de cada linea
                    for dato in range( len(info) ):
                        #Posicion diferente a tres son las que permanecen igual (NO REQUIEREN CAMBIO)
                        if dato != 3:
                            linea_nueva = linea_nueva + info[dato]
                            #Si el dato es la ultima linea, NO nos interesa agregar coma (puede saltarse a otra linea)
                            #por esto se deben separar condiciones segun linea en la que se encuentre
                            if dato == ( len(info) -1):
                                linea_nueva = linea_nueva
                            else:
                                linea_nueva = linea_nueva + ","

                        #En caso de que sea POSICION ASOCIADA A NOMBRE PROYECTO... (osea cambio)
                        else:
                            linea_nueva = linea_nueva + nombre_nuevo_proyecto + ","
                    
                    #Se escribe nuevo texto (el que reemplazara al otro).
                    NUEVO_TXT = NUEVO_TXT + linea_nueva

                #Si NO se llama igual el proyecto, con el nombre de proyecto que se desea cambiar, entonces se guarda linea antigua (sin cambios)
                else:
                    NUEVO_TXT = NUEVO_TXT + line
            
            #Se evitan problemas de lectura y decodificacion, al emplear Try Except (ej: evitar problemas de lineas vacias)
            except:
                pass
            
            
        # print(NUEVO_TXT)
        txt.close() 

        #---------AHORA SE ESCRIBE NUEVO TXT CON INFO ACTUALIZADA DE NOMBRE DE PROYECTOS---------------

        #Se abre archivo TXT en modo write, que contiene info de los proyectos y todos los registros
        txt = open( self.archivo, "w")
        txt.write(NUEVO_TXT)
        txt.close()

        
###-------------------------------------------------------------------------------------------------------------------------
##PRUEBAS DE ESCRITORIO
# CCC = CAMBIAR_NOMBRE_PROYECTO("ADIOS","BOREAL")
