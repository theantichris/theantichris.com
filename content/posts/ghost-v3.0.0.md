+++
title = 'Ghost v3.0.0 - Ground-Up Rewrite'
date = '2026-01-06T18:26:10-05:00'
draft = false
description = "v3.0.0 is a complete rewrite with output formatting, syntax highlighting, and cleaner architecture."
tags = ["ghost", "go", "golang", "ai", "genai", "ollama", "cli", "cobra", "viper", "lipgloss", "chroma"]
+++

[Ghost v3.0.0](https://github.com/theantichris/ghost/releases/tag/v3.0.0) is a complete rewrite, again. The v2 codebase felt bloated so I rebuilt it with output formats, syntax highlighting, and simpler architecture.

![Ghost v3 output formats](/img/ghost-v3.0.0/demo.gif)

## Back to Cobra and Viper

I switched back to [Cobra](https://github.com/spf13/cobra) and [Viper](https://github.com/spf13/viper) after experimenting with urfave/cli in v2.

urfave/cli required more boilerplate for config file loading and flag binding. Viper's config hierarchy (flags > env vars > config file > defaults) handles precedence cleanly.

## Output Formats

Ghost now supports outputting to JSON or Markdown via the `--format` flag now.

The format switch is straightforward. When writing to a TTY it applies syntax highlighting, otherwise outputs plain text for piping.

```go
func RenderContent(content, format string, isTTY bool) (string, error) {
    if !isTTY {
        return content, nil
    }

    switch format {
    case "json":
        return JSON(content), nil
    case "markdown":
        return glamour.Render(content)
    default:
        return content, nil
    }
}
```

## Syntax Highlighting

JSON and markdown output use [lipgloss](https://github.com/charmbracelet/lipgloss) for syntax highlighting. JSON gets a custom highlighter that parses tokens and applies cyberpunk themed colors. Markdown uses [glamour](https://github.com/charmbracelet/glamour).

```go
var (
    JSONKey    = lipgloss.NewStyle().Foreground(Accent1)
    JSONString = lipgloss.NewStyle().Foreground(SyntaxString)
    JSONNumber = lipgloss.NewStyle().Foreground(SyntaxString)
)

// Parse and style JSON tokens
if inKey {
    result.WriteString(JSONKey.Render(stringContent))
} else {
    result.WriteString(JSONString.Render(stringContent))
}
```

## LLM Package Simplification

The core types are minimal now. Just roles, messages, and optional image support.

```go
type Role string

const (
    RoleSystem    Role = "system"
    RoleUser      Role = "user"
    RoleAssistant Role = "assistant"
)

type ChatMessage struct {
    Role    Role     `json:"role"`
    Content string   `json:"content"`
    Images  []string `json:"images,omitempty"`
}
```

Starting fresh let me separate concerns better - CLI layer, API client, and formatting are cleanly split. The v2 code accumulated complexity from trying different approaches.

## Next Up

I realized I'm trying to make everything perfect and not making it very usable. I do want to get to TUI and do some UX improvements around images but without web search this is pretty useless as a digital assistant. I'll probably get to that next then come back to some UX improvements.
