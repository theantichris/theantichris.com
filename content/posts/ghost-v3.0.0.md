+++
title = 'Ghost v3.0.0 - Ground-Up Rewrite'
date = '2026-01-06T18:26:10-05:00'
draft = false
description = "v3.0.0 is a complete rewrite with output formatting, syntax highlighting, and cleaner architecture."
tags = ["ghost", "go", "golang", "ai", "genai", "ollama", "cli", "cobra", "viper", "lipgloss", "chroma"]
+++

[Ghost v3.0.0](https://github.com/theantichris/ghost/releases/tag/v3.0.0) is a complete rewrite, again. The v2 codebase felt bloated so I rebuilt it with output formats, syntax highlighting, and simpler architecture.

![Ghost v3 output formats](/img/ghostv3.gif)

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

## Two Functions Instead of One

In v2 I tried to overload a single Generate endpoint function to handle both streaming responses and image analysis. This got messy. v3 splits them into two focused functions.

```go
// AnalyzeImages sends a request to the chat endpoint with images to analyze and
// returns the response message.
func AnalyzeImages(ctx context.Context, host, model string, messages []ChatMessage) (ChatMessage, error) {
    request := ChatRequest{
        Model:    model,
        Stream:   false,
        Messages: messages,
    }

    var chatResponse ChatResponse

    err := requests.
        URL(host + "/chat").
        BodyJSON(&request).
        AddValidator(nil).
        Handle(func(response *http.Response) error {
            if response.StatusCode == http.StatusNotFound {
                return fmt.Errorf("%w: %s", ErrModelNotFound, request.Model)
            }

            if response.StatusCode != http.StatusOK {
                return fmt.Errorf("%w: %s", ErrUnexpectedStatus, response.Status)
            }

            return nil
        }).
        ToJSON(&chatResponse).
        Fetch(ctx)

    if err != nil {
        return ChatMessage{}, fmt.Errorf("%w", err)
    }

    return ChatMessage{
        Role:    RoleAssistant,
        Content: chatResponse.Message.Content,
    }, nil
}

// StreamChat sends a streaming request to the chat endpoint and returns the
// response message.
// onChunk is called for each streamed chunk of content.
func StreamChat(ctx context.Context, host, model string, messages []ChatMessage,
    onChunk func(string)) (ChatMessage, error) {

    request := ChatRequest{
        Model:    model,
        Stream:   true,
        Messages: messages,
    }

    var chatContent strings.Builder

    err := requests.
        URL(host + "/chat").
        BodyJSON(&request).
        AddValidator(nil).
        Handle(func(response *http.Response) error {
            defer func() {
                _ = response.Body.Close()
            }()

            if response.StatusCode == http.StatusNotFound {
                return fmt.Errorf("%w: %s", ErrModelNotFound, request.Model)
            }

            if response.StatusCode != http.StatusOK {
                return fmt.Errorf("%w: %s", ErrUnexpectedStatus, response.Status)
            }

            decoder := json.NewDecoder(response.Body)

            for {
                var chunk ChatResponse

                if err := decoder.Decode(&chunk); err == io.EOF {
                    break
                } else if err != nil {
                    return fmt.Errorf("%w: %w", ErrDecodeChunk, err)
                }

                onChunk(chunk.Message.Content)

                chatContent.WriteString(chunk.Message.Content)
            }

            return nil
        }).
        Fetch(ctx)

    if err != nil {
        return ChatMessage{}, fmt.Errorf("%w", err)
    }

    return ChatMessage{
        Role:    RoleAssistant,
        Content: chatContent.String(),
    }, nil
}
```

`AnalyzeImages` blocks until the full response comes back since image analysis doesn't benefit from streaming. I still need to wire this into the bubbletea program to show the processing message.

`StreamChat` uses a simpler callback than v2 for each chunk which lets the CLI layer handle rendering while the LLM package stays focused on the API.

Starting fresh let me separate concerns better. CLI layer, API client, and formatting are cleanly split. The v2 code accumulated complexity from trying different approaches.
