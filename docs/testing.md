# Guide des tests BDD avec Mamba

## Pourquoi Mamba

Le projet utilise **Mamba** car l'auteur vient du monde Ruby/RSpec. Mamba est le framework Python le plus proche de RSpec avec sa syntaxe `description`/`context`/`it`.

- **Mamba** : https://github.com/nestorsalceda/mamba (framework BDD)
- **Expects** : bibliothèque de matchers (équivalent de `should` en RSpec)

## Commandes

```bash
# Commande standard (OBLIGATOIRE avant tout PR)
mamba spec/ --enable-coverage --format=documentation

# Tests rapides pendant le dev
mamba spec/ --format=documentation

# Un seul fichier spec
mamba spec/pixel_palette_spec.py --enable-coverage

# Un seul dossier de specs
mamba spec/color/ --format=documentation
```

## Structure des specs

Les specs sont organisées en miroir de `lib/` :

```
spec/
├── conftest.py                         # Configuration commune
├── pixel_color_spec.py                 # -> lib/pixel_color.py
├── pixel_palette_spec.py               # -> lib/pixel_palette.py
└── color/
    ├── color_space_registry_spec.py    # -> lib/color/color_space_registry.py
    ├── color_space_behavior_spec.py    # -> lib/color/color_space_context.py
    ├── rgb_exporter_spec.py            # -> lib/color/color_spaces/rgb/rgb_exporter.py
    └── color_spaces/
        ├── rgb/
        │   ├── rgb_mixer_spec.py       # -> lib/color/color_spaces/rgb/rgb_mixer.py
        │   └── rgb_exporter_spec.py    # -> lib/color/color_spaces/rgb/rgb_exporter.py
        └── hsv/
            └── hsv_mixer_spec.py       # -> lib/color/color_spaces/hsv/hsv_mixer.py
```

**Règle** : `spec_pending/` contient les specs désactivées (en cours de travail).

## Anatomie d'une spec

```python
# spec/pixel_color_spec.py

from spec.conftest import *                    # Config commune

from mamba import description, context, it, before
from expects import expect, equal, be_true     # Matchers

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.pixel_color import PixelColor         # Import du code testé


with description('PixelColor') as self:        # describe (le sujet)

    with context('Création et initialisation'):  # context (la situation)

        with it('crée une couleur noir par défaut'):  # it (le comportement attendu)
            color = PixelColor(0, 0, 0)
            expect(color.r).to(equal(0))

    with context('#to_hex'):                     # convention : #method pour les methodes

        with it('renvoie la couleur au format hexadécimal'):
            color = PixelColor(255, 128, 64)
            expect(color.to_hex()).to(equal("#FF8040"))
```

## Équivalences RSpec -> Mamba

| RSpec | Mamba | Rôle |
|-------|-------|------|
| `describe` | `description` | Bloc principal (sujet testé) |
| `context` | `context` | Bloc de contexte (situation) |
| `it` | `it` | Cas de test individuel |
| `before(:each)` | `before.each` | Setup avant chaque test |
| `expect(x).to eq(y)` | `expect(x).to(equal(y))` | Assertion |
| `let(:color)` | variable dans `before.each` | Lazy setup |

## Matchers expects courants

```python
from expects import (
    expect, equal, be_true, be_false, be_none,
    be_empty, have_length, contain,
    start_with, end_with,
    be_above, be_below, be_above_or_equal, be_below_or_equal,
    raise_error
)

# Égalité
expect(color.r).to(equal(255))

# Booléens
expect(palette.is_empty).to(be_true)

# Collections
expect(registry.available_spaces()).to(contain('rgb'))
expect(palette.colors).to(have_length(5))
expect(colors).to(be_empty)

# Chaines
expect(formatted).to(start_with("#"))
expect(formatted).to(end_with(";"))

# Erreurs
expect(lambda: registry.get_mixer_class('unknown')).to(
    raise_error(ValueError, 'Espace colorimétrique inconnu: unknown')
)

# Comparaisons
expect(color.r).to(be_above_or_equal(0))
expect(color.r).to(be_below_or_equal(255))
```

