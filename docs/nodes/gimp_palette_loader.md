# GIMP Palette Loader

Loads a palette file in GIMP `.gpl`, `.pal`, or Adobe `.aco` format. Files must be placed in the ComfyUI `input` directory.

Many `.gpl` palettes are available on [Lospec](https://lospec.com/).

![GIMP Palette Loader](../gimp_gpl_loader.png)

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
| palette_file | FILE | — | Palette file to load (.gpl, .pal, .aco) |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| palette | PIXEL_PALETTE | The loaded palette |

## Category

`pixel_art/io`
