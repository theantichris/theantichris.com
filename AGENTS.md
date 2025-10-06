# Agent Guide for theantichris.com

## Build/Dev/Test Commands
- **Dev server**: `hugo server -D` (includes drafts)
- **Build**: `hugo --gc --minify` (outputs to `./public`)
- **Lint markdown**: Check against `.markdownlint.yml` rules (ATX headers, 4-space indent, no hard tabs)
- **No test suite**: This is a static Hugo site

## Code Style Guidelines

### Markdown Content (`content/**/*.md`)
- Use ATX-style headers (`#`, `##`, etc.)
- 4-space indentation for lists
- No hard tabs, use spaces only
- Front matter in TOML format (`+++` delimiters)
- Required front matter: `date`, `draft`, `title`

### Configuration (`hugo.toml`)
- TOML format for all config files
- Follow existing parameter structure under `[params]`

### Custom CSS (`assets/css/custom.css`)
- Minimal overrides only, theme provides base styles
- Follow theme's terminal aesthetic
