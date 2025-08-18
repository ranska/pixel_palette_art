class RGBMixer:
    def mix_with(self, a, ratio):
        r = round(self.r * (1 - ratio) + a.r * ratio)
        g = round(self.g * (1 - ratio) + a.g * ratio)
        b = round(self.b * (1 - ratio) + a.b * ratio)

        return r, g, b

    # TODO: extract private method mix_channel ?
