# Floppy-Bird

Floppy-Bird is an adapted, gesture-assisted version of a Flappy Bird-style Python game. The original game foundation comes from [LeonMarqs/Flappy-bird-python][6]. For this repository, **I created the custom hand-tracking module**, while **Claude Sonnet 5 assisted with adapting the game integration so the original gameplay could work with that module**. The result combines a Pygame playfield with a live OpenCV camera preview: the tracked position of your index finger controls the bird’s vertical movement, while keyboard input starts the game, triggers flaps, and restarts a round.

> **Keep the bird airborne, pass as many pipes as possible, and beat your saved high score.**

## At a Glance

| Category | Details |
| --- | --- |
| Project type | Desktop arcade game adaptation |
| Language | Python |
| Game framework | Pygame |
| Computer-vision input | OpenCV and MediaPipe Hands |
| Gesture input | Vertical position of the tracked index fingertip |
| Keyboard input | `Space` or `Up Arrow` |
| Window layout | 400 × 600 gameplay panel plus 640 × 600 camera panel |
| Frame rate | 15 game-loop ticks per second |
| Score persistence | `highscore.txt` |
| Original game foundation | [LeonMarqs/Flappy-bird-python][6] |
| Custom hand-tracking module | `hands.py`, created by Mehdi FERHAT |
| Adaptation assistance | Claude Sonnet 5 |
| Author of this adaptation | Mehdi FERHAT |

## Credits and Attribution

This project combines existing work with a custom input module and adaptation assistance. The contributions are intentionally separated below so that the origins of each part remain clear.

| Contributor or source | Credit |
| --- | --- |
| **Leonardo Marques (LeonMarqs)** | Created the original [Flappy-bird-python][6] game that provides the foundation for the adapted game loop and core Flappy Bird gameplay. |
| **Mehdi FERHAT** | Created the custom `hands.py` module that captures webcam frames, detects a hand with MediaPipe, and exposes the index-fingertip position used as gesture input. |
| **Claude Sonnet 5** | Assisted with adapting the game so that the original-style Pygame gameplay could work with the hand-tracking module. |
| **Zhaolingzhi** | The original [LeonMarqs repository README][6] credits the [FlapPyBird-master asset source][7]; that upstream asset attribution is preserved here. |

> This repository should be understood as an adaptation rather than a wholly original Flappy Bird implementation. Please preserve the upstream credits and review the original repositories’ licensing and asset terms before redistributing the project.

## Gameplay Loop

Floppy-Bird is organized around three game states: **WAIT**, **PLAY**, and **GAMEOVER**. The waiting screen animates the bird and scrolling ground while displaying the current high score. Pressing `Space` or `Up Arrow` applies the first flap, starts the round, and begins the background music.

During play, the camera is processed continuously. When a hand is detected, the game maps the index fingertip’s vertical camera position to the bird’s position in the gameplay panel. If no usable hand coordinate is available, the bird follows the normal gravity-based movement. Pipes move from right to left, and each successfully passed pipe increases the score.

A pixel-mask collision with a pipe or the ground ends the round. The game-over view displays the final score and saved high score. Pressing `Space` or `Up Arrow` resets the round and returns to the waiting state.

## Controls

| Input | Action |
| --- | --- |
| Move your index finger vertically | Control the bird’s vertical position while playing |
| `Space` | Start a round, flap during play, or restart after game over |
| `Up Arrow` | Alternative start, flap, or restart key |
| Close the game window | Release the camera and exit the application |

For the most reliable gesture input, keep one hand visible to the webcam and move the index fingertip within the camera frame. The custom hand-tracking module is configured to follow one hand at a time.

## What Is Included

### Split-Screen Presentation

The Pygame window reserves the left side for the game and the right side for a live camera preview. The game area is 400 pixels wide and 600 pixels high; the camera preview is scaled to 640 pixels wide while preserving the camera’s 16:9 proportions through vertical letterboxing.

### Physics and Obstacles

The bird uses an upward flap speed of `20` and gravity of `2.5`. Pipes move across the screen at a game speed of `15`, with a width of `80` pixels and a vertical gap of `150` pixels. New pipe heights are randomized to keep each run different.

### Audio Feedback

