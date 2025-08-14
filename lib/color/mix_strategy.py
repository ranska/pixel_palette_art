from colorsys import rgb_to_hsv, hsv_to_rgb

STRATEGIES = ["RGB", "HSV"]

def strategy_rgb(a, b, ratio):
    r = round(a.r * (1 - ratio) + b.r * ratio)
    g = round(a.g * (1 - ratio) + b.g * ratio)
    bb = round(a.b * (1 - ratio) + b.b * ratio)
    return r, g, bb

def strategy_hsv(a, b, ratio):
    r1, g1, b1 = a.r / 255, a.g / 255, a.b / 255
    r2, g2, b2 = b.r / 255, b.g / 255, b.b / 255

    h1, s1, v1 = rgb_to_hsv(r1, g1, b1)
    h2, s2, v2 = rgb_to_hsv(r2, g2, b2)

    dh = h2 - h1
    if abs(dh) > 0.5:
        if dh > 0:
            dh -= 1
        else:
            dh += 1
    h = (h1 + ratio * dh) % 1.0
    s = s1 * (1 - ratio) + s2 * ratio
    v = v1 * (1 - ratio) + v2 * ratio

    r, g, b = hsv_to_rgb(h, s, v)
    return round(r * 255), round(g * 255), round(b * 255)
