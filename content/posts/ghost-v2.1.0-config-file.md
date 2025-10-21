+++
title = 'Ghost V2.1.0 - Config File & Flags'
date = '2025-10-21T10:00:00-04:00'
draft = false
description = "v2.1.0 is out with config file and flag support"
tags = ["ghost", "tui", "bubbletea", "go", "golang", "ai", "genai", "ollama", "cli"]
+++

[Ghost v2.1.0](https://github.com/theantichris/ghost) is released with configuration support through CLI flags or a config file.

Configuration is supported for host, default model, and system prompt. All are optional with host and model having defaults.

The config file is located at `~/.config/ghost/config.toml`.

![ghost help command](/img/ghost-v2.1.0-config-file/help.png)

I used [urfave/alt-src](https://github.com/urfave/cli-altsrc) for reading a config file since I am already using [urfave/cli](https://github.com/urfave/cli). Again it was a lot less config than with [Viper](https://github.com/spf13/viper).

alt-src uses a Sourcer struct for reading config files from JSON, YAML, or TOML.

![load config function](/img/ghost-v2.1.0-config-file/load-config.png)

From there you just add the Sourcer as a source for the flag. alt-src will chain it in priority after a flag passed by CLI.

![initializing flags](/img/ghost-v2.1.0-config-file/init-flags.png)

You can get the value of flags using `cmd.String(<flag name>)`.

![calling flags](/img/ghost-v2.1.0-config-file/call-flags.png)
