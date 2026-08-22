import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from bv1helper import BV1Helper as bv1

img = cv2.imread("./resources/Set01.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

foto_imp = cv2.imread("./resources/imp-foto.jpg")

""" 1. Nutzen Sie die OpenCV -Funktion cv.Canny, um für ein eigenes Testbild Konturen zu
berechnen. Stellen Sie die Parameter der Funktion so ein, dass die Ergebnisse für weitere
Verarbeitungsschritte nützlich sein könnten. """
t_lower = 100
t_upper = 254

edge = cv2.Canny(img, threshold1=t_lower, threshold2=t_upper)
#edge_gray = cv2.Canny(img_gray, threshold1=t_lower, threshold2=t_upper)

#bv1.showImage(edge, "aufg1-canny-color-img")
#bv1.showImage(edge_gray, "Canny from gray Image")


""" 2. Implementieren Sie selbst den Median cut-Algorithmus, um damit ein 8-Bit-Grauwertbild
mit geringerer Bit-Tiefe darstellen zu können. """
def medianCut(gray_img: np.ndarray, num_levels: int) -> np.ndarray:
    pixels = gray_img.flatten()
    sorted_vals = np.sort(pixels)

    def split(values, levels):
        if levels == 1:
            return [values]
        median_idx = len(values) // 2
        v1 = values[:median_idx]
        v2 = values[median_idx:]
        return split(v1, levels // 2) + split(v2, levels // 2)

    bins = split(sorted_vals, num_levels)

    reps = [int(np.median(b)) if len(b) > 0 else 0 for b in bins]
    reps = np.array(reps)

    sorted_indices = np.argsort(reps)
    reps_sorted = reps[sorted_indices]
    thresholds = [(reps_sorted[i] + reps_sorted[i+1]) / 2 for i in range(len(reps_sorted)-1)]

    quantized = np.digitize(gray_img, bins=thresholds)
    lookup = {i: reps_sorted[i] for i in range(len(reps_sorted))}
    out_img = np.vectorize(lookup.get)(quantized).astype(np.uint8)

    return out_img


""" 3. Konvertieren Sie ein Farbbild mithilfe von OpenCV von RGB nach HSV. Implementieren
Sie eine einfache Regel (z. B. Intervalle in H, S und V), um eine bestimmte Farbe zu
erkennen. Erzeugen Sie ein Binärbild, in dem genau die Pixel gesetzt sind, die die
entsprechenden Kriterien erfüllen. Ein mögliches Testbild (IMP_Foto, s. u.) haben wir
Ihnen in ILU zur Verfügung gestellt. """

def extract_color_cluster(img: np.ndarray,
                          target_cluster: int,
                          k: int = 3,
                          sat_thresh: float = 0.25,
                          criteria: tuple = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2),
                          attempts: int = 10,
                          flags: int = cv2.KMEANS_PP_CENTERS) -> np.ndarray:

    # in HSV konvertieren und normalisieren
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] /= 255.0

    # Maske für ausreichend gesättigte Pixel
    sat_mask = hsv[..., 1] >= sat_thresh

    # Liste der Punkte für k-Means verwenden
    h_vals = hsv[..., 0][sat_mask]
    s_vals = hsv[..., 1][sat_mask]
    v_vals = hsv[..., 2][sat_mask] / 255.0
    samples = np.stack([h_vals, s_vals, v_vals], axis=-1)
    if samples.size == 0:
        raise ValueError("Keine Pixel mit Sättigung >= sat_thresh gefunden.")

    # k-Means
    samples32 = samples.astype(np.float32)
    compactness, labels, centers = cv2.kmeans(
        samples32,
        k,
        None,
        criteria,
        attempts,
        flags
    )

    # Erstelle ein Label-Bild mit -1 für ausgeschlossene Pixel
    label_img = -1 * np.ones(hsv.shape[:2], dtype=np.int32)
    label_img[sat_mask] = labels.flatten()

    # Ergebnisbild: weiß für target_cluster, sonst schwarz
    result = np.zeros_like(label_img, dtype=np.uint8)
    result[label_img == target_cluster] = 255

    return result



""" 4. Stellen Sie ein Farbbild mit sehr wenigen Farben dar. Um eine geeignete Palette zu
erzeugen, dürfen Sie Funktionen wie beispielsweise cv.kmeans aus OpenCV nutzen. Sie
können für das Berechnen der Palette mit unterschiedlichen Farbräumen experimentieren. """

