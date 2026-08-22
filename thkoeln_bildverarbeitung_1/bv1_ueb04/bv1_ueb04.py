import cv2
import numpy as np
import time
from matplotlib import pyplot as plt
import sys
from bv1helper import BV1Helper as bv1
import math

sys.setrecursionlimit(10**7)
runtimes = []

img = cv2.imread("./resources/Set01.jpg", cv2.IMREAD_GRAYSCALE)
lenna = cv2.imread("./resources/lenna.png", cv2.IMREAD_GRAYSCALE)
coins = cv2.imread("./resources/coins-on-black-01-rect.jpg")
coins_gray = cv2.cvtColor(coins, cv2.COLOR_RGB2GRAY)

""" 1. Implementieren Sie den Segmentierungs-Algorithmus regionLabel in allen drei vorgestellten Varianten. 
Wenden Sie diese auf einem binarisierten Testbild an. Visualisieren Sie (Zwischen-)Ergebnisse und
vergleichen Sie die Laufzeiten der drei Varianten """

def floodFillRecursive(img: np.ndarray, x: int, y: int, m_label: int):
    height, width = img.shape
    if y < height and x < width and img[y,x] == 255:
        img[y,x] = m_label
        floodFillRecursive(img, x+1, y, m_label)
        floodFillRecursive(img, x-1, y, m_label)
        floodFillRecursive(img, x, y+1, m_label)
        floodFillRecursive(img, x, y-1, m_label)

def floodFillDepthSearch(img: np.ndarray, x: int, y: int, m_label: int):
    stack = []
    stack.append((x,y))
    height, width = img.shape

    while len(stack) > 0:
        (x,y) = stack.pop()
        if y < height and y > 0 and x > 0 and x < width and img[y,x] == 255:
            img[y,x] = m_label
            stack.append((x+1, y))
            stack.append((x-1, y))
            stack.append((x, y+1))
            stack.append((x, y-1))

def floodFillBreadthSearch(img: np.ndarray, x: int, y: int, m_label: int):
    q = []
    q.append((x,y))
    height, width = img.shape

    while len(q) > 0:
        (x,y) = q.pop(0)
        if y < height and x < width and img[y,x] == 255:
            img[y,x] = m_label
            q.append((x+1, y))
            q.append((x-1, y))
            q.append((x, y+1))
            q.append((x, y-1))

def regionLabel(gray_img: np.ndarray, algorithm):
    start = time.time()

    height, width = gray_img.shape
    _thresh, binary = bv1.gaussianOtsu(gray_img)
    m = 2

    for y in range(height) :
        for x in range(width):
            if binary[y,x] == 255:
                # cv2.floodFill(image=binary, mask=None, seedPoint=(x,y), newVal=m)
                algorithm(binary, x, y, m)
                m += 1

    runtime = time.time() - start
    print(f"{algorithm} took {runtime} seconds to finish.")

    runtimes.append(int(runtime * 1000))

    return binary, m

""" 2. Nutzen Sie die Funktion cv2.findContours, um Objekte in einem Bild zu finden 
(z. B. glänzende Münzen sowie andere helle Gegenstände auf einem dunklen Hintergrund).
Berechnen Sie die Rundheit gefundener Objekte, dafür dürfen Sie auch auf Funktionen von OpenCV zurückgreifen """
def calcCircularity(orig_img: np.ndarray, contours: np.ndarray):
    output = orig_img.copy()

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 50:              # kleines Rauschen ausfiltern
            continue

        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue

        circularity = 4 * math.pi * (area / (perimeter * perimeter))

        # Auswahl ausschließlich runder Objekte (z.B. circularity > 0.75)
        if circularity > 0.75:
            # Umrandung und Zentrum zeichnen
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            center = (int(x), int(y))
            radius = int(radius)
            cv2.circle(output, center, radius, (0, 255, 0), 2)
            cv2.putText(output,
                        f"{circularity:.2f}",
                        (center[0]-20, center[1]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        
    return output


""" 3. Berechnen Sie für gefundene Objekte auch Hu-Momente (in OpenCV verfügbar). 
Können Sie Szenen konstruieren, in denen Sie mithilfe einer einfachen Logik basierend auf den
Hu-Momenten bestimmte Objekte in Bildern erkennen können? Auch wenn diese im Bild ganz unterschiedlich erscheinen? """

if __name__ == "__main__":
    # Aufgabe 1
    """ # Flood Fill Rekursiv
    algorithms = ["Rekursiv", "Tiefensuche", "Breitensuche"]
    runtimes = []

    labeled_img, count_areas = regionLabel(img, floodFillRecursive)
    #BV1Helper.showImage(labeled_img, "Rekursiv")
    print(f"There are {count_areas} areas in the labelled image. \n")
    
    # Flood Fill Tiefensuche
    labeled_img, count_areas_depth = regionLabel(img, floodFillDepthSearch)
    #BV1Helper.showImage(labeled_img, "Tiefensuche")
    print(f"There are {count_areas_depth} areas in the labelled image. \n")
    
    # Flood Fill Breitensuche
    labeled_img, count_areas_breadth = regionLabel(img, floodFillBreadthSearch)
    #BV1Helper.showImage(labeled_img, "Breitensuche")
    print(f"There are {count_areas_breadth} areas in the labelled image. \n")

    plt.bar(algorithms, runtimes)
    plt.ylabel("Laufzeit [ms]")
    plt.title("Laufzeiten Segementierungs-Algorithmen")
    plt.show() """

    # Aufgabe 2
    """ _th, coins_binary = bv1.gaussianOtsu(coins_gray, blur_size=8)

    contours, hierarchy = cv2.findContours(coins_binary, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(coins, contours, -1, (0, 255, 0), 2, cv2.LINE_AA)

    bv1.showImage(coins_binary, "aufg02-coins-binary")
    bv1.showImage(coins, "aufg02-coins-contours")
    bv1.showImage(calcCircularity(coins, contours), "aufg02-coins-circularity") """

    # Aufgabe 3