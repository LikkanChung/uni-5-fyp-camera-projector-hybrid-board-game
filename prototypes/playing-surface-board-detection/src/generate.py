# Generate QR code
import qrcode
import json
from PIL import Image

TEST_DIR = "tests/assets"


def generate(name, data):
    qr = qrcode.QRCode(
        version=2,  # 1 - 40, size
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # L,M,Q,H for 7, 15, 25, 30%
        box_size=20,
        border=1
    )
    qr.add_data(data)
    qr.make(fit=False)
    img = qr.make_image(fill="black", back_color="white")
    img.save(TEST_DIR + "/" + name + ".jpg")

    return img


def get_json(tag_id, tag_anchor):
    return json.dumps({
        "id": tag_id,
        "anchor": tag_anchor
    })


def main():
    tl = generate("tl", get_json("board", "tl"))
    tr = generate("tr", get_json("board", "tr"))
    bl = generate("bl", get_json("board", "bl"))
    br = generate("br", get_json("board", "br"))

    composite = Image.new("RGB", (2000, 2000), "white")
    composite.paste(tl, (100, 100))
    composite.paste(tr, (1200, 100))
    composite.paste(bl, (100, 1200))
    composite.paste(br, (1200, 1200))
    composite.save("tests/assets/composite.jpg")
