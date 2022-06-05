"""
    ################################################################################
    Given an image, apply SVD factorization to compress the image and then save it
    ################################################################################


    @Universidad: Javeriana Cali
    @Facultad: Ingenieri'a y Ciencias
    @Curso: Ana'lisis y Computacio'n Nume'rica
    @Tema: Factorizacio'n SVD
        
    @Autor:
        - Geiler Hipia Meji'a
        - Jair Narvaez Chamarro
        - Juan Villaroel Luengas
        - Laura Benavides Ocampo
        
    @Docente: Andres Felipe Amador Rodriguez
    @Versio'n: 1.0



"""
from PIL import Image
import numpy as np
import os

# Clase Img : Para representar una imagen en forma matricial
class Img:
    
    def __init__(self, path : str ) -> None:

        # Atributos de la clase Img
        #
        self.path = path
        self.image = None
        self.matrix = None
        self.red_matrix = None
        self.green_matrix = None
        self.blue_matrix = None
        self.width, self.height = 0, 0
        
        # Inicializacio'n
        #
        # Paso 1: Abrir imagen
        self.__openImage()
        # Paso 2: Generar matrix
        self.__generateMatrix()
        # Paso 3: Calcular las matrices R, G, B
        self.__setRGB()
        # Paso 4: Calcular el tama\~no
        self.__setSize()

    # Funcio'n para abrien la imagen
    #
    def __openImage(self) -> None:
        self.image = Image.open(self.path)

    # Funcio'n para generar la matrix
    #
    def __generateMatrix(self) -> None:
        self.matrix = np.array(self.image)

    # Funcion para establecer las matrices R, G, B
    #
    def __setRGB(self) -> None:
        
        # Inicializando las matrices R, G, B
        # - En la primera posicio'n [:,:, 0] se encuentra la matriz con 
        #   los valores correspodiente del rojo
        # - En la segunda posicio'n [:,:, 0] se encuentra la matriz con
        #   los valores correspondientes al verde
        # - En la tercera posicio'n [:,:, 0] se encuentra la matriz con
        #   los valores correspondientes al azul
    
        self.red_matrix = self.matrix[:, :, 0] 
        self.green_matrix = self.matrix[:, :, 1]
        self.blue_matrix =  self.matrix[:, :, 2]
    
    # Funcio'n para establecer las dimenciones dela imagen
    def __setSize(self) -> None:
        self.width, self.height = self.image.size

    def show(self):
        self.image.show()
    

class User:

    def __init__(self) -> None:
        self.__MAX_BYTES = 5000000
        self.__BYTES = 0
        self.__images = []

    def send(self, image, user) -> bool:
        return user.recv(image)

    def recv(self, image) -> bool:
        appended = False
        size = os.path.getsize(image.path) 
        if size + self.__BYTES <= self.__MAX_BYTES:
            self.__BYTES += size
            self.__images.append(image)
            appended = True
        return appended

    def getPercentageStored(self) -> float:
        return self.__BYTES * 100 / self.__MAX_BYTES
        
    def getBytesStore(self) -> float:
        return self.__BYTES

    def getAmountImages(self) -> int:
        return len(self.__images)


# Clase SVD: clase para representar la descomposición en Valores singulares(SVD)
#
class SVD:

    def __init__(self) -> None:
        # Sin atributos [not yet]
        pass

    # Funcio'n para comprimir una ima'gen
    # parametros: image : Img 
    #             k : int
    # retorno: Image
    #
    def compressImage(self, image : Img, k : int):

        # Para cada matriz R, G, B de la matriz M (matriz principal de la imagen original)
        # se comprime usando una cantidad k de valores singulares.
        #
        compressed_red = self.__compressMatrix(image.red_matrix, k)
        compressed_green = self.__compressMatrix(image.green_matrix, k)
        compressed_blue = self.__compressMatrix(image.blue_matrix, k)

        # Dado un array de valores se convierten a imagen
        red_image = Image.fromarray(compressed_red, mode = None)
        green_image = Image.fromarray(compressed_green, mode = None)
        blue_image = Image.fromarray(compressed_blue, mode = None)

        # Se retorna una image. Se usa merge para unir una imagen con
        # los valores R, G, B
        #
        return Image.merge(
            'RGB',
            (red_image,
            green_image,
            blue_image)
        )

    # Funcio'n para comprimir una matriz
    # Parametro: matrix : ..
    #            k : int
    # retorno: array como tipo uint8
    #
    def __compressMatrix(self, matrix, k : int):
        # Usando la funcio'n svd de la libreri'a numpy
        # calculamos la descomposicion de la matriz
        #
        U, S, VT = np.linalg.svd(matrix)
        # para cada matriz U, S, VT solamente se obtienen k columnas
        # solamente la matrix S (sigma) previamente se obtiene 
        # solamente su diagonal, finalmente se multiplican estas matriz
        # con el operadore @ (sobrecargado en numpy.array)
        #
        
        compressed_matrix = (U[:, 0 : k]             @ 
                            np.diag(S)[0 : k, 0 : k] @
                            VT[0 : k, :])

        # se retorna la matriz comprimidad como tipo uint8
        return compressed_matrix.astype('uint8')

    def compressAndSave(self, path, k):
        compressed_image = self.compressImage(Img(path), k)
        new_path = path[0 : path.find('.')] + '_' + str(k) + path[path.find('.'):]
        compressed_image.save(new_path)
        return new_path



class Manager:
    
    def __init__(self) -> None:
        self.userA = User()
        self.userB = User()
        self.__svd = SVD()
        self.lastImageUserA = str()
        self.lastImageUserB = str()

    def send(self, from_to, path, compress, k : int)  -> bool:

        ans = False
        self.lastImageUserA = path
        self.lastImageUserB = path

        if from_to =='AtoB':
            if compress:
                new_path = self.__svd.compressAndSave(path, k)
                ans = self.userA.send( Img( new_path ), self.userB )
                self.lastImageUserB = new_path
            else:
                ans = self.userA.send( Img(path), self.userB)

        elif from_to == 'BtoA':
            if compress:
                new_path = self.__svd.compressAndSave(path, k)
                self.lastImageUserA = new_path
                ans = self.userB.send( Img( new_path ), self.userA)
            else:
                ans = self.userB.send( Img(path), self.userA)   
        
        return ans


    def getSrcLastImages(self) -> str:

        srcA = self.lastImageUserA
        srcA = srcA[srcA.find("static/images") : ]  
        srcB = self.lastImageUserB
        srcB = srcB[srcB.find("static/images") : ]  
       
        return srcA, srcB