The game loads separate sounds for flapping, collisions, and scoring. A theme track begins when a round starts and stops when the bird collides with an obstacle. If `point.wav` is unavailable, the code falls back to `point.ogg`.

### Persistent High Scores

At startup, the game reads `highscore.txt`. When a completed run exceeds the stored value, the new score is written back to the same file so that the high score survives future launches.

## Technology Stack

| Technology | Role in the project |
| --- | --- |
| **Python** | Application and gameplay logic |
| **Pygame** | Window management, sprites, rendering, sound, events, and collision masks |
| **OpenCV** | Webcam capture, frame mirroring, color conversion, and camera input |
| **MediaPipe Hands** | Single-hand landmark tracking and index-fingertip detection |
| **NumPy** | Camera-frame and Pygame-surface conversion support |

## Project Structure

```text
Floppy-Bird/
├── assets/
│   ├── audio/          # Wing, collision, point, and theme sounds
│   └── sprites/        # Bird, pipe, ground, UI, background, and number sprites
├── game.py             # Adapted game loop, rendering, physics, scoring, and states
├── hands.py            # Custom webcam and MediaPipe index-fingertip tracking module
├── highscore.txt       # Persisted high-score value
├── .gitattributes
└── README.md
```

The game loads assets using relative paths such as `assets/sprites/...` and `assets/audio/...`. Run the program from the repository root so these paths resolve correctly. The overall game structure is adapted from [LeonMarqs/Flappy-bird-python][6], while `hands.py` is the custom hand-tracking module created by Mehdi FERHAT. Claude Sonnet 5 assisted with the code changes needed to connect the game loop to that module.

## Installation

### Requirements

You need **Python 3**, a working webcam, speakers or headphones for audio feedback, and the project’s complete `assets/` directory. The application uses a graphical desktop window, so it should be run in a local desktop session rather than a headless terminal environment.

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/flowasme/Floppy-Bird.git
   cd Floppy-Bird
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   ```

3. **Activate the environment.** On Windows:

   ```bash
   .venv\Scripts\activate
   ```

   On macOS or Linux:

   ```bash
   source .venv/bin/activate
   ```

4. **Install the dependencies:**

   ```bash
   pip install pygame opencv-python mediapipe numpy
   ```

## Launching the Game

From the project root, run:

```bash
python game.py
```

Allow the application to access the default webcam when prompted. The game window should open with the bird-and-pipes scene on the left and the camera feed on the right. If the camera is not detected, check that another application is not using it and that the operating system has granted camera permission to Python.

## Implementation Notes

The custom `hands.py` module created by Mehdi FERHAT opens the default camera at 1280 × 720 and 30 FPS, mirrors each frame, and extracts MediaPipe landmark `8`, corresponding to the index-finger tip. The adapted game converts that camera coordinate into the height of the gameplay panel before updating the bird.

The game loop and core Flappy Bird mechanics are based on the original work by [LeonMarqs][6]. Claude Sonnet 5 assisted with modifying the game integration so that the hand-tracking coordinate could drive the bird while the existing keyboard controls remained available. The main loop is capped at 15 ticks per second. Sprite masks are used for collision detection, the score is awarded when the bird fully passes a lower pipe, and each pipe pair is replaced after leaving the screen.

## Future Improvements

Potential extensions include adding a configurable camera selector, a calibration screen for gesture sensitivity, pause and mute controls, a restart button, adjustable difficulty, clearer on-screen instructions, and a settings menu for game speed and pipe spacing. A future version could also separate configuration values into a dedicated file and add automated tests for scoring, high-score persistence, and state transitions.

## Project Author

**Mehdi FERHAT**

Mehdi FERHAT created the custom hand-tracking module and assembled this adapted version of the game with the assistance credited above.

## References

[1]: https://github.com/flowasme/Floppy-Bird "Floppy-Bird source repository"
[2]: https://www.pygame.org/docs/ "Pygame documentation"
[3]: https://opencv.org/ "OpenCV"
[4]: https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker "MediaPipe Hand Landmarker"
[5]: https://numpy.org/ "NumPy"
[6]: https://github.com/LeonMarqs/Flappy-bird-python "LeonMarqs Flappy-bird-python repository"
[7]: https://github.com/zhaolingzhi/FlapPyBird-master "FlapPyBird-master asset source credited by the original repository"
