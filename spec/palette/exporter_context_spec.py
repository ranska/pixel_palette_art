# spec/palette/exporter_context_spec.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from lib.palette.exporter_context import PaletteExporter
from lib.pixel_palette import PixelPalette
from lib.pixel_color import PixelColor
from mamba import description, context, it, before
from expects import expect, equal, be_a, have_length, raise_error, be_empty


with description('PaletteExporter') as self:

    with before.each:
        self.colors = [
            PixelColor(255, 0, 0, "Rouge"),
            PixelColor(0, 255, 0, "Vert"),
            PixelColor(0, 0, 255, "Bleu"),
        ]
        self.palette = PixelPalette(name="Test", colors=self.colors)

    with context('context manager'):
        with it('retourne self a l entree du context'):
            ctx = PaletteExporter(self.palette, 'rgb')
            result = ctx.__enter__()
            expect(result).to(equal(ctx))
            ctx.__exit__(None, None, None)

        with it('initialise l exporter dans le context'):
            with PaletteExporter(self.palette, 'rgb') as ctx:
                expect(ctx.exporter).not_to(equal(None))

    with context('export'):
        with it('retourne le contenu formate'):
            with PaletteExporter(self.palette, 'rgb') as ctx:
                result = ctx.export(include_names=True)
                expect(result).to(be_a(str))
                # Doit contenir les valeurs RGB
                expect('255' in result).to(equal(True))

        with it('passe les kwargs au exporter'):
            with PaletteExporter(self.palette, 'rgb') as ctx:
                result = ctx.export(separator=', ', include_names=False)
                # Separator virgule au lieu de newline
                expect(', ' in result).to(equal(True))

    with context('export_list'):
        with it('retourne une liste de strings'):
            with PaletteExporter(self.palette, 'rgb') as ctx:
                result = ctx.export_list()
                expect(result).to(have_length(3))
                expect(result[0]).to(be_a(str))

        with it('retourne une liste vide pour une palette vide'):
            empty_palette = PixelPalette(name="Vide", colors=[])
            with PaletteExporter(empty_palette, 'rgb') as ctx:
                result = ctx.export_list()
                expect(result).to(be_empty)

    with context('export_tuples'):
        with it('retourne des tuples RGB avec RGBExporter'):
            with PaletteExporter(self.palette, 'rgb') as ctx:
                result = ctx.export_tuples()
                expect(result).to(have_length(3))
                expect(result[0]).to(equal((255, 0, 0)))
                expect(result[1]).to(equal((0, 255, 0)))
                expect(result[2]).to(equal((0, 0, 255)))

        with it('retourne une liste vide avec GimpExporter (pas de export_tuples)'):
            with PaletteExporter(self.palette, 'gimp') as ctx:
                result = ctx.export_tuples()
                expect(result).to(be_empty)

    with context('appels hors context'):
        with it('export leve RuntimeError'):
            ctx = PaletteExporter(self.palette, 'rgb')
            expect(lambda: ctx.export()).to(raise_error(RuntimeError))

        with it('export_list leve RuntimeError'):
            ctx = PaletteExporter(self.palette, 'rgb')
            expect(lambda: ctx.export_list()).to(raise_error(RuntimeError))

        with it('export_tuples leve RuntimeError'):
            ctx = PaletteExporter(self.palette, 'rgb')
            expect(lambda: ctx.export_tuples()).to(raise_error(RuntimeError))
