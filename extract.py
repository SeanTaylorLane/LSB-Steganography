import numpy as np
import cv2

print('Reading...')
img = cv2.imread('steg.png', cv2.IMREAD_UNCHANGED)

print('Extracting...')
img = np.bitwise_and(img, 0b00000011)
img = np.left_shift(img, np.asarray([6, 4, 2, 0], dtype=np.uint8))
img = np.bitwise_or.reduce(img, axis=2)

print('Reshaping...')
img = np.reshape(img, img.size)
img = bytearray(img)

print('Writing...')
f = open("result.7z", "wb")
f.write(img)

print('Done!')