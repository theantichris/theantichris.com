+++
title = 'Ghost Image Support'
date = '2025-11-01T07:55:43-04:00'
draft = false
description = "Ghost can now describe images."
tags = ["ghost", "tui", "go", "golang", "ai", "genai", "ollama", "cli"]
+++

I have not cut a new version yet but `main` now includes image descriptions with the prompt using the `--image` flag.

![ghost image description](/img/ghost-image-support/image.gif)

Adding image support was pretty straight forward.

Add the flags.

```go
&cli.StringFlag{
  Name:     "vision-model",
  Usage:    "LLM to use for analyzing images",
  Value:    "qwen2.5vl:7b",
  Sources:  cli.NewValueSourceChain(toml.TOML("vision.model", configFile)),
  OnlyOnce: true,
},
&cli.StringFlag{
  Name:     "vision-system",
  Usage:    "the system prompt to override the vision model",
  Value:    "",
  Sources:  cli.NewValueSourceChain(toml.TOML("vision.system_prompt", configFile)),
  OnlyOnce: true,
},
&cli.StringFlag{
  Name:     "vision-prompt",
  Usage:    "the prompt to send for image analysis",
  Value:    "Analyze the attached image(s) and produce a Markdown report containing a description of each image.",
  Sources:  cli.NewValueSourceChain(toml.TOML("vision.prompt", configFile)),
  OnlyOnce: true,
},
&cli.StringSliceFlag{
  Name:  "image",
  Usage: "path to an image (can be used multiple times)",
},
```

Add the `images` property to the generate request and making sure it is passed to the API. All code not shown.

```go
type generateRequest struct {
  Model        string   `json:"model"`            // The model name
  Stream       bool     `json:"stream"`           // If false the response is returned as a single object
  SystemPrompt string   `json:"system"`           // System message to override what is in the model file
  Prompt       string   `json:"prompt"`           // The prompt to generate a response for
  Images       []string `json:"images,omitempty"` // A list of base64 encoded images
}
```

Encode the images.

```go
func encodeImages(paths []string) ([]string, error) {
  if len(paths) == 0 {
    return []string{}, nil
  }

  encoded := make([]string, 0, len(paths))

  for _, path := range paths {
    imageBytes, err := os.ReadFile(path)

    if err != nil {
      return nil, fmt.Errorf("%w: failed to read image %s: %w", ErrInput, path, err)
    }

    encodedImage := base64.StdEncoding.EncodeToString(imageBytes)
    encoded = append(encoded, encodedImage)
  }

  return encoded, nil
}
```

Then send a generate request for image descriptions if any are passed and append the results to the prompt.

```go
func generate(ctx context.Context, prompt string, images []string, config config,
  llmClient llm.LLMClient) (string, error) {
    // If images, send a request to analyze them and add the response to the prompt.
    if len(images) > 0 {
      response, err := llmClient.Generate(ctx, config.visionSystemPrompt, config.visionPrompt, images)
      if err != nil {
        return "", err
      }

      prompt = fmt.Sprintf("%s\n\n%s", prompt, response)
    }

    // Send the main request.
    response, err := llmClient.Generate(ctx, config.systemPrompt, prompt, nil)
    if err != nil {
      return "", err
    }

    return response, nil
}
  ```

  Where I messed up here was getting to into refactoring which should have been done in separate PRs. I plan on being better about this going forward, both for my own sanity and better release notes.

  From here I still need to add the image support to the `health` command and finish the refactoring I wanted to do. This will most likely end in a v3.0.0 release as I am planning to take a look at the config and flag structure to make the language feel more natural.
