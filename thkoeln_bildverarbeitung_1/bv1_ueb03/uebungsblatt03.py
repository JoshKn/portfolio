import cv2
import numpy as np
from matplotlib import pyplot as plt

def showImage(img: np.ndarray, window_name="image"):
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def writeImage(img: np.ndarray, name: str) -> None:
    cv2.imwrite(f"./bv1_uebungsblatt03/output/{name}.jpg", img)

img = cv2.imread("./resources/Set01.jpg", cv2.IMREAD_GRAYSCALE)
img_orig = cv2.imread("./resources/Set01.jpg")
set3 = cv2.imread("./resources/Set03.jpg", cv2.IMREAD_GRAYSCALE)
lenna = cv2.imread("./resources/lenna.png", cv2.IMREAD_GRAYSCALE)
writing = cv2.imread("./resources/writing.jpg", cv2.IMREAD_GRAYSCALE)

""" 1.  Implementieren Sie selbst das Otsu-Verfahren (naive oder effiziente Implementierung,
das dürfen Sie entscheiden) und testen, dass es für die Binarisierung von Grauwertbildern
korrekte Ergebnisse liefert. Vergleichen Sie Ihre Ergebnisse mit denen der OpenCv-
Implementierung (cv.threshold(img, ..., cv.THRESH_BINARY+cv.THRESH_OTSU)) """
def getBitDepth(gray_image: np.ndarray) -> int:
    if gray_image.dtype == "uint8":
        return 256
    elif gray_image == "uint16":
        return 65536
    
def getHist(gray_image: np.ndarray) -> np.ndarray:
    bits = getBitDepth(gray_image)
    return cv2.calcHist([gray_image], [0], None, [bits], [0,bits])

def otsuEfficient(gray_image: np.ndarray) -> int:
    hist = getHist(img)

    thresh = -1
    var_max = -1
    c_0 = 0
    sum = 0
    total_sum = np.dot(np.arange(len(hist)), hist)

    for i in range(0, len(hist)):
        c_0 += hist[i]
        c_1 = gray_image.size - c_0
        sum += i*hist[i]
        mean_0 = sum / c_0
        mean_1 = (total_sum - sum) / c_1
        var_between = c_0 * c_1 * (mean_0 - mean_1)**2

        if var_max < var_between:
            var_max = var_between
            thresh = i

    return thresh


""" 2. Recherchieren Sie zur Variante cv.ADAPTIVE_THRESH_GAUSSIAN_C aus OpenCv und
probieren, ob Sie damit noch bessere Ergebnisse erzielen können. """
def gaussianOtsu(gray_image: np.ndarray):
    # using ADAPTIVE_THRESH_GAUSSIAN_C + THRESH_OTSU in cv2.threshold returned an inverted image
    # to save myself from inverting it back I used code from https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
    blur = cv2.GaussianBlur(gray_image, (5,5), 0)
    return cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


""" 3. Finden Sie ein Testbild, in dem nach Binarisierung noch deutliches Rauschen zu erkennen
ist. Nutzen Sie die Funktionen cv2.erode und / oder cv2.dilate, um das Rauschen so
gut wie möglich zu entfernen, ohne die übrigen Ergebnisse zu sehr zu verändern. """
def erodeDilate(image: np.ndarray, kernel_size=2):
    thresh, image = cv2.threshold(image, 0, getBitDepth(image) - 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    eroded = cv2.erode(image, kernel)
    dilated = cv2.dilate(eroded, kernel)

    return image, dilated

""" 4. Kombinieren Sie das Farbbild, mit dem Sie angefangen haben, und das Ergebnis Binär-
Bild folgendermaßen: Zeigen Sie im Eingabebild nur noch die Pixel an, die im Binärbild
auf 1 gesetzt wurden und machen alle anderen schwarz. Das Binärbild wird also als
Maske verwendet, das Pixel individuell ein- oder ausblendet. """
def diffInImage(original: np.ndarray, binary: np.ndarray) -> np.ndarray:
    # if binary pixel == 0 -> set original pixel == 0
    
    binary_3channel = cv2.merge([binary, binary, binary])
    return cv2.bitwise_and(original, binary_3channel)

if __name__ == "__main__":
    # Aufgabe 1
    """ otsu = otsuEfficient(img)
    print(f"Otsu: {otsu}")
    (T, thresh) = cv2.threshold(img, otsu, 255, cv2.THRESH_BINARY)
    showImage(thresh, "own Otsu")
    
    otsu_threshold, image_result = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,)
    print(f"CV2: {otsu_threshold}")
    showImage(image_result, "cv2 Otsu") """

    # Aufgabe 2
    """ threshhold, gauss_otsu = gaussianOtsu(img)
    print(f"Threshhold of Otsu with Gaussian Blur: {threshhold}")
    showImage(gauss_otsu) """
    
    # Aufgabe 3
    """ otsu, dilated_otsu = erodeDilate(set3)
    showImage(otsu, "set03-otsu-orig")
    showImage(dilated_otsu, "set03-otsu-dilated") """

    # Aufgabe 4
    """ #_thresh , binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,)
    _thresh , binary = gaussianOtsu(img)
    diff_img = diffInImage(img_orig, binary)
    writeImage(diff_img, "aufg04-diff-img-gaussOtsu") """