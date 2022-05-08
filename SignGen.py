from PIL import Image, ImageDraw, ImageFont
import numpy as np

import io
from wand.image import Image as ImageWand
from wand.font import Font
from wand.display import display

def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)

glitch_sign_coeffs = find_coeffs(
    np.array([(20,72), (308,13), (53,217), (344, 161)]), # destination points
    np.array([(0,0), (400,0), (0,200), (400,200)])       # source points
)

def glitch_sign(text, font_size):
    font = ImageFont.truetype("COMIC.TTF", font_size)
    img = Image.new('RGBA', (400, 200), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.text((200, 100), text, fill=(0, 0, 0), anchor="mm", font=font)

    img = img.transform((512, 512), Image.Transform.PERSPECTIVE, glitch_sign_coeffs, Image.Resampling.BICUBIC)

    glitch = Image.open("glitch.png")
    glitch.paste(img, (0, 0), img)
    return glitch

def glitch_rainbow(text, font_size=60):
    glitch = Image.open("glitchrainbow.png")

    with io.BytesIO() as f:
        font = ImageFont.truetype("COMIC.TTF", font_size)
        img1 = Image.new('RGBA', (500, 200), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img1)
        draw.text((250, 85), text, fill=(0, 0, 0), anchor="mm", font=font)
        img1.save(f, "PNG")
        image_blob = f.getvalue()

    with ImageWand(blob = image_blob) as img:
        img.background_color = 'transparent'
        img.font = Font('Arial', 20)
        img.virtual_pixel = 'transparent'
        img.distort('arc', (160, 0))
        img.format = 'png'
        f = io.BytesIO()
        img.save(file=f)
        f.seek(0)
        image_warp = Image.open(f)

    glitch.paste(image_warp, (-15, 0), image_warp)
    f.close()
    return glitch

if __name__ == "__main__":
    img = glitch_sign("Hello, world!", 40)
    img.save("output.png")
    img.show()

    img = glitch_rainbow("Hello, world!")
    img.save("output_rainbow.png")
    img.show()