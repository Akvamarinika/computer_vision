from skimage import color, exposure, morphology
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from scipy import ndimage as ndi
from skimage.measure import label, regionprops
from skimage.filters import (gaussian,
                             median,
                             threshold_yen,
                             try_all_threshold
                             )
from skimage.morphology import square
from skimage.segmentation import clear_border


def image_processing(image):
    image_gray = color.rgb2gray(image)
    image_gray = (gaussian(image_gray, sigma=1) * 255).astype("uint8")

    gamma_low = exposure.adjust_gamma(image_gray, gamma=0.1)
    gamma_low = exposure.equalize_adapthist(gamma_low)

    img_threshold = gamma_low.copy() > threshold_yen(gamma_low)
    img_bin = clear_border(morphology.dilation(~img_threshold, square(15)))
    img_with_median = median(img_bin, square(20))
    fill_contours = ndi.binary_fill_holes(img_with_median)

    LB_img, count_obj = label(fill_contours, background=0, return_num=True)

    return LB_img


if __name__ == "__main__":
    images = io.imread_collection('images/img*.jpg')

    count_pencils = 0
    img_number = 0

    for img in images:
        count_one_img = 0
        labeled_img = image_processing(img)
        img_without_artefacts = labeled_img > 0
        img_properties = regionprops(labeled_img)

        for prop in img_properties:
            if prop.area < 50000:
                img_without_artefacts[labeled_img == prop.label] = 0

            if prop.eccentricity > 0.99:
                count_pencils += 1
                count_one_img += 1

        img_number += 1
        print(f"Count pencils in img{img_number}: {count_one_img}")

        # plt.imshow(img_without_artefacts, cmap="Blues_r")
        # plt.colorbar()
        # plt.axis('off')
        # plt.show()

    print(f"Count pencils in all pictures: {count_pencils}")
