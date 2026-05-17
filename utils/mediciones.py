"""
utils/mediciones.py
Funciones de detección y cálculo postural usando MediaPipe.
"""
import cv2
import numpy as np
import mediapipe as mp
import math

mp_pose    = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_styles  = mp.solutions.drawing_styles


# ── Detección de landmarks ────────────────────────────────────────────────────

def detectar_landmarks(imagen_rgb: np.ndarray):
    """
    Recibe imagen RGB, devuelve (landmarks, imagen_anotada).
    Si no detecta cuerpo, devuelve (None, imagen_original).
    """
    with mp_pose.Pose(
        static_image_mode=True,
        model_complexity=2,
        min_detection_confidence=0.5
    ) as pose:
        resultados = pose.process(imagen_rgb)

        if not resultados.pose_landmarks:
            return None, imagen_rgb

        # Dibujar esqueleto
        imagen_anotada = imagen_rgb.copy()
        mp_drawing.draw_landmarks(
            imagen_anotada,
            resultados.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(
                color=(46, 134, 171), thickness=2, circle_radius=4
            ),
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(255, 255, 255), thickness=2
            )
        )

        # Resaltar los 6 puntos clave
        lm = resultados.pose_landmarks.landmark
        h, w, _ = imagen_rgb.shape
        puntos_clave = {
            11: ("H.Izq", (0, 200, 100)),
            12: ("H.Der", (0, 200, 100)),
            23: ("C.Izq", (255, 165, 0)),
            24: ("C.Der", (255, 165, 0)),
            27: ("T.Izq", (200, 50, 50)),
            28: ("T.Der", (200, 50, 50)),
        }
        for idx, (label, color) in puntos_clave.items():
            x = int(lm[idx].x * w)
            y = int(lm[idx].y * h)
            cv2.circle(imagen_anotada, (x, y), 8, color, -1)
            cv2.putText(imagen_anotada, label, (x + 8, y - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

        return resultados.pose_landmarks.landmark, imagen_anotada


# ── Calibración ───────────────────────────────────────────────────────────────

def calibrar_con_hoja(ancho_hoja_pixeles: float) -> float:
    """
    Calcula el factor de escala cm/píxel usando el ancho de una hoja carta.
    Hoja carta: 21.59 cm de ancho.
    """
    if ancho_hoja_pixeles <= 0:
        raise ValueError("El ancho en píxeles debe ser mayor que 0.")
    return 21.59 / ancho_hoja_pixeles


# ── Mediciones posturales ─────────────────────────────────────────────────────

def _px(landmark, w: int, h: int) -> tuple:
    """Convierte landmark normalizado a píxeles."""
    return int(landmark.x * w), int(landmark.y * h)


def calcular_asimetria_hombros(landmarks, w: int, h: int, factor_escala: float) -> float:
    """
    Diferencia de altura entre hombro izquierdo (11) y derecho (12).
    Devuelve el valor en centímetros.
    Un valor > 1.0 cm sugiere posible escoliosis.
    """
    lm = landmarks
    _, y_hizq = _px(lm[11], w, h)
    _, y_hder = _px(lm[12], w, h)
    diferencia_px = abs(y_hizq - y_hder)
    return diferencia_px * factor_escala


def calcular_dismetria_piernas(landmarks, w: int, h: int, factor_escala: float) -> float:
    """
    Diferencia de largo entre pierna izquierda y derecha.
    Largo = distancia desde cadera (23/24) hasta tobillo (27/28).
    Devuelve la diferencia en centímetros.
    Un valor > 1.0 cm sugiere posible dismetría de miembros inferiores.
    """
    lm = landmarks

    _, y_cizq = _px(lm[23], w, h)
    _, y_tizq = _px(lm[27], w, h)
    largo_izq_px = abs(y_tizq - y_cizq)

    _, y_cder = _px(lm[24], w, h)
    _, y_tder = _px(lm[28], w, h)
    largo_der_px = abs(y_tder - y_cder)

    diferencia_px = abs(largo_izq_px - largo_der_px)
    return diferencia_px * factor_escala


def calcular_angulo_cervical(landmarks, w: int, h: int) -> float | None:
    """
    Calcula el ángulo de proyección cervical anterior (foto de perfil).
    Usa puntos: oreja (7 o 8), hombro (11 o 12).
    El ángulo se mide respecto a la vertical.
    < 40° = proyección cervical anterior (postura de texto).
    Devuelve None si no hay suficiente visibilidad.
    """
    lm = landmarks

    # Usar lado izquierdo (7 = oreja izq, 11 = hombro izq)
    vis_oreja   = lm[7].visibility
    vis_hombro  = lm[11].visibility

    if vis_oreja < 0.5 or vis_hombro < 0.5:
        return None

    ox, oy = _px(lm[7], w, h)   # oreja
    hx, hy = _px(lm[11], w, h)  # hombro

    # Vector oreja → hombro
    dx = hx - ox
    dy = hy - oy

    # Ángulo respecto a la vertical (0° = perfectamente erguido)
    angulo_rad = math.atan2(abs(dx), abs(dy))
    angulo_deg = math.degrees(angulo_rad)

    # Convertir: 90° - ángulo para que > 50° sea "normal"
    return 90 - angulo_deg


# ── Clasificación IMC pediátrico ──────────────────────────────────────────────

def clasificar_imc_pediatrico(imc: float, edad: int) -> tuple[str, str]:
    """
    Clasificación simplificada de IMC para niños y adolescentes (OMS).
    Devuelve (estado_texto, clase_css).
    """
    # Umbrales aproximados para 11-15 años (simplificado)
    if edad <= 11:
        umbrales = (14.5, 18.0, 21.0, 25.0)
    elif edad <= 13:
        umbrales = (15.0, 18.5, 22.0, 26.5)
    else:
        umbrales = (15.5, 19.0, 23.5, 28.0)

    bajo, normal_min, sobrepeso, obesidad = umbrales

    if imc < bajo:
        return "Bajo peso severo", "status-derivar"
    elif imc < normal_min:
        return "Bajo peso", "status-alerta"
    elif imc < sobrepeso:
        return "Normal", "status-normal"
    elif imc < obesidad:
        return "Sobrepeso", "status-alerta"
    else:
        return "Obesidad", "status-derivar"
