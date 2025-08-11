# spec/pixel_palette_spec.py
from mamba import description, context, it, before
from expects import expect, be_empty, have_length, equal, be_true, be_false, contain, start_with, end_with, expect, equal, be_above_or_equal, be_below_or_equal
import sys
import os

# Ajout du chemin parent pour importer la lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.pixel_color import PixelColor

#
with description('PixelColor') as self:
    with context('Création et initialisation'):
        with it('crée une couleur noir par défaut'):
            color = PixelColor(0,0,0)
            color.b
            #  print(color.__class__)
            expect(color.r).to(equal(0))

    with context('#to_hex'):
        with it('renvoie la couleur au format hexadécimal'):
            pixel = PixelColor(255, 128, 64)
            expect(pixel.to_hex()).to(equal("#FF8040"))

    with context('.mixcolor'):
        with it('mixe deux couleurs selon la stratégie RGB'):
            a = PixelColor(255, 0, 0)  # rouge
            b = PixelColor(0, 0, 255)  # bleu
            mix = PixelColor.mixcolor(a, b, 0.5, "RGB")
            expect(mix.r).to(equal(128))
            expect(mix.g).to(equal(0))
            expect(mix.b).to(equal(128))

        #  with it('mixe deux couleurs selon la stratégie HSV'):
            #  a = PixelColor(255, 0, 0)  # rouge
            #  b = PixelColor(0, 255, 0)  # vert
            #  mix = PixelColor.mixcolor(a, b, 0.5, "HSV")
            #  expect(mix.r).to(be_above_or_equal(127))
            #  expect(mix.r).to(be_below_or_equal(130))
            #  expect(mix.g).to(be_above_or_equal(127))
            #  expect(mix.g).to(be_below_or_equal(130))
            #  expect(mix.b).to(be_above_or_equal(0))
            #  expect(mix.b).to(be_below_or_equal(5))
