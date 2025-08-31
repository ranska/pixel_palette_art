# lib/palette/exporters/exporter_registry.py

class ExporterRegistry:
    """Registry pour gérer les différents exporteurs de palettes."""

    _exporters = {}

    @classmethod
    def register(cls, name, exporter_class):
        """Enregistre un exporteur."""
        key = name.lower()
        cls._exporters[key] = exporter_class

    @classmethod
    def reset(cls):
        """Réinitialise complètement le registre."""
        cls._exporters.clear()

    @classmethod
    def get_exporter_class(cls, format_name):
        format_key = format_name.lower()
        if format_key not in cls._exporters:
            raise ValueError(f"Format d'export inconnu: {format_key}. "
                           f"Disponibles: {list(cls._exporters.keys())}")
        return cls._exporters[format_key]

    @classmethod
    def available_formats(cls):
        return list(cls._exporters.keys())