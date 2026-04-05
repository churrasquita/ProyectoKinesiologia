import cv2
import mediapipe as mp

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
        # extraer coordenadas del hombro izquierdo (punto 11)
        #los valores están 0.0 a 1.0
        h, w, _ = frame.shape
        cx = int(results.pose_landmarks.landmark[11].x * w)
        cy = int(results.pose_landmarks.landmark[11].y * h)
        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

    cv2.imshow('Deteccion de Antropometria', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.closeAllWindows()
