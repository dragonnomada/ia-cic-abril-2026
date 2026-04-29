# Modifica el programa para colocar botón fijo en el FRAME (cuadrado)
# y detectar si se pulsa (si se mantiene el dedo indice por 3 segundos seguidos)

import cv2
import os
import numpy
import mediapipe

def dibujar_mano(frame, landmarks):
    alto, ancho = frame.shape[:2]

    puntos = []

    for landmark in landmarks:
        x = int(landmark.x * ancho)
        y = int(landmark.y * alto)
        puntos.append((x, y))

    for inicio, fin in conexiones_mano:
        cv2.line(frame, puntos[inicio], puntos[fin], magenta, 2)

    for punto in puntos:
        cv2.circle(frame, punto, 4, amarillo, -1)

BaseOptions = mediapipe.tasks.BaseOptions
HandLandmarker = mediapipe.tasks.vision.HandLandmarker
HandLandmarkerOptions = mediapipe.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mediapipe.tasks.vision.RunningMode

modelo = "hand_landmarker.task"

if not os.path.exists(modelo):
    print(f"No encontre el modelo: {modelo}")
    print("Descarga el modelo Hand Landmarker y guardalo junto a vision11.py.")
    raise SystemExit(1)

conexiones_mano = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (0, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (5, 9),
    (9, 10),
    (10, 11),
    (11, 12),
    (9, 13),
    (13, 14),
    (14, 15),
    (15, 16),
    (13, 17),
    (0, 17),
    (17, 18),
    (18, 19),
    (19, 20),
]

capturador = cv2.VideoCapture(0)

# Nombre de la ventana (referencia)
ventana = "Manos con MediaPipe"

# Paleta de colores en BGR
azul = (255, 0, 0)
amarillo = (0, 255, 255)
magenta = (255, 0, 255)

opciones = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=modelo,
        delegate=BaseOptions.Delegate.CPU,
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)

numero_frame = 0

with HandLandmarker.create_from_options(opciones) as detector:
    while True:
        ok, frame = capturador.read()

        if not ok:
            break

        numero_frame += 1

        frame = numpy.ascontiguousarray(frame[:, ::-1])
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        imagen = mediapipe.Image(image_format=mediapipe.ImageFormat.SRGB, data=rgb)
        tiempo_ms = numero_frame * 33

        resultados = detector.detect_for_video(imagen, tiempo_ms)

        for landmarks in resultados.hand_landmarks:
            dibujar_mano(frame, landmarks)

        cv2.putText(
            frame,
            "Esc: salir",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            azul,
            2,
            cv2.LINE_AA,
        )

        cv2.imshow(ventana, frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

capturador.release()
cv2.destroyAllWindows()
