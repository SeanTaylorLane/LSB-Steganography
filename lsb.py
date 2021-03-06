import argparse
import cv2
import math
import numpy as np

IO_HIDE = 'hide'
IO_EXTRACT = 'extract'

def main():
    parser = argparse.ArgumentParser(description='Hides and extracts payloads in PNG images using LSB steganography')
    parser.add_argument('io_type', choices=[IO_HIDE, IO_EXTRACT], help='Whether to hide or extract a payload', type=str)
    parser.add_argument('image_path', help='Path to the PNG image to hide a payload into or extract a payload from', type=str)
    parser.add_argument('payload_path', nargs='?', help='Path to the payload, only needed when hiding', type=str)
    parser.add_argument('-o', '--output_filename', help='Name of the output file. When hiding, the output file will be a PNG file. When extracting, the output file can have any file extension or type', type=str)

    cli_args = parser.parse_args()

    if not cli_args.image_path.lower().endswith('.png'):
        parser.error('Only PNG images are supported right now!')
    if cli_args.io_type == IO_HIDE:
        if cli_args.payload_path is None:
            parser.error('Need to specify a payload file')
        hide(cli_args.image_path, cli_args.payload_path, cli_args.output_filename or 'steg.png')
    elif cli_args.io_type == IO_EXTRACT:
        extract(cli_args.image_path, cli_args.output_filename or 'payload')
    else:
        parser.error('Unknown IO type')
    print('Done!')

def hide(image_path, payload_path, output_filename):
    print('Reading...')
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    f = open(payload_path, 'rb')
    payload = list(f.read())
    print('Preparing payload...')
    if len(payload)*4+4 > img.size:
        raise Exception('Image dimensions are too small for payload')
    # First 4 bytes in steg image always say how many bytes are in the payload
    payload_size = len(payload).to_bytes(4, 'little')
    payload = list(payload_size) + payload
    formatted_payload = []
    for b in payload:
        formatted_payload += [b>>6, b>>4, b>>2, b]
    formatted_payload += [0b11111111] * (img.size-len(formatted_payload)) # these filler bytes can be anything
    formatted_payload = np.asarray(formatted_payload, dtype=np.uint8)
    formatted_payload = np.reshape(formatted_payload, img.shape)
    print('Preparing bitwise mask...')
    mask = [0b00000011] * len(payload) * 4
    mask += [0b00000000] * (img.size-len(mask))
    mask = np.asarray(mask, dtype=np.uint8)
    mask = np.reshape(mask, img.shape)
    print('Replacing least significant bits...')
    res = np.bitwise_xor(img, formatted_payload)
    res = np.bitwise_and(res, mask)
    res = np.bitwise_xor(res, img)
    print('Compressing and writing...')
    if not output_filename.lower().endswith('.png'):
        output_filename += '.png'
    cv2.imwrite(output_filename, res, [cv2.IMWRITE_PNG_COMPRESSION, 9])

def extract(image_path, output_filename):
    print('Reading...')
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    print('Extracting...')
    img = np.bitwise_and(img, 0b00000011)
    img = np.left_shift(img, np.asarray([6, 4, 2, 0], dtype=np.uint8))
    img = np.bitwise_or.reduce(img, axis=2)
    print('Reshaping...')
    img = np.reshape(img, img.size)
    # First 4 bytes in steg image always say how many bytes are in the payload
    payload_size = int.from_bytes(list(img[:4]), 'little')
    payload = bytearray(img[4:payload_size+4])
    print('Writing...')
    f = open(output_filename, 'wb')
    f.write(payload)

if __name__ == '__main__':
    main()