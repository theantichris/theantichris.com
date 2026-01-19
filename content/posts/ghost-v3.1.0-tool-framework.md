+++
title = "Ghost v3.1.0: Tool Framework and Web Search"
date = 2026-01-19T00:00:00-04:00
draft = false
description = "Ghost can now search the web and I built a framework to add more tools"
tags = ["ghost", "go", "ai", "ollama"]
+++

Ghost `v3.1.0` adds a tool framework that lets the LLM call external functions. The first tool is web search via [Tavily](https://www.tavily.com/), so ghost can now answer questions about current events instead of being limited to model training data.

{{< github-card user="theantichris" repo="ghost" >}}

## The Tool Interface

Every tool implements a simple interface:

```go
type Tool interface {
	Definition() llm.Tool
	Execute(ctx context.Context, args json.RawMessage) (string, error)
}
```

`Definition()` returns the JSON schema that tells the LLM what the tool does and what parameters it accepts. `Execute()` does the actual work when the LLM decides to call it.

## The Tool Call Loop

The interesting part is how ghost handles tool calls. When you send a prompt, ghost enters a loop:

```go
for {
	// I later refactored the loop to be in a conditional
	if len(tools) == 0 {
		break
	}

	resp, err := llm.Chat(cmd.Context(), url, model, messages, tools)
	if err != nil {
		streamProgram.Send(ui.StreamErrorMsg{Err: err})
		return
	}

	if len(resp.ToolCalls) == 0 {
		break
	}

	messages = append(messages, resp)

	for _, toolCall := range resp.ToolCalls {
		logger.Debug("executing tool", "name", toolCall.Function.Name)

		result, err := registry.Execute(cmd.Context(), toolCall.Function.Name, toolCall.Function.Arguments)
		if err != nil {
			logger.Error("tool execution failed", "name", toolCall.Function.Name, "error", err)
			result = fmt.Sprintf("error: %s", err.Error())
		}

		messages = append(messages, llm.ChatMessage{Role: llm.RoleTool, Content: result})
	}
}
```

1. Send the prompt to the LLM with available tool definitions
2. If the LLM responds with tool calls, execute them and append results to the message history
3. Loop until the LLM responds without requesting any tools
4. Stream the final response

This pattern lets the model chain multiple tool calls before giving a final answer.

## Demo

![ghost search](/img/ghost-v3.1.0-tool-framework/search.gif)

## What's Next

The framework is ready for more tools. File operations, code execution, API calls - anything that can return a string result can be a tool. I'll add new ones as I need them.

Next I'll be working on the TUI with [Bubbletea](https://github.com/charmbracelet/bubbletea).

Check the [release notes](https://github.com/theantichris/ghost/releases/tag/v3.1.0) for the full changelog.
