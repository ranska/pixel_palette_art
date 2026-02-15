# spec/parsers/adobe_aco_parser_spec.py

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from lib.parsers.adobe_aco_parser import AdobeAcoParser
from mamba import description, context, it
from expects import expect, equal, be_true, be_false, be_empty


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
        with it('retourne une liste vide (implementation basique)'):
            parser = AdobeAcoParser()
            content = bytes([0x00, 0x01, 0x00, 0x05])
            result = parser.parse(content)
            expect(result).to(be_empty)
