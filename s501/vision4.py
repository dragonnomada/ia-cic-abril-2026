import cv2
import numpy

def controladorRaton(evento, x, y, banderas, contexto):

    if evento == cv2.EVENT_MOUSEMOVE:
        contexto["x"] = x
        contexto["y"] = y


capturador = cv2.VideoCapture(0)

contexto = {
    "x": 0,
    "y": 0,
}

cv2.namedWindow("ventana1")
cv2.setMouseCallback("ventana1", controladorRaton, contexto)

while True:

    ok, frame = capturador.read()

    if ok:
        frame = numpy.ascontiguousarray(
            frame[:, ::-1]
        )

        alto, ancho, _ = frame.shape

        x = contexto["x"]
        y = contexto["y"]

        cv2.line(frame, (x, 0), (x, alto), (255, 0, 255), 2, cv2.LINE_AA)
        cv2.line(frame, (0, y), (ancho, y), (255, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, 
                    f"({x}, {alto - y})", (x + 10, y - 20), 
                    cv2.FONT_HERSHEY_COMPLEX, 1, 
                    (255, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow("ventana1", frame)

    teclaPulsada = cv2.waitKey(1) & 0xFF

    teclaEscape = teclaPulsada == 27

    if teclaEscape:
        break

capturador.release()
cv2.destroyAllWindows()