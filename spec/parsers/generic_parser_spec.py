# spec/parsers/generic_parser_spec.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from lib.parsers.generic_parser import GenericParser
from mamba import description, context, it
from expects import expect, equal, be_true, have_length, be_empty


with description('GenericParser') as self:

    with context('can_parse'):
        with it('accepte tout contenu'):
            parser = GenericParser()
            expect(parser.can_parse("anything")).to(be_true)

        with it('accepte une chaine vide'):
            parser = GenericParser()
            expect(parser.can_parse("")).to(be_true)

    with context('parse format hexadecimal'):
        with it('parse RRGGBB sans #'):
            parser = GenericParser()
            result = parser.parse("FF8000")
            expect(result).to(have_length(1))
            expect(result[0].r).to(equal(255))
            expect(result[0].g).to(equal(128))
            expect(result[0].b).to(equal(0))

        with it('parse hex avec un nom'):
            parser = GenericParser()
            result = parser.parse("FF8000 Orange")
            expect(result).to(have_length(1))
            expect(result[0].name).to(equal("Orange"))

        with it('parse plusieurs lignes hex'):
            parser = GenericParser()
            content = "FF0000\n00FF00\n0000FF"
            result = parser.parse(content)
            expect(result).to(have_length(3))

        with it('parse hex en minuscules'):
            parser = GenericParser()
            result = parser.parse("ff8000")
            expect(result).to(have_length(1))
            expect(result[0].r).to(equal(255))

        with it('ignore les lignes commencant par # (commentaires)'):
            parser = GenericParser()
            result = parser.parse("#FF8000")
            expect(result).to(be_empty)

    with context('parse format RGB'):
        with it('parse rgb(r,g,b)'):
            parser = GenericParser()
            result = parser.parse("rgb(255,128,0)")
            expect(result).to(have_length(1))
            expect(result[0].r).to(equal(255))
            expect(result[0].g).to(equal(128))
            expect(result[0].b).to(equal(0))

        with it('parse r,g,b sans prefix'):
            parser = GenericParser()
            result = parser.parse("255,128,0")
            expect(result).to(have_length(1))
            expect(result[0].r).to(equal(255))

        with it('parse r g b separes par des espaces'):
            parser = GenericParser()
            result = parser.parse("255 128 0")
            expect(result).to(have_length(1))
            expect(result[0].r).to(equal(255))

        with it('parse rgb avec un nom'):
            parser = GenericParser()
            result = parser.parse("255,128,0 Orange")
            expect(result).to(have_length(1))
            expect(result[0].name).to(equal("Orange"))

    with context('lignes speciales'):
        with it('ignore les lignes vides'):
            parser = GenericParser()
            content = "FF0000\n\n00FF00"
            result = parser.parse(content)
            expect(result).to(have_length(2))

        with it('ignore les commentaires #'):
            parser = GenericParser()
            content = "# ceci est un commentaire\n255,0,0"
            result = parser.parse(content)
            expect(result).to(have_length(1))

        with it('ignore les lignes non reconnues'):
            parser = GenericParser()
            content = "pas une couleur\nFF0000"
            result = parser.parse(content)
            expect(result).to(have_length(1))

    with context('contenu vide'):
        with it('retourne une liste vide'):
            parser = GenericParser()
            result = parser.parse("")
            expect(result).to(be_empty)
