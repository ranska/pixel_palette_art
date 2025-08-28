# spec/pixel_palette_spec.py


from spec.conftest import *

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
            color = PixelColor(255, 128, 64)
            expect(color.to_hex()).to(equal("#FF8040"))

    with context('Copie de couleur'):
        with it('crée une copie avec couleur et nom'):
            color      = PixelColor(255, 128, 64)
            color_copy = color.create_copy()

            expect(color.r).to(equal(color_copy.r))
            expect(color.g).to(equal(color_copy.g))
            expect(color.b).to(equal(color_copy.b))
            #
            expect(color.name).to(equal(color_copy.name))
            expect(color.color_space).to(equal(color_copy.color_space))
