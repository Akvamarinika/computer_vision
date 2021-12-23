import cv2
import numpy as np
from skimage.exposure import adjust_gamma, equalize_adapthist

if __name__ == '__main__':
    VIDEO_DEVICE_ID = 0

    BLUR_SIZE_FILTER = (0, 0)
    BLUR_STD = 5

    POINT_WEIGHT = 1

    MS_WAIT_KEY = 3

    camera = cv2.VideoCapture(VIDEO_DEVICE_ID)

    text = cv2.imread('text.png')
    # text = cv2.flip(text, 1)

    while camera.isOpened():
        completion_code, image = camera.read()
        blur = cv2.GaussianBlur(image, BLUR_SIZE_FILTER, BLUR_STD)
        # gamma_correction = adjust_gamma(blur, gamma=2.0)

        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(gray, connectivity=4)
        sizes = stats[1:, -1]
        nb_components = nb_components - 1
        min_size = 70000
        thresh = np.zeros((output.shape))

        for i in range(0, nb_components):
            if sizes[i] >= min_size:
                thresh[output == i + 1] = 255

        ret, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
        # struct = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
        # thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, struct)

        thresh = cv2.dilate(thresh, None, iterations=3)

        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros(image.shape[:2], dtype=np.uint8)

        for i, cnt in enumerate(contours):
            if hierarchy[0][i][2] == -1:
                if cv2.contourArea(cnt) > 30000:
                    epsilon = 0.03 * cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, epsilon, True)

                    cv2.drawContours(image, [approx], 0, (120, 120, 120), 3)

                    points = []
                    for p in approx:
                        print(*p)
                        cv2.circle(image, tuple(*p), 6, (0, 255, 0), 3)
                        points.append(*p)

                        if len(points) == 3:
                            rows, cols, _ = image.shape
                            pts2 = np.float32([[0, 0], [0, rows], [cols, 0]])
                            pts1 = np.float32(points)

                            matrix = cv2.getAffineTransform(pts2, pts1)
                            dst = cv2.warpAffine(text, matrix, (cols, rows))
                            image = cv2.addWeighted(dst, 0.3, image, 0.8, 1)

                            break

        cv2.imshow("Camera", image)
        key = cv2.waitKey(MS_WAIT_KEY)

        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
