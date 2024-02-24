import cv2
import os

#clase Seguimiento manos.

import SeguimientoManos as sm

#Crear capeta


nombre = 'Letra_I'
direccion='C:/lesco-recognizer/data'
carpeta=direccion + '/'+nombre


#si no esta creada la carpeta creela

if not os.path.exists(carpeta):
    print("carpeta Creada:" ,carpeta)
    #Crear Carpeta
    os.makedirs(carpeta)

#lectura camara
cap= cv2.VideoCapture(0)
#resolucion
cap.set(3,1280)
cap.set(4,720)

#Declaramaos contador
cont=0

#declarar detector
detector=sm.detectormanos(Confdeteccion=0.9)

while True:
    #Realizar la lectura de la capturadora
    ret, frame = cap.read()

    #Extraer informacion de la mano
    frame=detector.encontrarmanos(frame, False)

    #Posicion de un sola mano

    lista1,bbox, mano= detector.encontrarposicion(frame, ManoNum=0, dibujarPuntos =False, dibujarBox=False, color=[0,255,0])

    #Si hay mano
    if mano ==1:
        #extraer informacion del cuadro
        xmin,ymin,xmax,ymax = bbox

        #asignamos margen

        xmin = xmin -40
        ymin =ymin -40
        xmax=xmax +40
        ymax =ymax +40


        recorte = frame[ymin:ymax,xmin:xmax]

        #Redimencion
        recorte=cv2.resize(recorte,(640,640), interpolation=cv2.INTER_CUBIC)

        

        #ALMACENAR IMAGENES
        ruta_archivo = os.path.join(carpeta + "/I_{}.jpg".format(cont))
        print("Ruta del archivo a guardar:", ruta_archivo)
        cv2.imwrite(ruta_archivo, recorte)

        #Aumentamos contador
        cont=cont+1

        cv2.imshow("Recorte", recorte)
      #  cv2.rectangle(frame,(xmin,ymin),(xmax ,ymax),[0,255,0],2)

    #mostrar FPS
    cv2.imshow("Lenguaje de vocales", frame)
    t= cv2.waitKey(1)
    if t == 27 or cont ==100:
        break

cap.release()
cv2.destroyAllWindows()