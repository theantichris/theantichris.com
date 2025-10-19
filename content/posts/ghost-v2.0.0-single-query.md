+++
title = 'Ghost V2.0.0 Single Query'
date = '2025-10-19T06:23:42-04:00'
draft = true
description = "Version v2.0.0 is out with single query command."
tags = ["ghost", "tui", "bubbletea", "go", "golang", "ai", "genai", "ollama", "cli"]
+++

Yesterday I release the first version of the major refactor for [Ghost](https://github.com/theantichris/ghost). This includes just a single, root command to run a prompt against the `/generate` endpoint.

![Sending ghost a prompt](/img/ghost-v2.0.0-single-query/root.gif)

# Exit Codes

I decided I wanted to be able to tie errors to proper exit codes so created a package that defined a new error type. Why? I'm just like that.

![exit code definition](/img/ghost-v2.0.0-single-query/exitcode.png)

This uses a list of constants.

![exit codes](/img/ghost-v2.0.0-single-query/exitcodes.png)

You can just wrap the exit code with the error.

![exit code wrapping](/img/ghost-v2.0.0-single-query/cmd-errors.png)

Then unwrap.

![unwrapping exit codes](/img/ghost-v2.0.0-single-query/main-unwrap.png)

I'll probably create this as a standalone package to use in other projects if I end up liking it.

## Switching to urfave/cli

As I mentioned in the previous post I switched from [Cobra](https://github.com/spf13/cobra) to [urfave/cli](https://cli.urfave.org/). I haven't gotten to flags and configs yet but bootstrapping was pretty simple. You can see `main.go` in the image above and here is the definition for the command. The actual logic is extracted into a function for testing.

![root command definition](/img/ghost-v2.0.0-single-query/root-definition.png)

## Ollama API

This time I am using the `/generate` endpoint over `/chat` for the single query. Since there is no state or chat history it felt more proper.

![generate definition](/img/ghost-v2.0.0-single-query/ollama-generate.png)

What was really exciting to me here was finding the [Requests](https://github.com/earthboundkid/requests) library. It cuts out all the boilerplate for doing HTTP requests in Go and makes it more fluid and expressive.

## Up Next

Styling the command output with [Bubbletea](https://github.com/charmbracelet/bubbletea) and maybe [Glamour](https://github.com/charmbracelet/glamour), adding support for piped input, adding images to queries.
