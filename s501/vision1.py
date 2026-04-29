# pip install numpy
# pip install opencv-contrib-python
# pip install mediapipe

import cv2

# Iniciamos un capturador de videos (frame)
capturador = cv2.VideoCapture(0) # Webcam #0

# Loop - Ciclo de captura / Ciclo logico / Ciclo de render
# render -> pintado / refrescado
while True:
    ok, frame = capturador.read()

    if ok:
        cv2.imshow("ventana1", frame)
    else:
        print("No se pudo capturar el frame")

    teclaPulsada = cv2.waitKey(1) & 0xFF # Mascara de bits

    teclaEscape = teclaPulsada == 27 # ASCII
    teclaEnter = teclaPulsada == 13 # ASCII
    teclaA = teclaPulsada == ord("a") # ASCII

    if teclaEscape:
        break
    if teclaA:
        print("Hola mundo")
    if teclaEnter:
        print("Se pulso ENTER")

# Liberamos el capturador (destruimos los recursos asociados)
capturador.release()

# Libera las ventas abiertas
cv2.destroyAllWindows()