import cv2
import numpy as np
import matplotlib.pyplot as plt

def edge_mask(img, line_size=7, blur_value=7):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,line_size, blur_value)
    return edges

def color_quantization(img,k):
    data = np.float32(img).reshape((-1,3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,20,0.001)
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result
def cartoon(img,params=[7,7,11]):

    edges = edge_mask(img, params[0], params[1])
    res = color_quantization(img,params[2])
    blurr = cv2.bilateralFilter(res, d=7, sigmaColor=200,sigmaSpace=200)
    c = cv2.bitwise_and(blurr,blurr,mask=edges)
    return c