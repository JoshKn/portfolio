import cv2
import numpy as np
import time
from matplotlib import pyplot as plt

def showImage(img: np.ndarray, window_name="image"):
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

""" 
1. Schreiben Sie zwei Varianten einer Funktion, die für ein Bild und beliebigen Wert von Gamma 
eine Gamma-Korrektur berechnet und das Ergebnis zurückgibt: erst mit LUT und dann ohne LUT.   
Vergleichen Sie die Ergebnisse und die Laufzeiten der beiden Varianten.
"""

def calcGammaCorr(img: np.ndarray, gamma: float) -> np.ndarray:
    start = time.time()

    height, width, depth = img.shape
    output = np.zeros((height, width, depth), dtype= "uint8")

    for y in range(0, height):
        for x in range(0, width):
            for color in range(0, depth):
                output[y, x, color] = pow((img[y,x,color]/255), gamma) * 255

    print(f"calcGammaCorrLoop() took {time.time() - start}s to finish.")
    return output


def calcGammaCorrLUT(img: np.ndarray, gamma: float) -> np.ndarray:
    start = time.time()

    lut = [0 for i in range(256)]
    height, width, depth = img.shape
    output = np.zeros((height, width, depth), dtype= "uint8")

    for y in range(0, height):
        for x in range(0, width):
            for color in range(0, depth):
                pixel_value = img[y, x, color]
                
                if lut[pixel_value] == 0:
                    lut[pixel_value] = pow((img[y,x,color]/255), gamma) * 255 
                
                output[y, x, color] = lut[pixel_value]

    print(f"calcGammaCorrLUT() took {time.time() - start}s to finish.")
    return output

def calcGammaCorrNP(img: np.ndarray, gamma: float) -> np.ndarray:
    start = time.time()

    output = pow((img/255), gamma) * 255

    print(f"calcGammaCorr() took {time.time() - start}s to finish.")
    return output.astype("uint8")

""" 
2. Schreiben Sie Code, der das Histogramm eines gegebenen Grauwertbildes berechnet und anzeigt.
"""
def showGrayHist(img: np.ndarray, title="Histogram"):
    plt.hist(img.ravel(), 256, [0,256])
    plt.title(title)
    plt.show()

""" 
3. Untersuchen Sie die Möglichkeiten, wie mann ein Farbbild in Python in ein Grauwertbild umwandeln kann:
img_gray = cv2.imread("bild.jpg", cv2.IMREAD_GRAYSCALE) oder ohne den Grauwertparameter beim Laden und nachträglich
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) oder mit cv2.COLOR_BGR2GRAY.
Können Sie Unterschiede finden? 
"""
def imgToGray(img_path):
    img = cv2.imread(img_path)
    img_grayscale = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img_rgb2gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img_bgr2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    showImage(img_grayscale, "Grayscale")
    showImage(img_rgb2gray, "RGB")
    showImage(img_bgr2gray, "BGR")


""" 
4. Nehmen Sie mindestens zwei Testbilder auf (oder suchen Sie geeignete Bilder aus dem Internet),
die deutlich unterschiedliche Eigenschaften haben, z.B. sehr dunkel / sehr hell. schwache / starke Kontraste, usw.
Wandeln Sie Farbbilder in Grauwertbilder um. Wie bilden sich die Eigenschaften im Histogramm ab?
Wie sieht ein "optimales" Histogramm aus? 
Können Sie Ihre Gamma-Korrektur nutzen, um die Bilder dementsprechend zu verbessern?
"""
def comparingImages(img1_path: str, img2_path: str):
    img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

    showGrayHist(img1, img1_path)
    showGrayHist(img2, img2_path)

def gammaCorrect(img, gamma):
    corr = calcGammaCorrNP(img, gamma)
    showImage(corr)
    showGrayHist(corr)

if __name__ == "__main__":
    img1 = cv2.imread("./resources/Set01.jpg", cv2.IMREAD_GRAYSCALE)
    gamma = 2.2

    """ gammaCor = calcGammaCorr(img1, gamma)
    gammaCorLUT = calcGammaCorrLUT(img1, gamma)
    
    showImage(gammaCor, window_name="normal")
    showImage(gammaCorLUT, window_name="LUT") """
    
    """ showImage(img1)
    showGrayHist(img1) """

    """ imgToGray(img_path="./resources/Set01.jpg") """

    """ comparingImages("./resources/plants.jpg", "./resources/mountains.jpg") """

    """ plants = cv2.imread("./resources/plants.jpg", cv2.IMREAD_GRAYSCALE)
    mountains = cv2.imread("./resources/mountains.jpg", cv2.IMREAD_GRAYSCALE)

    gammaCorrect(plants, 0.5) """
