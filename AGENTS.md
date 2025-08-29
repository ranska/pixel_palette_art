# Pixel Palette Art - Agent Configuration

## Project Info
- **Language**: Python
- **Framework**: ComfyUI Custom Nodes
- **Purpose**: Pixel art palette manipulation tools
- **Testing**: Mamba (BDD framework)

## Development Commands

### Testing
```bash
mamba spec/
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
- `lib/`: Core color manipulation libraries
- `nodes/`: ComfyUI custom nodes
- `spec/`: Test specifications (Mamba)
- `docs/`: Documentation and images

## Common Tasks
- Run tests before PR: `mamba spec/`
- Extract palette from image: Use PixelPaletteExtractor node
- Load GIMP palettes: Use gimp_gpl_loader node
- Mix colors: Use color mixer nodes (RGB/HSV)