import math
import numpy as np


def nominal_resolution(file_name):
    with open(file_name, 'r') as file:
        max_size_in_mm = file.readline()
        arr = np.loadtxt(file.readlines(), comments='#', ndmin=2)
        count_px = 0

        for y in range(arr.shape[0]):
            for x in range(arr.shape[1]):
                if x == 1:
                    count_px += 1

        print(file_name, "nominal resolution: ", float(max_size_in_mm) / count_px)


def calculate_offset_along_one_axis(array1, array2):
    offset = 0

    for y_idx in range(array1.shape[0]):
        for x_idx in range(array1.shape[1]):
            if array1[y_idx][x_idx] != array2[y_idx][x_idx]:
                offset += 1
        if offset > 0:
            return offset

    return offset


def calc_coord_offset(arr):
    # test = []

    for y_idx in range(1, arr.shape[0] - 1):
        for x_idx in range(1, arr.shape[1] - 1):
            if arr[y_idx][x_idx] == 1 and arr[y_idx - 1][x_idx - 1] == 0:
                return y_idx, x_idx
                # test.append([y_idx, x_idx])
            if arr[y_idx][x_idx] == 1 and arr[y_idx + 1][x_idx + 1] == 0:
                return y_idx, x_idx

    return 0, 0


def images_offset(file_img1, file_img2, ):
    arr1 = np.loadtxt(file_img1, comments='#', ndmin=2, skiprows=2)
    arr2 = np.loadtxt(file_img2, comments='#', ndmin=2, skiprows=2)

    coord_img1 = calc_coord_offset(arr1)
    coord_img2 = calc_coord_offset(arr2)

    y_offset = math.fabs(coord_img2[0] - coord_img1[0])
    x_offset = math.fabs(coord_img2[1] - coord_img1[1])

    print("y_offset: ", y_offset)
    print("x_offset: ", x_offset)


if __name__ == '__main__':
    nominal_resolution("resources/figure1.txt")
    nominal_resolution("resources/figure2.txt")
    nominal_resolution("resources/figure3.txt")
    nominal_resolution("resources/figure4.txt")
    nominal_resolution("resources/figure5.txt")
    nominal_resolution("resources/figure6.txt")
    nominal_resolution("resources/img1.txt")
    nominal_resolution("resources/img2.txt")

    images_offset("resources/img1.txt", "resources/img2.txt")