## Setup et teardown

```python
with description('ColorSpaceRegistry'):

    # Appelé avant chaque `it` dans tout le bloc description
    def before_each(self):
        ColorSpaceRegistry._spaces = {}  # Reset du registry

    with context('when registering'):

        with it('registers a space'):
            ColorSpaceRegistry.register('rgb', mock_exporter)
            expect(ColorSpaceRegistry.available_spaces()).to(contain('rgb'))
```

**Important** : les registries sont des singletons (variables de classe). Il faut les reset dans `before_each` pour éviter les effets de bord entre tests.

## Mocks

```python
from unittest.mock import Mock

mock_exporter = Mock()
mock_mixer = Mock()

ColorSpaceRegistry.register('rgb', mock_exporter, mock_mixer)
result = ColorSpaceRegistry.get_mixer_class('rgb')
expect(result).to(equal(mock_mixer))
```

Pour tester les exporters en isolation, un `MockPixelColor` existe :

```python
class MockPixelColor:
    def __init__(self, r, g, b, name=""):
        self.r = r
        self.g = g
        self.b = b
        self.name = name
```

## Données de test

Le fichier `mamba_config.py` fournit des palettes de test :

```python
from mamba_config import PALETTES_SAMPLES

SAMPLE_GIMP_PALETTE   # Format GIMP .gpl complet
SAMPLE_HEX_PALETTE    # Couleurs en hexadécimal
SAMPLE_RGB_PALETTE    # Couleurs en rgb()
MALFORMED_PALETTE     # Données invalides (tests d'erreur)
```

## Coverage

Configuration dans `.coveragerc` :

```ini
[run]
source = .
omit =
    */venv/*
    */tests/*
    */spec/*       # Les specs elles-memes
    */nodes/*      # Les nodes ComfyUI (non testés)
    __init__.py
    nodes.py
    mamba_config.py
```

**Philosophie** : on mesure la couverture de `lib/` uniquement. Les nodes ComfyUI sont des wrappers et ne sont pas testés unitairement.

Rapports HTML dans `htmlcov/`.

## Ce qui est testé vs ce qui ne l'est pas

### Testé (lib/)
- PixelColor : création, copie, hex, distance
- PixelPalette : gradient, monochrome, manipulation
- ColorSpaceRegistry : enregistrement, recherche, fusion, erreurs
- RGBMixer : mélange linéaire
- HSVMixer : mélange HSV
- RGBExporter : tous les formats de sortie (hex, rgb, hsl, css, gimp...)

### Non testé (volontairement)
- nodes/ : wrappers ComfyUI (tests d'intégration uniquement si nécessaire)
- __init__.py : registration ComfyUI

### Lacunes connues
- Parsers (gimp_parser, generic_parser, adobe_aco_parser) : pas de specs
- Palette exporters (gimp_exporter, hex_exporter, rgb_exporter au niveau palette) : pas de specs
- `spec_pending/` contient des tests désactivés a reprendre

## Écrire une nouvelle spec

Template pour un nouveau composant :

```python
# spec/parsers/gimp_parser_spec.py

from spec.conftest import *

from mamba import description, context, it, before
from expects import expect, equal, have_length, be_true, be_false

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from lib.parsers.gimp_parser import GimpParser


with description('GimpParser') as self:

    with before.each:
        self.parser = GimpParser()

    with context('#can_parse'):

        with it('returns True for valid GIMP palette content'):
            content = "GIMP Palette\nName: Test\n#\n255   0   0\tRouge"
            expect(self.parser.can_parse(content)).to(be_true)

        with it('returns False for non-GIMP content'):
            content = "#FF0000\n#00FF00"
            expect(self.parser.can_parse(content)).to(be_false)

    with context('#parse'):

        with it('extracts colors from GIMP palette'):
            content = "GIMP Palette\nName: Test\n#\n255   0   0\tRouge"
            colors = self.parser.parse(content)
            expect(colors).to(have_length(1))
            expect(colors[0].r).to(equal(255))
```
