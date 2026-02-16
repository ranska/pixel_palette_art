# spec/palette/exporters/amiga_exporter_spec.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from lib.palette.exporters.amiga_exporter import AmigaExporter
from lib.pixel_color import PixelColor
from mamba import description, context, it
from expects import expect, equal, contain, start_with, end_with


with description('AmigaExporter') as self:

    with context('quantize_channel'):
        with it('quantifie 0 en 0'):
            expect(AmigaExporter.quantize_channel(0)).to(equal(0))

        with it('quantifie 255 en 15'):
            expect(AmigaExporter.quantize_channel(255)).to(equal(15))

        with it('quantifie 128 en 8'):
            expect(AmigaExporter.quantize_channel(128)).to(equal(8))

        with it('quantifie 17 en 1'):
            expect(AmigaExporter.quantize_channel(17)).to(equal(1))

    with context('format txt'):
        with it('exporte une couleur en #RGB'):
            exporter = AmigaExporter()
            colors = [PixelColor(255, 0, 0)]
            result = exporter.export(colors)
            expect(result).to(equal("#F00"))

        with it('exporte plusieurs couleurs'):
            exporter = AmigaExporter()
            colors = [
                PixelColor(255, 0, 0),
                PixelColor(0, 255, 0),
                PixelColor(0, 0, 255),
            ]
            result = exporter.export(colors)
            lines = result.split('\n')
            expect(len(lines)).to(equal(3))
            expect(lines[0]).to(equal("#F00"))
            expect(lines[1]).to(equal("#0F0"))
            expect(lines[2]).to(equal("#00F"))

        with it('inclut les noms quand demande'):
            exporter = AmigaExporter()
            colors = [PixelColor(255, 0, 0, "Rouge")]
            result = exporter.export(colors, include_names=True)
            expect(result).to(contain("/* Rouge */"))

        with it('exporte blanc en #FFF'):
            exporter = AmigaExporter()
            colors = [PixelColor(255, 255, 255)]
            result = exporter.export(colors)
            expect(result).to(equal("#FFF"))

        with it('exporte noir en #000'):
            exporter = AmigaExporter()
            colors = [PixelColor(0, 0, 0)]
            result = exporter.export(colors)
            expect(result).to(equal("#000"))

    with context('format c'):
        with it('inclut le header avec le nom de palette'):
            exporter = AmigaExporter()
            colors = [PixelColor(255, 0, 0)]
            result = exporter.export(colors, output_format='c', palette_name='Test')
            expect(result).to(contain("// Palette: Test"))

        with it('inclut PALETTE_SIZE'):
            exporter = AmigaExporter()
            colors = [PixelColor(255, 0, 0), PixelColor(0, 255, 0)]
            result = exporter.export(colors, output_format='c')
            expect(result).to(contain("#define PALETTE_SIZE 2"))

        with it('genere un tableau UWORD'):
            exporter = AmigaExporter()
            colors = [PixelColor(255, 0, 0)]
            result = exporter.export(colors, output_format='c')
            expect(result).to(contain("UWORD palette[] = {"))

        with it('exporte les valeurs 12-bit correctement'):
            exporter = AmigaExporter()
            colors = [PixelColor(255, 0, 0)]
            result = exporter.export(colors, output_format='c')
            expect(result).to(contain("0x0F00"))

        with it('termine le tableau avec un point-virgule'):
            exporter = AmigaExporter()
            colors = [PixelColor(255, 0, 0)]
            result = exporter.export(colors, output_format='c')
            expect(result).to(end_with("};"))

        with it('pas de virgule apres le dernier element'):
            exporter = AmigaExporter()
            colors = [
                PixelColor(255, 0, 0, "Rouge"),
                PixelColor(0, 255, 0, "Vert"),
            ]
            result = exporter.export(colors, output_format='c', include_names=True)
            lines = result.split('\n')
            # Avant-derniere ligne = dernier element (sans virgule)
            last_entry = lines[-2]
            expect(last_entry).to(contain("0x00F0"))
            expect(last_entry).not_to(contain(","))
            # L'avant-avant-derniere doit avoir une virgule
            first_entry = lines[-3]
            expect(first_entry).to(contain("0x0F00,"))

        with it('inclut les noms en commentaires'):
            exporter = AmigaExporter()
            colors = [PixelColor(255, 0, 0, "Rouge")]
            result = exporter.export(colors, output_format='c', include_names=True)
            expect(result).to(contain("/* Rouge */"))

    with context('palette vide'):
        with it('retourne une chaine vide en format txt'):
            exporter = AmigaExporter()
            result = exporter.export([])
            expect(result).to(equal(""))

        with it('genere un tableau vide en format c'):
            exporter = AmigaExporter()
            result = exporter.export([], output_format='c')
            expect(result).to(contain("#define PALETTE_SIZE 0"))
            expect(result).to(contain("UWORD palette[] = {"))
            expect(result).to(contain("};"))
