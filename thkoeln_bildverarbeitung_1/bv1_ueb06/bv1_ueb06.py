import cv2
import numpy as np
import os
from matplotlib import pyplot as plt
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from bv1helper import BV1Helper as bv1

""" 1. Erzeugen Sie ein eigenes Foto-Mosaik! Als „Bausteine“ können Sie z. B. die CIFAR10-
Bildchen nutzen, siehe Vorlesungsfolien. Gehen Sie dabei darauf ein, welches Abstandsmaß 
für den betrachteten Anwendungsfall aus Ihrer Sicht am geeignetsten ist. Eine wichtige Frage 
ist auch, wie man es erreichen kann, dass jedes Bild im Mosaik nur ein einziges Mal vorkommt. 
Das müssen Sie nicht unbedingt implementieren, aber bitte skizzieren Sie mindestens ein 
mögliches Vorgehen. """
img = cv2.imread("./resources/lenna.png")

def mosaic(color_img: np.ndarray, block_size=10, mosaic_tiles=None) -> np.ndarray:
    """Creates a mosaic image of color_img using mosaic_tiles to replace blocks in color_img."""
    # https://medium.com/@aarongrove/creating-image-mosaics-with-python-8e4c25dd9bf9
    start = time.time()

    if mosaic_tiles == None:
        mosaic_tiles, _, _ = bv1.load_cifar("./resources/cifar-10-batches-py/data_batch_1")

    h, w, _ = color_img.shape
    h_blocky = h - (h % block_size)
    w_blocky = w - (w % block_size)
    img = color_img[:h_blocky, :w_blocky] # zero to h_blocky (after : is not included in selection)
    output = np.zeros_like(img)

    for y in range(0, h_blocky, block_size): # 0 to image height using steps of block_size
        for x in range(0, w_blocky, block_size):
            block = img[y:y+block_size, x:x+block_size]

            # gets mean value of each color channel in the block
            block_mean = block.reshape(-1,3).mean(axis=0) # reshapes to three columns and whatever rows it needs; mean over each column
            
            # get most similar image from mosaic_tiles
            cifar_features = mosaic_tiles.reshape(len(mosaic_tiles), -1, 3).mean(axis=1)
            dists = np.linalg.norm(cifar_features - block_mean, axis=1)
            index = np.argmin(dists)
            tile = cv2.resize(mosaic_tiles[index], (block_size, block_size), interpolation=cv2.INTER_AREA)

            output[y:y+block_size, x:x+block_size] = tile

    print(f"mosaic took {time.time() - start} seconds to run.")
    return output


""" 2. Suchen Sie sich ein geeignetes Testbild und verändern es sinnvoll, ähnlich einem „Filter“
im Sinne von Instagram o. ä. In der Vorlesung hatten wir die Beispiele „vintage“ für
beliebige Fotos, Beauty für Portraits sowie Filter für Landschaftsaufnahmen. Erzeugen
Sie ein beeindruckendes Ergebnis und erklären die Bildverarbeitungs-Schritte, die dafür
notwendig waren. """
indo = cv2.imread("./resources/indo.jpg")

def sigmoid(k, min, max):
    x = np.arange(256, dtype=np.float32) / 255.0
    y = 1.0 / (1.0 + np.exp(-k * (x - 0.5))) # sigmoid funktion 1/(1+e^(-k * (x-0.5))
    y = np.clip((y - y.min()) / (y.max() - y.min()) * 255, min, max) 

    return y.astype(np.uint8) 

def sigmoid_contrast(img: np.ndarray, k=4, min=0, max=255) -> np.ndarray:
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    lut = sigmoid(k, min, max)
    l_lut = cv2.LUT(l, lut)

    lab = cv2.merge((l_lut, a, b))
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def increase_saturation(img: np.ndarray, increase_percentage: float = 1.2) -> np.ndarray:
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[...,1] = hsv[...,1] * increase_percentage
    
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

if __name__ == "__main__":
    # Aufgabe 1
    """mosaic_img = mosaic(img, block_size=5)
    bv1.writeImage(mosaic_img, "aufg1_mosaic") """

    #Aufgabe 2
    contrasty_image = sigmoid_contrast(indo, k=6)
    sat_image = increase_saturation(indo)
    sat_contr_image = sigmoid_contrast(sat_image)

    plt.plot(sigmoid(10, 0 , 255))
    plt.show()
    bv1.showImage(indo, "orig")
    bv1.showImage(contrasty_image, "aufg2-contrast")
    bv1.showImage(sat_image, "aufg2-saturated")
    bv1.showImage(sat_contr_image, "aufg2-saturated-contrast")
