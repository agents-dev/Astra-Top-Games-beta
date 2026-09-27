# HELLAS · 希腊文明

[Open the game source](https://github.com/MXMX0811/gpt-6-astra-game/tree/main/civilization-v-hellas)
[Play the game](https://astra-civilization-v-hellas.pages.dev)

**Overall rating:** 58/100. New catalog top at 58/100, above Ashlands (55 overall, ~94k-line procedural RPG with zero inspectable screenshots and a failing gate check), Kart Royale (50 overall, ~60k-line single-track 3D racer with 70-score sunset screenshots), Frosty Tactics (48, 50-battle tactics with D&D depth but no inspectable frames), THORNMERE (46 overall, 60-score retro pixel RPG), neverquest (45, deepest text systems but 30-score monochrome UI) and SpaceHo2 (42, 30-star 4X with no screenshots). HELLAS exceeds all of them on combined verified breadth: 6 eras, 39 techs, 30 policies, 20 units, 22 buildings, 6 wonders, 4 victory routes, city-state and Persia diplomacy, ZOC and promotion tactics, bilingual UI, autosave with import-export, 26 rule tests plus localization checks and an 80-turn sim, 9 JS modules bundled with Three.js r180 and esbuild into a ~785KB single file, and a live public Pages build with an inspected 1280x720 gameplay frame. Far from AAA: single small map, no multiplayer, no voice, cinematics or live-ops scale, simplified Civ V tribute systems, 10 commits and 6 stars, and source plus stills do not prove playability, performance, balance or fun. Evidence gaps: judged from unauthenticated REST and raw files plus web fetches because gh CLI had no token, one gameplay screenshot inspected, no full campaign played, no performance or balance data.

**Screenshot score:** 68/100. Inspected 1280x720 gameplay frame shows coherent stylized low-poly 3D hex strategy: mountain, forest, farm and coast tiles, Athens city badge, top resource bar in gold, research and policy panels, scout unit card with 5 attack and 100 HP, blue movement fill with gold selection, pixel minimap, END TURN button and anchored AEGEAN SEA label. Polished dense UI and consistent palette place it just below Kart Royale and Turbo Kart Rally (both 70 for golden-hour 3D circuits with crowds, lighting and speed composition) on lighting dynamism and scene spectacle, and above THORNMERE (60 for flat 320x240 retro pixels), Taipo (55 for sparse 2D TD board), chess rot (40), Blackjack and Beachy (35) and neverquest (30 for text dashboard) on 3D scene detail and UI polish. The sibling iron-tide teaser is a harbor menu, discounted as non-gameplay. Judged from stills only with no motion or feel inferred.

## Screenshots

![Inspected 1280x720 gameplay frame: low-poly 3D hex island with grey mountains, green forests, yellow farms and cyan coast; central Athens badge with population 3; top bar with 143 gold, 4 science, 13 culture, 0 faith, 7 happiness and turn 12 in 3560 BC; left research panel for Mining and social-policy progress; scout unit card with 5 strength, 0/3 movement and 100/100 HP; right Alexander of Greece panel with city-state bonus; pixel minimap with 14 percent explored and gold END TURN button; AEGEAN SEA label over dark water. The game's own runtime output, not concept art.](https://raw.githubusercontent.com/MXMX0811/gpt-6-astra-game/main/assets/hellas-teaser.jpg)

Inspected 1280x720 gameplay frame: low-poly 3D hex island with grey mountains, green forests, yellow farms and cyan coast; central Athens badge with population 3; top bar with 143 gold, 4 science, 13 culture, 0 faith, 7 happiness and turn 12 in 3560 BC; left research panel for Mining and social-policy progress; scout unit card with 5 strength, 0/3 movement and 100/100 HP; right Alexander of Greece panel with city-state bonus; pixel minimap with 14 percent explored and gold END TURN button; AEGEAN SEA label over dark water. The game's own runtime output, not concept art.

## Play

- Open https://astra-civilization-v-hellas.pages.dev in a WebGL2 browser, no login needed.
- Click a unit, then click a blue-highlighted hex to move or a red-marked enemy to attack.
- Click a city name to manage population, production, research, culture, gold and buildings.
- Press T for technology, P for policies, H for guide, Tab for next unit, Enter or the END TURN button to end the round.
- Pan by mouse drag or one-finger touch drag, zoom by wheel or two-finger pinch, rotate by right-drag, Q/E or two-finger rotate.
- Win by conquest, technology, culture or diplomacy; autosave persists locally with export and import in the menu.

## Mechanics

- Turn-based hex strategy on a 28x20 Mediterranean map with fog of war, ruins, barbarian camps and territory borders
- Civilization development across 6 eras with 39 technologies, 6 policy branches with 30 policies, 20 units, 22 buildings, 6 wonders and 6 improvements
- Greek faction traits: hoplites, companion cavalry, halved city-state influence decay and doubled recovery from negative influence
- City economy with population, food, production, science, culture, gold, happiness, faith, strategic and luxury resources
- Diplomacy and war with 4 city-states, the Persian Empire and barbarians: gifts, commissions, trade, peace deals, war declarations, enemy pathfinding and reinforcements
- Tactical combat with melee counterattacks, ranged attacks, terrain defense, zones of control, fortify-heal, experience promotions and city capture
- Four victory routes: conquest, technology, culture and diplomacy, with autosave, manual saves and file import and export
- Bilingual Chinese-English UI with in-game encyclopedia, movement and attack range highlights, rotatable 3D camera and optional ambient music

## Tags

- turn-based-strategy
- 4x-like
- hex-grid
- 3d
- threejs
- civilization-tribute
- single-player
- bilingual
- browser-game

## Controls

- Mobile controls: Supported
- Motion controls: Not established
- Gamepad: Not established
- Keyboard/mouse: Supported

## Player modes

- Human players: 1
- Modes: single-player

## Reconstructed prompt

Build HELLAS, a single-player 3D turn-based Greek civilization strategy browser game in Three.js inspired by Civilization V: 28x20 hex Mediterranean map with fog of war, 6 eras, 39 techs, 30 policies, 20 units, 22 buildings, 6 wonders, 4 city-states plus Persia and barbarians, melee counterattacks, ranged fire, terrain defense, zones of control, promotions and city capture, four victories, bilingual Chinese-English UI, touch plus keyboard-mouse camera, autosave with import-export, modular source with rule tests, esbuild single-file output and a public static hosting link.

## Source evidence

- Repo MXMX0811/gpt-6-astra-game is public, created 2026-09-25, pushed 2026-09-25, 6 stars, 0 forks, description one-sentence web 3D game demo, JavaScript dominant. gh CLI had no token so evidence gathered via unauthenticated REST and raw fetches. ([source](https://api.github.com/repos/MXMX0811/gpt-6-astra-game))
- Repo holds two independent games: civilization-v-hellas with 9 JS modules and world-of-warships with 6 modules; target HELLAS directory verified with README, build script, package files, src and tests. ([source](https://api.github.com/repos/MXMX0811/gpt-6-astra-game/contents/civilization-v-hellas))
- HELLAS game README defines a single-player 3D turn-based strategy game, 28x20 hex map, 6 eras, 39 techs, 6 policy branches with 30 policies, 20 units, 22 buildings, 6 wonders, 4 city-states plus Persia and barbarians, 4 victory routes, and public play link. Establishes single-player mode with 1 human player. ([source](https://github.com/MXMX0811/gpt-6-astra-game/blob/main/civilization-v-hellas/README.md))
- HELLAS controls table documents mouse drag pan, wheel zoom, right-drag and Q/E rotate, click select-move-attack, Enter end turn, Tab next unit, T/P/F/G/H/Esc shortcuts, plus touch one-finger drag, two-finger zoom and two-finger rotate. Establishes keyboard-mouse and mobile touch support; no gamepad or motion controls documented. ([source](https://github.com/MXMX0811/gpt-6-astra-game/blob/main/civilization-v-hellas/README.md))
- HELLAS package is civilization-v-hellas 1.0.0 with Three.js 0.180.0, i18next and esbuild, test script running engine, combat and i18n checks; src lists app, data, engine, panels, world, sound, style and locales. ([source](https://raw.githubusercontent.com/MXMX0811/gpt-6-astra-game/main/civilization-v-hellas/package.json))
- Root README states one sentence per game generated full 3D web games, HELLAS at ~785KB single file with 9 modules, with teasers from the running games and public Cloudflare Pages links without login. ([source](https://github.com/MXMX0811/gpt-6-astra-game/blob/main/README.md))
- Live HELLAS Pages build opens the playable game with history-writing prompt, other-faction turns, drag pan, wheel zoom, right-drag rotate and click-unit-then-blue-tile move text, not a repo or promo page. ([source](https://astra-civilization-v-hellas.pages.dev))
- Sibling IRON TIDE Pages build opens a separate playable 5v5 naval game with harbor, ship selection, sortie and pause flows, confirming the repo is a two-game collection and HELLAS is the rated entry. ([source](https://astra-world-of-warships.pages.dev))

## Fictional reviews

Treat these as illustrative, not real user reviews.

- 82/100: Fictional illustrative review one: settled my second city by turn 30, rushed iron working for hoplites, and held off Persia with zone-of-control blocks while my triremes scouted the Aegean. For a one-sentence browser Civ it feels shockingly complete.
- 62/100: Fictional illustrative review two: deep tech and policy trees with four victory paths, but the AI diplomacy feels scripted, late turns drag, and one hex map cannot carry a full campaign the way the kart racers carry three laps of speed.
- 95/100: Fictional illustrative review three: a bilingual 3D hex strategy game with fog of war, promotions, wonders, autosave and an 80-turn sim harness from a single Chinese sentence? As an AI-generation experiment this is the most ambitious strategy entry in the catalog.

## Links

- [https://github.com/MXMX0811/gpt-6-astra-game](https://github.com/MXMX0811/gpt-6-astra-game)
- [https://github.com/MXMX0811/gpt-6-astra-game/tree/main/civilization-v-hellas](https://github.com/MXMX0811/gpt-6-astra-game/tree/main/civilization-v-hellas)
- [https://github.com/MXMX0811/gpt-6-astra-game/blob/main/civilization-v-hellas/README.md](https://github.com/MXMX0811/gpt-6-astra-game/blob/main/civilization-v-hellas/README.md)
- [https://github.com/MXMX0811/gpt-6-astra-game/blob/main/README.md](https://github.com/MXMX0811/gpt-6-astra-game/blob/main/README.md)
- [https://astra-civilization-v-hellas.pages.dev](https://astra-civilization-v-hellas.pages.dev)
- [https://astra-world-of-warships.pages.dev](https://astra-world-of-warships.pages.dev)
