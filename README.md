# theantichris.com

Personal website built with [Hugo](https://gohugo.io) using the [Terminal theme](https://github.com/panr/hugo-theme-terminal) with a custom Cyberwave color palette.

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

## Building

Build the site for production:

```bash
hugo --gc --minify
```

Output will be in `./public`

## Project Structure

- `content/` - Markdown content files
- `assets/css/custom.css` - Custom styling with Cyberwave palette
- `static/` - Static assets (images, fonts, etc.)
- `hugo.toml` - Hugo configuration
- `themes/terminal/` - Terminal theme (submodule)

## Customization

### Colors

The site uses the Cyberwave color palette:
- Background: `#091a1f`
- Text: `#cdcefb`
- Accent (cyan): `#16e6c9`
- Magenta: `#bc3fbc`
- Yellow: `#e5e510`

### Font

Using [VT323](https://fonts.google.com/specimen/VT323) for that retro terminal aesthetic.

## License

Content © Christopher Lamm. Theme by [panr](https://github.com/panr).
