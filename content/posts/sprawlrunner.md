+++
title = 'General Updates & sprawlrunner'
date = '2025-11-24T08:30:14-05:00'
draft = false
description = "Updates on what I have been up to and announcing the sprawlrunner game."
tags = ["tui", "cli", "tcell", "roguelike", "video game", "go", "golang", "linux", "ai"]
+++

It's been a while since I've posted anything here, so I wanted to drop a quick update on what I've been doing.

---

## Customizing my Linux desktop

I have been using [Linux](https://cachyos.org/) as a daily driver for the first time in over a decade. It's come along so much since then that I no longer need to boot into Windows. It is stable and runs every game I have thrown at it so far.

Most of my free hacking time lately has gone into making my Linux desktop feel more like *my* machine instead of just another generic setup. You can check this out in my [dotfiles](https://github.com/theantichris/dotfiles)

I've been:

- Tuning my window manager and status bar so everything important is one glance away.
- Cleaning up keybindings and shortcuts so I can stay on the keyboard.
- Iterating on themes and layout to give things a more cyberdeck / netrunner console vibe instead of a stock desktop.

None of this is huge on its own, but the small quality of life improvements stack up. The end result is a system that feels fast, minimal, and built around how I actually work.

---

## ghost: small, steady improvements

I've made a few improvements to the UX of ghost.

- Better missing model detection.
- Cleaning up code and structure.

When it reaches the next meaningful milestone, I'll do a deeper post.

---

## Learning game development with **sprawlrunner**

When I was a teenager I loved playing [ADOM](https://www.adom.de/home/index.html). I started playing it again and don't care much for the newer versions.

This inspired me to finally learn some game development and make my own cyberpunk roguelike game called [sprawlrunner](https://github.com/theantichris/sprawlrunner).

A few things about it:

- **Vibe:** Shadowrun style cyberpunk. Gritty streets, megacorps, magic, chrome, all that good stuff.
- **Style:** ASCII / terminal style roguelike. Think old school: text, glyphs, tiles.
- **Tech:** Written in Go, running in the terminal. I want something I can iterate on quickly, keep portable, and actually understand top to bottom.

My goals with sprawlrunner:

- Learn the fundamentals of game development: input, rendering, game loops, state, combat, progression, etc.
- Explore how to make a world feel alive with minimal graphics and a lot of systems.
- Have a playground for experimenting with ideas around hacking, runs, and emergent gameplay in a cyberpunk setting.

I’m intentionally starting small: menus, movement, basic interactions. No promises about timelines, features, or whether this ever becomes a real game. The main goal is to learn in public and have fun building something weird and nerdy.
