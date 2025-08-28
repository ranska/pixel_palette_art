# spec/pixel_palette_spec.py


from spec.conftest import *

from mamba import description, context, it, before
from expects import expect, be_empty, have_length, equal, be_true, be_false, contain, start_with, end_with, expect, equal, be_above_or_equal, be_below_or_equal
import sys
import os

# Ajout du chemin parent pour importer la lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.pixel_color   import PixelColor
from lib.pixel_palette import PixelPalette

#
with description('PixelPalette') as self:
    with context('Création'):
        with it('crée une palette n fois meme couleur'):
            color = PixelColor(255, 128, 64)

            palette = PixelPalette.create_monochrome(color, 5, "test")

            expect(len(palette)).to(equal(5))
            for color_p in palette.colors:
                expect(color.r).to(equal(color_p.r))
                expect(color.g).to(equal(color_p.g))
                expect(color.b).to(equal(color_p.b))


