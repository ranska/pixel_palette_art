# Architecture des Registries

## Philosophie

Le projet utilise le **pattern Registry** comme pilier architectural pour permettre l'ajout de nouveaux systemes de couleurs, formats d'export et formats de parsing sans modifier le code existant (principe Open/Closed).

Chaque registry fonctionne comme un annuaire : les composants s'y inscrivent a l'import, et le reste du code les retrouve par leur nom.

## Les trois registries

### 1. ColorSpaceRegistry

**Fichier** : `lib/color/color_space_registry.py`

Gere les espaces colorimétriques. Chaque espace peut avoir un **mixer** (mélange de couleurs) et/ou un **exporter** (conversion de format).

```python
class ColorSpaceRegistry:
    _spaces = {}  # {"rgb": {"exporter": RGBExporter, "mixer": RGBMixer}, ...}

    @classmethod
    def register(cls, name, exporter_class=None, mixer_class=None)

    @classmethod
    def get_mixer_class(cls, space_name) -> MixerClass

    @classmethod
    def get_exporter_class(cls, space_name) -> ExporterClass

    @classmethod
    def available_spaces(cls) -> List[str]
```

**Particularités** :
- Accepte l'enregistrement partiel (mixer seul OU exporter seul)
- Fusionne les enregistrements multiples (on peut enregistrer le mixer puis l'exporter séparément)
- Noms normalisés en minuscules (insensible a la casse)
- Leve `ValueError` si on demande un espace inconnu ou un mixer absent

**Espaces enregistrés** :
| Espace | Mixer | Exporter |
|--------|-------|----------|
| rgb    | RGBMixer | RGBExporter |
| hsv    | HSVMixer | - |

### 2. ExporterRegistry

**Fichier** : `lib/palette/exporters/exporter_registry.py`

Gere les formats d'export de palettes entieres.

```python
class ExporterRegistry:
    _exporters = {}  # {"gimp": GimpExporter, "hex": HexExporter, ...}

    @classmethod
    def register(cls, name, exporter_class)

    @classmethod
    def get_exporter_class(cls, format_name) -> ExporterClass

    @classmethod
    def available_formats(cls) -> List[str]
```

**Formats enregistrés** :
| Format | Classe | Description |
|--------|--------|-------------|
| gimp   | GimpExporter | Format GIMP .gpl |
| hex    | HexExporter  | Couleurs hexadécimales |
| rgb    | RGBExporter  | Format rgb(r,g,b) |

Chaque exporter hérite de `BaseExporter` (ABC) et implémente `export(colors, **kwargs) -> str`.

### 3. ParserRegistry

**Fichier** : `lib/parsers/parser_registry.py`

Gere les formats de parsing (lecture) de palettes.

```python
class ParserRegistry:
    _parsers = {}  # {"gimp": GimpParser, "generic": GenericParser, ...}

    @classmethod
    def register(cls, name, parser_class)

    @classmethod
    def get_parser_class(cls, format_name) -> ParserClass

    @classmethod
    def available_formats(cls) -> List[str]
```

**Parsers enregistrés** :
| Format | Classe | Détection |
|--------|--------|-----------|
| gimp   | GimpParser | Premiere ligne = "GIMP Palette" |
| generic | GenericParser | Fallback : hex (#RRGGBB) ou rgb(r,g,b) |
| adobe_aco | AdobeAcoParser | Format binaire Adobe (stub) |

Chaque parser hérite de `BaseParser` (ABC) et implémente :
- `can_parse(content) -> bool` : détection du format
- `parse(content) -> List[PixelColor]` : extraction des couleurs

## Mécanisme d'auto-enregistrement

L'enregistrement se fait dans les `__init__.py` de chaque module, exécutés au moment de l'import.

### Chaine d'initialisation

```
__init__.py (racine ComfyUI)
  └── import nodes
        └── import lib
              └── lib/__init__.py
                    ├── import color
                    │     └── color/__init__.py
                    │           └── import color_spaces
                    │                 └── color_spaces/__init__.py
                    │                       ├── import RGBMixer  → s'auto-enregistre
                    │                       └── import HSVMixer  → s'auto-enregistre
                    ├── import palette.exporters
                    │     └── exporters/__init__.py
                    │           ├── ExporterRegistry.register("gimp", GimpExporter)
                    │           ├── ExporterRegistry.register("hex", HexExporter)
                    │           └── ExporterRegistry.register("rgb", RGBExporter)
                    └── import parsers
                          └── parsers/__init__.py
                                ├── ParserRegistry.register("gimp", GimpParser)
                                ├── ParserRegistry.register("generic", GenericParser)
                                └── ParserRegistry.register("adobe_aco", AdobeAcoParser)
```

### Deux styles d'enregistrement

**Style 1 - Auto-enregistrement dans le composant** (ColorSpaceRegistry) :
Les mixers s'enregistrent eux-memes dans leur propre fichier.

```python
# lib/color/color_spaces/rgb/rgb_mixer.py
from ...color_space_registry import ColorSpaceRegistry

class RGBMixer:
    @staticmethod
    def mix_with(color_a, color_b, ratio):
        ...

ColorSpaceRegistry.register('rgb', mixer_class=RGBMixer)
```

**Style 2 - Enregistrement centralisé dans __init__.py** (ExporterRegistry, ParserRegistry) :

```python
# lib/palette/exporters/__init__.py
ExporterRegistry.register("gimp", GimpExporter)
ExporterRegistry.register("hex", HexExporter)
```

## Ajouter un composant

### Nouveau color space (ex: HSL)

```
lib/color/color_spaces/hsl/
├── __init__.py
├── hsl_mixer.py       # class HSLMixer avec mix_with() + auto-register
└── hsl_exporter.py    # class HSLExporter (optionnel)
```

1. Créer le dossier et les fichiers
2. Le mixer doit appeler `ColorSpaceRegistry.register('hsl', mixer_class=HSLMixer)` en fin de fichier
3. Importer le mixer dans `lib/color/color_spaces/__init__.py`
4. Tester dans `spec/color/color_spaces/hsl/`

### Nouvel exporter de palette (ex: CSS)

1. Créer `lib/palette/exporters/css_exporter.py` héritant de `BaseExporter`
2. Implémenter `export(colors, **kwargs) -> str`
3. Ajouter dans `lib/palette/exporters/__init__.py` :
   ```python
   ExporterRegistry.register("css", CSSExporter)
   ```
4. Tester dans `spec/palette/exporters/`

### Nouveau parser (ex: ASE Adobe Swatch Exchange)

1. Créer `lib/parsers/ase_parser.py` héritant de `BaseParser`
2. Implémenter `can_parse()` et `parse()`
3. Ajouter dans `lib/parsers/__init__.py` :
   ```python
   ParserRegistry.register("ase", AseParser)
   ```
4. Tester dans `spec/parsers/`

## Context Managers associés

### ColorSpaceContext

Permet de changer temporairement l'espace de couleur d'un `PixelColor` :

```python
color = PixelColor(255, 0, 0)  # color_space = "rgb"

with color.using_color_space("hsv"):
    mixed = color.mix_with(other, 0.5)  # utilise HSVMixer
# color_space restauré a "rgb" automatiquement
```

### PaletteExporter

Gere le cycle de vie de l'export d'une palette :

```python
with PaletteExporter(palette, "hex") as ctx:
    text = ctx.export(separator="\n", include_names=True)
    colors_list = ctx.export_list()
    tuples = ctx.export_tuples()
```

## Considérations pour les tests

Les registries utilisent des variables de classe (`_spaces`, `_exporters`, `_parsers`) qui persistent entre les tests. Il faut les réinitialiser :

```python
# Dans before.each
ColorSpaceRegistry._spaces = {}
# ou
ColorSpaceRegistry.reset()
```
