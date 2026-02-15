# Create Color From RGB

Creates a `PIXEL_COLOR` from individual red, green and blue channel values, with an optional name.

This is the primary way to define a color for use with other Pixel Palette Art nodes.

![Create Color From RGB](../create_color.png)

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
| red | INT | 255 | Red channel (0–255) |
| green | INT | 0 | Green channel (0–255) |
| blue | INT | 0 | Blue channel (0–255) |
| color_name | STRING | *(empty)* | Optional color name |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| color | PIXEL_COLOR | The created color |

## Category

`pixel_art/colors`
