# lib/parsers/base_parser.py

from abc import ABC, abstractmethod
from typing import List, Optional
from ..pixel_color import PixelColor

class BaseParser(ABC):
    """Classe de base pour les parsers de palettes."""

    @abstractmethod
    def can_parse(self, content: str) -> bool:
        """Détermine si ce parser peut traiter le contenu."""
        pass

    @abstractmethod
    def parse(self, content: str) -> List[PixelColor]:
        """Parse le contenu et retourne la liste des couleurs."""
        pass