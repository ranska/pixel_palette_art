# Copy Subset

Extracts a contiguous range of colors from a palette, creating a new smaller palette. Both start and end indices are inclusive.

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
| palette | PIXEL_PALETTE | — | Source palette |
| start_index | INT | 0 | First color index to include (0–255) |
| end_index | INT | 3 | Last color index to include (0–255) |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| subset | PIXEL_PALETTE | The extracted sub-palette |

## Category

`pixel_art/palette`
