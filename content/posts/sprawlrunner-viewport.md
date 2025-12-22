+++
title = 'Sprawlrunner: Camera and Viewport Work, HUD, and Title Screen'
date = '2025-12-22T14:41:34-05:00'
draft = false
description = "Recent Sprawlrunner work: a real camera + viewport (render only what's visible), a basic HUD/message log, and a title screen that makes it feel like a game."
tags = ["sprawlrunner", "gamedev", "rougelike", "go", "ebiten", "ui"]
+++

I've been working on [Sprawlrunner](https://github.com/theantichris/sprawlrunner) and finished my first milestone for basic movement, camera, and HUD.

It was mostly plumbing but upgraded how the game feels:

- The map is bigger than the screen now (viewport and camera)
- The player has basic context (HUD and message log)
- There's an actual title screen now

---

## Viewport and Camera

I was rendering the entire map every frame. That was fine for getting started but it doesn't work for exploration. I split the screen into fixed regions.

- Map viewport: 56x20 tiles
- Stats pane: 24 tiles wide on right
- Message log: 4 lines tall at the bottom

The camera is just a world space point. Every frame I convert that into a rectangle of world tiles the player should be able to see. I haven't implemented field of vision yet.

The logic is:

1. Center the viewport around the camera
2. Clamp that rectangle so it never goes negative or past the map bounds

```go
// CalculateViewportBounds returns the tile coordinates visible in the viewport.
func (renderer *EbitenRenderer) CalculateViewportBounds() (int, int, int, int) {
    // Calculate viewport bounds centered on camera
    minX := renderer.game.CameraX - mapViewportWidth/2
    minY := renderer.game.CameraY - mapViewportHeight/2
    maxX := minX + mapViewportWidth
    maxY := minY + mapViewportHeight

    // Clamp to map bounds
    if minX < 0 {
       minX = 0
       maxX = mapViewportWidth
    }

    if minY < 0 {
       minY = 0
       maxY = mapViewportHeight
    }

    if maxX > renderer.game.Width {
       maxX = renderer.game.Width
       minX = maxX - mapViewportWidth
    }

    if maxY > renderer.game.Height {
       maxY = renderer.game.Height
       minY = maxY - mapViewportHeight
    }

    return minX, minY, maxX, maxY
}
```

Once I have `(minX, minY)` rendering becomes a simple coordinate transform.

- Iterate only the tiles inside the viewport bounds
- Convert world tile coords to screens tile coords by subtracting the viewport origin

```go
// RenderMap draws all the tiles from the game map that are visible in the viewport.
func (renderer *EbitenRenderer) RenderMap(screen *ebiten.Image, game *Game) {
	minX, minY, maxX, maxY := renderer.CalculateViewportBounds()

	for y := minY; y < maxY; y++ {
		for x := minX; x < maxX; x++ {
			tile := game.Tiles[y][x]

			// Render at screen position offset by viewport origin
			screenX := x - minX
			screenY := y - minY

			renderer.RenderTile(screen, tile, screenX, screenY)
		}
	}
}
```

I used the same trick for the player.

```go
// CalculatePlayerScreenPosition returns the player's screen coordinates
// relative to the viewport origin.
func (renderer *EbitenRenderer) CalculatePlayerScreenPosition() (int, int) {
	minX, minY, _, _ := renderer.CalculateViewportBounds()

	screenX := renderer.game.Player.X - minX
	screenY := renderer.game.Player.Y - minY

	return screenX, screenY
}
```

The game world and the screen are two different coordinate systems and the viewport origin is the bridge between them.

## HUD

Once the map was constrained to a viewport the HUD was easily implemented.

I went with:

- Stats panel on the right, currently hardcoded with test values
- Message log on the bottoms, currently just for the quit game prompt

## Title Screen

I also added a title screen with some ASCII art logo and prompts for the player to start the game or quit.
