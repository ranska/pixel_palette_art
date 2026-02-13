# lib/parsers/parser_registry.py

class ParserRegistry:
    """Registry pour gérer les différents parsers de palettes."""

    _parsers = {}

    @classmethod
    def register(cls, name, parser_class):
        """Enregistre un parser."""
        key = name.lower()
        cls._parsers[key] = parser_class

    @classmethod
    def reset(cls):
        """Réinitialise complètement le registre."""
        cls._parsers.clear()

    @classmethod
    def get_parser_class(cls, format_name):
        format_key = format_name.lower()
        if format_key not in cls._parsers:
            raise ValueError(f"Format inconnu: {format_key}. "
                           f"Disponibles: {list(cls._parsers.keys())}")
        return cls._parsers[format_key]

    @classmethod
    def available_formats(cls):
        return list(cls._parsers.keys())