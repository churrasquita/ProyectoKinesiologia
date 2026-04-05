import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions

#coniguración
options = vision.PoseLandmarkerOptions(
    base_options = BaseOptions(model_asset_path = "./proyecto/pruebas/pose_landmarker_lite.task"),
    running_mode = vision.RunningMode.IMAGE)

landmarker = vision.PoseLandmarker.create_from_options(options)

#imagen de entrada

image = cv2.imread("./proyecto/pruebas/yoga.jpg")
if image is None:
    print("Error: No se encontró la imagen en la ruta especificada.")
else:
    scale_percent = 800 / image.shape[1] 
    dim = (800, int(image.shape[0] * scale_percent))
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    h,w,_ = image.shape
    image_rgb_data= cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    mp_image=mp.Image(image_format=mp.ImageFormat.SRGB, data = image_rgb_data)

    # obtener los resultados

    pose_result = landmarker.detect(mp_image)
    print(pose_result)

    for lm in pose_result.pose_landmarks:
        #print(lm)
        #print(lm[26])
        #x_right_knee = int(lm[26].x *w)
        #y_right_knee = int(lm[26].y *h)
        #cv2.circle(image, (x_right_knee, y_right_knee), 10, (0, 255, 0), -1)
        for each_lm in lm:
            if each_lm.visibility >0.9:
                x_each_lm = int(each_lm.x *w)
                y_each_lm = int(each_lm.y *h)
                cv2.circle(image, (x_each_lm, y_each_lm), 10, (0, 255, 0), -1)

    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()