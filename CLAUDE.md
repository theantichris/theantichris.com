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

See `BLOG_GUIDELINES.md` for working relationship, style guide, and release post patterns.

## Ghost Release Post Workflow

### Information Gathering
- Get release notes from GitHub (`mcp__github__get_latest_release`)
- Read the PR for implementation details (`mcp__github__pull_request_read`)
- Read the linked issue for design decisions and context
- Review previous release posts for the established pattern

### Release Post Structure (v3.x pattern)
1. Opening paragraph - version number + main feature, one sentence
2. `{{< github-card user="theantichris" repo="ghost" >}}` immediately after
3. Demo gif early (`/img/ghost-vX.X.X-<feature>/demo.gif`)
4. Code section with brief explanation of why it matters
5. "What's Next" section teasing upcoming work
6. Release notes link at the end

### File Naming
`content/posts/ghost-vX.X.X-<feature-slug>.md`

### Tags for Ghost Posts
`ghost`, `go`, `ai`, `ollama`, plus feature-specific tags (e.g., `bubbletea`, `tui`)
