import os
import cv2
import numpy as np
import streamlit as st
from webcam import webcam
from images import image_transformations
from PIL import Image
title = st.empty()
title.header("Image Filter")
img_extensions = ["jpg","png","jpeg"]

def show_info():
    st.subheader('''
    Creator Jainam Jain: 
    ''')
    st.markdown("### **Filters used:Cartoon")
    st.write("")
st.sidebar.subheader("Choose the mode of operation: ")
selected_option = st.sidebar.selectbox("",["Select from below","Image Filters","Video Filters"])

if selected_option == "Image Filters":
    title.header("Image Filters")
    img_operation_mode = st.selectbox("Upload Images from: ",["--  Select from below  --","Local Storage","Take a snap from Webcam"])

    if img_operation_mode == "Local Storage":
        uploaded_file = st.file_uploader("Upload images from local storage here",type = img_extensions)
        if uploaded_file is not None:

            image_byte = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            uploaded_file.seek(0)
            img_bytes = uploaded_file.read()
            decoded_img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), -1)
            result = decoded_img
            inp_img = cv2.imdecode(image_byte, 1)
            filter = st.selectbox("Choose an Image filter: ",["Basic Image Editing","Thug Life","Green Screen","Moustaches",\
            "Devil-ie","Heart Eyes","John Cena XD","Cartoonie","Face Blur"],0)
            image_transformations(result,inp_img,filter,uploaded_file.name.split("."))

    elif img_operation_mode == "Take a snap from Webcam":
        result = webcam()
        if result is None:
            st.write("Waiting for capture...")
        else:
            st.write("Got an image from the webcam :P")
            result = cv2.cvtColor(np.asarray(result,np.uint8),cv2.COLOR_RGB2BGR)

            filter = st.selectbox("Choose an Image filter: ",["Basic Image Editing","Thug Life","Green Screen","Moustaches",\
            "Devil-ie","Heart Eyes","John Cena XD","Cartoonie","Face Blur"],0)
            image_transformations(result,filter)

    else:
        st.sidebar.markdown('''
        This section contains filters to be applied on images.

        Images can be uploaded either from local storage (or) from your webcamera.
        ''')
        st.sidebar.markdown("Choose the source of image, from the drop list on right :point_right:")
        st.sidebar.subheader("Tips for operating on Image Filters: ")
        st.sidebar.markdown('''
            * Un edited pictures provide the best results.
            * Link to download the edited pictures are at the bottom of the page
            ''')

