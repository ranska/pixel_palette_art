
# spec/rgb_mixer_spec.py

# NOTE: we test here pixel color using a mix

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from lib.color.color_spaces import *  # exécute les registers
# TODO: cause I'm a python newbe...
from lib.color.color_spaces.hsv.hsv_mixer import HSVMixer
from lib.color.color_space_registry import ColorSpaceRegistry
#

from lib.pixel_color import PixelColor
#
from mamba import description, context, it
from expects import expect, equal



#

with description('PixelColor') as self:

    with before.each:
        ColorSpaceRegistry.register('hsv', mixer_class = HSVMixer)
    #
    #
    with context('with default color space'):
        with it('mix as hsv'):
            color_a = PixelColor(255, 0, 0, "red")
            color_b = PixelColor(0, 255, 0, "green")

            with color_a.using_color_space('hsv'):
                color_a.mix_with(color_b, 0.5)
            expect(color_a.r).to(equal(255))
            expect(color_a.g).to(equal(255))
            expect(color_a.b).to(equal(0))

        with it('mix as hsv with default value 0.5'):
            color_a = PixelColor(255, 0, 0, "red")
            color_b = PixelColor(0, 255, 0, "green")

            with color_a.using_color_space('hsv'):
                color_a.mix_with(color_b)
            expect(color_a.r).to(equal(255))
            expect(color_a.g).to(equal(255))
            expect(color_a.b).to(equal(0))

    with context('wrapping de teinte (ecart > 180 degres)'):
        with it('mix rouge (0) et bleu (240) passe par le chemin court (dh -= 1)'):
            # Rouge = 0°, Bleu = 240° → écart > 180°, dh positif → dh -= 1
            color_a = PixelColor(255, 0, 0, "red")
            color_b = PixelColor(0, 0, 255, "blue")

            with color_a.using_color_space('hsv'):
                color_a.mix_with(color_b, 0.5)
            # Le mix doit passer par magenta/rose, pas par vert
            # On vérifie que le résultat a une composante rouge significative
            expect(color_a.r).not_to(equal(0))

        with it('mix bleu (240) et rouge (0) passe par le chemin court (dh += 1)'):
            # Bleu = 240°, Rouge = 0° → écart > 180°, dh négatif → dh += 1
            color_a = PixelColor(0, 0, 255, "blue")
            color_b = PixelColor(255, 0, 0, "red")

            with color_a.using_color_space('hsv'):
                color_a.mix_with(color_b, 0.5)
            # Même résultat attendu (passage par magenta)
            expect(color_a.r).not_to(equal(0))
