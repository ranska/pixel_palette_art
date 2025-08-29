from ...color_space_registry import ColorSpaceRegistry
from colorsys import rgb_to_hsv, hsv_to_rgb


class HSVMixer:

    @staticmethod
    def mix_with(color_a, color_b, ratio):
        r1, g1, b1 = color_a.r / 255, color_a.g / 255, color_a.b / 255
        r2, g2, b2 = color_b.r / 255, color_b.g / 255, color_b.b / 255

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

#
#
ColorSpaceRegistry.register('hsv', mixer_class = HSVMixer)
