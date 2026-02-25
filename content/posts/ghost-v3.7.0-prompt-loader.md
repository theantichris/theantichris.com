+++
title = "Ghost v3.7.0: Prompt Loader"
date = 2026-02-24T00:00:00-05:00
draft = false
description = "Ghost prompts are now editable markdown files you can customize without touching source code"
tags = ["ghost", "go", "ai", "ollama"]
+++

Ghost `v3.7.0` adds a prompt loader. All of Ghost's prompts live as editable markdown files at `~/.config/ghost/prompts/` so you can customize its personality and behavior without touching source code.

{{< github-card user="theantichris" repo="ghost" >}}

## Editable Prompts

Ghost uses five prompt files, each controlling a different part of the system:

| File               | Purpose                                             |
|--------------------|-----------------------------------------------------|
| `system.md`        | Main system prompt that defines Ghost's personality |
| `vision_system.md` | System prompt for the vision/image analysis module  |
| `vision.md`        | Instructions sent with each image analysis request  |
| `json.md`          | Format instructions for JSON output mode            |
| `markdown.md`      | Format instructions for Markdown output mode        |

On first run Ghost writes defaults to disk. Edit any file and restart to apply your changes.

## Self-Healing Defaults

`LoadPrompts` uses a table-driven approach to map each filename to its embedded default and a destination in the `Prompt` struct:

```go
func LoadPrompts(configDir string, logger *log.Logger) (Prompt, error) {
	prompt := Prompt{}

	promptDir := filepath.Join(configDir, "prompts")

	err := os.MkdirAll(promptDir, 0750)
	if err != nil {
		logger.Error(ErrPromptLoad.Error(), "error", err.Error())
		return prompt, fmt.Errorf("%w: %w", ErrPromptLoad, err)
	}

	targets := []struct {
		filename     string
		defaultValue string
		dest         *string
	}{
		{"system.md", systemPrompt, &prompt.System},
		{"vision_system.md", visionSystemPrompt, &prompt.VisionSystem},
		{"vision.md", visionPrompt, &prompt.Vision},
		{"json.md", jsonPrompt, &prompt.JSON},
		{"markdown.md", markdownPrompt, &prompt.Markdown},
	}

	for _, target := range targets {
		result, err := loadPrompt(promptDir, target.filename, target.defaultValue)
		if err != nil {
			logger.Error(ErrPromptLoad.Error(), "file", target.filename, "error", err.Error())
			return prompt, err
		}

		*target.dest = result
	}

	return prompt, nil
}
```

The `loadPrompt` helper handles the read or create logic for each file. If the file exists it reads it. If it's missing it writes the embedded default to disk and returns that. Delete a file and it regenerates on next run. The custom files are never overwritten.

```go
func loadPrompt(promptDir, filename, defaultValue string) (string, error) {
	path := filepath.Join(promptDir, filename)

	bytes, err := os.ReadFile(path)
	if err != nil {
		if errors.Is(err, fs.ErrNotExist) {
			err := os.WriteFile(path, []byte(defaultValue), 0640)
			if err != nil {
				return "", fmt.Errorf("%w: %w", ErrPromptLoad, err)
			}

			return defaultValue, nil
		}

		return "", fmt.Errorf("%w: %w", ErrPromptLoad, err)
	}

	return string(bytes), nil
}
```

The old exported constants (`SystemPrompt`, `JSONPrompt`, etc.) became unexported and now serve purely as embedded defaults for regeneration.

## Threading Prompts Through the App

With prompts coming from files instead of constants, they need to flow through the application. `LoadPrompts` runs during config init and the result gets stored in the command context. Both the root command and chat command extract prompts from context and pass them into the TUI layer. Function signatures that previously referenced package level constants (`NewMessageHistory`, `AnalyseImages`) now accept the loaded prompts as parameters. The whole `Prompt` struct travels through `ModelConfig` into the chat and stream models so every code path uses the same loaded set.

## What's Next

I'm going to take some time to learn how large [Bubbletea](https://github.com/charmbracelet/bubbletea) application are structured. Ghost's TUI layer has grown organically and could benefit from some refactoring to reduce complexity.

Check the [release notes](https://github.com/theantichris/ghost/releases/tag/v3.7.0) for the full changelog.
