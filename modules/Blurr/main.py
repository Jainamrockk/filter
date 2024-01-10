import cv2
import numpy as np
from helper.utils import points2array

def blur_all_faces(input_imag,landmark_files):
    detector,predictor = landmark_files
    msg = None
    detections = detector(input_imag, 1)
    if len(detections) == 0:
        msg = "No faces detected"
        return input_imag, msg
    
    canvas = input_imag.copy()
    for rect in detections:
        landmarks = predictor(input_imag, rect)
        landmarks = points2array(landmarks.parts())
        indices = list(range(16)) + [26,25,24,19,18,17,0]
        pts = np.array(landmarks)[indices].reshape(-1,1,2)        
        canvas = cv2.fillPoly(canvas,[pts],(255,255,255))
        canvas = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
        face_mask = cv2.threshold(canvas, 250, 255, cv2.THRESH_BINARY)[1]
        face_mask_in = cv2.bitwise_not(face_mask)
        blurred_face = cv2.GaussianBlur(input_imag, (37, 37), 150)
        blurred_face = cv2.bitwise_and(blurred_face, blurred_face, mask=face_mask_inv)
        bg = cv2.bitwise_and(input_imag, input_imag, mask=face_mask_in)
        input_img = cv2.bitwise_or(bg,blurred_face)

        return input_img,msg
    