def quantizeImage_kmeans(color_img, k_colors=8, color_space='HSV', attempts=10, criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)):
    cs = color_space.upper()
    if cs == 'HSV':
        img_cs = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)
    elif cs == 'YUV':
        img_cs = cv2.cvtColor(color_img, cv2.COLOR_BGR2YUV)
    elif cs == 'LAB':
        img_cs = cv2.cvtColor(color_img, cv2.COLOR_BGR2Lab)
    elif cs == 'XYZ':
        img_cs = cv2.cvtColor(color_img, cv2.COLOR_BGR2XYZ)
    else:
        raise ValueError(f"Unbekannter Farbraum: {color_space}")

    pixel_vals = img_cs.reshape((-1, 3)).astype(np.float32) # in farbkanäle aufsplitten

    _, labels, centers = cv2.kmeans(
        pixel_vals,
        k_colors,
        None,
        criteria,
        attempts,
        cv2.KMEANS_PP_CENTERS
    )
    centers = centers.astype(np.uint8)

    quantized_vals = centers[labels.flatten()]
    quantized_cs = quantized_vals.reshape(img_cs.shape)

    if cs == 'HSV':
        quantized_bgr = cv2.cvtColor(quantized_cs, cv2.COLOR_HSV2BGR)
    elif cs == 'YUV':
        quantized_bgr = cv2.cvtColor(quantized_cs, cv2.COLOR_YUV2BGR)
    elif cs == 'LAB':
        quantized_bgr = cv2.cvtColor(quantized_cs, cv2.COLOR_Lab2BGR)
    elif cs == 'XYZ':
        quantized_bgr = cv2.cvtColor(quantized_cs, cv2.COLOR_XYZ2BGR)

    return quantized_bgr

if __name__ == "__main__":
    # Aufgabe 2
    """ bv1.showImage(img_gray, "Gray Image")
    medianCut_img = medianCut(gray_img=img_gray, num_levels=2)
    bv1.showImage(medianCut_img, "median-cut-q02")
    medianCut_img = medianCut(gray_img=img_gray, num_levels=8)
    bv1.showImage(medianCut_img, "median-cut-q08")
    medianCut_img = medianCut(gray_img=img_gray, num_levels=16)
    bv1.showImage(medianCut_img, "median-cut-q16") """

    # Aufgabe 3
    """ clustered_img = extract_color_cluster(foto_imp, target_cluster=0, k=3)
    bv1.showImage(clustered_img, "aufg03-clustered-k3") """

    # Aufgabe 4
    bv1.showImage(img, "Normal Color")

    # basic hsv testing
    q_hsv_8 = quantizeImage_kmeans(img)
    bv1.showImage(q_hsv_8, "aufg04-quant-hsv-08")
    q_hsv_16 = quantizeImage_kmeans(img, k_colors=16)
    bv1.showImage(q_hsv_16, "aufg04-quant-hsv-16")
    q_hsv_32 = quantizeImage_kmeans(img, k_colors=32)
    bv1.showImage(q_hsv_32, "aufg04-quant-hsv-32")

    # testing different color spaces
    q_lab_32 = quantizeImage_kmeans(img, color_space="lab", k_colors=32)
    bv1.showImage(q_lab_32, "aufg04-quant-lab-32")
    q_yuv_32 = quantizeImage_kmeans(img, color_space="yuv", k_colors=32)
    bv1.showImage(q_yuv_32, "aufg04-quant-yuv-32")
    """ q_xyz_32 = quantizeImage_kmeans(img, color_space="xyz", k_colors=32)
    bv1.showImage(q_xyz_32, "aufg04-quant-xyz-32") """
    
    # yuv colors looked best -> try out different k's
    """ q_yuv_32 = quantizeImage_kmeans(img, color_space="yuv", k_colors=8)
    bv1.showImage(q_yuv_32, "aufg04-quant-yuv-08")
    q_yuv_32 = quantizeImage_kmeans(img, color_space="yuv", k_colors=16)
    bv1.showImage(q_yuv_32, "aufg04-quant-yuv-16")
    q_yuv_32 = quantizeImage_kmeans(img, color_space="yuv", k_colors=32)
    bv1.showImage(q_yuv_32, "aufg04-quant-yuv-32") """