# spec/palette/exporters/css_exporter_spec.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

from lib.palette.exporters.css_exporter import CSSExporter
from lib.pixel_color import PixelColor
from mamba import description, context, it
from expects import expect, equal, contain, start_with, end_with


with description('CSSExporter') as self:

    with context('export basique'):
        with it('utilise le selecteur :root par defaut'):
            exporter = CSSExporter()
            colors = [PixelColor(255, 0, 0, "Red")]
            result = exporter.export(colors)
            expect(result).to(start_with(":root {"))

        with it('ferme le bloc avec une accolade'):
            exporter = CSSExporter()
            colors = [PixelColor(255, 0, 0, "Red")]
            result = exporter.export(colors)
            expect(result).to(end_with("}"))

        with it('exporte une couleur avec son nom'):
            exporter = CSSExporter()
            colors = [PixelColor(255, 0, 0, "Red")]
            result = exporter.export(colors)
            expect(result).to(contain("--red: #ff0000;"))

        with it('exporte une couleur sans nom avec un index'):
            exporter = CSSExporter()
            colors = [PixelColor(0, 0, 255)]
            result = exporter.export(colors)
            expect(result).to(contain("--color-0: #0000ff;"))

        with it('exporte plusieurs couleurs'):
            exporter = CSSExporter()
            colors = [
                PixelColor(255, 0, 0, "Red"),
                PixelColor(0, 255, 0, "Green"),
                PixelColor(0, 0, 255, "Blue"),
            ]
            result = exporter.export(colors)
            expect(result).to(contain("--red: #ff0000;"))
            expect(result).to(contain("--green: #00ff00;"))
            expect(result).to(contain("--blue: #0000ff;"))

    with context('include_names=False'):
        with it('utilise des index pour toutes les couleurs'):
            exporter = CSSExporter()
            colors = [
                PixelColor(255, 0, 0, "Red"),
                PixelColor(0, 255, 0, "Green"),
            ]
            result = exporter.export(colors, include_names=False)
            expect(result).to(contain("--color-0: #ff0000;"))
            expect(result).to(contain("--color-1: #00ff00;"))

    with context('selecteur personnalise'):
        with it('utilise le selecteur fourni'):
            exporter = CSSExporter()
            colors = [PixelColor(255, 0, 0, "Red")]
            result = exporter.export(colors, selector=".palette")
            expect(result).to(start_with(".palette {"))

    with context('sanitisation CSS'):
        with it('convertit les espaces en tirets'):
            result = CSSExporter._sanitize_css_name("Dark Red")
            expect(result).to(equal("dark-red"))

        with it('convertit les underscores en tirets'):
            result = CSSExporter._sanitize_css_name("dark_red")
            expect(result).to(equal("dark-red"))

        with it('supprime les caracteres speciaux'):
            result = CSSExporter._sanitize_css_name("rouge@#$!")
            expect(result).to(equal("rouge"))

        with it('passe en lowercase'):
            result = CSSExporter._sanitize_css_name("ROUGE")
            expect(result).to(equal("rouge"))

        with it('supprime les tirets multiples'):
            result = CSSExporter._sanitize_css_name("dark - - red")
            expect(result).to(equal("dark-red"))

        with it('retourne une chaine vide pour un nom sans caracteres valides'):
            result = CSSExporter._sanitize_css_name("@#$!")
            expect(result).to(equal(""))

    with context('palette vide'):
        with it('exporte un bloc vide'):
            exporter = CSSExporter()
            result = exporter.export([])
            expect(result).to(equal(":root {\n}"))
