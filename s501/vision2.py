import cv2
import numpy

capturador = cv2.VideoCapture(0)

while True:
    
    ok, frame = capturador.read()

    if ok:
        # frame = cv2.flip(frame, 1) # Reflejo horizontal
        frame = numpy.ascontiguousarray(
            frame[:, ::-1] # Devuelve la matriz en el mismo numero de filas, pero con las columnas invertidas
        )

        cv2.imshow("ventana1", frame)
    else:
        print("! Error en la captura del frame")

    ultimaTecla = cv2.waitKey(1) & 0xFF

    teclaEscape = ultimaTecla == 27
    
    if teclaEscape:
        break

capturador.release()
cv2.destroyAllWindows()