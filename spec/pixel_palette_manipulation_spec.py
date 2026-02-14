# spec/pixel_palette_manipulation_spec.py

from spec.conftest import *

from mamba import description, context, it
from expects import expect, equal, have_length, raise_error, be_above

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.pixel_palette import PixelPalette
from lib.pixel_color import PixelColor


# =============================================================================
# copy_subset
# =============================================================================

with description('PixelPalette copy_subset'):
    with context('cas nominal'):
        with it('retourne un sous-ensemble de couleurs (inclusif)'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")
            palette.add_color(0, 255, 0, "Vert")
            palette.add_color(0, 0, 255, "Bleu")
            palette.add_color(255, 255, 0, "Jaune")
            palette.add_color(255, 0, 255, "Magenta")

            subset = palette.copy_subset(1, 3)

            expect(subset.colors).to(have_length(3))
            expect(subset.colors[0].rgb_tuple).to(equal((0, 255, 0)))
            expect(subset.colors[1].rgb_tuple).to(equal((0, 0, 255)))
            expect(subset.colors[2].rgb_tuple).to(equal((255, 255, 0)))

        with it('retourne une seule couleur quand start == end'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")
            palette.add_color(0, 255, 0, "Vert")

            subset = palette.copy_subset(0, 0)

            expect(subset.colors).to(have_length(1))
            expect(subset.colors[0].rgb_tuple).to(equal((255, 0, 0)))

        with it('retourne toute la palette quand start=0 end=last'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")
            palette.add_color(0, 255, 0, "Vert")
            palette.add_color(0, 0, 255, "Bleu")

            subset = palette.copy_subset(0, 2)

            expect(subset.colors).to(have_length(3))

    with context('immutabilite'):
        with it('ne modifie pas la palette originale'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")
            palette.add_color(0, 255, 0, "Vert")
            palette.add_color(0, 0, 255, "Bleu")

            subset = palette.copy_subset(0, 1)
            subset.colors[0] = PixelColor(0, 0, 0, "Noir")

            expect(palette.colors[0].rgb_tuple).to(equal((255, 0, 0)))

    with context('validation'):
        with it('refuse start > end'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")
            palette.add_color(0, 255, 0, "Vert")

            expect(lambda: palette.copy_subset(1, 0)).to(raise_error(ValueError))

        with it('refuse un index negatif'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")

            expect(lambda: palette.copy_subset(-1, 0)).to(raise_error(IndexError))

        with it('refuse un end hors limites'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")

            expect(lambda: palette.copy_subset(0, 5)).to(raise_error(IndexError))


# =============================================================================
# append_palette
# =============================================================================

with description('PixelPalette append_palette'):
    with context('cas nominal'):
        with it('combine deux palettes'):
            palette_a = PixelPalette(name="A")
            palette_a.add_color(255, 0, 0, "Rouge")
            palette_a.add_color(0, 255, 0, "Vert")

            palette_b = PixelPalette(name="B")
            palette_b.add_color(0, 0, 255, "Bleu")

            result = palette_a.append_palette(palette_b)

            expect(result.colors).to(have_length(3))
            expect(result.colors[0].rgb_tuple).to(equal((255, 0, 0)))
            expect(result.colors[1].rgb_tuple).to(equal((0, 255, 0)))
            expect(result.colors[2].rgb_tuple).to(equal((0, 0, 255)))

        with it('genere un nom combine'):
            palette_a = PixelPalette(name="Chaud")
            palette_a.add_color(255, 0, 0)

            palette_b = PixelPalette(name="Froid")
            palette_b.add_color(0, 0, 255)

            result = palette_a.append_palette(palette_b)

            expect(result.name).to(equal("Chaud + Froid"))

    with context('palettes vides'):
        with it('gere une palette vide a droite'):
            palette_a = PixelPalette()
            palette_a.add_color(255, 0, 0, "Rouge")

            palette_b = PixelPalette()

            result = palette_a.append_palette(palette_b)

            expect(result.colors).to(have_length(1))
            expect(result.colors[0].rgb_tuple).to(equal((255, 0, 0)))

        with it('gere une palette vide a gauche'):
            palette_a = PixelPalette()

            palette_b = PixelPalette()
            palette_b.add_color(0, 0, 255, "Bleu")

            result = palette_a.append_palette(palette_b)

            expect(result.colors).to(have_length(1))

        with it('gere deux palettes vides'):
            result = PixelPalette().append_palette(PixelPalette())

            expect(result.colors).to(have_length(0))

    with context('immutabilite'):
        with it('ne modifie pas les palettes originales'):
            palette_a = PixelPalette()
            palette_a.add_color(255, 0, 0, "Rouge")

            palette_b = PixelPalette()
            palette_b.add_color(0, 0, 255, "Bleu")

            result = palette_a.append_palette(palette_b)
            result.colors[0] = PixelColor(0, 0, 0)

            expect(palette_a.colors[0].rgb_tuple).to(equal((255, 0, 0)))
            expect(palette_b.colors[0].rgb_tuple).to(equal((0, 0, 255)))


# =============================================================================
# insert_palette
# =============================================================================

with description('PixelPalette insert_palette'):
    with context('cas nominal'):
        with it('insere au debut (index 0)'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")
            palette.add_color(0, 0, 255, "Bleu")

            sub = PixelPalette()
            sub.add_color(0, 255, 0, "Vert")

            result = palette.insert_palette(sub, 0)

            expect(result.colors).to(have_length(3))
            expect(result.colors[0].rgb_tuple).to(equal((0, 255, 0)))
            expect(result.colors[1].rgb_tuple).to(equal((255, 0, 0)))
            expect(result.colors[2].rgb_tuple).to(equal((0, 0, 255)))

        with it('insere au milieu'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")
            palette.add_color(0, 0, 255, "Bleu")

            sub = PixelPalette()
            sub.add_color(0, 255, 0, "Vert")
            sub.add_color(255, 255, 0, "Jaune")

            result = palette.insert_palette(sub, 1)

            expect(result.colors).to(have_length(4))
            expect(result.colors[0].rgb_tuple).to(equal((255, 0, 0)))
            expect(result.colors[1].rgb_tuple).to(equal((0, 255, 0)))
            expect(result.colors[2].rgb_tuple).to(equal((255, 255, 0)))
            expect(result.colors[3].rgb_tuple).to(equal((0, 0, 255)))

        with it('insere a la fin (index == len)'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")

            sub = PixelPalette()
            sub.add_color(0, 255, 0, "Vert")

            result = palette.insert_palette(sub, 1)

            expect(result.colors).to(have_length(2))
            expect(result.colors[0].rgb_tuple).to(equal((255, 0, 0)))
            expect(result.colors[1].rgb_tuple).to(equal((0, 255, 0)))

    with context('palettes vides'):
        with it('insere dans une palette vide (index 0)'):
            palette = PixelPalette()

            sub = PixelPalette()
            sub.add_color(255, 0, 0, "Rouge")

            result = palette.insert_palette(sub, 0)

            expect(result.colors).to(have_length(1))

        with it('insere une palette vide'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")

            result = palette.insert_palette(PixelPalette(), 0)

            expect(result.colors).to(have_length(1))

    with context('immutabilite'):
        with it('ne modifie pas les palettes originales'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0, "Rouge")

            sub = PixelPalette()
            sub.add_color(0, 255, 0, "Vert")

            result = palette.insert_palette(sub, 0)
            result.colors[0] = PixelColor(0, 0, 0)

            expect(palette.colors[0].rgb_tuple).to(equal((255, 0, 0)))
            expect(sub.colors[0].rgb_tuple).to(equal((0, 255, 0)))

    with context('validation'):
        with it('refuse un index negatif'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0)

            expect(lambda: palette.insert_palette(PixelPalette(), -1)).to(
                raise_error(IndexError))

        with it('refuse un index > len(palette)'):
            palette = PixelPalette()
            palette.add_color(255, 0, 0)

            expect(lambda: palette.insert_palette(PixelPalette(), 5)).to(
                raise_error(IndexError))


# =============================================================================
# mix_with_palette
# =============================================================================

with description('PixelPalette mix_with_palette'):
    with context('meme taille, sans offset'):
        with it('mixe en RGB a 50%'):
            palette_a = PixelPalette()
            palette_a.add_color(255, 0, 0, "Rouge")
            palette_a.add_color(0, 0, 255, "Bleu")

            palette_b = PixelPalette()
            palette_b.add_color(0, 255, 0, "Vert")
            palette_b.add_color(255, 255, 0, "Jaune")

            result = palette_a.mix_with_palette(palette_b, 0.5, "rgb")

            expect(result.colors).to(have_length(2))
            # Rouge + Vert a 50% RGB = (128, 128, 0)
            expect(result.colors[0].rgb_tuple).to(equal((128, 128, 0)))

        with it('ratio 0.0 garde la palette self'):
            palette_a = PixelPalette()
            palette_a.add_color(255, 0, 0)

            palette_b = PixelPalette()
            palette_b.add_color(0, 255, 0)

            result = palette_a.mix_with_palette(palette_b, 0.0, "rgb")

            expect(result.colors[0].rgb_tuple).to(equal((255, 0, 0)))

        with it('ratio 1.0 donne la palette other'):
            palette_a = PixelPalette()
            palette_a.add_color(255, 0, 0)

            palette_b = PixelPalette()
            palette_b.add_color(0, 255, 0)

            result = palette_a.mix_with_palette(palette_b, 1.0, "rgb")

            expect(result.colors[0].rgb_tuple).to(equal((0, 255, 0)))

    with context('avec HSV'):
        with it('mixe en HSV'):
            palette_a = PixelPalette()
            palette_a.add_color(255, 0, 0, "Rouge")

            palette_b = PixelPalette()
            palette_b.add_color(0, 255, 0, "Vert")

            result = palette_a.mix_with_palette(palette_b, 0.5, "hsv")

            expect(result.colors).to(have_length(1))
            # Le milieu HSV entre rouge et vert est jaune
            expect(result.colors[0].g).to(equal(255))

    with context('tailles differentes'):
        with it('copie les couleurs sans correspondance de self'):
            palette_a = PixelPalette()
            palette_a.add_color(255, 0, 0, "Rouge")
            palette_a.add_color(0, 255, 0, "Vert")
            palette_a.add_color(0, 0, 255, "Bleu")

            palette_b = PixelPalette()
            palette_b.add_color(128, 128, 128, "Gris")

            result = palette_a.mix_with_palette(palette_b, 0.5, "rgb")

            expect(result.colors).to(have_length(3))
            # Couleur 0 : mixee
            # Couleurs 1 et 2 : copiees de self
            expect(result.colors[1].rgb_tuple).to(equal((0, 255, 0)))
            expect(result.colors[2].rgb_tuple).to(equal((0, 0, 255)))

        with it('copie les couleurs sans correspondance de other'):
            palette_a = PixelPalette()
            palette_a.add_color(255, 0, 0, "Rouge")

            palette_b = PixelPalette()
            palette_b.add_color(128, 128, 128, "Gris")
            palette_b.add_color(0, 255, 0, "Vert")
            palette_b.add_color(0, 0, 255, "Bleu")

            result = palette_a.mix_with_palette(palette_b, 0.5, "rgb")

            expect(result.colors).to(have_length(3))
            # Couleurs 1 et 2 : copiees de other
            expect(result.colors[1].rgb_tuple).to(equal((0, 255, 0)))
            expect(result.colors[2].rgb_tuple).to(equal((0, 0, 255)))

    with context('avec offset'):
        with it('decale le mix de other'):
            palette_a = PixelPalette()
            palette_a.add_color(255, 0, 0, "Rouge")
            palette_a.add_color(0, 255, 0, "Vert")
            palette_a.add_color(0, 0, 255, "Bleu")

            palette_b = PixelPalette()
            palette_b.add_color(128, 128, 128, "Gris")

            # offset=1 : other[0] correspond a self[1]
            result = palette_a.mix_with_palette(palette_b, 0.5, "rgb", offset=1)

            expect(result.colors).to(have_length(3))
            # self[0] : pas de correspondance → copie rouge
            expect(result.colors[0].rgb_tuple).to(equal((255, 0, 0)))
            # self[1] : mixe avec other[0] (Vert + Gris)
            expect(result.colors[1].rgb_tuple).not_to(equal((0, 255, 0)))
            # self[2] : pas de correspondance → copie bleu
            expect(result.colors[2].rgb_tuple).to(equal((0, 0, 255)))

    with context('palettes vides'):
        with it('retourne une palette vide si les deux sont vides'):
            result = PixelPalette().mix_with_palette(PixelPalette(), 0.5, "rgb")

            expect(result.colors).to(have_length(0))

        with it('copie self si other est vide'):
            palette_a = PixelPalette()
            palette_a.add_color(255, 0, 0)

            result = palette_a.mix_with_palette(PixelPalette(), 0.5, "rgb")

            expect(result.colors).to(have_length(1))
            expect(result.colors[0].rgb_tuple).to(equal((255, 0, 0)))

    with context('immutabilite'):
        with it('ne modifie pas les palettes originales'):
            palette_a = PixelPalette()
            palette_a.add_color(255, 0, 0, "Rouge")

            palette_b = PixelPalette()
            palette_b.add_color(0, 255, 0, "Vert")

            result = palette_a.mix_with_palette(palette_b, 0.5, "rgb")

            expect(palette_a.colors[0].rgb_tuple).to(equal((255, 0, 0)))
            expect(palette_b.colors[0].rgb_tuple).to(equal((0, 255, 0)))
