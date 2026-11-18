"""
utils/mediciones.py
Funciones de detección y cálculo postural usando la API moderna de MediaPipe Tasks.

Calibración: ya no se usa un objeto de referencia. La escala píxel → cm se obtiene
de la talla real del alumno (medida con tallímetro) dividida por la altura de la
persona en la foto, estimada con los landmarks (ojos → planta del pie).
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

# Altura de los ojos como fracción de la talla (vértex → ojos ≈ 6.5 % de la talla).
# Se usa porque MediaPipe no entrega un punto en la coronilla.
# Nota: no se usa la máscara de segmentación de MediaPipe porque en la versión
# 0.10.x leerla (numpy_view sobre VEC32F1) aborta el proceso completo.
FRACCION_OJOS_TALLA = 0.935

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


# Puntos y conexiones que se dibujan según la vista
_VISTAS = {
    "frontal": {
        "conexiones": [(11, 12), (11, 23), (12, 24), (23, 24), (23, 27), (24, 28)],
        "puntos": {
            11: ("H.Izq", (100, 200, 0)),
            12: ("H.Der", (100, 200, 0)),
            23: ("C.Izq", (0, 165, 255)),
            24: ("C.Der", (0, 165, 255)),
            27: ("T.Izq", (50, 50, 200)),
            28: ("T.Der", (50, 50, 200)),
        },
    },
    "perfil": {
        "conexiones": [],
        "puntos": {},
    },
}


def detectar_landmarks(imagen_rgb: np.ndarray, vista: str = "frontal"):
    """
    Recibe imagen RGB y la vista ("frontal" o "perfil"); devuelve
    (landmarks, imagen_anotada). Si no detecta cuerpo, devuelve (None, imagen_original).
    """
    imagen_anotada = imagen_rgb.copy()
    h, w, _ = imagen_rgb.shape

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imagen_rgb)
    with _LOCK:
        pose_result = _obtener_landmarker().detect(mp_image)

    if not pose_result.pose_landmarks:
        return None, imagen_rgb

    landmarks_detectados = pose_result.pose_landmarks[0]

    config = _VISTAS[vista]
    conexiones, puntos_clave = config["conexiones"], dict(config["puntos"])

    if vista == "perfil":
        # Se dibuja el lado del cuerpo que mira a la cámara: oreja → hombro.
        oreja, hombro = lado_visible_perfil(landmarks_detectados)
        conexiones = [(oreja, hombro)]
        puntos_clave = {
            oreja: ("Oreja", (200, 0, 200)),
            hombro: ("Hombro", (100, 200, 0)),
        }

    grosor = max(2, int(round(min(h, w) / 400)))
    for p1, p2 in conexiones:
        lm1 = landmarks_detectados[p1]
        lm2 = landmarks_detectados[p2]
        if lm1.visibility > 0.5 and lm2.visibility > 0.5:
            pt1 = (int(lm1.x * w), int(lm1.y * h))
            pt2 = (int(lm2.x * w), int(lm2.y * h))
            cv2.line(imagen_anotada, pt1, pt2, (255, 255, 255), grosor, cv2.LINE_AA)

    if vista == "perfil":
        # Línea horizontal de referencia que pasa por el hombro (ángulo craneovertebral)
        lm_h = landmarks_detectados[hombro]
        if lm_h.visibility > 0.5:
            x, y = int(lm_h.x * w), int(lm_h.y * h)
            largo = int(0.15 * w)
            cv2.line(imagen_anotada, (x - largo, y), (x + largo, y),
                     (255, 255, 0), grosor, cv2.LINE_AA)

    radio = max(6, int(round(min(h, w) / 120)))
    escala_txt = max(0.45, min(h, w) / 1400)
    for idx, (label, color) in puntos_clave.items():
        each_lm = landmarks_detectados[idx]
        if each_lm.visibility > 0.5:
            x = int(each_lm.x * w)
            y = int(each_lm.y * h)
            cv2.circle(imagen_anotada, (x, y), radio, color, -1)
            cv2.putText(imagen_anotada, label, (x + radio, y - radio),
                        cv2.FONT_HERSHEY_SIMPLEX, escala_txt, color, grosor // 2 + 1, cv2.LINE_AA)

    return landmarks_detectados, imagen_anotada


# ── Calibración con la talla del alumno ───────────────────────────────────────

def altura_persona_px(landmarks, w: int, h: int):
    """
    Devuelve (y_superior, y_inferior) con la extensión vertical estimada de la
    persona en píxeles, o None si no se puede estimar.

    - Abajo: el punto más bajo entre talones (29, 30) y puntas de pie (31, 32).
    - Arriba: MediaPipe no marca la coronilla, así que se extrapola desde la
      altura de los ojos (2, 5), que en promedio está al 93.5 % de la talla.
    """
    pies = [landmarks[i].y for i in (29, 30, 31, 32) if landmarks[i].visibility > 0.3]
    ojos = [landmarks[i].y for i in (2, 5) if landmarks[i].visibility > 0.3]
    if not pies or not ojos:
        return None
    y_pies = max(pies) * h
    y_ojos = (sum(ojos) / len(ojos)) * h
    alto_ojos_pies = y_pies - y_ojos
    if alto_ojos_pies <= 0:
        return None
    alto_total = alto_ojos_pies / FRACCION_OJOS_TALLA
    return int(round(y_pies - alto_total)), int(round(y_pies))


def calibrar_con_talla(talla_cm: float, altura_px: float) -> float:
    """Factor de escala (cm/píxel) = talla real / altura de la persona en la foto."""
    if altura_px <= 0:
        raise ValueError("La altura en píxeles debe ser mayor que 0.")
    if talla_cm <= 0:
        raise ValueError("La talla debe ser mayor que 0.")
    return talla_cm / altura_px


def dibujar_altura(imagen: np.ndarray, y_sup: int, y_inf: int) -> np.ndarray:
    """Dibuja la línea vertical usada para calibrar (de cabeza a pies)."""
    h, w = imagen.shape[:2]
    salida = imagen.copy()
    x = int(0.04 * w)
    grosor = max(2, int(round(min(h, w) / 400)))
    color = (255, 200, 0)
    cv2.line(salida, (x, y_sup), (x, y_inf), color, grosor, cv2.LINE_AA)
    for y in (y_sup, y_inf):
        cv2.line(salida, (x - 3 * grosor, y), (x + 3 * grosor, y), color, grosor, cv2.LINE_AA)
    return salida


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


def lado_visible_perfil(landmarks) -> tuple:
    """
    En la foto de costado solo un lado mira a la cámara. Devuelve los índices
    (oreja, hombro) del lado con mejor visibilidad: izquierdo (7, 11) o derecho (8, 12).
    """
    vis_izq = landmarks[7].visibility + landmarks[11].visibility
    vis_der = landmarks[8].visibility + landmarks[12].visibility
    return (7, 11) if vis_izq >= vis_der else (8, 12)


def calcular_angulo_cervical(landmarks, w: int, h: int) -> float | None:
    """
    Ángulo craneovertebral aproximado (foto de costado): ángulo entre la
    horizontal que pasa por el hombro y la recta hombro → oreja.
    90° = oreja justo sobre el hombro; valores menores = cabeza adelantada.
    """
    oreja, hombro = lado_visible_perfil(landmarks)
    if landmarks[oreja].visibility < 0.5 or landmarks[hombro].visibility < 0.5:
        return None

    ox, oy = _px(landmarks[oreja], w, h)
    hx, hy = _px(landmarks[hombro], w, h)

    dx = hx - ox
    dy = hy - oy
    if dx == 0 and dy == 0:
        return None

    angulo_rad = math.atan2(abs(dx), abs(dy))
    return 90 - math.degrees(angulo_rad)
