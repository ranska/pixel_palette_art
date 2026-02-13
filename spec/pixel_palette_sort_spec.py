# spec/pixel_palette_sort_spec.py

from spec.conftest import *

from mamba import description, context, it, before
from expects import expect, equal, have_length

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.pixel_palette import PixelPalette
from lib.pixel_color import PixelColor


with description('PixelPalette sort_by_hue'):
    with it('trie les couleurs par teinte'):
        # Given: palette avec couleurs dans le désordre de teinte
        palette = PixelPalette()
        palette.add_color(0, 255, 0, "Vert")       # hue ~0.33
        palette.add_color(255, 0, 0, "Rouge")       # hue 0.0
        palette.add_color(0, 0, 255, "Bleu")        # hue ~0.67

        # When
        palette.sort_by_hue()

        # Then: rouge (0.0) < vert (0.33) < bleu (0.67)
        expect(palette.colors[0].name).to(equal("Rouge"))
        expect(palette.colors[1].name).to(equal("Vert"))
        expect(palette.colors[2].name).to(equal("Bleu"))

    with it('ne modifie pas une palette déjà triée'):
        palette = PixelPalette()
        palette.add_color(255, 0, 0, "Rouge")
        palette.add_color(0, 255, 0, "Vert")
        palette.add_color(0, 0, 255, "Bleu")

        palette.sort_by_hue()

        expect(palette.colors[0].name).to(equal("Rouge"))
        expect(palette.colors[1].name).to(equal("Vert"))
        expect(palette.colors[2].name).to(equal("Bleu"))

    with it('gère une palette avec une seule couleur'):
        palette = PixelPalette()
        palette.add_color(255, 0, 0, "Rouge")

        palette.sort_by_hue()

        expect(palette.colors).to(have_length(1))
        expect(palette.colors[0].name).to(equal("Rouge"))

    with it('gère les couleurs achromatiques (noir, blanc, gris)'):
        # Les gris ont une saturation de 0, hue = 0
        palette = PixelPalette()
        palette.add_color(0, 255, 0, "Vert")
        palette.add_color(128, 128, 128, "Gris")   # hue 0.0
        palette.add_color(255, 0, 0, "Rouge")       # hue 0.0

        palette.sort_by_hue()

        # Gris et Rouge ont la même hue (0.0), mais sort est stable
        expect(palette.colors[2].name).to(equal("Vert"))


with description('PixelPalette sort_by_brightness'):
    with it('trie les couleurs par luminosité'):
        # Given: palette avec luminosités variées
        palette = PixelPalette()
        palette.add_color(255, 255, 255, "Blanc")   # luminosité max
        palette.add_color(0, 0, 0, "Noir")           # luminosité min
        palette.add_color(128, 128, 128, "Gris")     # luminosité moyenne

        # When
        palette.sort_by_brightness()

        # Then: noir < gris < blanc
        expect(palette.colors[0].name).to(equal("Noir"))
        expect(palette.colors[1].name).to(equal("Gris"))
        expect(palette.colors[2].name).to(equal("Blanc"))

    with it('utilise la luminosité perceptuelle'):
        # Le vert est perçu plus lumineux que le rouge ou le bleu
        # Formule: 0.299*R + 0.587*G + 0.114*B
        palette = PixelPalette()
        palette.add_color(0, 0, 255, "Bleu")        # 0.114 * 255 = 29.07
        palette.add_color(255, 0, 0, "Rouge")       # 0.299 * 255 = 76.245
        palette.add_color(0, 255, 0, "Vert")        # 0.587 * 255 = 149.685

        # When
        palette.sort_by_brightness()

        # Then: bleu < rouge < vert (luminosité perceptuelle)
        expect(palette.colors[0].name).to(equal("Bleu"))
        expect(palette.colors[1].name).to(equal("Rouge"))
        expect(palette.colors[2].name).to(equal("Vert"))

    with it('trie en place (modifie la palette originale)'):
        palette = PixelPalette()
        palette.add_color(255, 255, 255, "Blanc")
        palette.add_color(0, 0, 0, "Noir")

        palette.sort_by_brightness()

        expect(palette.colors[0].name).to(equal("Noir"))
        expect(palette.colors[1].name).to(equal("Blanc"))
