class RGBMixer:
    def mix_with(color_a, a, ratio):
        r = round(color_a.r * (1 - ratio) + a.r * ratio)
        g = round(color_a.g * (1 - ratio) + a.g * ratio)
        b = round(color_a.b * (1 - ratio) + a.b * ratio)

        return r, g, b

    # TODO: extract private method mix_channel ?
