# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
 code in this repository.

## Project Overview

Personal technical blog and portfolio built with Hugo using the Terminal theme.
 Deployed automatically to GitHub Pages at theantichris.com.

## Commands

```bash
hugo new content/posts/<title>
```

## Architecture

- **Static site generator**: Hugo with Terminal theme (git submodule)
- **Content**: Markdown files in `content/` with TOML front matter
- **Styling**: Custom CSS in `assets/css/custom.css` (Cyberwave color palette)
- **Images**: Store in `static/img/<post-name>/`, reference as `/img/<post-name>/image.png`
- **Deployment**: GitHub Actions → GitHub Pages on push to main
- **Social**: Auto-posts new articles to Mastodon via workflow

### Key Files

| File                                  | Purpose                    |
|---------------------------------------|----------------------------|
| `hugo.toml`                           | Site configuration         |
| `content/posts/_template.md`          | Post front matter template |
| `layouts/shortcodes/github-card.html` | GitHub repo card shortcode |
| `BLOG_GUIDELINES.md`                  | Blog writing guidelines    |

## Shortcodes

### github-card

Requires named parameters:

```hugo
{{< github-card user="theantichris" repo="ghost" >}}
```

## Blog Writing

See `BLOG_GUIDELINES.md` for working relationship and style guide.
