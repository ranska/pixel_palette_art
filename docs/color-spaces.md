# Systeme d'espaces colorimétriques

## Concepts

Un **espace colorimétrique** (color space) définit comment les couleurs sont représentées et manipulées. Chaque espace a potentiellement :

- Un **Mixer** : algorithme de mélange entre deux couleurs
- Un **Exporter** : conversion vers des formats texte (hex, rgb, hsl...)

Le systeme permet de mélanger des couleurs dans différents espaces pour obtenir des résultats perceptuellement différents.

## Espaces disponibles

### RGB (Red, Green, Blue)

**Mixer** : `lib/color/color_spaces/rgb/rgb_mixer.py`
**Exporter** : `lib/color/color_spaces/rgb/rgb_exporter.py`

Le mixer RGB fait une **interpolation linéaire** sur chaque canal :

```python
r = int(color_a.r * (1 - ratio) + color_b.r * ratio)
g = int(color_a.g * (1 - ratio) + color_b.g * ratio)
b = int(color_a.b * (1 - ratio) + color_b.b * ratio)
```

Simple et rapide, mais les dégradés peuvent paraitre "ternes" car le mélange n'est pas perceptuellement uniforme.

L'exporter RGB fournit de nombreux formats de sortie :
- `to_hex()` : `#FF8000`
- `to_hex_alpha(alpha)` : `#FF8000FF`
- `to_rgb_string()` : `rgb(255, 128, 0)`
- `to_rgba_string(alpha)` : `rgba(255, 128, 0, 1.0)`
- `to_rgb_tuple()` : `(255, 128, 0)`
- `to_rgba_tuple(alpha)` : `(255, 128, 0, 255)`
- `to_hsl_string()` : `hsl(30, 100%, 50%)`
- `to_css_var(name)` : `--name: #FF8000;`
- `to_gimp_palette_line(index)` : `255 128   0	Orange`

### HSV (Hue, Saturation, Value)

**Mixer** : `lib/color/color_spaces/hsv/hsv_mixer.py`
**Exporter** : aucun (utilise l'exporter RGB pour la sortie)

Le mixer HSV convertit en HSV, interpole, puis reconvertit en RGB :

```python
h1, s1, v1 = colorsys.rgb_to_hsv(r1/255, g1/255, b1/255)
h2, s2, v2 = colorsys.rgb_to_hsv(r2/255, g2/255, b2/255)

# Interpolation avec gestion du wraparound de la teinte
h = h1 + ratio * delta_h  # chemin le plus court sur le cercle
s = s1 * (1-ratio) + s2 * ratio
v = v1 * (1-ratio) + v2 * ratio
```

Le HSV produit des dégradés plus naturels car il suit le cercle chromatique. Le mélange rouge-vert passe par le jaune/orange au lieu du brun terne du RGB.

## Utilisation dans le code

### Mélange direct (espace par défaut)

```python
from lib.pixel_color import PixelColor

red = PixelColor(255, 0, 0)
blue = PixelColor(0, 0, 255)

# Mix en RGB (espace par défaut)
purple = red.create_copy()
purple.mix_with(blue, 0.5)
# -> (127, 0, 127)
```

### Mélange avec changement d'espace

```python
red = PixelColor(255, 0, 0)
green = PixelColor(0, 255, 0)

mixed = red.create_copy()
with mixed.using_color_space("hsv"):
    mixed.mix_with(green, 0.5)
# mixed.color_space est restauré a "rgb"
# mais le mélange a été fait en HSV -> jaune vif au lieu de brun
```

### Dégradé dans une palette

```python
palette = PixelPalette()
palette.add_color(255, 0, 0, "Rouge")     # index 0
palette.add_color(128, 128, 128, "Gris")  # index 1
palette.add_color(128, 128, 128, "Gris")  # index 2
palette.add_color(0, 0, 255, "Bleu")      # index 3

# Remplace les couleurs entre index 0 et 3 par un dégradé HSV
palette.create_gradient(0, 3, color_space="hsv")
```

## Ajouter un nouvel espace

### Exemple : HSL (Hue, Saturation, Lightness)

1. Créer la structure :

```
lib/color/color_spaces/hsl/
├── __init__.py
└── hsl_mixer.py
```

2. Implémenter le mixer :

```python
# lib/color/color_spaces/hsl/hsl_mixer.py
import colorsys
from ...color_space_registry import ColorSpaceRegistry

class HSLMixer:
    @staticmethod
    def mix_with(color_a, color_b, ratio=0.5):
        # Convertir RGB -> HLS (attention : colorsys utilise HLS pas HSL)
        h1, l1, s1 = colorsys.rgb_to_hls(color_a.r/255, color_a.g/255, color_a.b/255)
        h2, l2, s2 = colorsys.rgb_to_hls(color_b.r/255, color_b.g/255, color_b.b/255)

        # Interpoler
        h = h1 + (h2 - h1) * ratio
        l = l1 + (l2 - l1) * ratio
        s = s1 + (s2 - s1) * ratio

        # Reconvertir HLS -> RGB
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r * 255), int(g * 255), int(b * 255)

# Auto-enregistrement
ColorSpaceRegistry.register('hsl', mixer_class=HSLMixer)
```

3. Enregistrer l'import dans `lib/color/color_spaces/__init__.py` :

```python
from .hsl.hsl_mixer import HSLMixer
```

4. Écrire les specs :

```python
# spec/color/color_spaces/hsl/hsl_mixer_spec.py
from mamba import description, context, it, before
from expects import expect, equal

with description('HSLMixer'):
    with context('when mixing two colors'):
        with it('interpolates in HSL space'):
            ...
```

## Comparaison visuelle des mélanges

```
Rouge (255,0,0) + Vert (0,255,0) a ratio 0.5 :
  RGB -> (127, 127, 0)   brun/olive terne
  HSV -> (255, 255, 0)   jaune vif (passe par le cercle chromatique)
  HSL -> resultats similaires a HSV mais luminosité différente
```

## Diagramme de flux

```
PixelColor.mix_with(other, ratio)
  │
  ├── Regarde self.color_space ("rgb", "hsv", etc.)
  │
  ├── ColorSpaceRegistry.get_mixer_class(color_space)
  │     └── Retourne la classe du mixer
  │
  ├── mixer.mix_with(self, other, ratio)
  │     └── Retourne (r, g, b) tuple
  │
  └── Met a jour self.r, self.g, self.b
```
