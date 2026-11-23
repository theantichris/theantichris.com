+++
title = "Ghost v4.0.0: A Smaller Foundation"
date = 2026-11-23T00:00:00-05:00
draft = false
description = "Ghost v4 rebuilds the conversation core with streaming responses, cancellation, and less complexity"
tags = ["ghost", "go", "ai", "ollama", "cli"]
+++

Ghost `v4.0.0` is another rebuild. I wanted to reduce complexity and apply what I learned building v3. This release starts with a smaller foundation: a CLI that sends a prompt to [Ollama](https://ollama.com/), streams the response, and supports cancellation.

{{< github-card user="theantichris" repo="ghost" >}}

## Starting Smaller

By the end of v3, Ghost had an interactive TUI, file and image support, web search, persistent threads, and editable prompts. In the [v3.7 post](/posts/ghost-v3.7.0-prompt-loader/), I mentioned that the TUI had grown organically and could benefit from refactoring.

v4 starts over with a narrower scope. The current CLI handles one prompt per invocation. The TUI and the broader v3 feature set aren't part of this release. The previous implementation is preserved on the [archive/v3 branch](https://github.com/theantichris/ghost/tree/archive/v3).

## Conversation State Outside the UI

In v3, the TUI started model requests, handled streamed chunks, updated the display, and appended completed responses to conversation history. Conversation behavior lived alongside interface behavior.

v4 moves conversation state and turn handling into an `internal/conversation` package. A `Session` owns the message history. A `Turn` takes a snapshot of that history with the new prompt and streams response events. The CLI handles writing those events to standard output.

The useful boundary is in `RunTurnStream`: it adds the user prompt and assistant response to the session only after streaming succeeds. If the request fails or is canceled, the session history stays unchanged.

```go
func RunTurnStream(ctx context.Context, session *Session, id TurnID, model string, prompt string, chat ChatStreamFunc, emit func(TurnEvent) error) (Message, error) {
	if err := ctx.Err(); err != nil {
		return Message{}, fmt.Errorf("run streaming conversation turn: %w", err)
	}

	turn := NewTurn(id, model, session.Messages(), prompt)
	var response Message
	err := turn.Stream(ctx, chat, func(event TurnEvent) error {
		if event.Kind == TurnEventCompleted {
			response = Message{Role: RoleAssistant, Content: event.Content}
		}

		return emit(event)
	})
	if err != nil {
		return Message{}, fmt.Errorf("run streaming conversation turn: %w", err)
	}

	if err := ctx.Err(); err != nil {
		return Message{}, fmt.Errorf("run streaming conversation turn: %w", err)
	}

	session.AppendUser(prompt)
	session.AppendAssistant(response.Content)

	return response, nil
}
```

Partial output can still be visible in the terminal. Displaying a chunk and adding a completed exchange to conversation history are separate operations.

The CLI passes an `emit` callback to `RunTurnStream`. It writes each content chunk as it arrives.

```go
emit := func(event conversation.TurnEvent) error {
	var content string

	switch event.Kind {
	case conversation.TurnEventContent:
		content = event.Content
	case conversation.TurnEventCompleted:
		if strings.HasSuffix(event.Content, "\n") {
			return nil
		}

		content = "\n"
	default:
		return nil
	}

	if _, err := io.WriteString(output, content); err != nil {
		return fmt.Errorf("write assistant response: %w", err)
	}

	return nil
}
```

The current CLI creates a fresh session for each invocation, but the conversation package can carry history across turns without depending on a TUI framework.

## Streaming and Cancellation

Ghost writes response content to standard output as it arrives. Errors go to standard error. Pressing `Ctrl+C` cancels the request, leaves any partial output visible.

```go
ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
defer stop()

if err := run(ctx, os.Args[1:], os.Stdout, client.ChatStream); err != nil {
	_, _ = fmt.Fprintf(os.Stderr, "ghost // uplink failure: %v\n", err)
	os.Exit(1)
}
```

Cancellation also reaches the conversation layer. A turn checks its context while streaming and before committing the exchange, so an interrupted response doesn't become a completed entry in the session.

## What's Next

The broader direction is still a TUI-first cyberdeck but I will be taking a break from this project for a while though to work on my own [Linux desktop shell](https://github.com/theantichris/cyberdeckos).

Check the [release notes](https://github.com/theantichris/ghost/releases/tag/v4.0.0) for the full changelog.
