# lib/color/color_space_registry.py

class ColorSpaceRegistry:
    """Registry pour gérer les différents espaces colorimétriques."""

    _spaces = {}

    @classmethod
    def register(cls, name, exporter_class, mixer_class=None):
        cls._spaces[name.lower()] = {
            'exporter': exporter_class,
            'mixer': mixer_class
        }

    @classmethod
    def get_exporter_class(cls, space_name):
        space = space_name.lower()
        if space not in cls._spaces:
            raise ValueError(f"Espace colorimétrique inconnu: {space}. "
                           f"Disponibles: {list(cls._spaces.keys())}")
        return cls._spaces[space]['exporter']

    @classmethod
    def get_mixer_class(cls, space_name):
        space = space_name.lower()
        if space not in cls._spaces:
            raise ValueError(f"Espace colorimétrique inconnu: {space}")
        mixer = cls._spaces[space]['mixer']
        if mixer is None:
            raise ValueError(f"Pas de mixer disponible pour: {space}")
        return mixer

    @classmethod
    def available_spaces(cls):
        return list(cls._spaces.keys())

    @classmethod
    def get_space_info(cls, space_name):
        space = space_name.lower()
        if space not in cls._spaces:
            raise ValueError(f"Espace colorimétrique inconnu: {space}")
        return cls._spaces[space].copy()
