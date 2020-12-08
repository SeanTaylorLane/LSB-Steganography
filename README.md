# What is this?

Hides and extracts arbitrary payloads in PNG images without adding any additional data to the image by using **L**east **S**ignificant **B**it (LSB) steganography.

Steganography is the practice of hiding information within plain sight via another piece of information so that the existence of a secret payload is unknown or at least plausibly deniable. It's used for [international espionage](https://www.wired.com/2010/06/alleged-spies-hid-secret-messages-on-public-websites/), [data exfiltration](https://www.internetandtechnologylaw.com/trade-secrets-theft-steganography-picture/), [malware](https://www.welivesecurity.com/2016/12/06/readers-popular-websites-targeted-stealthy-stegano-exploit-kit-hiding-pixels-malicious-ads/), and [fingerprinting](https://www.businessinsider.nl/genius-accuses-google-of-copying-its-lyrics-and-diverting-traffic-2019-6?international=true&r=US)- pretty cool!

LSB steganography works by replacing the least significant bits in each pixel with payload data. For a regular PNG image, each pixel is comprised of 4 bytes: one byte each for Red, Green, Blue, and Alpha (transparency). If you replace the last 2 bits of each byte with some payload bits, then the numeric value of that byte will change by at most 3 which is hard to casually notice since the values are out of 255. This way we can hide a byte of payload data per pixel while only affecting the pixel channel intensities by at most ~1%. 

LSB is pretty easy to detect via statistical analysis, even without access to the original image. There are other methods that are practically impossible to detect! If you want to learn more about better methods and countermeasures I recommend checking out [Simon Wiseman's Defenders Guide to Steganography](https://www.researchgate.net/publication/319943090_Defenders_Guide_to_Steganography), it's short and makes sense!

# Usage

```bash
# Get dependencies (opencv and numpy)
pip install -r requirements.txt

# Hide a payload in an image
python3 lsb.py hide sunset.png launchcodes.txt -o steg.png

# Extract a payload from an image
python3 lsb.py extract steg.png -o thelaunchcodes.txt

# Get full CLI documentation
python3 lsb.py --help
```

# Example
This picture of my dog is hiding Doom and an emulator for running it as a .7z file: https://drive.google.com/file/d/1ASs0Ww9uT7LCRYfwDVB8SDaoiNlB0Wn9/view?usp=sharing

Comparison:

![Doom hidden in picture of my dog](https://i.imgur.com/MHpxk5x.png)

# LSB caveats
* Won't work with lossy compression (like JPEG)
* Large payloads make PNG compression ineffective, so the compressed result image will most likely be larger than the compresed original
* Easily detectable even without original image

# TODO
* Hide can be faster
* ~~The extracted payload will usually have garbage data appended to it which is unnecessary~~
