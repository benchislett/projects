import numpy as np
from PIL import Image, ImageSequence
import cv2
import time
import curses

from process_font import font_image, font_size, CHARS

VIDEO_FILE = './test.mp4'

stdscr = curses.initscr()  # initialize the screen
curses.noecho()  # hide user key input


def main():
    vid = cv2.VideoCapture(VIDEO_FILE)
    while (True):
        ret, frame = vid.read()
        if not ret:
            break
        frame_pixels = np.mean(np.asarray(frame), -1)
        ratio = frame_pixels.shape[1] / \
            frame_pixels.shape[0] * font_size[1] / font_size[0]
        x = curses.COLS
        y = curses.LINES
        if (x > y):  # maintain aspect ratio
            x = int(y * ratio)
        else:
            y = int(x * ratio)
        block_x = frame_pixels.shape[1] // x
        block_y = frame_pixels.shape[0] // y

        font_arr = np.mean(np.asarray(font_image.resize(
            (block_x * len(CHARS), block_y))), -1).astype(np.uint8)

        means = []
        for i in range(len(CHARS)):
            means.append(np.mean(font_arr[:, i * block_x:(i+1) * block_x]))
        means = list(map(lambda x: 255. * (x - min(means)) /
                         (max(means) - min(means)), means))  # normalize to [0,255]

        for i in range(x - 1):
            for j in range(y - 1):
                chunk = frame_pixels[j *
                                     block_y:(j+1)*block_y, i*block_x:(i+1)*block_x]
                #similarities = []
                # for val in means:
                #    similarities.append(abs(val - np.mean(chunk)))
                #char = CHARS[similarities.index(min(similarities))]
                char = CHARS[int(np.mean(chunk) / 255. * (len(CHARS) - 1))]
                stdscr.addstr(j, i, char)
        stdscr.refresh()


# teardown
def teardown():
    curses.echo()
    curses.endwin()


# execute
if __name__ == '__main__':
    try:
        main()
    finally:
        teardown()
