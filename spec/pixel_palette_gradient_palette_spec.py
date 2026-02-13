# spec/pixel_palette_gradient_palette_spec.py

from spec.conftest import *

from mamba import description, context, it
from expects import expect, equal, have_length, raise_error

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.pixel_palette import PixelPalette
from lib.pixel_color import PixelColor


with description('PixelPalette create_gradient_palette'):
    with context('avec interpolation RGB'):
        with it('crée une palette de 2 couleurs (les extrêmes)'):
            start = PixelColor(255, 0, 0, "Rouge")
            end = PixelColor(0, 0, 255, "Bleu")

            palette = PixelPalette.create_gradient_palette(start, end, 2)

            expect(palette.colors).to(have_length(2))
            expect(palette.colors[0].rgb_tuple).to(equal((255, 0, 0)))
            expect(palette.colors[1].rgb_tuple).to(equal((0, 0, 255)))

        with it('crée un dégradé de 5 couleurs'):
            start = PixelColor(0, 0, 0, "Noir")
            end = PixelColor(255, 255, 255, "Blanc")

            palette = PixelPalette.create_gradient_palette(start, end, 5)

            expect(palette.colors).to(have_length(5))
            expect(palette.colors[0].rgb_tuple).to(equal((0, 0, 0)))
            expect(palette.colors[4].rgb_tuple).to(equal((255, 255, 255)))
            # Milieu = gris moyen
            expect(palette.colors[2].rgb_tuple).to(equal((128, 128, 128)))

        with it('préserve le nom des couleurs extrêmes'):
            start = PixelColor(255, 0, 0, "Rouge Feu")
            end = PixelColor(0, 0, 255, "Bleu Nuit")

            palette = PixelPalette.create_gradient_palette(start, end, 3)

            expect(palette.colors[0].name).to(equal("Rouge Feu"))
            expect(palette.colors[2].name).to(equal("Bleu Nuit"))

        with it('ne modifie pas les couleurs originales'):
            start = PixelColor(255, 0, 0, "Rouge")
            end = PixelColor(0, 255, 0, "Vert")

            PixelPalette.create_gradient_palette(start, end, 5)

            expect(start.rgb_tuple).to(equal((255, 0, 0)))
            expect(end.rgb_tuple).to(equal((0, 255, 0)))

    with context('avec interpolation HSV'):
        with it('crée un dégradé en passant par les teintes'):
            start = PixelColor(255, 0, 0, "Rouge")   # hue 0°
            end = PixelColor(0, 255, 0, "Vert")       # hue 120°

            palette = PixelPalette.create_gradient_palette(start, end, 3, "hsv")

            expect(palette.colors).to(have_length(3))
            expect(palette.colors[0].rgb_tuple).to(equal((255, 0, 0)))
            expect(palette.colors[2].rgb_tuple).to(equal((0, 255, 0)))
            # La couleur intermédiaire doit être dans les jaunes (entre rouge et vert en HSV)
            mid = palette.colors[1]
            expect(mid.g).to(equal(255))  # Le milieu HSV entre rouge et vert est jaune

    with context('validation'):
        with it('refuse moins de 2 couleurs'):
            start = PixelColor(255, 0, 0)
            end = PixelColor(0, 255, 0)

            expect(lambda: PixelPalette.create_gradient_palette(start, end, 1)).to(
                raise_error(ValueError)
            )

        with it('refuse 0 couleurs'):
            start = PixelColor(255, 0, 0)
            end = PixelColor(0, 255, 0)

            expect(lambda: PixelPalette.create_gradient_palette(start, end, 0)).to(
                raise_error(ValueError)
            )
