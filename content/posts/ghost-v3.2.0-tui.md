+++
title = "Ghost v3.2.0: Interactive TUI"
date = 2026-01-25T00:00:00-05:00
draft = false
description = "Ghost now has an interactive TUI with vim keybindings, input history, and multiline input"
tags = ["ghost", "go", "ai", "ollama", "bubbletea", "tui"]
+++

Ghost `v3.2.0` adds a full interactive TUI built with [Bubbletea](https://github.com/charmbracelet/bubbletea). Vim-style navigation, input history, and multiline input.

{{< github-card user="theantichris" repo="ghost" >}}

## Demo

![ghost TUI](/img/ghost-v3.2.0-tui/demo.gif)

## Vim-style Modes

The TUI has three modes: normal, insert, and command. Normal mode for scrolling through the conversation, insert mode for typing prompts, and command mode for `:q` to quit.

Navigation in normal mode uses vim keybindings: `j`/`k` to scroll, `ctrl+d`/`ctrl+u` for half-page jumps, `gg` for top, `G` for bottom. Press `i` to enter insert mode.

```go
func (model ChatModel) handleNormalMode(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	wasAwaitingG := model.awaitingG
	model.awaitingG = false

	switch msg.String() {
	case "i":
		model.mode = ModeInsert
		model.input.Focus()
		return model, textinput.Blink

	case "j":
		model.viewport.ScrollDown(1)

	case "k":
		model.viewport.ScrollUp(1)

	case "ctrl+d":
		model.viewport.HalfPageDown()

	case "ctrl+u":
		model.viewport.HalfPageUp()

	case "g":
		if wasAwaitingG {
			model.viewport.GotoTop()
		} else {
			model.awaitingG = true
		}

	case "G":
		model.viewport.GotoBottom()
	}

	return model, nil
}
```

The `gg` command requires tracking state between keypresses. When `g` is pressed, `awaitingG` is set to true. If `g` is pressed again before any other key, it scrolls to top.

## Input History and Multiline

Insert mode handles input history with up/down arrows and multiline input with shift+enter.

```go
func (model ChatModel) handleInsertMode(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd

	switch msg.String() {
	case "esc":
		model.mode = ModeNormal
		model.input.Blur()

	case "shift+enter", "ctrl+j":
		value := model.input.Value() + "\n"
		model.input.SetValue(value)
		return model, nil

	case "up":
		if len(model.inputHistory) == 0 {
			return model, nil
		}

		model.inputHistoryIndex--
		if model.inputHistoryIndex < 0 {
			model.inputHistoryIndex = 0
		}

		model.input.SetValue(model.inputHistory[model.inputHistoryIndex])

	case "down":
		if len(model.inputHistory) == 0 {
			return model, nil
		}

		model.inputHistoryIndex++
		if model.inputHistoryIndex >= len(model.inputHistory) {
			model.inputHistoryIndex = len(model.inputHistory)
			model.input.SetValue("")
			return model, nil
		}

		model.input.SetValue(model.inputHistory[model.inputHistoryIndex])

	case "enter":
		value := model.input.Value()

		if strings.TrimSpace(value) == "" {
			return model, nil
		}

		model.inputHistory = append(model.inputHistory, value)
		model.inputHistoryIndex = len(model.inputHistory)

		model.input.SetValue("")
		model.messages = append(model.messages, llm.ChatMessage{Role: llm.RoleUser, Content: value})
		model.chatHistory += fmt.Sprintf("You: %s\n\nghost: ", value)
		model.viewport.SetContent(model.renderHistory())

		return model, model.startLLMStream()

	default:
		model.input, cmd = model.input.Update(msg)
		return model, cmd
	}

	return model, nil
}
```

History index starts at the length of the history array. Pressing up decrements it to recall previous inputs. Pressing down past the end clears the input, letting you start fresh.

## What's Next

TUI polish and feature parity with the CLI. The TUI needs file and image support to match what the non-interactive mode can do.

Check the [release notes](https://github.com/theantichris/ghost/releases/tag/v3.2.0) for the full changelog.
