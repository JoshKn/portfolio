import cv2
import numpy as np

# 1. Schreiben Sie Code, der "Hello World!" ausgibt
print("Hello World!")

# 2. Schreiben Sie eine Schleife, die die Zahlen von 1 bis 100 ausgibt
for i in range(100):
    print(i + 1)

# 3. Schreiben Sie Code, der die ersten n Primzahlen ausgibt. 
# Verwenden Sie dabei eine eigene Funktion, um zu prüfen, ob eine Zahl prim ist
def isPrime(number: int) -> bool:
    for i in range(2, number):
        if number % i != 0:
            pass
        else:
            return False
    return True

def returnNPrimes(n: int):
    primes = []
    i = 1

    while True:
        if isPrime(i):
            primes.append(i)
            if len(primes) == n:
                return primes
            i += 1
        else:
            i += 1

print(returnNPrimes(6))

# 4. Lesen Sie eine Bild I mit OpenCV ein und zeigen es an
imgPath = "./resources/Set01.jpg"

def showImage(img: np.ndarray, window_name="image"):
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread(imgPath)
showImage(img)

# 5. Speichern Sie das Bild in einem komprimierten, verlustbehafteten Format
output_dir = "./bv1_uebungsblatt01/"
output_file_name = "output.jpg"

cv2.imwrite(output_dir + output_file_name, img, [cv2.IMWRITE_JPEG_QUALITY, 20])
# cv2.imwrite(output_dir + "outpug.png", img) # no difference

# 6. Laden Sie das im letzten Schritt gespeicherte Bild Il wieder ein
img_l = cv2.imread(output_dir + output_file_name)

# 7. Nutzen Sie eine geeignete Punktoperation, um Unterschiede zwischen I und Il zu ermitteln und darzustellen
def findDifferencesInImage(img1: np.ndarray, img2: np.ndarray):
    if img1.shape != img2.shape:
        return "Error: Images bust be same size."
    
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    
    height, width, depth = gray1.shape

    diff_img = np.zeros((height, width, 1), dtype= "uint8")

    for y in range(0, height):
        for x in range(0, width):
            diff = abs(gray1[y,x,0] - gray2[y,x,0])
            diff_img[y, x] += diff

    cv2.imwrite(f"{output_dir}diff_img.jpg", diff_img)
    showImage(diff_img)

findDifferencesInImage(img, img_l)
