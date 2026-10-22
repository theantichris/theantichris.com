# theantichris.com

Personal website built with [Hugo](https://gohugo.io) using the [Terminal theme](https://github.com/panr/hugo-theme-terminal) with a custom Cyberpunk color palette.

## Development

Initialize the theme.

```bash
git submodule update --init --recursive
```

Start the development server (includes drafts):

```bash
hugo server -D
```

Visit http://localhost:1313

## Create a new post

```bash
hugo new content/posts/<title>
```

## Building

Build the site for production:

```bash
hugo --gc --minify
```

Output will be in `./public`

## Project Structure

- `content/` - Markdown content files
- `assets/css/custom/theme.css` - Custom styling with Cyberpunk palette
- `static/` - Static assets (images, fonts, etc.)
- `hugo.toml` - Hugo configuration
- `themes/terminal/` - Terminal theme (submodule)

## Customization

### Colors

The site follows the palette in Christopher's dotfiles (`.chezmoidata/cyberpunk.yaml`):

- Background: `#16161E`
- Panels: `#1F1F28`
- Text: `#EAEAF2`
- Accent (cyan): `#00F0FF`
- Links: `#00FFFF`
- Magenta: `#FF00FF`
- Pink (decoration): `#CA0174`
- Yellow (hover and focus): `#FFD300`

Muted text uses a lighter mix of the dotfiles' `#8A86A0` and primary text to
maintain contrast on panel backgrounds. Pink is reserved for decoration.
Custom styles load after the theme through `layouts/partials/extended_head.html`.

### Typography and accessibility

Prose uses the system sans-serif font. Headings, navigation, commands, and code
use the theme's bundled Fira Code, with monospace fallbacks. No Google Fonts
request is needed. The layout uses a centered reading column, visible navigation
on mobile, underlined links, keyboard focus indicators, a skip link, and reduced
motion support.

## License

Content © Christopher Lamm. Theme by [panr](https://github.com/panr).
