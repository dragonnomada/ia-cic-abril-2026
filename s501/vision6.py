import cv2
import numpy

capturador = cv2.VideoCapture(0)

contexto = {
    "canal": None
}

while True:

    ok, frame = capturador.read()

    if ok:
        frame = numpy.ascontiguousarray(
            frame[:, ::-1]
        )

        # Canal rojo
        frame_rojo = numpy.zeros_like(frame)
        frame_rojo[:, :, 2] = frame[:, :, 2]
        
        # Canal verde
        frame_verde = numpy.zeros_like(frame)
        frame_verde[:, :, 1] = frame[:, :, 1]
        
        # Canal verde
        frame_azul = numpy.zeros_like(frame)
        frame_azul[:, :, 0] = frame[:, :, 0]

        if contexto["canal"] is None:
            cv2.imshow("ventana1", frame)
        elif contexto["canal"] == "rojo":
            cv2.imshow("ventana1", frame_rojo)
        elif contexto["canal"] == "verde":
            cv2.imshow("ventana1", frame_verde)
        elif contexto["canal"] == "azul":
            cv2.imshow("ventana1", frame_azul)

    teclaPulsada = cv2.waitKey(1) & 0xFF

    teclaEscpe = teclaPulsada == 27
    
    teclaA = teclaPulsada == ord("a")
    teclaB = teclaPulsada == ord("b")
    teclaC = teclaPulsada == ord("c")
    teclaX = teclaPulsada == ord("x")

    if teclaEscpe:
        break
    elif teclaA:
        contexto["canal"] = "rojo"
    elif teclaB:
        contexto["canal"] = "verde"
    elif teclaC:
        contexto["canal"] = "azul"
    elif teclaX:
        contexto["canal"] = None

capturador.release()
cv2.destroyAllWindows()