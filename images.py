import cv2
import os
import base64
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import streamlit as st
from modules.Cartoon.main import cartoon
from modules.ThugLife.main import thug_life
# from helper.utils import file_checker
# from helper.descriptor import file_info
# from helper.rcnn_utils import generate_rcnn_mask

img_extensions = ["jpg","png","jpeg"]

def get_binary_file_downloader_html(bin_file,file_label='File'):
    with open(bin_file,'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<h3><a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a></h3>'
    return href

def image_transformations(result,inp_img,filter,img_extension = "jpg"):
        result = result[:,:,:3]
        # filter_info(filter)
        if filter == "Basic Image Editing":
            gamma = st.slider("Gamma Correction",0.0,5.0,1.0,step = 0.1)
            saturation = st.slider("Saturation", 0.0, 2.0, 1.0, step=0.1)
            blurring = st.checkbox("Bluring", False)
            if blurring:
                col1,col2 = st.columns(2)
                blur_area = col1.slider("Blur Area",1,100,1,2)
                blur_intensity = col2.slider("Blur Intensity", 0, 500, 0, 1)
                result = cv2.GaussianBlur(result, (blur_area, 1), blur_intensity)

            apply_vignette = st.checkbox("Apply Vignette effect",False)
            if apply_vignette:
                vignette_effect = st.slider("Vignette Intensity",1,120,1)
                rows, cols = result.shape[:2]
                kernel_x = cv2.getGaussianKernel(cols, vignette_effect + 139)
                kernel_y = cv2.getGaussianKernel(rows, vignette_effect + 139)
                kernel = kernel_y*kernel_x.T
                filter = 255 * kernel / np.linalg.norm(kernel)
                vignette_img = np.copy(result)
                for i in range(3):
                    vignette_img[:,:,i] = vignette_img[:,:,i]*filter
                    result = vignette_img

            hsvImg = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
            hsvImg[..., 1] = np.clip(hsvImg[..., 1] * saturation, 0, 255)
            hsvImg[..., 2] = np.power((hsvImg[..., 2] / 255.0), 1 / (gamma + 0.1)) * 255.0
            result = cv2.cvtColor(hsvImg, cv2.COLOR_HSV2BGR)
        elif filter == "Cartoonie":
            line_size = st.slider("Number of edges",3,101,7,2)
            blurVal = st.slider("Blurr effect",3,101,7,2)
            totalCols = st.slider("Total Color in images",2,100,11,1)
            result = cartoon(result,[line_size,blurVal,totalCols])
        elif filter == "Thug Life":
            angle = st.slider("Angle",-360,360,0,1)
            x = st.slider("Shift X",-1.0,1.0,0.0,0.1)
            y = st.slider("Shift Y", -1.0, 1.0, 0.0, 0.1)
            result = thug_life(inp_img,angle,x,y)
        if np.all(result != None):
            st.image(result, use_column_width=True, clamp=True, channels="BGR")
            filename = img_extension[0] + "." + img_extension[-1]
            cv2.imwrite(filename, result)
            st.markdown(get_binary_file_downloader_html(filename,
            'From Here '),
            unsafe_allow_html=True)