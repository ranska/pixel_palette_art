from ...color_space_registry import ColorSpaceRegistry

class RGBMixer:
    @staticmethod
    def mix_with(color_a, color_b, ratio):
        r = round(color_a.r * (1 - ratio) + color_b.r * ratio)
        g = round(color_a.g * (1 - ratio) + color_b.g * ratio)
        b = round(color_a.b * (1 - ratio) + color_b.b * ratio)

        return r, g, b

    # TODO: extract private method mix_channel ?

ColorSpaceRegistry.register('rgb', mixer_class = RGBMixer)
