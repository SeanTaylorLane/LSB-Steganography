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
This picture of my dog is hiding Doom and an emulator for running it: https://drive.google.com/file/d/1ASs0Ww9uT7LCRYfwDVB8SDaoiNlB0Wn9/view?usp=sharing

Comparison:

![Doom hidden in picture of my dog](https://i.imgur.com/MHpxk5x.png)

# TODO
* Hide can be faster
* The extracted payload will usually have garbage data appended to it which is unnecessary

# LSB Caveats
* Won't work with lossy compression (like JPEG)
* Makes PNG compression ineffective, so the result image will most likely be larger than the original
* Easily detectable even without source image
