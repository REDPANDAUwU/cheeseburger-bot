import os
import webcolors

r = 0
g = 0
b = 0

change = 10

while r < 255:
    while g < 255:
        while b < 255:
            hex_code = webcolors.rgb_to_hex((r, g, b))
            print(hex_code)
            os.system(f'convert im.gif -dispose previous -fill "{hex_code}" -opaque "#009084" '
                      f'./gifs/{hex_code.strip("#")}1.gif')
            hex_code_dark = webcolors.rgb_to_hex((int(r/2), int(g/2), int(b/2)))
            os.system(f'convert ./gifs/{hex_code.strip("#")}1.gif -dispose previous -fill "{hex_code_dark}" '
                      f'-opaque "#004557" "./gifs/{hex_code.strip("#")}.gif"')
            os.remove(f'./gifs/{hex_code.strip("#")}1.gif')
            b += change
        b = 0
        g += change
    g = 0
    r += change

