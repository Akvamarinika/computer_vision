from enum_colors import Color
from skimage import color
import numpy as np
from matplotlib import pyplot as plt
from skimage.measure import regionprops, label


def count_figures_by_colors(masked_img, coords):
    pixels_color = []
    hue = masked_img[:, :, 0]

    for coord in coords:
        pixels_color.append(hue[coord[0], coord[1]])

    hsv_colors = np.sort(np.array(pixels_color))

    main_colors = {}

    for hsv_color in hsv_colors:
        r_color = round(hsv_color, 4)
        name_color = Color.det_color(r_color)
        if name_color in main_colors:
            main_colors[name_color] += 1
        else:
            main_colors[name_color] = 1

    return main_colors


def masking_image_with_binary_mask(binary_mask, hsv_image):
    mask_HSV = np.stack((binary_mask, binary_mask, binary_mask), axis=2)
    masked_image_hsv = np.where(mask_HSV == 1, hsv_image, mask_HSV)
    return masked_image_hsv


def get_coord_center(region):
    center_y = region.coords.shape[0] // 2
    return region.coords[center_y]


def create_binary_masks(img):
    binary_img = np.sum(np.copy(img), 2)
    binary_img[binary_img > 0] = 1

    labeled_img = label(binary_img).astype(dtype='int32')
    print('objects: ', np.max(labeled_img))

    rectangle_filter = []
    circle_filter = []

    rect_coords = []
    cir_coords = []

    regions = regionprops(labeled_img, cache=False)
    for region in regions:
        # circularity = (4 * math.pi * region.area) / (region.perimeter * region.perimeter)
        if np.all(region.image):
            rectangle_filter.append(region.label)
            center = get_coord_center(region)
            rect_coords.append(center)
        else:
            circle_filter.append(region.label)
            center = get_coord_center(region)
            cir_coords.append(center)

    rectangle_filter = np.array(rectangle_filter)

    rect_mask = np.isin(labeled_img, rectangle_filter)
    print('rectangles: ', len(rectangle_filter))

    cir_mask = np.isin(labeled_img, circle_filter)
    print('circles: ', len(circle_filter))

    return rect_mask, cir_mask, rect_coords, cir_coords


if __name__ == '__main__':
    image = plt.imread("balls_and_rects.png")
    rectangle_mask, circle_mask, rectangle_coords, circle_coords = create_binary_masks(image)

    hsv_img = color.rgb2hsv(image)

    masked_circle_hsv = masking_image_with_binary_mask(circle_mask, hsv_img)
    masked_rectangle_hsv = masking_image_with_binary_mask(rectangle_mask, hsv_img)

    circle_colors = count_figures_by_colors(masked_circle_hsv, np.array(circle_coords))
    print('\ncircles: ', circle_colors)

    rectangle_colors = count_figures_by_colors(masked_rectangle_hsv, np.array(rectangle_coords))
    print('\nrectangles: ', rectangle_colors)

    plt.figure()
    plt.subplot(121)
    plt.imshow(masked_circle_hsv, cmap='hsv', vmin=0, vmax=1)
    plt.subplot(122)
    plt.imshow(masked_rectangle_hsv, cmap='hsv', vmin=0, vmax=1)
    plt.show()
