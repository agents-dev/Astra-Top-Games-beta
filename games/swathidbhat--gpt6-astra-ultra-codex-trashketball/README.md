# Trashketball — Out of Office

[Open the game source](https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball)

**Overall rating:** 34/100. Far from AAA: one throw mechanic, one basket per room, no AI opponents, multiplayer, campaign, cinematics, audio depth, or live-ops scale; source and docs do not prove playability, performance, or balance. Compared against the local catalog (Ashlands 55, Kart Royale 50, THORNMERE 46, neverquest 45, Turbo Kart Rally 40, Taipo 35, Flip Runner 33, Top-10 Tension 32, chess rot 30, Neural Sight 30, TypeScript-Blackjack 28, Beachy Beachy Ball 25, curiositY 18): Trashketball exceeds Beachy Beachy Ball and Blackjack on real-time 3D scope and technical execution (two fully modelled procedural rooms, exact-drag physics, rim/wall/obstacle collision, trajectory preview, automated physics suite), and sits in the Flip Runner/Taipo band for a complete narrow loop with progression. It trails Turbo Kart Rally (full AI field, items, laps, menus, inspected 70/100 screenshots), neverquest (far deeper progression systems), and Kart Royale/Ashlands (much larger 3D systems ambition), and visual polish is unverified with zero inspectable gameplay frames, so it caps at 34.

**Screenshot score:** not scored. No inspectable gameplay screenshot.

## Play

- Open the app locally with npm install then npm run dev (no public playable build was found).
- Aim by moving the pointer over the room or with the arrow keys; watch the dotted trajectory preview.
- Set power by holding and pulling downward, with the slider, or with + / - keys.
- Throw with pointer release, Space, or the Throw paper button; each basket scores 10 points.
- Reach 100 points to unlock Level 2, the oceanfront Airbnb, and continue tossing there.

## Mechanics

- First-person aim/power/release paper toss with live simulated trajectory preview and landing marker
- Custom deterministic ballistics: gravity 9.81 m/s2, exact linear-drag integration, 120 Hz fixed steps, 12 mm collision substeps
- Rim, tapered bin-wall, floor, and furniture-obstacle rebounds; descent-through-opening scoring, one score per ball
- Two rooms with distinct baskets and distances: Severance-style office at 4.8 m and oceanfront Airbnb at 5.5 m
- Score progression: 10 points per basket, Level 2 unlock at 100 points, streak/baskets/shots tracking, restart and level switching
- Procedural Three.js rooms only, no external models or images at runtime; WebGL2 required; sound, fullscreen, help, and WebMCP throw/state/level tools

## Tags

- 3d
- first-person
- paper-toss
- physics
- single-player
- casual
- sports
- three-js

## Controls

- Mobile controls: Supported
- Motion controls: Not established
- Gamepad: Not established
- Keyboard/mouse: Supported

## Player modes

- Human players: 1
- Modes: single-player

## Reconstructed prompt

Build a first-person 3D paper-toss game called Trashketball Out of Office with Three.js: a Severance-inspired office level and an unlockable oceanfront Airbnb level at 100 points, aim with mouse plus arrow keys, drag or slider plus +/- for power, Space or button to throw, dotted trajectory preview, custom gravity plus drag physics with rim and wall bounces, 10 points per basket, score/streak HUD, sound, fullscreen, help, restart, and physics unit tests.

## Source evidence

- Repository is public TypeScript Next.js/Three.js game created 2026-09-05, 0 stars, 1 fork, no homepage, Pages disabled, no deployments, 4 commits-era layout with app/, lib/, tests/. ([source](https://api.github.com/repos/swathidbhat/gpt6-astra-ultra-codex-trashketball))
- README identifies the game as Trashketball Out of Office: first-person Three.js paper-toss in two modelled rooms, Level 1 Severance office, Level 2 oceanfront Airbnb unlocking at 100 points, 10 points per basket. ([source](https://raw.githubusercontent.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/main/README.md))
- README controls: move over room to aim, hold and drag downward for power then release, slider and Throw paper button also work with touch, keyboard arrows aim, +/- power, Space throws, plus sound/fullscreen/instructions/restart. ([source](https://raw.githubusercontent.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/main/README.md))
- App UI confirms single-player scoring loop: total score, baskets/shots, streak, throw power slider, Throw paper button with SPACE hint, level cards, escape progress, and help steps for aim/power/throw. ([source](https://raw.githubusercontent.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/main/app/page.tsx))
- Game engine uses pointermove/pointerdown/pointerup aiming and drag-power plus keydown handlers for arrows, Space, +/-; no gamepad, accelerometer, gyroscope, or multiplayer code paths; state is single score/shots/streak session. ([source](https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/lib/game.ts))
- Physics module defines two baskets, launch velocity from yaw/elevation/power, exact drag integration, 120 Hz steps with 12 mm substeps, rim/wall/floor/obstacle reflection, descent-based single scoring, and trajectory prediction. ([source](https://raw.githubusercontent.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/main/lib/physics.ts))
- Scenes module builds both rooms procedurally (office desks/terminals/chairs/partitions/mesh bin; beach glass wall/ocean waves/sofas/timber bin) with no external model or image downloads at runtime. ([source](https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/lib/scenes.ts))
- No gameplay screenshots exist to inspect: public/ contains only favicon.svg and the repo has no docs/screenshots image files; graphics quality therefore cannot be scored from stills. ([source](https://api.github.com/repos/swathidbhat/gpt6-astra-ultra-codex-trashketball/contents/public?ref=main))
- No verified playable URL: API homepage is null, Pages disabled, deployments list empty, and README documents only local npm run dev with no live build link. ([source](https://api.github.com/repos/swathidbhat/gpt6-astra-ultra-codex-trashketball))

## Fictional reviews

Treat these as illustrative, not real user reviews.

- 82/100: Nailed three in a row from the back of the office and the paper trail felt great. Unlocking the beach house at 100 points is a perfect little carrot.
- 64/100: Fun toss-and-adjust loop and I like the live trajectory preview, but one basket and one throw angle gets repetitive fast.
- 100/100: The Severance-style office made me laugh out loud and then the ocean level blew me away. Best coffee-break game I have played all year.

## Links

- [https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball](https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball)
- [https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/README.md](https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/README.md)
- [https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/app/page.tsx](https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/app/page.tsx)
- [https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/lib/game.ts](https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/lib/game.ts)
- [https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/lib/physics.ts](https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/lib/physics.ts)
- [https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/lib/scenes.ts](https://github.com/swathidbhat/gpt6-astra-ultra-codex-trashketball/blob/main/lib/scenes.ts)
