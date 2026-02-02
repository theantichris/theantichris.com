+++
title = "Ghost v3.4.0: Unified File Handling"
date = 2026-02-02T00:00:00-05:00
draft = false
description = "Ghost's :r command now handles all files - text and images - with automatic MIME type detection"
tags = ["ghost", "go", "ai", "ollama", "bubbletea", "tui", "vision"]
+++

Ghost `v3.4.0` unifies file handling under a single `:r` command. Text files and images are now routed automatically via MIME type detection.

{{< github-card user="theantichris" repo="ghost" >}}

## One Command, Any File

The [v3.3.0 post](/posts/ghost-v3.3.0-file-support/) teased image support as the last piece for TUI feature parity. This release delivers that and goes further: instead of separate commands for text (`:r`) and images (`:i`), there's now just `:r`. Ghost figures out what to do with the file.

The routing logic reads the first 512 bytes and uses Go's `http.DetectContentType` to identify the MIME type:

```go
type FileType string

const (
	FileTypeText  FileType = "text"
	FileTypeImage FileType = "image"
	FileTypeDir   FileType = "dir"
)

var imageFileTypes = []string{
	"image/png",
	"image/jpeg",
	"image/webp",
}

func DetectFileType(path string) (FileType, error) {
	info, err := os.Stat(path)
	if err != nil {
		return "", fmt.Errorf("%w: %w", ErrFileAccess, err)
	}

	if info.IsDir() {
		return FileTypeDir, nil
	}

	if info.Size() > maxFileSize {
		return "", fmt.Errorf("%w (%d bytes)", ErrFileSize, info.Size())
	}

	file, err := os.Open(path)
	if err != nil {
		return "", fmt.Errorf("%w: %w", ErrReadFile, err)
	}
	defer func() { _ = file.Close() }()

	buffer := make([]byte, 512)
	n, err := file.Read(buffer)
	if err != nil {
		return "", fmt.Errorf("%w: %w", ErrReadFile, err)
	}

	mime := http.DetectContentType(buffer[:n])
	mediaType := strings.SplitN(mime, ";", 2)[0]

	if isImage(mediaType, path) {
		return FileTypeImage, nil
	}

	if isText(mediaType) {
		return FileTypeText, nil
	}

	return "", ErrFileTypeUnsupported
}
```

Text files get injected into the message history. Images route to the vision model for analysis and inject the description. Unsupported binaries (executables, archives, etc.) get rejected with a helpful error.

SVG files needed special handling since they're XML but should be analyzed as images:

```go
func isImage(mediaType, path string) bool {
	if slices.Contains(imageFileTypes, mediaType) {
		return true
	}

	if mediaType == "text/xml" && filepath.Ext(path) == ".svg" {
		return true
	}

	return false
}
```

The MIME detector sees SVG as `text/xml`, so the function falls back to checking the file extension.

## What's Next

TUI polish and possibly chat persistence.

Check the [release notes](https://github.com/theantichris/ghost/releases/tag/v3.4.0) for the full changelog.
