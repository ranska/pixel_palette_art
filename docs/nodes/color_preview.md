# Color Preview

Renders a solid-color image with an optional text overlay showing the color value. The text format (hex, rgb, hsl, css), size, position and color can all be configured.

Useful for previewing individual colors in a ComfyUI workflow.

![Color Preview workflow](../screenshots/01_color_preview_workflow.png)

![Color Preview result](../screenshots/01_color_preview_result.png)

## Inputs

| Name | Type | Default | Description |
|------|------|---------|-------------|
| color | PIXEL_COLOR | — | Color to preview |
| width | INT | 256 | Image width in pixels (64–1024) |
| height | INT | 256 | Image height in pixels (64–1024) |
| show_text | BOOLEAN | True | Show color value as text overlay |
| text_format | `hex` \| `rgb` \| `hsl` \| `css` | hex | Format of the text overlay |
| text_color | `black` \| `white` \| `auto` | auto | Text color (auto adjusts based on luminance) |
| text_size | INT | 24 | Font size (12–72) |
| text_position | `center` \| `bottom` \| `top` | center | Text placement |
| background_color | STRING | transparent | Background color behind the swatch |

## Outputs

| Name | Type | Description |
|------|------|-------------|
| image | IMAGE | The preview image |

## Category

`pixel_art/output`
