import cv2
import numpy as np
import imutils
import streamlit as st
import base64
def detect_face(input_img):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_image = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 1:
        return faces[0]
    else:
        return None

def thug_life(input_img,angle,x,y):
    face_coords = detect_face(input_img)

    if face_coords is None:
        return input_img

    sunglass_img = cv2.imread('media/glasses.png', cv2.IMREAD_UNCHANGED)
    sunglass_img = imutils.rotate(sunglass_img, angle=angle)
    face_width, face_height = face_coords[2], face_coords[3]
    sunglass_img_resized = cv2.resize(sunglass_img, (face_width, face_height))

    # Check if the image has an alpha channel
    if sunglass_img_resized.shape[2] == 4:
        alpha_channel_resized = cv2.resize(sunglass_img_resized[:, :, 3], (face_width, face_height))
    else:
        # If no alpha channel, create a default one
        alpha_channel_resized = np.ones((face_height, face_width), dtype=np.uint8) * 255

    thug_glass = alpha_channel_resized / 255.0
    thug_glass = np.stack([thug_glass] * 3, axis=-1)
    offset_y = int(face_height * y)  # Adjust the offset based on your preference
    start_y = max(0, face_coords[1] - offset_y)
    offset_x = int(face_width * x)  # Adjust the offset based on your preference
    start_x = max(0, face_coords[1] - offset_x)
    roi = input_img[start_y: start_y + face_height, start_x:start_x + face_width]

    glass_bgr = sunglass_img_resized[:, :, :3]
    overlay = (1 - thug_glass) * roi + thug_glass * glass_bgr
    input_img[start_y: start_y + face_height, start_x:start_x + face_width] = overlay
    music_file = 'media/ThugLife.mp3'
    audio_bytes = open(music_file,'rb').read()
    audio_bytes = base64.b64encode(audio_bytes).decode()
    st.markdown(f'<audio autoplay controls><source src="data:audio/mp3;base64,{audio_bytes}" type="audio/mp3"></audio>', unsafe_allow_html=True)

    return input_img
