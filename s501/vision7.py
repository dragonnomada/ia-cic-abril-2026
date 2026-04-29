import cv2
import numpy

def mascara_roja(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # H: ángulo, S: staturación, V: brillo
    mask_lower = cv2.inRange(hsv, (0, 120, 70), (10, 255, 255)) # 0°-10°
    mask_high = cv2.inRange(hsv, (170, 120, 70), (180, 255, 255)) # 170°-180°

    mask = mask_lower | mask_high

    return mask

capturador = cv2.VideoCapture(0)

contexto = {
    "mascara": None
}

while True:

    ok, frame = capturador.read()

    if ok:
        frame = numpy.ascontiguousarray(
            frame[:, ::-1]
        )

        frame_mask = numpy.zeros_like(frame)

        mask = mascara_roja(frame)

        frame_mask[:, :, 2] = mask

        if contexto["mascara"] is None:
            cv2.imshow("ventana1", frame)
        else:
            cv2.imshow("ventana1", frame_mask)
        

    teclaPulsada = cv2.waitKey(1) & 0xFF

    teclaEscpe = teclaPulsada == 27
    
    teclaA = teclaPulsada == ord("a")
    teclaX = teclaPulsada == ord("x")

    if teclaEscpe:
        break
    elif teclaA:
        contexto["mascara"] = True
    elif teclaX:
        contexto["mascara"] = None

capturador.release()
cv2.destroyAllWindows()