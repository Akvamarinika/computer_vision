import numpy as np
import matplotlib.pyplot as plt


def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1


def linear_gradient_based_on_existing(your_image):
    size_img = your_image.shape[0]
    image_empty = np.zeros((size_img, size_img, 3), dtype="uint8")
    main_colors = np.diagonal(your_image, axis1=1, axis2=2, offset=0)

    for idx in range(image_empty.shape[0]):
        up_color = np.repeat(main_colors, 2, axis=0)[:size_img:]
        image_empty[np.arange(idx + 1), np.arange(idx, -1, -1), :] = up_color[idx]  # над основной диагональю

        down_color = np.repeat(main_colors, 2, axis=0)[size_img::]
        image_empty[np.arange(size_img - 1, idx, -1), np.arange(idx + 1, size_img)] = down_color[idx]  # под основной диагональю

    return image_empty


def another_beautiful_linear_gradient(your_image):
    size_img = your_image.shape[0]
    image_empty = np.zeros((size_img, size_img, 3), dtype="uint8")
    main_colors = np.diagonal(your_image, axis1=1, axis2=2, offset=0)

    for idx in range(image_empty.shape[0]):
        image_empty[np.arange(size_img - idx), np.arange(size_img - idx) + idx, :] = main_colors[idx]  # над основной диагональю
        image_empty[np.arange(size_img - idx) + idx, np.arange(size_img - idx), :] = main_colors[idx]  # под основной диагональю

    return image_empty


if __name__ == '__main__':
    size = 300
    image = np.zeros((size, size, 3), dtype="uint8")
    assert image.shape[0] == image.shape[1]

    color1 = [255, 0, 0]
    color2 = [0, 0, 255]

    for y, val in enumerate(np.linspace(0, 1, image.shape[0])):
        r = lerp(color1[0], color2[0], val)
        g = lerp(color1[1], color2[1], val)
        b = lerp(color1[2], color2[2], val)

        image[y:, :, :] = [r, g, b]

    linear_gradient_image = linear_gradient_based_on_existing(image)
    other_gradient_image = another_beautiful_linear_gradient(image)
    plt.figure(figsize=(10, 10), dpi=80)
    plt.figure(1)
    plt.subplot(321,  title="example gradient")
    plt.imshow(image, interpolation='none')
    plt.subplot(324, title="linear gradient")
    plt.imshow(linear_gradient_image, interpolation='none')
    plt.subplot(325, title="other gradient")
    plt.imshow(other_gradient_image, interpolation='none')
    plt.show()

