# Modifica el programa para guardar el rostro en una imagen PNG
# con la fecha de captura, genera cientos de fotos recortadas 
# sonriendo y enojado para entrenar un modelo ML/DL que determine
# si la persona está feliz o enojada

import cv2
import numpy

capturador = cv2.VideoCapture(0)

while True:
    ok, frame = capturador.read()

    if not ok:
        break

    frame = numpy.ascontiguousarray(frame[:, ::-1])

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

    cv2.imshow("Camara", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

capturador.release()
cv2.destroyAllWindows()
