+++
title = "Ghost v3.3.0: TUI File Support"
date = 2026-01-28T00:00:00-05:00
draft = false
description = "Ghost's TUI can now read files into the conversation with the :r command"
tags = ["ghost", "go", "ai", "ollama", "bubbletea", "tui"]
+++

Ghost `v3.3.0` adds file support to the TUI. `:r <filepath>` reads files into the conversation, vim-style.

{{< github-card user="theantichris" repo="ghost" >}}

## Demo

![ghost TUI file support](/img/ghost-v3.3.0-file-support/demo.gif)

## Handling Files In Command Mode

Reading the file in isn't much different than piping a file in the CLI. The trickier part was specifying the file to read from the TUI.

I updated the command handler to split on the first space to support arguments. `:r /path/to/file` loads file contents into the message history so the LLM has context. I'll be able to add new commands that accept arguments easily.

```go
case tea.KeyEnter:
	parts := strings.SplitN(model.cmdBuffer, " ", 2)
	cmd := parts[0]
	var arg string
	if len(parts) > 1 {
		arg = strings.TrimSpace(parts[1])
	}

	switch cmd {
	case "q":
		model.logger.Info("disconnecting from ghost")
		return model, tea.Quit

	case "r":
		if arg == "" {
			model.chatHistory += fmt.Sprintf("\n[%s error: no file path provided]\n", theme.GlyphError)
			model.viewport.SetContent(model.renderHistory())
			model.mode = ModeNormal
			model.cmdBuffer = ""
			return model, nil
		}

		content, err := agent.ReadFileForContext(arg)
		if err != nil {
			model.logger.Error("file read failed", "path", arg, "error", err)
			model.chatHistory += fmt.Sprintf("\n[%s error: %s]\n", theme.GlyphError, err.Error())
			model.viewport.SetContent(model.renderHistory())
			model.mode = ModeNormal
			model.cmdBuffer = ""
			return model, nil
		}

		model.messages = append(model.messages, llm.ChatMessage{Role: llm.RoleUser, Content: content})
		model.logger.Info("file loaded into context", "path", arg)
		model.chatHistory += fmt.Sprintf("\n[%s loaded: %s]\n", theme.GlyphInfo, arg)
		model.viewport.SetContent(model.renderHistory())
	}

	model.mode = ModeNormal
	model.cmdBuffer = ""
```

File contents get formatted as `[FILE: path]\n{contents}` and added as a user message. In the CLI I'm appending the contents to the user prompt which I want to go back and change it to this pattern to keep history clean.

## What's Next

Image support in the TUI. The last piece needed for feature parity with non-interactive mode.

Check the [release notes](https://github.com/theantichris/ghost/releases/tag/v3.3.0) for the full changelog.
