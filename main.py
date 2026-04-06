import cv2
import mediapipe as mp

import numpy as np

def calcular_angulo(a, b, c):
    a = np.array(a) # Punto extremo 1 (ej: Hombro)
    b = np.array(b) # Vértice (ej: Codo)
    c = np.array(c) # Punto extremo 2 (ej: Muñeca)
    
    # Calculamos los radianes con atan2
    radianes = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angulo = np.abs(radianes * 180.0 / np.pi)
    
    # Nos aseguramos que el ángulo no exceda los 180 grados (típico en kinesiología)
    if angulo > 180.0:
        angulo = 360 - angulo
        
    return angulo

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose =mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0) #ccamara por defecto

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # convertir a RGB (MediaPipe usa RGB, OpenCV usa BGR)
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    # dibujar los puntos 
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        
        landmarks = results.pose_landmarks.landmark
        
        h, w, _ = frame.shape
        
        # coordenadas [x, y] escaladas a los píxeles de la imagen
        hombro = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w,
                  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
        
        codo = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w,
                landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h]
        
        muneca = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w,
                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]

        # 3. Calcular el ángulo
        angulo_codo = calcular_angulo(hombro, codo, muneca)

        # 4. Visualizar el ángulo en pantalla
        cv2.putText(frame, str(int(angulo_codo)) + " deg", 
                    tuple(np.multiply(codo, [1, 1]).astype(int)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('Deteccion de Antropometria', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.closeAllWindows()
