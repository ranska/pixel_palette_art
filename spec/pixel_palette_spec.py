# spec/pixel_palette_spec.py

from mamba import description, it
from expects import expect, equal, raise_error
import sys
import os

# Ajout du chemin parent pour importer la lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.pixel_palette import PixelPalette
from lib.pixel_color import PixelColor

with description('PixelPalette create_gradient method'):
    with it('modifies existing colors between indices with RGB interpolation'):
        # Given: une palette avec 5 couleurs
        palette = PixelPalette()
        palette.add_color(255, 0, 0, "Red")      # index 0
        palette.add_color(128, 128, 128, "Gray1") # index 1 - à modifier
        palette.add_color(128, 128, 128, "Gray2") # index 2 - à modifier
        palette.add_color(128, 128, 128, "Gray3") # index 3 - à modifier
        palette.add_color(0, 255, 0, "Green")     # index 4

        # When: créer un dégradé entre index 0 et 4
        palette.create_gradient(0, 4, "rgb")

        # Then: les couleurs intermédiaires sont modifiées
        expect(palette.colors[0].rgb_tuple).to(equal((255, 0, 0)))    # Rouge inchangé
        expect(palette.colors[4].rgb_tuple).to(equal((0, 255, 0)))    # Vert inchangé

        # Les couleurs intermédiaires sont interpolées
        # Index 1: 75% Red + 25% Green = (191, 64, 0)
        expect(palette.colors[1].rgb_tuple).to(equal((191, 64, 0)))
        # Index 2: 50% Red + 50% Green = (128, 128, 0)
        expect(palette.colors[2].rgb_tuple).to(equal((128, 128, 0)))
        # Index 3: 25% Red + 75% Green = (64, 191, 0)
        expect(palette.colors[3].rgb_tuple).to(equal((64, 191, 0)))

    with it('requires at least one color between indices'):
        # Given: une palette avec seulement 2 couleurs consécutives
        palette = PixelPalette()
        palette.add_color(255, 0, 0, "Red")      # index 0
        palette.add_color(0, 255, 0, "Green")   # index 1

        # When/Then: doit lever une erreur
        expect(lambda: palette.create_gradient(0, 1, "rgb")).to(raise_error(ValueError))

    with it('requires index1 to be less than index2'):
        # Given: une palette avec 3 couleurs
        palette = PixelPalette()
        palette.add_color(255, 0, 0, "Red")      # index 0
        palette.add_color(128, 128, 128, "Gray") # index 1
        palette.add_color(0, 255, 0, "Green")    # index 2

        # When/Then: doit lever une erreur
        expect(lambda: palette.create_gradient(2, 0, "rgb")).to(raise_error(ValueError))

    with it('works with HSV color space'):
        # Given: une palette avec des couleurs pour test HSV
        palette = PixelPalette()
        palette.add_color(255, 0, 0, "Red")      # index 0 - Hue: 0°
        palette.add_color(128, 128, 128, "Gray1") # index 1
        palette.add_color(128, 128, 128, "Gray2") # index 2
        palette.add_color(0, 255, 0, "Green")    # index 3 - Hue: 120°

        # When: créer un dégradé HSV
        palette.create_gradient(0, 3, "hsv")

        # Then: les couleurs sont interpolées dans l'espace HSV
        expect(palette.colors[0].rgb_tuple).to(equal((255, 0, 0)))    # Rouge inchangé
        expect(palette.colors[3].rgb_tuple).to(equal((0, 255, 0)))    # Vert inchangé

        # Les intermédiaires sont des teintes entre rouge et vert
        # (jaune, jaune-vert, etc. selon l'interpolation HSV)

    with it('raises IndexError for invalid indices'):
        # Given: une palette avec 3 couleurs
        palette = PixelPalette()
        palette.add_color(255, 0, 0, "Red")
        palette.add_color(0, 255, 0, "Green")
        palette.add_color(0, 0, 255, "Blue")

        # When/Then: index hors limites
        expect(lambda: palette.create_gradient(0, 10, "rgb")).to(raise_error(IndexError))

    with it('preserves color names'):
        # Given: une palette avec des noms
        palette = PixelPalette()
        palette.add_color(255, 0, 0, "Start Red")    # index 0
        palette.add_color(128, 128, 128, "Middle1")  # index 1
        palette.add_color(128, 128, 128, "Middle2")  # index 2
        palette.add_color(0, 255, 0, "End Green")    # index 3

        # When: créer un dégradé
        palette.create_gradient(0, 3, "rgb")

        # Then: les noms des couleurs d'origine sont préservés
        expect(palette.colors[0].name).to(equal("Start Red"))
        expect(palette.colors[3].name).to(equal("End Green"))
        # Les couleurs intermédiaires gardent leurs noms originaux
        expect(palette.colors[1].name).to(equal("Middle1"))
        expect(palette.colors[2].name).to(equal("Middle2"))