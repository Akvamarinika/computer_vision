from skimage import draw
import numpy as np
from matplotlib import pyplot as plt
from skimage.measure import label, regionprops


def lakes_and_bays(image):
    b = ~image
    lb = label(b)
    regs = regionprops(lb)
    count_lakes = 0
    count_bays = 0
    for reg in regs:
        on_bound = False
        for y, x in reg.coords:
            if y == 0 or x == 0 or y == image.shape[0] - 1 or x == image.shape[1] - 1:
                on_bound = True
                break

        if not on_bound:
            count_lakes += 1
        else:
            count_bays += 1

    return count_lakes, count_bays


def has_vline(region):  # vertical line
    lines = np.sum(region.image, 0) // region.image.shape[0]  # count ones == h
    return 1 in lines


def filling_factor(region):
    return np.sum(region.image) / region.image.size


def equals_bays_area(region):
    lake = region.filled_image ^ region.image
    bays = label(~region.image ^ lake)
    areas_bays = []
    for i in range(1, np.max(bays) + 1):
        area = np.sum(bays == i)
        areas_bays.append(area)

    areas_bays = np.array(areas_bays)
    return np.all(areas_bays == areas_bays[0])

# cb == count bays
def recognize(region):
    if np.all(region.image):
        return "-"
    cl, cb = lakes_and_bays(region.image)
    if cl == 2:
        if has_vline(region):
            return "B"
        else:
            return "8"

    if cl == 1:
        if cb == 3:
            return "A"
        else:
            if cb == 2 and equals_bays_area(region):
                return "D"
            elif cb == 2:
                return "P"
            else:
                return "0"

    if cl == 0:
        if has_vline(region):
            return "1"
        if cb == 2:
            return "/"
        _, cut_cb = lakes_and_bays(region.image[2: -2, 2: -2])  # cutting region
        if cut_cb == 4:
            return "X"
        if cut_cb == 5:
            cy = region.image.shape[0] // 2
            cx = region.image.shape[1] // 2
            if region.image[cy, cx] > 0:  # full centre pixel == *
                return "*"
            return "W"
    return None


if __name__ == '__main__':
    image = plt.imread("symbols.png")
    binary = np.sum(image, 2)
    binary[binary > 0] = 1

    labeled = label(binary)
    print(f" counts obj: {np.max(labeled)}")
    print(image.shape)
    regions = regionprops(labeled)

    d = {None: 0}
    for region in regions:
        symbol = recognize(region)
        if symbol is not None:
            labeled[np.where(labeled == region.label)] = 0

        if symbol not in d:
            d[symbol] = 1
        else:
            d[symbol] += 1

    print(d)

    print("recognized: ", round((1. - d[None] / sum(d.values())) * 100, 2), "%")
    plt.imshow(labeled, cmap="gray")
    plt.show()

# {None: 0, 'D': 31, 'X': 23, '/': 35, '*': 39, '1': 42, 'A': 35, 'P': 37, 'B': 61, '-': 31, 'W': 26, '0': 30, '8': 10}
