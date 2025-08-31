# Pixel Palette Art - Agent Configuration

## Vue d'ensemble
Projet de nœuds ComfyUI pour manipulation de palettes de couleurs pixel art.
Architecture orientée espaces de couleur avec séparation claire lib/nodes.

## Testing Strategy
- **Framework**: Mamba (BDD framework Python)
- **Coverage**: Activé systématiquement avec `--enable-coverage`
- **Flag obligatoire**: `--format=documentation` pour sortie lisible
- **Commande standard**: `mamba spec/ --enable-coverage --format=documentation`

## Architecture Orientée Color Spaces
```
lib/
├── color/
│   ├── color_spaces/     # Espaces RGB, HSV, etc.
│   │   ├── rgb/         # Mixers et exporters RGB
│   │   └── hsv/         # Mixers HSV avec interpolation circulaire
│   ├── color_space_context.py    # Context pour changement d'espace
│   └── color_space_registry.py   # Registre des espaces disponibles
├── pixel_color.py       # Classe PixelColor avec méthodes de blend
└── pixel_palette.py     # Gestion palettes avec create_gradient()
```

### Points clés architecture :
- **Séparation claire** : logique métier (lib/) vs interface ComfyUI (nodes/)
- **Extensible** : nouveaux espaces de couleur faciles à ajouter
- **Testable** : toute la logique dans lib/ est testée, nodes/ seulement intégration

## Règles de développement
- ✅ **Tester lib/** : Tous les composants métier doivent avoir des specs
- ❌ **Ne pas tester nodes/** : Les nœuds ComfyUI sont des wrappers d'intégration
- 🔄 **Coverage obligatoire** : Toujours lancer avec `--enable-coverage`
- 📚 **Documentation** : Format documentation pour lisibilité des tests

## Development Commands

### Testing
```bash
# Tests complets avec coverage (OBLIGATOIRE)
mamba spec/ --enable-coverage --format=documentation

# Tests rapides (développement)
mamba spec/ --format=documentation

# Tests d'un module spécifique
mamba spec/pixel_palette_spec.py --enable-coverage
```

### Development Setup
```bash
pip install -r requirements-dev.txt
```

### Linting (if available)
```bash
# Add linting commands here when implemented
# ruff check .  # Example
# black --check .  # Example
```

## Git Workflow
- Uses Git Flow
- Default branch: `develop`
- Main branches: `main`, `develop`
- Feature branches: `feature/*`
- Release branches: `release/*`
- Hotfix branches: `hotfix/*`

## Project Structure
- `lib/`: Core color manipulation libraries (TESTÉ)
- `nodes/`: ComfyUI custom nodes (NON TESTÉ - wrappers d'intégration)
- `spec/`: Test specifications (Mamba)
- `docs/`: Documentation and images

## Common Tasks
- Run tests before PR: `mamba spec/ --enable-coverage --format=documentation`
- Extract palette from image: Use PixelPaletteExtractor node
- Load GIMP palettes: Use gimp_gpl_loader node
- Mix colors: Use color mixer nodes (RGB/HSV)
- Create gradients: Use PixelPalette.create_gradient(index1, index2, color_space)

## Évolution future
- Ajout d'espaces HSL, LAB, etc.
- Tests d'intégration ComfyUI (si nécessaire)
- Benchmarks de performance des mixers
- Nouveaux algorithmes de génération de palettes
