# LSB-Steganography

Hides and extracts arbitrary payloads in PNG images using LSB steganography

# Usage

```bash
# Get dependencies (opencv and numpy)
pip install -r requirements.txt

# Hide a payload in an image
python3 lsb.py hide sunset.png launchcodes.txt -o steg.png

# Extract a payload from an image
python3 lsb.py extract steg.png -o codes.txt

# Get full CLI documentation
python3 lsb.py --help
```

# Example
I hid Doom and an emulator for running it in a picture of my dog:

![Doom hidden in picture of my dog](https://i.imgur.com/MHpxk5x.png)

# TODO
* Hide can be faster
* The extracted payload will usually have garbage data appended to it which is unnecessary

# LSB Caveats
* Won't work with lossy compression (like JPEG)
* Makes PNG compression ineffective, so the result image will most likely be larger than the original
* Easily detectable even without source image
