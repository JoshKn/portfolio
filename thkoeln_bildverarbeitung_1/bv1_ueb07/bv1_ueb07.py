import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from bv1helper import BV1Helper as bv1

img = cv2.imread("./resources/lenna.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

"""1. Implementieren Sie eine Funktion, die Nächste-Nachbar-Interpolation umsetzt. Die
Funktion soll aufgerufen werden mit drei Parametern: einem Bild, einer x-Koordinate
und einer y-Koordinate, wobei die beiden zuletzt genannten Gleitkommawerte sein sollen.
Die Funktion soll dann den interpolierten Wert zurückgeben. Es ist ausreichend, wenn
die Interpolation für Grauwertbilder funktioniert. """
def scale_nn_interpol_forw(gray_img: np.ndarray, sx=500, sy=500) -> np.ndarray:
    sx, sy = round(sx), round(sy)

    scaled_img = np.zeros_like(gray_img, shape=(sx, sy))

    scaleX = sx/gray_img.shape[0]
    scaleY = sy/gray_img.shape[1]

    for y in range(1, gray_img.shape[0]):
        for x in range(1, gray_img.shape[1]):
            xDst = round(x * scaleX)
            yDst = round(y * scaleY)
            scaled_img[xDst, yDst] = gray_img[x,y]

    return scaled_img

def scale_nn_interpol_backw(gray_img: np.ndarray, sx=500, sy=500) -> np.ndarray:
    sx, sy = round(sx),round(sy)

    scaled_img = np.zeros_like(gray_img, shape=(sx, sy))

    scaleX = sx / gray_img.shape[0]
    scaleY = sy / gray_img.shape[1]

    for y in range(1, sy):
        for x in range(1, sx):
            xSrc = round(x/scaleX)
            ySrc = round(y/scaleY)
            scaled_img[x,y] = gray_img[xSrc, ySrc]
    return scaled_img

"""2. Implementieren Sie eine Funktion, die bilineare Interpolation umsetzt (mit den gleichen
Parametern und Anforderungen wie oben)."""

def bl_interpol(gray_img: np.ndarray, x, y):
    """Applies bilinear interpolation to two specific coordinates of an image.
    Returns interpolated gray value."""
    x_1 = int(x)
    x_2 = x_1 + 1
    y_1 = int(y)
    y_2 = y_1 + 1

    i_y_1 = gray_img[x_1, y_1] + (x - x_1) * gray_img[x_2, y_1]
    i_y_2 = gray_img[x_1, y_2] + (x - x_1) * gray_img[x_2, y_2]

    to_ret = i_y_1 + (y-y_1) * i_y_2

    return to_ret

def scale_bl_interpol(gray_img: np.ndarray, sx=768, sy=768) -> np.ndarray:
    """Scales an image using bilinear interpolation."""
    sx, sy = round(sx), round(sy)
    scaled_img = np.zeros_like(gray_img, shape=(sx, sy))

    scaleX = sx / gray_img.shape[0]
    scaleY = sy / gray_img.shape[1]

    for y in range(1, sy):
        for x in range(1, sx):
            xSrc = x / scaleX
            ySrc = y / scaleY
            scaled_img[x,y] = bl_interpol(gray_img, xSrc, ySrc)
    
    return scaled_img
 
"""3. Schreiben Sie eine Funktion, die ein Bild um sein Zentrum dreht. Dabei soll wahlweise
eine der Interpolations-Methoden (s. o.) genutzt werden."""

"""4. Suchen Sie sich ein geeignetes Testbild und stellen die Ergebnisse dar. Drehen Sie das
Bild mehrfach um den gleichen Winkel hin und her. Dokumentieren Sie Ihre Ergebnisse
und diskutieren Sie die Beobachtungen."""

if __name__ == "__main__":
    # Aufgabe 1
    """ bv1.showImage(scale_nn_interpol_forw(img_gray, 768.3, 768.3), "aufg1-nn-forw")
    bv1.showImage(scale_nn_interpol_backw(img_gray, 767.9, 768.8), "aufg1-nn-backw") """

    # Aufgabe 2
    bv1.showImage(scale_bl_interpol(img_gray, 768.3, 768.3), "aufg2-bl-forw")