# Color to Formatted String

Converts a `PIXEL_COLOR` to a formatted text string. Supports many common color formats including hex, RGB tuples, HSL, CSS custom properties, and GIMP palette lines.

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
| color | PIXEL_COLOR | — | Color to format |
| format_type | `hex` \| `hex_alpha` \| `rgb` \| `rgba` \| `tuple` \| `tuple_alpha` \| `hsl` \| `css` \| `gimp` | hex | Output format |
| alpha_value | FLOAT | 1.0 | Alpha as float 0.0–1.0 (for rgba/hex_alpha) |
| alpha_int | INT | 255 | Alpha as integer 0–255 (for tuple_alpha) |
| css_var_name | STRING | color | CSS custom property name (for css format) |
| gimp_index | INT | -1 | Column index in GIMP format (-1 = auto) |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| formatted_color | STRING | The formatted color string |

## Category

`pixel_art/output`
