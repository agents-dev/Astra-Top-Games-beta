# Beat Streets — Web

[Open the game source](https://github.com/Lewiscowles1986/beatstreets-online)
[Play the game](https://lewiscowles1986.github.io/beatstreets-online/)

**Overall rating:** 53/100. Far from AAA (single-genre 2D arcade port, no multiplayer, no voice/cinematics/live-ops scale), but the most rigorously verified action game in the catalog. Most relevant comparators: Ashlands (55 overall, broader open-world RPG systems scope but zero inspectable screenshots), Kart Royale (50 overall, complete 3D kart loop on one 1.6km track with 70/100 screenshots), THORNMERE (46 overall, strongest retro-RPG package with 60/100 screenshots) and neverquest (45 overall, deepest systems breadth but text-UI only at 30/100 screenshots). Beat Streets beats Kart Royale on campaign scope (29 stages vs one track), combat-system depth (4 attacks, 4 enemy families, portals, weapons, powerups) and verification discipline (bit-exact CPython RNG parity plus hard per-pixel Playwright fidelity gates), and beats THORNMERE/neverquest on moment-to-moment real-time action and technical execution. It stays below Ashlands (55) on sheer systems breadth (RPG skills/quests/dialogue/magic vs one arcade loop). Evidence gaps: judged from public source plus reference frames only, never played live end-to-end, so playability, balance, pacing and performance are unverified and not proven by code or stills.

**Screenshot score:** 62/100. Three inspected 800x480 gameplay frames show coherent commercial-quality cartoon brawler art: shaded hero and enemies, textured brick walls, shuttered shopfronts with graffiti/posters/lamps, tiled sidewalks, and a full arcade HUD (health/stamina bars, score, life icons). Above Taipo (55, sparser flat pixel TD board), chess rot (40) and the flat DOM games (Blackjack/Beachy 35, neverquest 30) on character detail, texture depth and HUD polish, and roughly at THORNMERE (60) level for stylistic coherence. Below Kart Royale and Turbo Kart Rally (both 70) which show denser 3D scenes with dynamic chase framing, crowds, lighting and sense of speed that a side-on single-plane street cannot match. Judged from stills only; no motion or game feel inferred.

## Screenshots

![Inspected 800x480 gameplay frame: hero in white shirt and blue jeans punching an orange-jumpsuit vax enemy at the right edge of a brick street with green shutters, lamp, BOSS poster and graffiti; full arcade HUD with green health bar, heart, 0000 score and blue stamina bar. The game's own runtime output, densest combat action of the inspected frames.](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/e2e/reference/beatstreets-action-heropunch.png)

Inspected 800x480 gameplay frame: hero in white shirt and blue jeans punching an orange-jumpsuit vax enemy at the right edge of a brick street with green shutters, lamp, BOSS poster and graffiti; full arcade HUD with green health bar, heart, 0000 score and blue stamina bar. The game's own runtime output, densest combat action of the inspected frames.

![Inspected 800x480 gameplay frame: yellow-jumpsuit enemy mid-attack with arms raised beside the hero on a brick street with shutters, wall lamp, posters and drainpipe; full HUD with health/stamina/score/lives. The game's own runtime output showing enemy attack animation.](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/e2e/reference/beatstreets-action-enemyattack.png)

Inspected 800x480 gameplay frame: yellow-jumpsuit enemy mid-attack with arms raised beside the hero on a brick street with shutters, wall lamp, posters and drainpipe; full HUD with health/stamina/score/lives. The game's own runtime output showing enemy attack animation.

![Inspected 800x480 gameplay frame: lone idle hero in fighting stance on an empty brick street with shuttered door, graffiti and drainpipe; full HUD visible. The game's own runtime output, least action of the three frames.](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/e2e/reference/beatstreets-gameplay-stage.png)

Inspected 800x480 gameplay frame: lone idle hero in fighting stance on an empty brick street with shuttered door, graffiti and drainpipe; full HUD visible. The game's own runtime output, least action of the three frames.

## Play

- Open https://lewiscowles1986.github.io/beatstreets-online/ in a desktop browser and click Play
- Press Space (or Z) on the title screen, then again on the controls screen, to start the story intro
- Press Space to skip the scrolling intro text once it finishes typing, then fight the first wave
- Move with Arrow keys or WASD; punch with Space/Z, kick with X, elbow with C, flying kick with A
- Walk right past each defeated wave when the green arrow blinks to scroll the street forward through all 29 stages
- Pick up barrels, sticks and chains to throw or swing them; grab health and extra-life powerups; destroy enemy portals quickly
- Pause with Esc; enter the Konami code during play to open the cheat menu (god mode, one-punch, stage select)

## Mechanics

- Side-scrolling beat-em-up across 29 data-driven stages with wave gates and a blinking advance arrow
- Four hero attacks: punch, kick, elbow and flying kick with hit-boxes, combos and stamina costs
- Four enemy families (Vax, Hoodie, Scooterboy, Boss) plus enemy-spawning portals, with colour variants and AI approach/attack behaviour
- Throwable/pickup weapons: barrels, sticks and chains with limited durability
- Health and stamina bars, score, lives with extra-life animation, health and extra-life powerups
- Scrolling camera with boundary tracking, scrolling road and repeating background tiles
- Intro/outro teletype story text with a stolen-item choice, title/controls/pause/game-over flow
- Seeded deterministic RNG mirroring CPython random for bit-exact replays, plus Konami-code cheat menu with god mode, one-punch and stage select

## Tags

- beat-em-up
- brawler
- 2d
- arcade
- side-scrolling
- typescript
- browser-game
- canvas
- webgl
- port
- single-player
- retro

## Controls

- Mobile controls: Not established
- Motion controls: Not established
- Gamepad: Supported
- Keyboard/mouse: Supported

## Player modes

- Human players: 1
- Modes: single-player

## Reconstructed prompt

Port the Code the Classics Beat Streets brawler to the web in TypeScript: Vite + React shell with lazy-loaded Canvas 2D and WebGL renderers, a Zod-validated data-driven DSL for the 29 stages/characters/attacks/story, a pure framework-free engine (player, 4 enemy families, portals, scooters, barrel/stick/chain weapons, powerups, scrolling, scoring), keyboard plus gamepad plus WebSocket controllers, HUD/menus/intro text/game-over screens, Storybook component library, Vitest + Playwright tests, and a bit-exact fidelity harness against authentic pygame reference frames, deployed to GitHub Pages.

## Source evidence

- Public repo Lewiscowles1986/beatstreets-online is a TypeScript web port of the Code the Classics Beat Streets pygame game (Canvas 2D now, WebGL later), data-driven via a typed DSL, not a pygame API clone. ([source](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/README.md))
- Repo metadata via public API: TypeScript, created 2026-08-26, default branch main, 0 stars/0 forks, has\_pages true, no homepage set, no license. ([source](https://api.github.com/repos/Lewiscowles1986/beatstreets-online))
- Stack is Vite static build plus React shell, Canvas/WebGL Render abstraction, Zod DSL, Vitest + Playwright ATDD, Storybook, with GitHub Pages deploy of app plus Storybook. ([source](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/docs/ARCHITECTURE.md))
- Fidelity harness regenerates authentic pygame reference frames and gates the web build with hard per-pixel thresholds (title 1%, intro 2%, stage 1.5%, controls/game-over 0.5%, action frames 1.5%); engine reimplements CPython MT19937 RNG for bit-exact seeded replays. ([source](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/docs/FIDELITY.md))
- Game bunded data has 29 stages; engine Game owns exactly one Player plus enemies/weapons/powerups/scooters, stage scrolling, spawning, scoring and win/lose flow — a single-hero campaign with no second-player or network multiplayer code. ([source](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/packages/engine/src/engine/game.ts))
- Keyboard controls verified in source: arrows/WASD move, Space/Z punch (button 0), X kick (button 1), C elbow (button 2), A flying kick (button 3), Esc pause; canvas aria-label instructs arrow keys plus Space. ([source](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/src/components/GameCanvas.tsx))
- Physical gamepad support verified: Browser Gamepad API adapter mapping 4 logical buttons plus stick/hat movement with dead-zone, polled via navigator.getGamepads, merged with keyboard input; GamepadPanel component exists. ([source](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/packages/engine/src/core/controller-gamepad.ts))
- No on-screen joystick, touch buttons, accelerometer or gyroscope code found in GameCanvas or engine controllers (keyboard, gamepad and WebSocket adapters only); no source statement rules touch/motion in or out. ([source](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/src/components/GameCanvas.tsx))
- Deployed Pages site serves the real app shell (Vite bundle with engine, story, data and webgl-render chunks); the Play button lazy-mounts the GameCanvas host, so this URL opens the playable game, not just a repo or screenshot page. ([source](https://lewiscowles1986.github.io/beatstreets-online/))
- Gameplay scope evidence: punch/kick/elbow/flying-kick, Vax/Hoodie/Scooterboy/Boss/Portal enemies, barrel/stick/chain weapons, health and extra-life powerups, 800x480 resolution, score/lives/stamina HUD — consistent with the classic belt-scroll brawler loop. ([source](https://api.github.com/repos/Lewiscowles1986/beatstreets-online/contents/packages/engine/src/engine))

## Fictional reviews

Treat these as illustrative, not real user reviews.

- 85/100: Fictional illustrative review one: finally, a Code the Classics brawler I can play in a tab — 29 stages of scrolling street fights, barrels to throw, sticks and chains that wear out, portals spawning hoodie gangs. The punch-kick-elbow-flying-kick kit feels straight out of the arcade.
- 62/100: Fictional illustrative review two: the cartoon street art is crisp and the HUD is pure arcade, but it is a faithful port rather than a modern reinvention — one hero, keyboard-first, no co-op or touch sticks, so judge it as a loving preservation job, not a new Streets of Rage.
- 100/100: Fictional illustrative review three: the bit-exact fidelity harness is the real boss fight — seeded CPython RNG parity, per-pixel Playwright gates, Canvas plus WebGL renderers. As an agentic rebuild experiment this is the most rigorously verified game in the catalog.

## Links

- [https://github.com/Lewiscowles1986/beatstreets-online](https://github.com/Lewiscowles1986/beatstreets-online)
- [https://lewiscowles1986.github.io/beatstreets-online/](https://lewiscowles1986.github.io/beatstreets-online/)
- [https://api.github.com/repos/Lewiscowles1986/beatstreets-online](https://api.github.com/repos/Lewiscowles1986/beatstreets-online)
- [https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/README.md](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/README.md)
- [https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/docs/FIDELITY.md](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/docs/FIDELITY.md)
- [https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/docs/ARCHITECTURE.md](https://raw.githubusercontent.com/Lewiscowles1986/beatstreets-online/main/docs/ARCHITECTURE.md)
