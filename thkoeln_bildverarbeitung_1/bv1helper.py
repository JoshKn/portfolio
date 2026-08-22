import cv2
import numpy as np
import time
import pickle
from matplotlib import pyplot as plt

class BV1Helper:
    runtimes = []

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

    def getGrayHist(img: np.ndarray, title="Histogram") -> None:
        plt.hist(img.ravel(), 256, [0,256])
        plt.title(title)
        plt.show()

    def comparingImages(img1_path: str, img2_path: str) -> None:
        """Displays histogram of both images to be compared."""
        img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)

        BV1Helper.showGrayHist(img1, img1_path)
        BV1Helper.showGrayHist(img2, img2_path)

    def gammaCorrect(img, gamma=2.2) -> None:
        """Corrects the gamma value of an image. Automatically displays result + histogram."""
        corr = BV1Helper.calcGammaCorrNP(img, gamma)
        BV1Helper.showImage(corr)
        BV1Helper.showGrayHist(corr)

    def getBitDepth(gray_image: np.ndarray) -> int:
        """Determine if the image's bitdepth is 8 Bit or 16 Bit. Returns number of bits."""
        if gray_image.dtype == "uint8":
            return 256
        elif gray_image == "uint16":
            return 65536
        
    def getHist(gray_image: np.ndarray) -> np.ndarray:
        """Create histogram of a grayscale image."""
        bits = BV1Helper.getBitDepth(gray_image)
        return cv2.calcHist([gray_image], [0], None, [bits], [0,bits])
    
    def otsuEfficient(gray_image: np.ndarray) -> int:
        hist = BV1Helper.getHist(gray_image)

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
    
    def gaussianOtsu(gray_image: np.ndarray, blur_size=5, thresh=127) -> tuple[int, np.ndarray]:
        blur = cv2.GaussianBlur(gray_image, (5,5), 0)
        #return cv2.adaptiveThreshold(src=blur, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C, thresholdType=cv2.THRESH_BINARY_INV, blockSize=11, C=2)
        return cv2.threshold(blur,thresh,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    def erodeDilate(image: np.ndarray, kernel_size=2) -> tuple[np.ndarray, np.ndarray]:
        _thresh, image = cv2.threshold(image, 0, BV1Helper.getBitDepth(image) - 1, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((kernel_size, kernel_size), np.uint8)

        eroded = cv2.erode(image, kernel)
        dilated = cv2.dilate(eroded, kernel)

        return image, dilated
    
    def diffInImage(original: np.ndarray, binary: np.ndarray) -> np.ndarray:
        """Calcualate difference between an image and a binary mask."""
        binary_3channel = cv2.merge([binary, binary, binary])
        return cv2.bitwise_and(original, binary_3channel)
    
    def showImage(img: np.ndarray, window_name="image", cmap=None) -> None:
        """Displays an image. Quit by pressing any key."""
        cv2.imshow(window_name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    def writeImage(img: np.ndarray, name: str) -> None:
        """Writes image as JPG to a specific path."""
        cv2.imwrite(f"./bv1_ueb07/output/{name}.jpg", img)

    def regionLabel(gray_img: np.ndarray, algorithm) -> tuple[np.ndarray, int]:
        height, width = gray_img.shape
        _thresh, binary = BV1Helper.gaussianOtsu(gray_img)
        m = 2

        for y in range(height) :
            for x in range(width):
                if binary[y,x] == 255:
                    # cv2.floodFill(image=binary, mask=None, seedPoint=(x,y), newVal=m)
                    algorithm(binary, x, y, m)
                    m += 1

        return binary, m
    
    def floodFillRecursive(img: np.ndarray, x: int, y: int, m_label: int) -> None:
        height, width = img.shape
        if y < height and x < width and img[y,x] == 255:
            img[y,x] = m_label
            BV1Helper.floodFillRecursive(img, x+1, y, m_label)
            BV1Helper.floodFillRecursive(img, x-1, y, m_label)
            BV1Helper.floodFillRecursive(img, x, y+1, m_label)
            BV1Helper.floodFillRecursive(img, x, y-1, m_label)

    def floodFillDepthSearch(img: np.ndarray, x: int, y: int, m_label: int) -> None:
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

    def floodFillBreadthSearch(img: np.ndarray, x: int, y: int, m_label: int) -> None:
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

    def floodFillRecursive(img: np.ndarray, x: int, y: int, m_label: int):
        height, width = img.shape
        if y < height and x < width and img[y,x] == 255:
            img[y,x] = m_label
            BV1Helper.floodFillRecursive(img, x+1, y, m_label)
            BV1Helper.floodFillRecursive(img, x-1, y, m_label)
            BV1Helper.floodFillRecursive(img, x, y+1, m_label)
            BV1Helper.floodFillRecursive(img, x, y-1, m_label)

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
        _thresh, binary = BV1Helper.gaussianOtsu(gray_img)
        m = 2

        for y in range(height) :
            for x in range(width):
                if binary[y,x] == 255:
                    # cv2.floodFill(image=binary, mask=None, seedPoint=(x,y), newVal=m)
                    algorithm(binary, x, y, m)
                    m += 1

        runtime = time.time() - start
        print(f"{algorithm} took {runtime} seconds to finish.")

        BV1Helper.runtimes.append(int(runtime * 1000))

        return binary, m
    
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

        reps = [int(np.mean(b)) if len(b) > 0 else 0 for b in bins]
        reps = np.array(reps)

        sorted_indices = np.argsort(reps)
        reps_sorted = reps[sorted_indices]
        thresholds = [(reps_sorted[i] + reps_sorted[i+1]) / 2 for i in range(len(reps_sorted)-1)]

        quantized = np.digitize(gray_img, bins=thresholds)
        lookup = {i: reps_sorted[i] for i in range(len(reps_sorted))}
        out_img = np.vectorize(lookup.get)(quantized).astype(np.uint8)

        return out_img

    def detectColor_kMeans(color_img: np.ndarray, k=4, target_hue=60, hue_tolerance=10) -> np.ndarray:
        hsv_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)

        pixel_values = hsv_img.reshape((-1, 3))
        pixel_values = np.float32(pixel_values)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
        _, labels, centers = cv2.kmeans(pixel_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        centers = np.uint8(centers)

        hue_values = centers[:, 0].astype(int)
        diffs = np.minimum(abs(hue_values - target_hue), 180 - abs(hue_values - target_hue))
        target_cluster = [i for i, d in enumerate(diffs) if d <= hue_tolerance]

        if not target_cluster:
            target_cluster = [int(np.argmin(diffs))]

        labels = labels.flatten()
        mask = np.zeros_like(labels, dtype=np.uint8)
        for cluster in target_cluster:
            mask[labels == cluster] = 1
        mask = mask.reshape((hsv_img.shape[0], hsv_img.shape[1]))

        rgb_mask = np.dstack([mask, mask, mask]) * 255

        return rgb_mask
    
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

        pixel_vals = img_cs.reshape((-1, 3)).astype(np.float32)

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
    
    def load_cifar(path):
        """Loads CIFAR10 dataset. Returns data, labels, filenames as tuples."""
        with open(path, 'rb') as f:
            batch = pickle.load(f, encoding='bytes')
        data = batch[b'data']          # shape (10000, 3072), dtype=uint8
        labels = batch[b'labels']      # Liste von ints
        filenames = batch[b'filenames']# Liste von byte-strings
        
        data = data.reshape(-1, 3, 32, 32) # flat → (N,3,32,32)
        data = data.transpose(0, 2, 3, 1) # (N, H, W, C) und uint8 belassen

        return data, labels, filenames
    
    def mosaic(color_img: np.ndarray, block_size=10, mosaic_tiles=None) -> np.ndarray:
        """Creates a mosaic image of color_img using mosaic_tiles to replace blocks in color_img. Takes super long tho."""
        # https://medium.com/@aarongrove/creating-image-mosaics-with-python-8e4c25dd9bf9
        start = time.time()

        if mosaic_tiles == None:
            mosaic_tiles, _, _ = BV1Helper.load_cifar("./resources/cifar-10-batches-py/data_batch_1")

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
    
    def sigmoid(k, min, max):
        """Creates a sigmoid function (s-curve) as an uint8 array.
        k: steepness of the curve, min: min value of image, max: max value of image"""
        x = np.arange(256, dtype=np.float32) / 255.0
        y = 1.0 / (1.0 + np.exp(-k * (x - 0.5))) # sigmoid funktion
        y = np.clip((y - y.min()) / (y.max() - y.min()) * 255, min, max)

        return y.astype(np.uint8) 

    def sigmoid_contrast(img: np.ndarray, k=4, min=0, max=255) -> np.ndarray:
        """Alters contrast of the image using a sigmoid function (s-curve).
        k: steepness of the curve, min: min value of image, max: max value of image"""
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
    
        lut = BV1Helper.sigmoid(k, min, max)
        l_lut = cv2.LUT(l, lut)
    
        lab = cv2.merge((l_lut, a, b))
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    def increase_saturation(img: np.ndarray, increase_percentage: float = 1.2) -> np.ndarray:
        """Increases saturation of an image by a given factor."""
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[...,1] = hsv[...,1] * increase_percentage
        
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)