import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import morphology
import skimage.measure


def area(LB, label=1):
    pixels_all = np.where(LB == label)  # список координат по всем осям
    return len(pixels_all[0])


def count_all_objects_with_area(src_img):
    dst_img = np.copy(src_img)
    LB_img = skimage.measure.label(dst_img)

    areas_count = {}
    for label in range(1, np.max(LB_img)):
        area_obj = area(LB_img, label)

        if area_obj in areas_count:
            areas_count[area_obj] += 1
        else:
            areas_count[area_obj] = 1
    print(areas_count)


def labels_obj_right(LB_image):
    struct_right = np.array([
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ])

    img_obj_right = morphology.binary_opening(LB_image, struct_right)
    LB_image_maskingRight = LB_image[img_obj_right]  # return одномерный массив
    labels_right = list(set(LB_image_maskingRight.copy().astype('uint')))
    print(f"All labels right: {labels_right}")
    print(f"Count objects right: {len(labels_right)} \n")
    plt.subplot(232)
    plt.imshow(img_obj_right, cmap="hot")

    return labels_right


def labels_obj_up(LB_image):
    struct_up = np.array([
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1]
    ])

    struct_full = np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1]
    ])

    mask_obj_full = morphology.binary_opening(LB_image, struct_full)
    mask_obj_up = morphology.binary_opening(LB_image, struct_up)
    img_obj_up = mask_obj_full ^ mask_obj_up
    img_obj_up = morphology.binary_opening(img_obj_up, struct_up)

    LB_image_maskingUp = LB_image[img_obj_up]
    labels_up = list(set(LB_image_maskingUp.copy().astype('uint')))
    print(f"All labels up: {labels_up}")
    print(f"Count objects up: {len(labels_up)}\n")

    plt.subplot(233)
    plt.imshow(img_obj_up, cmap="hot")

    return labels_up


def labels_obj_down(LB_image):
    struct_down = np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1, 1]
    ])

    struct_full = np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1]
    ])

    mask_obj_full = morphology.binary_opening(LB_image, struct_full)
    mask_obj_down = morphology.binary_opening(LB_image, struct_down)
    img_obj_down = mask_obj_full ^ mask_obj_down
    img_obj_down = morphology.binary_opening(img_obj_down, struct_down)

    LB_image_maskingUp = LB_image[img_obj_down]
    labels_down = list(set(LB_image_maskingUp.copy().astype('uint')))
    print(f"All labels down: {labels_down}")
    print(f"Count objects down: {len(labels_down)}\n")

    plt.subplot(234)
    plt.imshow(img_obj_down, cmap="hot")

    return labels_down


def labels_obj_left(LB_image):
    struct_left = np.array([
        [1, 1, 1, 1],
        [1, 1, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]
    ])

    img_obj_left = morphology.binary_opening(LB_image, struct_left)
    LB_image_maskingLeft = LB_image[img_obj_left]
    labels_left = list(set(LB_image_maskingLeft.copy().astype('uint')))
    print(f"All labels left: {labels_left}")
    print(f"Count objects left: {len(labels_left)}\n")

    plt.subplot(235)
    plt.imshow(img_obj_left, cmap="hot")

    return labels_left


def labels_obj_full(LB_image):
    struct_full = np.array([
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1]
    ])

    img_obj_full = morphology.binary_opening(LB_image, struct_full)
    LB_image_maskingFull = LB_image[img_obj_full]
    labels_full = list(set(np.copy(LB_image_maskingFull).astype('uint')))
    print(f"All labels full: {labels_full}")
    print(f"Count objects full: {len(labels_full)}\n")

    plt.subplot(236)
    plt.imshow(img_obj_full, cmap="hot")

    return labels_full


if __name__ == "__main__":
    image = np.load("ps.npy").astype("uint")
    plt.figure(figsize=(15, 20))
    plt.subplot(231)
    plt.imshow(image)

    LB_image = skimage.measure.label(image)
    print(f"Count objects: {np.max(LB_image)}")

    labels_all = list(set(np.copy(LB_image).ravel().astype('uint')))[1:]
    print(f"Count objects 2: {len(labels_all)}\n")

    labels_left = labels_obj_left(np.copy(LB_image))
    labels_right = labels_obj_right(np.copy(LB_image))
    labels_full = labels_obj_full(np.copy(LB_image))
    labels_up = labels_obj_up(np.copy(LB_image))
    labels_down = labels_obj_down(np.copy(LB_image))

    found_labels = np.hstack(
        (np.copy(labels_right), np.copy(labels_up), np.copy(labels_down), np.copy(labels_left), np.copy(labels_full)))
    not_found_labels = np.setdiff1d(labels_all, found_labels)
    print(f"Count NotFound labels: {len(not_found_labels)}")
    print(f"All NotFound labels: {not_found_labels}")
    print(f"Sum all objects: {len(labels_right) + len(labels_left) + len(labels_up) + len(labels_down) + len(labels_full)}")
    # count_all_objects_with_area(image)

    plt.show()
