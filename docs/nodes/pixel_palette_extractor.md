# Pixel Palette Extractor

Extracts unique colors from an image and renders them as a palette grid. Useful for analyzing the color composition of pixel art or any image.

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
| image | IMAGE | — | Source image |
| palette_width | INT | 16 | Number of colors per row (1–32) |
| color_size | INT | 32 | Size of each color cell in pixels (8–128) |
| show_indices | BOOLEAN | False | Show color indices on each cell |
| font_size | INT | 10 | Font size for index labels (6–24) |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| palette_image | IMAGE | The rendered palette image |

## Category

`image/color`
