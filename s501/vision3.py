import cv2
import numpy

capturador = cv2.VideoCapture(0)

while True:

    ok, frame = capturador.read()

    if ok:
        frame = numpy.ascontiguousarray(
            frame[:, ::-1]
        )

        # ============= LOGICA ======================
        alto, ancho, _ = frame.shape

        x = int(ancho / 2)
        y = int(alto / 2)
        
        # Coordenada (x, y)
        posicion = (x, y)
        # Color (b, g, r) [r, g, b / 0-255]
        rojo = (0, 0, 255)
        verde = (0, 255, 0)
        azul = (255, 0, 0)
        amarillo = (0, 255, 255)
        magenta = (255, 0, 255)
        cyan = (255, 255, 0)

        cv2.circle(frame, posicion, 8, rojo, -1, cv2.LINE_AA)
        cv2.circle(frame, posicion, 12, azul, 2, cv2.LINE_AA)
        cv2.circle(frame, posicion, 16, verde, 2, cv2.LINE_AA)
        cv2.circle(frame, posicion, 20, amarillo, 2, cv2.LINE_AA)
        cv2.circle(frame, posicion, 24, magenta, 2, cv2.LINE_AA)
        cv2.circle(frame, posicion, 28, cyan, 2, cv2.LINE_AA)
        
        ancho_2 = int(ancho / 2)
        alto_2 = int(alto / 2)

        p1 = (ancho_2, 0)
        p2 = (ancho_2, alto)
        
        p3 = (0, alto_2)
        p4 = (ancho, alto_2)

        cv2.line(frame, p1, p2, magenta, 2, cv2.LINE_AA) # Verticial centrada horizontalmente
        cv2.line(frame, p3, p4, magenta, 2, cv2.LINE_AA) # Horizontal centrada verticalmente
        # ===========================================

        cv2.imshow("ventana1", frame)

    teclaPulsada = cv2.waitKey(1) & 0xFF

    teclaEscape = teclaPulsada == 27

    if teclaEscape:
        break

capturador.release()
cv2.destroyAllWindows()