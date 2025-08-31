# lib/parsers/__init__.py

from .base_parser import BaseParser
from .parser_registry import ParserRegistry
from .gimp_parser import GimpParser
from .generic_parser import GenericParser
from .adobe_aco_parser import AdobeAcoParser

# Enregistrer les parsers
ParserRegistry.register("gimp", GimpParser)
ParserRegistry.register("generic", GenericParser)
ParserRegistry.register("adobe_aco", AdobeAcoParser)