# spec/palette_renderer_spec.py

from spec.conftest import *

from mamba import description, context, it, before
from expects import expect, equal, be_a, be_above, be_above_or_equal

import sys
import os
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.pixel_palette import PixelPalette
from lib.pixel_color import PixelColor
from lib.palette.palette_renderer import PaletteRenderer


with description('PaletteRenderer') as self:
    with before.each:
        self.palette = PixelPalette()
        self.palette.add_color(255, 0, 0, "Rouge")
        self.palette.add_color(0, 255, 0, "Vert")
        self.palette.add_color(0, 0, 255, "Bleu")
        self.palette.add_color(255, 255, 0, "Jaune")
        self.renderer = PaletteRenderer(self.palette)

    with context('rendu en grille'):
        with it('retourne une image PIL'):
            img = self.renderer.render(layout="grid")
            expect(img).to(be_a(Image.Image))
            expect(img.mode).to(equal('RGB'))

        with it('calcule la taille correcte pour une grille 2 colonnes'):
            img = self.renderer.render(layout="grid", cell_size=32, columns=2)
            # 4 couleurs en 2 colonnes = 2 lignes
            expect(img.width).to(equal(64))   # 2 * 32
            expect(img.height).to(equal(64))   # 2 * 32

        with it('calcule la taille correcte pour une grille 4 colonnes'):
            img = self.renderer.render(layout="grid", cell_size=16, columns=4)
            # 4 couleurs en 4 colonnes = 1 ligne
            expect(img.width).to(equal(64))    # 4 * 16
            expect(img.height).to(equal(16))   # 1 * 16

        with it('affiche les bonnes couleurs aux bons pixels'):
            img = self.renderer.render(layout="grid", cell_size=10, columns=4)
            # Le pixel central de chaque cellule doit être de la bonne couleur
            expect(img.getpixel((5, 5))).to(equal((255, 0, 0)))     # Rouge
            expect(img.getpixel((15, 5))).to(equal((0, 255, 0)))    # Vert
            expect(img.getpixel((25, 5))).to(equal((0, 0, 255)))    # Bleu
            expect(img.getpixel((35, 5))).to(equal((255, 255, 0)))  # Jaune

        with it('ajoute de la hauteur pour le texte'):
            img_sans = self.renderer.render(layout="grid", cell_size=32, columns=4)
            img_avec = self.renderer.render(layout="grid", cell_size=32, columns=4, show_hex=True)
            expect(img_avec.height).to(be_above(img_sans.height))

    with context('rendu horizontal'):
        with it('crée une bande horizontale'):
            img = self.renderer.render(layout="horizontal", cell_size=20)
            expect(img.width).to(equal(80))   # 4 * 20
            expect(img.height).to(equal(20))

        with it('affiche les couleurs de gauche à droite'):
            img = self.renderer.render(layout="horizontal", cell_size=10)
            expect(img.getpixel((5, 5))).to(equal((255, 0, 0)))     # Rouge
            expect(img.getpixel((15, 5))).to(equal((0, 255, 0)))    # Vert

    with context('rendu vertical'):
        with it('crée une bande verticale'):
            img = self.renderer.render(layout="vertical", cell_size=20)
            expect(img.width).to(equal(20))
            expect(img.height).to(equal(80))   # 4 * 20

        with it('affiche les couleurs de haut en bas'):
            img = self.renderer.render(layout="vertical", cell_size=10)
            expect(img.getpixel((5, 5))).to(equal((255, 0, 0)))     # Rouge
            expect(img.getpixel((5, 15))).to(equal((0, 255, 0)))    # Vert

        with it('ajoute une zone de texte à droite'):
            img = self.renderer.render(layout="vertical", cell_size=20, show_hex=True)
            expect(img.width).to(be_above(20))  # Plus large que la cellule seule

    with context('palette vide'):
        with it('retourne une image placeholder'):
            empty = PixelPalette()
            renderer = PaletteRenderer(empty)
            img = renderer.render()
            expect(img).to(be_a(Image.Image))
            expect(img.width).to(be_above(0))
            expect(img.height).to(be_above(0))

    with context('gestion des colonnes'):
        with it('limite les colonnes au nombre de couleurs'):
            # 4 couleurs avec columns=10 -> seulement 4 colonnes
            img = self.renderer.render(layout="grid", cell_size=10, columns=10)
            expect(img.width).to(equal(40))  # 4 * 10, pas 10 * 10

        with it('gère une seule couleur'):
            single = PixelPalette()
            single.add_color(255, 0, 0, "Rouge")
            renderer = PaletteRenderer(single)
            img = renderer.render(layout="grid", cell_size=32, columns=8)
            expect(img.width).to(equal(32))
            expect(img.height).to(equal(32))
