from PIL import Image, ImageDraw, ImageFont
import numpy as np

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

if __name__ == "__main__":
    img = glitch_sign("Hello, world!", 40)
    img.save("output.png")
    img.show()