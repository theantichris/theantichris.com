+++
title = 'Ghost v1.1.0 and Another Refactor'
date = '2025-10-13T19:55:28-04:00'
draft = false
description = "Version 1.1.0 is out with chat command but I'm rewriting it...again."
tags = ["ghost", "tui", "bubbletea", "go", "golang", "ai", "genai", "ollama", "cli"]
+++

Last week I released version 1.1.0 of [Ghost](https://github.com/theantichris/ghost) which adds the `chat` command that launches a TUI chat application backed by [Ollama](https://ollama.com/). I did this to learn how to make TUIs with [Bubbletea](https://github.com/charmbracelet/bubbletea).

![Ghost's chat command](/img/ghost-v1-1-0-and-another-refactor/chat.gif)

Now that I did this I think I'm going to write the whole thing over for the 4th time (I think 4th). Why?

Part of the reason I started this project was to reteach myself how to code after ~5 years of not really doing it after I shifted into leadership. A lot has changed since then and I've learned a lot over the past few months. I'm not happy with how the code is now. I feel it is over complicated from me trying all sorts of things. I didn't really follow TDD approaches as it slowed down the learning process. I think I can and want to do better.

I have a new branch where I deleted all the old code and started from scratch. Here are the things I'm doing differently.

- Using [urfave/cli](https://cli.urfave.org/) instead of [Cobra](https://github.com/spf13/cobra) and [Viper](https://github.com/spf13/viper).
  - I think the API is much simpler and lightweight.
- Following strict TDD in my approach to keep the code and interactions simple.
- Using table tests.
  - I really hated table tests for a long time. I think they over complicate tests and make them less documentation like. I think I can write them better.
- Using golden tests.
  - I didn't even know this was a thing until recently. This seems really handy for testing long output strings you get with Bubbletea views.
  - [Golide](https://github.com/sebdah/goldie) looks like a great library for this and has made it simple.
- Instead of an `ask` command for a single prompt I'm making that the default `ghost` command and will use Bubbletea for its output instead of straight stdout.
- Most options will be in the config file and I'm not making everything set in config file or environment variables or flags.

So here I go again but this time with a much better codebase and application, hopefully.
