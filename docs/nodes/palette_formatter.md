# Palette Formatter

Exports a palette as a formatted text string. Supports RGB, hex, raw tuple, and GIMP `.gpl` formats. Useful for copying palettes to external tools or saving them as text.

![Palette Formatter workflow](../screenshots/08_palette_formatter_workflow.png)

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
| palette | PIXEL_PALETTE | — | Palette to format |
| format_type | `rgb` \| `hex` \| `raw` \| `gimp` | rgb | Output format |
| separator | STRING | `\n` | Separator between color entries |
| include_header | BOOLEAN | True | Include format header (e.g. GIMP Palette header) |
| include_names | BOOLEAN | True | Include color names in output |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| formatted_text | STRING | The formatted palette text |

## Category

`pixel_art/output`
