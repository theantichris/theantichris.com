+++
title = "Ghost v3.6.0: Persistent Threads"
date = 2026-02-22T00:00:00-05:00
draft = false
description = "Ghost now saves conversations to disk with persistent chat threads"
tags = ["ghost", "go", "ai", "ollama", "bubbletea", "tui"]
+++

Ghost `v3.6.0` adds persistent chat threads. Conversations are saved to disk automatically, and you can browse, search, and reload them between sessions.

{{< github-card user="theantichris" repo="ghost" >}}

## Saving Conversations

Ghost hasn't been saving conversations make it kind of useless for a daily driver, every session started from scratch. This release saves messages to disk as they happen. Both user and assistant messages persist immediately so nothing is lost if the process exits unexpectedly.

Threads are stored as JSON files under `$XDG_DATA_HOME/ghost/threads/`. I went with lazy creation: no thread exists until you actually send a message. The title is your first message, truncated to ~50 characters at a word boundary. Same pattern as ChatGPT and similar tools.

```go
func (model ChatModel) saveMessage(chatMsg llm.ChatMessage) ChatModel {
	if model.threadID == "" {
		thread, err := model.createThread(chatMsg.Content)
		if err != nil {
			return model
		}

		model.threadID = thread.ID
	}

	_, err := model.store.AddMessage(model.threadID, chatMsg)
	if err != nil {
		model.logger.Error("failed to add message to thread", "thread_id", model.threadID, "error", err)
	}

	return model
}
```

```go
func (model ChatModel) createThread(content string) (*storage.Thread, error) {
	words := strings.Fields(content)
	title := ""

	for _, word := range words {
		if len(title)+len(word)+1 > 50 {
			break
		}

		if title != "" {
			title += " "
		}

		title += word
	}

	thread, err := model.store.CreateThread(title)
	if err != nil {
		model.logger.Error("failed to create new thread", "error", err)
	}

	return thread, err
}
```

If storage fails (disk full, permissions, whatever) the error gets logged and the chat keeps working. Persistence is a best effort enhancement, not a gate on the core experience.

## Loading Threads

`:t` opens a thread list sorted by most recent. Select a thread and press enter to load it. The thread list supports `/` for searching by title using fuzzy matching.

`loadThread()` rebuilds the full conversation from storage. Every message goes back into the LLM's context so it picks up where you left off. System and tool messages are included in the message slice but filtered out of the display. You see your conversation history, the model sees everything it needs.

```go
func (model ChatModel) loadThread(threadID string) (ChatModel, error) {
	messages, err := model.store.GetMessages(threadID)
	if err != nil {
		model.logger.Error("failed to get messages", "thread_id", threadID, "error", err.Error())
		return model, err
	}

	var chatMessages []llm.ChatMessage
	var chatHistory strings.Builder
	for _, message := range messages {
		chatMessage := llm.ChatMessage{
			Role:      message.Role,
			Content:   message.Content,
			Images:    message.Images,
			ToolCalls: message.ToolCalls,
		}

		chatMessages = append(chatMessages, chatMessage)

		if message.Role == llm.RoleSystem || message.Role == llm.RoleTool {
			continue
		}

		label := "You"
		if message.Role == llm.RoleAssistant {
			label = "ghost"
		}

		history := fmt.Sprintf("%s: %s \n\n", label, message.Content)
		chatHistory.WriteString(history)
	}

	model.threadID = threadID
	model.messages = chatMessages
	model.chatHistory = chatHistory.String()

	return model, nil
}
```

## New Chat

`:n` starts a fresh conversation. It clears the message history, display, and thread ID but keeps the system prompt intact. Simple reset.

```go
func (model ChatModel) newChat() (tea.Model, tea.Cmd) {
	model.messages = []llm.ChatMessage{{Role: llm.RoleSystem, Content: model.systemPrompt}}
	model.chatHistory = ""
	model.threadID = ""
	model.viewport.SetContent("")
	model.cmdInput.Reset()
	model.mode = ModeNormal

	return model, nil
}
```

## What's Next

Prompt management. Being able to customize and switch system prompts is the next step toward making ghost genuinely useful for daily use.

Check the [release notes](https://github.com/theantichris/ghost/releases/tag/v3.6.0) for the full changelog.
