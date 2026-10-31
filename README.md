# Penultimate

A tile-based fantasy role-playing game in the spirit of Ultima I–IV, written
in Python and Tk using only the standard library.

One adventurer wanders an overworld of wilderness, towns and dungeons, talks
to townsfolk, buys weapons and armour, and runs errands for **Lord
Canadian**, the kindly and endlessly apologetic ruler of the realm.
Moosedain the Wicked, a sorcerer with the head of a moose, has sent his
minions to steal four royal relics. Recover them, and Lord Canadian will
forge the Maple Blade, the one weapon that can harm Moosedain himself.

Every new game generates a new world: the map, towns, people, shops,
dungeons, bosses and quests. Within a game, the world stays the same.

## Running

```bash
./penultimate
```

You need Python 3 with Tk (on macOS with Homebrew: `brew install
python-tk`). Sound effects and music play through `afplay` (macOS),
`paplay` or `aplay`. If none of them is available, the game is silent.

To build a macOS app with an icon:

```bash
./penultimate --build-app [DIR]
```

## Playing

| Key | Action |
| --- | --- |
| Arrow keys / WASD | Move. Walk into monsters to fight and into people to talk |
| Space | Wait a turn |
| P | Drink a healing potion |
| M | Map of the lands you have seen |
| ? | Help |
| + / − | Zoom in / out |
| V | Sound effects on / off |
| B | Music on / off |
| N | New game (a whole new world) |
| Ctrl-Q / Cmd-Q | Quit |

**Talking.** Walk into a person, or into a shop counter with someone behind
it, then type a word and press Return. Everyone knows NAME, JOB and BYE;
most people know NEWS, and words they say in CAPITALS are worth asking
about. Shopkeepers answer BUY. Townsfolk know where the dungeons are and
which boss holds which relic.

**Lord Canadian** sits on his throne in Castle Canadian. Ask him about your
QUEST. He heals you whenever you visit and raises your level once you have
earned enough experience.

**Survival.** You eat as you travel, so buy rations at taverns. Swamps can
poison you; healers and potions cure it. Monsters get tougher the farther
you go from the castle and the deeper you go into dungeons. If you die,
Lord Canadian brings you back, but your gold is lost.

The game is saved to `~/.penultimate.json` whenever you change location and
when you quit, and it resumes next time.

## Files

- `penultimate`: the game. The tile graphics (16×16 pixel art) are stored
  in it as base64 PNGs in `TILE_PNG`, and the app icon as `ICON_PNG`.
- `make_tiles.py`: the pixel-art source for the tiles. Edit the art there
  and run it to rewrite the `TILE_PNG` and `ICON_PNG` blocks in
  `penultimate`; `./make_tiles.py --sheet sheet.png` also writes a preview
  of every tile.

The music is four original chiptune loops written as note data in the
`MUSIC` table. They are synthesized on first run and cached in
`~/.cache/penultimate`, and are re-rendered automatically if a tune
changes.

## License

MIT. See [LICENSE](LICENSE).
