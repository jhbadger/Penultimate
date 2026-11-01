# Penultimate

A tile-based fantasy role-playing game in the spirit of Ultima I–IV, written
in Python and Tk using only the standard library.

One adventurer wanders an overworld of wilderness, towns and dungeons, talks
to townsfolk, buys weapons and armour, and runs errands for **Lord
Canadian**, the kindly and endlessly apologetic ruler of the realm.
Moosedain the Wicked, a sorcerer with the head of a moose, has sent his
minions to steal four royal relics. Recover them, and Lord Canadian will
forge the Maple Blade, the one weapon that can harm Moosedain himself.

Every new game begins with character creation (a name, and a class:
fighter, mage or ranger) and generates a new world: the map, towns, people,
shops, dungeons, bosses and quests. Within a game, the world stays the
same.

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
| F, then a direction | Fire a hockey puck from your sling |
| C, then a number | Cast a spell (aimed spells then ask for a direction) |
| P | Drink a healing potion |
| M | Map of the lands you have seen |
| J | Journal: your quest and your errands |
| ? | Help |
| + / − | Zoom in / out |
| V | Sound effects on / off |
| B | Music on / off |
| N | New game (a whole new world) |
| Ctrl-Q / Cmd-Q | Quit |

### Touch, mouse and gamepad

The game plays without a keyboard. **Tap or click** a square to walk there
(you stop if a monster comes into view), tap next to yourself to step,
fight or talk, and tap yourself to wait. When aiming the sling or a spell,
tap in the direction to fire. Spells, shopping and conversation topics
appear as menus to tap. The buttons below the map (Wait, Sling, Cast,
Potion, Map, Journal, Menu) cover the rest, with Menu holding help, zoom,
sound, music, new game and quit.

**Android:** install [Pydroid 3](https://play.google.com/store/apps/details?id=ru.iiec.pydroid3),
open `penultimate` in it and run it. Tiles are scaled up for phone screens,
and the on-screen keyboard only appears if you tap the box to type. There
is no sound on Android.

**Gamepad (Linux, including the Steam Deck):** the game reads the
joystick device directly, so an Xbox-style pad works with nothing to
install. On a Steam Deck, add `penultimate` to Steam as a non-Steam game
and use the Gamepad controller layout.

| Button | Action |
| --- | --- |
| D-pad / left stick | Move (hold to keep going); move through menus; aim |
| A | Wait a turn; choose in a menu |
| B | Back: close a menu, map or help; stop aiming; say bye |
| X | Fire the sling |
| Y | Cast a spell |
| LB | Drink a potion |
| RB | Journal |
| View | Map |
| Start | Menu |

Other pads may number their buttons differently; `PAD_BUTTONS` near the
top of the gamepad code maps them.

**Talking.** Walk into a person, or into a shop counter with someone behind
it, then type a word and press Return. Everyone knows NAME, JOB and BYE;
most people know NEWS, and words they say in CAPITALS are worth asking
about. Shopkeepers answer BUY. Townsfolk know where the dungeons are and
which boss holds which relic.

**Lord Canadian** sits on his throne in Castle Canadian. Ask him about your
QUEST. He heals you whenever you visit and raises your level once you have
earned enough experience.

**Errands.** Some townsfolk need HELP, and say so when you meet them. Ask,
and they'll send you to slay monsters, fetch something stolen from a
dungeon, catch a runaway goose, or carry a parcel to a shopkeeper in
another town, for gold and experience. Each town has two errands; press J
to see the ones you've taken on.

**Classes.** Fighters are tough and strong. Mages are frail but start with
the Frost Bolt and Heal spells and have the most magic points. Rangers are
quick and start with a hockey puck sling and leather armour.

**Shops.** Every town has a blacksmith, armourer, healer, inn, tavern,
outfitter and mage. Outfitters sell canoes, puck slings, pucks and
rations; mages sell spellbooks: Heal, Cure, Light, Frost Bolt, Sorry (an
apology so heartfelt that monsters run away), Portage (back to the
castle) and, in every mage's shop, Donutify, which turns a lesser monster
(or, regrettably, a villager) into a giant donut. Walk over a donut to eat
it for 50 food.

**Canoes.** Carry a canoe and you can paddle onto any lake or sea (sea
serpents permitting). Islands off the coast hold inukshuks with gifts
beneath them.

**Dungeons** come in kinds: torchlit stone halls, ice caves where slick
ice sends you sliding, flooded mines whose pools slow you down, and lava
caverns that burn. Every level hides traps (pits, poisoned darts and alarm
bells), and nimble heroes spot them sooner. Some levels lock the stairs or
the boss behind gates; the key is somewhere else on the level.

**Day and night.** Time passes as you play. At night you can't see as far,
more and fiercer monsters roam, and only inns and taverns stay open. A
night at the inn wakes you at 8 am. The Light spell helps in the dark.

**Wood witches** lurk in the forests and can turn you into a beaver: few
hit points, only a bite to fight with, and no one understands you. Only
Lord Canadian can turn you back.

**Survival.** You eat as you travel, so buy rations at taverns. Swamps can
poison you; healers and potions cure it. Monsters get tougher the farther
you go from the castle and the deeper you go into dungeons. If you die,
Lord Canadian brings you back, but your gold is lost.

The game is saved to `~/.penultimate.json` whenever you change location and
when you quit, and it resumes next time.

## Files

- `penultimate`: the game. The tile graphics (16×16 pixel art, with a
  second animation frame for creatures, water and flames) are stored in it
  as base64 PNGs in `TILE_PNG`, and the app icon as `ICON_PNG`.
- `make_tiles.py`: the pixel-art source for the tiles. Edit the art there
  and run it to rewrite the `TILE_PNG` and `ICON_PNG` blocks in
  `penultimate`; `./make_tiles.py --sheet sheet.png` also writes a preview
  of every tile. The dungeon themes and the animation frames are generated
  there from the base tiles.

The music is four original chiptune loops written as note data in the
`MUSIC` table. They are synthesized on first run and cached in
`~/.cache/penultimate`, and are re-rendered automatically if a tune
changes.

## License

MIT. See [LICENSE](LICENSE).
