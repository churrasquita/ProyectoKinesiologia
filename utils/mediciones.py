"""
utils/mediciones.py
Funciones de detección y cálculo postural usando la API moderna de MediaPipe Tasks.
"""
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions
import math
import os
import threading
import urllib.request
from functools import lru_cache

MODELO_PATH = "pose_landmarker_full.task"
MODELO_URL = (
    "https://storage.googleapis.com/mediapipe-models/pose_landmarker/"
    "pose_landmarker_full/float16/latest/pose_landmarker_full.task"
)


_LOCK = threading.Lock()


def _asegurar_modelo() -> str:
    # El .task está en .gitignore, así que en Streamlit Cloud no viene con el repo.
    if not os.path.exists(MODELO_PATH):
        urllib.request.urlretrieve(MODELO_URL, MODELO_PATH)
    return MODELO_PATH

# ── Detección de landmarks con la API Nueva ───────────────────────────────────

@lru_cache(maxsize=1)
def _obtener_landmarker():
    # Se crea una sola vez y se reutiliza entre fotos y recargas de Streamlit.
    options = vision.PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=_asegurar_modelo()),
        running_mode=vision.RunningMode.IMAGE,
    )
    return vision.PoseLandmarker.create_from_options(options)


def detectar_landmarks(imagen_rgb: np.ndarray):
    """
    Recibe imagen RGB, devuelve (landmarks, imagen_anotada).
    Si no detecta cuerpo, devuelve (None, imagen_original).
    """

    imagen_anotada = imagen_rgb.copy()
    h, w, _ = imagen_rgb.shape

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imagen_rgb)
    with _LOCK:
        pose_result = _obtener_landmarker().detect(mp_image)

    if not pose_result.pose_landmarks:
        return None, imagen_rgb

    # Extraemos la primera persona detectada
    landmarks_detectados = pose_result.pose_landmarks[0]

    # Dibujar esqueleto manualmente (Hombros, Caderas, Tobillos)
    conexiones = [(11, 12), (11, 23), (12, 24), (23, 24), (23, 27), (24, 28)]
    for p1, p2 in conexiones:
        lm1 = landmarks_detectados[p1]
        lm2 = landmarks_detectados[p2]
        if lm1.visibility > 0.5 and lm2.visibility > 0.5:
            pt1 = (int(lm1.x * w), int(lm1.y * h))
            pt2 = (int(lm2.x * w), int(lm2.y * h))
            cv2.line(imagen_anotada, pt1, pt2, (255, 255, 255), 2, cv2.LINE_AA)

    # Resaltar y etiquetar los puntos clave de evaluación postural
    puntos_clave = {
        11: ("H.Izq", (100, 200, 0)),
        12: ("H.Der", (100, 200, 0)),
        23: ("C.Izq", (0, 165, 255)),
        24: ("C.Der", (0, 165, 255)),
        27: ("T.Izq", (50, 50, 200)),
        28: ("T.Der", (50, 50, 200)),
        7:  ("Oreja.I", (200, 0, 200)) 
    }
    
    for idx, (label, color) in puntos_clave.items():
        each_lm = landmarks_detectados[idx]
        if each_lm.visibility > 0.5:
            x = int(each_lm.x * w)
            y = int(each_lm.y * h)
            cv2.circle(imagen_anotada, (x, y), 8, color, -1)
            cv2.putText(imagen_anotada, label, (x + 8, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

    return landmarks_detectados, imagen_anotada


# ── Calibración con Objeto 3D (Actualizado a 28 cm) ───────────────────────

def calibrar_con_hoja(ancho_objeto_pixeles: float) -> float:
    if ancho_objeto_pixeles <= 0:
        raise ValueError("El ancho en píxeles debe ser mayor que 0.")
    return 28.0 / ancho_objeto_pixeles


# ── Mediciones posturales matemáticas ─────────────────────────────────────────

def _px(landmark, w: int, h: int) -> tuple:
    return int(landmark.x * w), int(landmark.y * h)


def calcular_asimetria_hombros(landmarks, w: int, h: int, factor_escala: float) -> float:
    _, y_hizq = _px(landmarks[11], w, h)
    _, y_hder = _px(landmarks[12], w, h)
    return abs(y_hizq - y_hder) * factor_escala


def calcular_dismetria_piernas(landmarks, w: int, h: int, factor_escala: float) -> float:
    _, y_cizq = _px(landmarks[23], w, h)
    _, y_tizq = _px(landmarks[27], w, h)
    largo_izq_px = abs(y_tizq - y_cizq)

    _, y_cder = _px(landmarks[24], w, h)
    _, y_tder = _px(landmarks[28], w, h)
    largo_der_px = abs(y_tder - y_cder)

    return abs(largo_izq_px - largo_der_px) * factor_escala


def calcular_angulo_cervical(landmarks, w: int, h: int) -> float | None:
    vis_oreja = landmarks[7].visibility
    vis_hombro = landmarks[11].visibility

    if vis_oreja < 0.5 or vis_hombro < 0.5:
        return None

    ox, oy = _px(landmarks[7], w, h)
    hx, hy = _px(landmarks[11], w, h)

    dx = hx - ox
    dy = hy - oy

    angulo_rad = math.atan2(abs(dx), abs(dy))
    return 90 - math.degrees(angulo_rad)
