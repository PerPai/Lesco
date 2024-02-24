import cv2
import os
import numpy as np
import re
import app as talk
from ultralytics import YOLO

# Clase Seguimiento manos.
import SeguimientoManos as sm

hablar = input("¿Deseas que el sistema hable? (1: Sí, 0: No): ")
# Lectura camara
cap= cv2.VideoCapture(2)
# Resolucion
cap.set(3,1280)
cap.set(4,720)

# Leer nuestro modelo
model = YOLO('vocales.pt')
# Declarar detector
detector=sm.detectormanos(Confdeteccion=0.9)

# Crear una variable para almacenar la última letra detectada
ultima_letra = None

while True:
    # Realizar la lectura de la capturadora
    ret, frame = cap.read()

    # Extraer informacion de la mano
    frame=detector.encontrarmanos(frame, False)

    # Posicion de un sola mano
    lista1,bbox, mano= detector.encontrarposicion(frame, ManoNum=0, dibujarPuntos =False, dibujarBox=False, color=[0,255,0])

    # Si hay mano
    if mano >=1:    

        # Extraer informacion del cuadro
        xmin,ymin,xmax,ymax = bbox

        # Asignamos margen
        xmin = xmin -120
        ymin =ymin -120
        xmax=xmax +120
        ymax =ymax +120

        recorte = frame[ymin:ymax,xmin:xmax]
        
        # Verificar si la imagen está vacía
        if recorte.size != 0:
            # Redimensionar la imagen
            recorte=cv2.resize(recorte,(640,640), interpolation=cv2.INTER_CUBIC)
       
            # Extraer resultados
            resultados = model.predict(recorte, conf=0.9)
            
            # Obtener las anotaciones
            anotaciones = resultados[0].plot()
            
            # Obtener las clases detectadas
            detecciones = resultados[0].boxes

            # Imprimir las letras de las predicciones
            for i in range(len(detecciones)):
                clase_idx = detecciones.cls[i].item()
                letra_detectada = model.names[clase_idx]
                print("Letra detectada:", letra_detectada)

                if letra_detectada != "La imagen recortada está vacía":
                    # Si la letra detectada es diferente de la última letra detectada,
                    # hacer que el sistema hable y actualizar la última letra detectada
                    if letra_detectada != ultima_letra:
                        if hablar == '1':
                            talk.speaker(letra_detectada)
                        ultima_letra = letra_detectada
        else:
            print("La imagen recortada está vacía")     
            
        cv2.imshow("Recorte", anotaciones)

    # Mostrar FPS
    cv2.imshow("Lenguaje de vocales", frame)
    t= cv2.waitKey(1)
    if t == 27:
        break

cap.release()
cv2.destroyAllWindows()
