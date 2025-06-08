import qrcode
from pyzbar import pyzbar
from PIL import Image

"""
code=qrcode.make("https://github.com/KeremReyhani")
code.save("gitcode.png")"""

qr=pyzbar.decode(Image.open("gitcode.png"))
print(qr)