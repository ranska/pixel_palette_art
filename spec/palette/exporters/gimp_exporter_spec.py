# spec/palette/exporters/gimp_exporter_spec.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from lib.palette.exporters.gimp_exporter import GimpExporter
from lib.pixel_color import PixelColor
from mamba import description, context, it
from expects import expect, equal, contain


with description('GimpExporter') as self:

    with context('export basique'):
        with it('genere le header GIMP Palette'):
            exporter = GimpExporter()
            colors = [PixelColor(255, 0, 0, "Rouge")]
            result = exporter.export(colors)
            expect(result).to(contain("GIMP Palette"))

        with it('exporte une couleur avec son nom'):
            exporter = GimpExporter()
            colors = [PixelColor(255, 128, 0, "Orange")]
            result = exporter.export(colors)
            expect(result).to(contain("255 128   0\tOrange"))

        with it('exporte une couleur sans nom'):
            exporter = GimpExporter()
            colors = [PixelColor(0, 0, 0)]
            result = exporter.export(colors)
            lines = result.split('\n')
            # La ligne de couleur ne doit pas avoir de tab (pas de nom)
            expect(lines[-1]).to(equal("  0   0   0"))

        with it('exporte plusieurs couleurs'):
            exporter = GimpExporter()
            colors = [
                PixelColor(255, 0, 0, "Rouge"),
                PixelColor(0, 255, 0, "Vert"),
                PixelColor(0, 0, 255, "Bleu"),
            ]
            result = exporter.export(colors)
            lines = result.split('\n')
            # header + # + 3 couleurs
            expect(len(lines)).to(equal(5))

        with it('inclut le separateur # apres le header'):
            exporter = GimpExporter()
            colors = [PixelColor(255, 0, 0)]
            result = exporter.export(colors)
            lines = result.split('\n')
            expect(lines[1]).to(equal("#"))

    with context('avec metadata'):
        with it('inclut le nom de la palette'):
            exporter = GimpExporter()
            colors = [PixelColor(255, 0, 0, "Rouge")]
            metadata = {'name': 'Ma Palette'}
            result = exporter.export(colors, metadata=metadata)
            expect(result).to(contain("Name: Ma Palette"))

        with it('inclut le nombre de colonnes'):
            exporter = GimpExporter()
            colors = [PixelColor(255, 0, 0, "Rouge")]
            metadata = {'columns': 8}
            result = exporter.export(colors, metadata=metadata)
            expect(result).to(contain("Columns: 8"))

        with it('inclut name et columns ensemble'):
            exporter = GimpExporter()
            colors = [PixelColor(255, 0, 0)]
            metadata = {'name': 'Test', 'columns': 16}
            result = exporter.export(colors, metadata=metadata)
            expect(result).to(contain("Name: Test"))
            expect(result).to(contain("Columns: 16"))

    with context('sans metadata'):
        with it('fonctionne sans metadata'):
            exporter = GimpExporter()
            colors = [PixelColor(255, 0, 0)]
            result = exporter.export(colors)
            lines = result.split('\n')
            expect(lines[0]).to(equal("GIMP Palette"))
            expect(lines[1]).to(equal("#"))

    with context('palette vide'):
        with it('exporte uniquement le header'):
            exporter = GimpExporter()
            result = exporter.export([])
            expect(result).to(equal("GIMP Palette\n#"))
