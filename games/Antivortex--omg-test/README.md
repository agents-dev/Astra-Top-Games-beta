# omg-test

[Open the game source](https://github.com/Antivortex/omg-test)

**Overall rating:** 10/100. Catalog was read (18 rated games, scores 18-55); target is not listed so nothing was excluded. Far from AAA: no playable loop, progression, opponents, audio, or builds. The entire game is one PuzzleStartPopup (thumbnail grid + preview + four buttons) whose Start/Ad handlers only Debug.Log. Most relevant comparators: curiositY (18 overall, finished 15-level playable browser loop with near-zero visuals) is the catalog floor and the target trails it because curiositY is actually playable while omg-test starts nothing; Beachy Beachy Ball (25, complete menu-to-finish roll-to-star loop) and TypeScript-Blackjack (28, complete rules-faithful card game) both ship finished loops the target lacks; Neural Sight (30, narrow photographic tech prototype) at least renders real-time 3D output, while omg-test has zero inspectable rendered frames. Credit only for clean prototype engineering (custom DI, MVP popup system, object pooling, 12 content photos, Unity 6000 URP setup). Evidence gaps: no README/docs, no screenshots or video, no Pages/releases/deployments or other playable URL, and no playtest; source cannot prove playability, performance, or balance, and the three inspected JPGs are raw photo assets, not gameplay.

**Screenshot score:** not scored. No inspectable gameplay screenshot.

## Play

- Open the Unity project (Unity 6000.2.10f1, URP 2D) and run GameScene
- When the PuzzleStartPopup appears, click one of the 12 puzzle thumbnails to preview it
- Press Start Free, Start for Coins, Watch Ad, or Close — note the Start/Ad buttons only write Debug.Log lines and start no puzzle gameplay

## Mechanics

- 12-image puzzle thumbnail selector with single-selection highlight
- Large preview image that follows the selected thumbnail
- Start Free / Start for Coins / Watch Ad buttons that only emit Debug.Log stubs
- Close button that hides the popup
- Custom SimpleContext dependency injection wiring ResourceManager, PopupSystem, and PopupsFactory
- Pooled thumbnail GameObject creation via GoPool

## Tags

- puzzle
- jigsaw-prototype
- unity
- urp-2d
- csharp
- menu-prototype

## Controls

- Mobile controls: Not established
- Motion controls: Not established
- Gamepad: Not established
- Keyboard/mouse: Not established

## Player modes

- Human players: 1
- Modes: single-player

## Reconstructed prompt

Build a Unity (URP 2D) jigsaw-picture puzzle game prototype with a custom DI container, an MVP popup system with object pooling, and a puzzle-start popup showing 12 selectable photo thumbnails, a large preview, and Start Free / Start for Coins / Watch Ad / Close buttons

## Source evidence

- Public repo Antivortex/omg-test, Unity project on main branch, primary language ShaderLab with C# and HLSL, no description, no homepage, no topics, 0 stars, 0 forks, no GitHub Pages, releases, or deployments, so no playable build is published ([source](https://api.github.com/repos/Antivortex/omg-test))
- Initial commit message declares this a Unity puzzle game prototype: MVP with custom DI container, MVP popup system, and puzzle start popup UI ([source](https://github.com/Antivortex/omg-test/commit/7b5506c))
- AppController.Start builds a SimpleContext, registers ResourceManager (PuzzleImages/), PopupSystem, PopupsFactory, and the popup view, then shows only the PuzzleStartPopup — there is no other game flow ([source](https://github.com/Antivortex/omg-test/blob/main/Assets/Game/AppController.cs))
- PuzzleStartPopupModel holds 12 image names (puzzle\_01..puzzle\_12) with a single SelectedIndex — a local single-user selection with no networking or multiplayer systems anywhere in the 232-entry file tree ([source](https://github.com/Antivortex/omg-test/blob/main/Assets/Game/Popups/PuzzleStartPopup/PuzzleStartPopupModel.cs))
- Presenter loads the 12 sprites, drives thumbnails/preview/selection, and all Start paths (Start Free, Start for Coins, Watch Ad) only call Debug.Log with the selected image name; only Close hides the popup — no puzzle-board gameplay exists ([source](https://github.com/Antivortex/omg-test/blob/main/Assets/Game/Popups/PuzzleStartPopup/PuzzleStartPopupPresenter.cs))
- View is uGUI Button/Image/Transform wiring (thumbnail pool, preview image, four buttons) with no on-screen joystick, accelerometer/gyroscope, gamepad, or keyboard bindings; Input System package is present as a dependency but no input actions are defined, so touch/motion/gamepad/keyboard support is unestablished ([source](https://github.com/Antivortex/omg-test/blob/main/Assets/Game/Popups/PuzzleStartPopup/PuzzleStartPopupView.cs))
- Inspected puzzle\_01 (paddleboarder at sea), puzzle\_02 (swing by a lake at sunset), and puzzle\_05 (jellyfish underwater): stock-style content photos with no HUD, UI, or puzzle grid — curated reference assets for puzzle content, not the game's own rendered output, so no gameplay screenshot exists to score ([source](https://github.com/Antivortex/omg-test/tree/main/Assets/Game/Resources/PuzzleImages))

## Fictional reviews

Treat these as illustrative, not real user reviews.

- 35/100: A tidy little puzzle-menu prototype: picking through a dozen photos is pleasant, but nothing happens when you press Start.
- 20/100: Pleasant thumbnails, zero payoff — every button just logs to the console and the actual jigsaw never appears.
- 55/100: Clean Unity architecture under the hood, and the photo set is nice, but as a game this is a lobby with no rooms.

## Links

- [https://github.com/Antivortex/omg-test](https://github.com/Antivortex/omg-test)
- [https://github.com/Antivortex/omg-test/commit/7b5506c](https://github.com/Antivortex/omg-test/commit/7b5506c)
- [https://github.com/Antivortex/omg-test/blob/main/Assets/Game/AppController.cs](https://github.com/Antivortex/omg-test/blob/main/Assets/Game/AppController.cs)
- [https://github.com/Antivortex/omg-test/blob/main/Assets/Game/Popups/PuzzleStartPopup/PuzzleStartPopupPresenter.cs](https://github.com/Antivortex/omg-test/blob/main/Assets/Game/Popups/PuzzleStartPopup/PuzzleStartPopupPresenter.cs)
- [https://github.com/Antivortex/omg-test/blob/main/Assets/Game/Popups/PuzzleStartPopup/PuzzleStartPopupView.cs](https://github.com/Antivortex/omg-test/blob/main/Assets/Game/Popups/PuzzleStartPopup/PuzzleStartPopupView.cs)
- [https://github.com/Antivortex/omg-test/blob/main/Assets/Game/Popups/PuzzleStartPopup/PuzzleStartPopupModel.cs](https://github.com/Antivortex/omg-test/blob/main/Assets/Game/Popups/PuzzleStartPopup/PuzzleStartPopupModel.cs)
