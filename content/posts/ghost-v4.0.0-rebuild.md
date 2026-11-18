+++
title = "Ghost v4.0.0: A Smaller Foundation"
date = 2026-11-18T00:00:00-05:00
draft = true
description = "Ghost v4 rebuilds the conversation core with streaming responses, cancellation, and less complexity"
tags = ["ghost", "go", "ai", "ollama", "cli"]
+++

Ghost `v4.0.0` is another rebuild. I wanted to reduce complexity and apply what I learned building v3. This release starts with a smaller foundation: a CLI that sends a prompt to [Ollama](https://ollama.com/), streams the response, and supports cancellation.

{{< github-card user="theantichris" repo="ghost" >}}

> **Screenshot placeholder:** Show a terminal running `ghost --model qwen3:0.6b "Explain Go interfaces in two sentences."` with the completed response. Save it as `/img/ghost-v4.0.0-rebuild/cli.png`. A short recording could show the response arriving incrementally.

## Starting Smaller

By the end of v3, Ghost had an interactive TUI, file and image support, web search, persistent threads, and editable prompts. In the [v3.7 post](/posts/ghost-v3.7.0-prompt-loader/), I mentioned that the TUI had grown organically and could benefit from refactoring.

v4 starts over with a narrower scope. The current CLI handles one prompt per invocation. The TUI and the broader v3 feature set aren't part of this release. The previous implementation is preserved on the [archive/v3 branch](https://github.com/theantichris/ghost/tree/archive/v3).

## Conversation State Outside the UI

In v3, the TUI started model requests, handled streamed chunks, updated the display, and appended completed responses to conversation history. Conversation behavior lived alongside interface behavior.

v4 moves conversation state and turn handling into an `internal/conversation` package. A `Session` owns the message history. A `Turn` takes a snapshot of that history with the new prompt and streams response events. The CLI handles writing those events to standard output.

The useful boundary is in `RunTurnStream`: it adds the user prompt and assistant response to the session only after streaming succeeds. If the request fails or is canceled, the session history stays unchanged.

> **Code placeholder:** Insert the full `RunTurnStream` function from `internal/conversation/turn.go` at the `v4.0.0` tag. Show how it creates a turn from the session history, forwards events, checks for errors and cancellation, then appends the completed exchange. Keep the function intact so the order is visible.

Partial output can still be visible in the terminal. Displaying a chunk and adding a completed exchange to conversation history are separate operations.

The current CLI creates a fresh session for each invocation, but the conversation package can carry history across turns without depending on a TUI framework.

## Streaming and Cancellation

Ghost writes response content to standard output as it arrives. Errors go to standard error. Pressing `Ctrl+C` cancels the request, leaves any partial output visible, and exits with a nonzero status.

> **Screenshot placeholder:** Show a longer response interrupted with `Ctrl+C`, including the partial output and cancellation diagnostic. Run `echo $?` afterward to show the nonzero exit status. Save it as `/img/ghost-v4.0.0-rebuild/cancellation.png`.

Cancellation also reaches the conversation layer. A turn checks its context while streaming and before committing the exchange, so an interrupted response doesn't become a completed entry in the session.

## What's Next

The broader direction is still a TUI-first cyberdeck. This release establishes the conversation core before building the interface back around it.

Check the [release notes](https://github.com/theantichris/ghost/releases/tag/v4.0.0) for the full changelog.
