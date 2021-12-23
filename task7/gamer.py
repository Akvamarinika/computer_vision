import webbrowser
import time
import cv2
import numpy as np
import keyboard
import pyautogui
import mss


def get_screenshot(left_coeff, top_coeff, weight_coeff, height_coeff):
    left = int(monitorSizes["width"] * left_coeff)
    top = int(monitorSizes["height"] * top_coeff)
    weight = int(monitorSizes["width"] / weight_coeff)  # 12.8
    height = int(monitorSizes["height"] * height_coeff)  # 0.12

    roi = pyautogui.screenshot(region=(left, top, weight, height))
    roi_BGR = cv2.cvtColor(np.array(roi), cv2.COLOR_RGB2BGR)

    return roi_BGR


if __name__ == '__main__':
    pyautogui.PAUSE = 0.0

    sct = mss.mss()
    monitorSizes = sct.monitors[0]

    webbrowser.open('https://chromedino.com/', new=2)
    time.sleep(5)
    pyautogui.press('space')

    start_time = time.time()
    while True:
        if time.time() - start_time > 3000:
            delta = 7
            obstacle_zone = get_screenshot(0.4, 0.267, 15 - delta, 0.05)
        else:
            obstacle_zone = get_screenshot(0.4, 0.267, 14, 0.05)

        bird = get_screenshot(0.39, 0.25, 16, 0.03)

        bird = np.array(bird)
        if np.all(bird[bird.shape[0] - 1:, :] < 100):
            bird_black_pixels_count = np.sum(bird < 100)
            bird_white_pixels_count = np.sum(bird > 100)

            if 550 < bird_black_pixels_count < 850:
                pyautogui.keyDown('space')

        dark_pixels = np.sum(obstacle_zone < 100)

        print('dark ', dark_pixels)

        if 550 < dark_pixels < 30000:
            pyautogui.keyDown('space')
            time.sleep(0.01)
            pyautogui.keyUp('space')

        cv2.imshow('T-Rex',  obstacle_zone)

        if keyboard.is_pressed('q'):
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            break

