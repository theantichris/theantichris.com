+++
title = "Test on save for Go in the terminal"
date = 2025-10-09T00:00:00-04:00
draft = false
description = "How to setup test on save for Go in the terminal."
tags = ["go", "testing", "automation", "fd", "entr", "gotestsum"]
+++

## Introduction

Switching from Visual Studio Code to Helix for writing code had me missing the test on save feature for instant feedback I had with VSCode. Switching to a new pane or tab in kitty was a minor annoyance but still an annoyance. Doing some research I found a great solution using fd with entr and gotestsum.
                                                                             
You can use fd to find your go files, entr to watch those files for changes and run tests on file change, and gotestsum to format and display the output. Here's how.

## Install                                                                  

```bash
brew install fd enter gotestsum
```
                                                                             
## Usage                                                                    

```bash
fd -e go -E vendor -E gen -E dist | entr -c gotestsum -- -cover ./...
```
                                                                             
This will setup entr to watch all Go files in the current directory and subdirectories, excluding vendor, generated, and distribution directories.

Gotestsum will output the test results with code coverage information.

I have this setup with an alias `gotw` to mimic my other `go test` aliases. 
                                                                             
I open a new terminal pane below where I'm working in Helix and run this command. I get instant feedback on test results on every save. 
