#Repaso de clase para leer, editar, agregar lineas nuevas, buscar y actualizar un txt (para proyecto Alejo de empresa)
#Archivo con el que se podra hacer ACTUALIZACION, ELIMINICACION y TRABAJOS CON EL TXT DE REGISTROS (la info total historica)

class ArchivoTexto:
    def __init__(self, ruta):
        self._ruta = ruta
        # txt = open(self._ruta, "r")
        # self.operaciones_totales = []
        # for line in txt:
        #     self.operaciones_totales = self.operaciones_totales + str( line )
        # txt.close()
        

    #Esto se encarga de generar un nuevo registro para el archivo en donde se esten guardando estos
    def agregar_operacion(self,str_operacion):
        txt = open(self._ruta, "a")
        txt.write( "\n{}".format(str_operacion))
        txt.close()

    
    def leer(self):
        print("INFO ARCHIVO REGISTROS\n")
        txt = open( self._ruta, "r")
        info_lineas = txt.readlines()
        for line in info_lineas:
                print(line.split(',')[0])
        txt.close() 
    
