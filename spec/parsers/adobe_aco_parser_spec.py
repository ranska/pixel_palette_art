# spec/parsers/adobe_aco_parser_spec.py

import sys
import os
import struct
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from lib.parsers.adobe_aco_parser import AdobeAcoParser
from mamba import description, context, it
from expects import expect, equal, be_true, be_false, be_empty, have_length


def _build_aco_header(num_colors):
    """Construit le header ACO v1 : version 1 + nombre de couleurs"""
    return struct.pack('>HH', 1, num_colors)


def _build_rgb_entry(r, g, b):
    """Construit un bloc couleur RGB ACO (color space 0, valeurs 0-65535)"""
    w = round(r * 65535 / 255)
    x = round(g * 65535 / 255)
    y = round(b * 65535 / 255)
    return struct.pack('>HHHHH', 0, w, x, y, 0)


def _build_non_rgb_entry(color_space=1):
    """Construit un bloc couleur non-RGB (ex: HSB = 1)"""
    return struct.pack('>HHHHH', color_space, 0, 0, 0, 0)


with description('AdobeAcoParser') as self:

    with context('can_parse'):
        with it('detecte un fichier ACO valide (bytes)'):
            parser = AdobeAcoParser()
            content = bytes([0x00, 0x01, 0x00, 0x05])
            expect(parser.can_parse(content)).to(be_true)

        with it('refuse un fichier avec mauvais magic bytes'):
            parser = AdobeAcoParser()
            content = bytes([0x01, 0x00, 0x00, 0x05])
            expect(parser.can_parse(content)).to(be_false)

        with it('refuse un fichier trop court'):
            parser = AdobeAcoParser()
            content = bytes([0x00])
            expect(parser.can_parse(content)).to(be_false)

        with it('refuse une chaine de caracteres'):
            parser = AdobeAcoParser()
            expect(parser.can_parse("not binary")).to(be_false)

        with it('refuse un bytes vide'):
            parser = AdobeAcoParser()
            expect(parser.can_parse(b'')).to(be_false)

    with context('parse'):
        with it('parse une couleur RGB'):
            parser = AdobeAcoParser()
            content = _build_aco_header(1) + _build_rgb_entry(255, 0, 0)
            result = parser.parse(content)
            expect(result).to(have_length(1))
            expect(result[0].r).to(equal(255))
            expect(result[0].g).to(equal(0))
            expect(result[0].b).to(equal(0))

        with it('parse plusieurs couleurs RGB'):
            parser = AdobeAcoParser()
            content = (_build_aco_header(3)
                       + _build_rgb_entry(255, 0, 0)
                       + _build_rgb_entry(0, 255, 0)
                       + _build_rgb_entry(0, 0, 255))
            result = parser.parse(content)
            expect(result).to(have_length(3))
            expect(result[0].r).to(equal(255))
            expect(result[1].g).to(equal(255))
            expect(result[2].b).to(equal(255))

        with it('ignore les couleurs non-RGB'):
            parser = AdobeAcoParser()
            content = (_build_aco_header(3)
                       + _build_rgb_entry(255, 0, 0)
                       + _build_non_rgb_entry(1)    # HSB, ignoré
                       + _build_rgb_entry(0, 0, 255))
            result = parser.parse(content)
            expect(result).to(have_length(2))
            expect(result[0].r).to(equal(255))
            expect(result[1].b).to(equal(255))

        with it('retourne liste vide pour 0 couleurs'):
            parser = AdobeAcoParser()
            content = _build_aco_header(0)
            result = parser.parse(content)
            expect(result).to(be_empty)

        with it('gere un fichier tronque en retournant les couleurs lisibles'):
            parser = AdobeAcoParser()
            # Annonce 3 couleurs mais n'en fournit qu'une complete
            content = _build_aco_header(3) + _build_rgb_entry(128, 64, 32) + b'\x00\x00'
            result = parser.parse(content)
            expect(result).to(have_length(1))
            expect(result[0].r).to(equal(128))
            expect(result[0].g).to(equal(64))
            expect(result[0].b).to(equal(32))

        with it('retourne liste vide si content trop court pour le header'):
            parser = AdobeAcoParser()
            result = parser.parse(bytes([0x00, 0x01]))
            expect(result).to(be_empty)

        with it('retourne liste vide si content n est pas bytes'):
            parser = AdobeAcoParser()
            result = parser.parse("not binary")
            expect(result).to(be_empty)
