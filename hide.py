import numpy as np
import cv2

print('Reading...')
img = cv2.imread('daisy.png', cv2.IMREAD_UNCHANGED)
f = open("Doom.7z", "rb")
bytes = list(f.read())

print('Preparing payload...')
if len(bytes)*4 > img.size:
    raise Exception('Image dimensions are too small for payload')
payload = []
for b in bytes:
    payload += [b>>6, b>>4, b>>2, b]
payload += [0b11111111] * (img.size-len(payload)) # these filler bytes can be anything
payload = np.asarray(payload, dtype=np.uint8)
payload = np.reshape(payload, img.shape)

print('Preparing bitwise mask...')
mask = [0b00000011] * len(bytes) * 4
mask += [0b00000000] * (img.size-len(mask))
mask = np.asarray(mask, dtype=np.uint8)
mask = np.reshape(mask, img.shape)

print('Replacing least significant bits...')
res = np.bitwise_xor(img, payload)
res = np.bitwise_and(res, mask)
res = np.bitwise_xor(res, img)

print('Writing...')
cv2.imwrite('steg.png', res)

print('Done!')