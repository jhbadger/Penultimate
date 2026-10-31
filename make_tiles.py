#!/usr/bin/env python3
"""make_tiles.py - pixel-art source for penultimate's tiles.

Each tile is a 16x16 grid of palette letters ("." is transparent).  Running
this script renders every tile to a PNG and rewrites the TILE_PNG block of
./penultimate with the base64 data, the same way the other tk programs keep
their icons.  It also refreshes ICON_PNG from penultimate's own icon art.

    ./make_tiles.py              update ./penultimate in place
    ./make_tiles.py --sheet OUT  also write a 4x preview sheet of all tiles
"""

import base64
import os
import re
import struct
import subprocess
import sys
import tempfile
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
PROGRAM = os.path.join(HERE, "penultimate")

PALETTE = {
    ".": None,
    "k": (16, 16, 16), "K": (42, 40, 38),
    "g": (58, 143, 58), "G": (36, 100, 40), "l": (110, 190, 80),
    "a": (128, 140, 72), "A": (94, 104, 50),
    "b": (24, 48, 128), "B": (40, 90, 190), "c": (110, 165, 240),
    "y": (226, 206, 140), "Y": (196, 174, 104),
    "n": (139, 90, 43), "N": (90, 56, 26), "o": (184, 128, 72),
    "s": (138, 138, 138), "S": (88, 88, 88), "w": (200, 200, 200),
    "W": (255, 255, 255),
    "r": (200, 50, 40), "R": (122, 28, 20),
    "q": (160, 82, 45), "Q": (100, 52, 26),
    "f": (240, 192, 144), "F": (200, 148, 100),
    "u": (110, 64, 170), "U": (62, 34, 102),
    "e": (232, 197, 71), "E": (168, 134, 31),
    "m": (76, 100, 60), "M": (100, 88, 58),
    "t": (230, 120, 30),
    "d": (58, 50, 44), "D": (78, 68, 58),
    "p": (232, 140, 150),
}

TILES = {}


def tile(name, art):
    rows = [r for r in art.strip("\n").split("\n")]
    if len(rows) != 16:
        raise SystemExit("%s: %d rows" % (name, len(rows)))
    for i, r in enumerate(rows):
        r = r.rstrip()
        if len(r) > 16:
            raise SystemExit("%s row %d: %d columns" % (name, i, len(r)))
        for ch in r:
            if ch not in PALETTE:
                raise SystemExit("%s row %d: bad colour %r" % (name, i, ch))
        rows[i] = r.ljust(16, ".")
    TILES[name] = rows


# ── Overworld terrain ────────────────────────────────────────────────────────

tile("deep", """
bbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbb
bbbBBBbbbbbbbbbb
bbBbbbBbbbbbbbbb
bbbbbbbbbbbbbbbb
bbbbbbbbbbbBBBbb
bbbbbbbbbbBbbbBb
bbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbb
bbbbbBBBbbbbbbbb
bbbbBbbbBbbbbbbb
bbbbbbbbbbbbbbbb
bbbbbbbbbbbbbbbb
BBbbbbbbbbbbbbBB
bbBbbbbbbbbbbBbb
bbbbbbbbbbbbbbbb
""")

tile("water", """
BBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBB
BBBccBBBBBBBBBBB
BBcBBcBBBBBBBBBB
BBBBBBBBBBBBBBBB
BBBBBBBBBBccBBBB
BBBBBBBBBcBBcBBB
BBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBB
BBBBccBBBBBBBBBB
BBBcBBcBBBBBBBBB
BBBBBBBBBBBBBBBB
BBBBBBBBBBBBBccB
cBBBBBBBBBBBcBBc
BBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBB
""")

tile("grass", """
gggggggggggggggg
gggglggggggggggg
gggggggggggGgggg
ggGggggggggggggg
gggggggglggggggg
gggggggggggggggg
glggggGgggggggGg
gggggggggggggggg
gggggggggglggggg
ggggGggggggggggg
gggggggggggggggg
gggggglgggggGggg
ggGggggggggggggg
gggggggggggggggg
gggglgggggggglgg
gggggggggggggggg
""")

tile("forest", """
gggGGGGggggggggg
ggGGlGGGgggGGGGg
gGGlGGGGGgGGlGGG
gGGGGGGGGgGlGGGG
gGGGGGGGGgGGGGGG
ggGGGGGGgggGGGGg
gggGGGGggggGNGgg
ggggNNgggGGGNggg
gggggNggGGlGGGGg
ggGGGGgGGlGGGGGG
gGGlGGGGGGGGGGGG
gGlGGGGGGGGGGGGg
gGGGGGGGgGGGGGgg
ggGGGGGggggNNggg
gggNNgggggggNggg
ggggNggggggggggg
""")

tile("hills", """
gggggggggggggggg
gggggggggggggggg
ggggggaaaggggggg
gggggaalaaaggggg
ggggaalaaaaAgggg
gggaalaaaaaaAggg
ggaaaaaaaaaaaAgg
gggggggggggggggg
gggggggggaaagggg
ggaaagggaalaaggg
gaalaaAgaalaaaAg
aalaaaaAalaaaaaA
aaaaaaaaaaaaaaaa
gggggggggggggggg
gggggggggggggggg
gggggggggggggggg
""")

tile("mountain", """
ggggggSWSggggggg
gggggSWWWSgggggg
ggggSWWsWWSggggg
gggSsWsssWsSgggg
gggSssssssssSggg
ggSssssSssssSggg
gSssssSSsssssSgg
gSsssSSssssSWSSg
SsssSSsssssWWWSg
SsssSsssssWWsWWS
SssSsssssSsssssS
SssSssssSssssssS
SsSsssssSssssssS
SSsssssSsssssssS
SsssssSSssssssss
SSSSSSSSSSSSSSSS
""")

tile("swamp", """
mmmmmmmmmmmmmmmm
mmMMmmmmmmmmlmmm
mMMMMmmmmmmmlmmm
mmMMmmmmmmmlmlmm
mmmmmmmmmmmmmmmm
mmmmmmlmmmMMMmmm
mmmmmlmlmMMMMMmm
mmmmmmmmmmMMMmmm
mlmmmmmmmmmmmmmm
mlmlmmmMMMmmmmmm
mmmmmmMMMMMmmmmm
mmmmmmmMMMmmmmlm
mmmmmmmmmmmmmlml
mmMMmmmmmmmmmmmm
mMMMMmmmlmmmmmmm
mmMMmmmmmmmmmmmm
""")

tile("sand", """
yyyyyyyyyyyyyyyy
yyyyyYyyyyyyyyyy
yyyyyyyyyyyyYyyy
yYyyyyyyyyyyyyyy
yyyyyyyyyYyyyyyy
yyyyyyyyyyyyyyyy
yyyYyyyyyyyyyyYy
yyyyyyyyyyyyyyyy
yyyyyyyyYyyyyyyy
yyyyyyyyyyyyyyyy
yYyyyyyyyyyYyyyy
yyyyyyyyyyyyyyyy
yyyyyYyyyyyyyyyy
yyyyyyyyyyyyyyYy
yyyyyyyyyyyyyyyy
yyYyyyyyyyyyyyyy
""")

tile("town", """
gggggggggggggggg
ggggrrgggggggggg
gggrrrrggggrrggg
ggrrrrrrggrrrrgg
grrrrrrrrrrrrrrg
gwwwwwwwgwwwwwwg
gwkwwnwwgwkwwnwg
gwwwwnwwgwwwwnwg
gggggggggggggggg
gggggrrggggggggg
ggggrrrrgggggggg
gggrrrrrrggggggg
ggrrrrrrrrgggggg
gggwwwwwwggggggg
gggwkwwnwggggggg
gggwwwwnwggggggg
""")

tile("castle", """
ggggggggrrrggggg
ggggggggrrgggggg
ggggggggkggggggg
gsgsggggkggsgsgg
gsssgsgsksgsssgg
gsssssssssssssgg
gsksssssssssksgg
gsssswwwwwsssSgg
gssssskkkssssSgg
gsssskkkkksssSgg
gsssskkkkksssSgg
gSSSSkkkkkSSSSgg
ggggggyyyggggggg
gggggyyyyygggggg
ggggyyyyyyyggggg
gggggggggggggggg
""")

tile("dungeon", """
gggggggggggggggg
gggggSSSSSSggggg
ggggSsssssSSgggg
gggSsssssssSSggg
ggSssskkkkssSSgg
ggSsskkkkkkssSgg
gSsskkkkkkkksSSg
gSskkkkkkkkkksSg
gSskkkkkkkkkksSg
gSskkkkkkkkkksSg
gSSkkkkkkkkkkSSg
ggSkkkkkkkkkkSgg
gggSkkkkkkkkSggg
ggggYyyyyyyYgggg
gggYyyyyyyyyYggg
gggggggggggggggg
""")

tile("lair", """
gggggggggggggggg
gggggUUUUUUggggg
ggggUuuuuuUUgggg
gggUuuuuuuuUUggg
ggUuuukkkkuuUUgg
ggUuukkrrkkuuUgg
gUuukkkkkkkkuUUg
gUukkrkkkkrkkuUg
gUukkkkkkkkkkuUg
gUukkkkrrkkkkuUg
gUUkkkkkkkkkkUUg
ggUkkkkkkkkkkUgg
gggUkkkkkkkkUggg
ggggMmmmmmmMgggg
gggMmmmmmmmmMggg
gggggggggggggggg
""")

# ── Town and castle ──────────────────────────────────────────────────────────

tile("brick", """
qqqqqqqSqqqqqqqS
qQQQQQQSqQQQQQQS
qQQQQQQSqQQQQQQS
SSSSSSSSSSSSSSSS
qqqSqqqqqqqSqqqq
QQQSqQQQQQQSqQQQ
QQQSqQQQQQQSqQQQ
SSSSSSSSSSSSSSSS
qqqqqqqSqqqqqqqS
qQQQQQQSqQQQQQQS
qQQQQQQSqQQQQQQS
SSSSSSSSSSSSSSSS
qqqSqqqqqqqSqqqq
QQQSqQQQQQQSqQQQ
QQQSqQQQQQQSqQQQ
SSSSSSSSSSSSSSSS
""")

tile("stone", """
wwwwwwwswwwwwwws
wwwwwwwswwwwwwws
wwwwwwwswwwwwwws
wwwwwwwswwwwwwws
wwwwwwwswwwwwwws
wwwwwwwswwwwwwws
wwwwwwwswwwwwwws
ssssssssssssssss
wwwswwwwwwwswwww
wwwswwwwwwwswwww
wwwswwwwwwwswwww
wwwswwwwwwwswwww
wwwswwwwwwwswwww
wwwswwwwwwwswwww
wwwswwwwwwwswwww
ssssssssssssssss
""")

tile("cobble", """
yYYyyyYyyyYYyyyY
YyyyYyYyyyyyYyyY
YyyyYYYYyyyyYYYY
yYYYyyyyYYYYyyyy
yyyYyyyyyyyYyyyy
yyyYyyyyyyyYyyyy
YYYYYyyyyyYYYyyY
yyyyyYYYYYyyyYYy
yyyyyYyyyyyyyYyy
YyyyyYyyyyyyyYyy
YYyyYYYyyyyYYYYY
yyYYyyyYYYYyyyyy
yyYyyyyyyyYyyyyy
yYYyyyyyyyYyyyyy
YyyYYyyyyYYYyyyy
yyyyyYYYYyyyYYYy
""")

tile("wood", """
oooooooooooooooo
oooooooooooooooo
nnnnnnnnnnnnnnnn
oooooNoooooooooo
oooooNoooooooooo
nnnnnnnnnnnnnnnn
ooooooooooooNooo
ooooooooooooNooo
nnnnnnnnnnnnnnnn
ooNooooooooooooo
ooNooooooooooooo
nnnnnnnnnnnnnnnn
oooooooooNoooooo
oooooooooNoooooo
nnnnnnnnnnnnnnnn
oooooooooooooooo
""")

tile("counter", """
oooooooooooooooo
oooooooooooooooo
NNNNNNNNNNNNNNNN
oooooooooooooooo
oooooooooooooooo
NNNNNNNNNNNNNNNN
nnnnnnnnnnnnnnnn
nNNNNNNnnNNNNNNn
nNnnnnNnnNnnnnNn
nNnnnnNnnNnnnnNn
nNnnnnNnnNnnnnNn
nNnnnnNnnNnnnnNn
nNNNNNNnnNNNNNNn
nnnnnnnnnnnnnnnn
NNNNNNNNNNNNNNNN
oooooooooooooooo
""")

tile("carpet", """
eRrrrrrrrrrrrrRe
eRrrrrrrrrrrrrRe
eRrrrrrRrrrrrrRe
eRrrrrRrRrrrrrRe
eRrrrRrrrRrrrrRe
eRrrRrrrrrRrrrRe
eRrrrRrrrRrrrrRe
eRrrrrRrRrrrrrRe
eRrrrrrRrrrrrrRe
eRrrrrrrrrrrrrRe
eRrrrrrRrrrrrrRe
eRrrrrRrRrrrrrRe
eRrrrRrrrRrrrrRe
eRrrrrRrRrrrrrRe
eRrrrrrRrrrrrrRe
eRrrrrrrrrrrrrRe
""")

tile("throne", """
eRrrEeeeeeeErrRe
eRrrEeRRRReErrRe
eRrrEeRrrReErrRe
eRrrEeRrrReErrRe
eRrrEeRrrReErrRe
eRrrEeRRRReErrRe
eRrEEEEEEEEEErRe
eRrEuuuuuuuuErRe
eRrEuuuuuuuuErRe
eRrEEEEEEEEEErRe
eRrEeRrrrrReErRe
eRrEeRrrrrReErRe
eRrEERrrrrREErRe
eRrrrrrrrrrrrrRe
eRrrrrrrrrrrrrRe
eRrrrrrrrrrrrrRe
""")

tile("fountain", """
yYYyyyYyyyYYyyyY
YyyywwwwwwwwyyyY
YyywsssssssswyYY
yYwsBBBBBBBBswyy
yywsBBBcBBBBswyy
yywsBBcWcBBBswyy
YYwsBBBcBBBBswyY
yywsBBBWBBBBswYy
yywsBBcWcBBBswyy
YywsBBBBBBcBswyy
YywsBcBBBBBBswYY
yywsBBBBBBBBswyy
yyYwsssssssswyyy
yYYywwwwwwwwyyyy
YyyYYyyyyYYYyyyy
yyyyyYYYYyyyYYYy
""")

tile("door", """
qqSNNNNNNNNNNSqq
QQSNnnnNNnnnNSQQ
QQSNnnnNNnnnNSQQ
SSSNnnnNNnnnNSSS
qqSNnnnNNnnnNSqq
QQSNnnnNNnnnNSQQ
QQSNnnnNNnnnNSQQ
SSSNnnnNNnnnNSSS
qqSNnnnNNnneNSqq
QQSNnnnNNnneNSQQ
QQSNnnnNNnnnNSQQ
SSSNnnnNNnnnNSSS
qqSNnnnNNnnnNSqq
QQSNnnnNNnnnNSQQ
QQSNnnnNNnnnNSQQ
SSSNNNNNNNNNNSSS
""")

SIGN_BASE = """
yYYyyyYyyyYYyyyY
YNNNNNNNNNNNNNNY
YNooooooooooooNY
yNo..........oNy
yNo..........oNy
yNo..........oNy
YNo..........oNY
yNo..........oNy
yNo..........oNy
YNo..........oNy
YNooooooooooooNY
yNNNNNNNNNNNNNNy
yyYyyyNNYyYyyyyy
yYYyyyNNyyYyyyyy
YyyYYyNNyYYYyyyy
yyyyyYNNYyyyYYYy
"""


def sign(name, icon):
    """A wooden shop sign on a post; icon is 7 rows of 10 columns."""
    rows = SIGN_BASE.strip("\n").split("\n")
    for i, r in enumerate(icon.strip("\n").split("\n")):
        r = r.ljust(10, "o").replace(".", "o")
        rows[3 + i] = rows[3 + i][:3] + r + rows[3 + i][13:]
    tile(name, "\n".join(rows))


sign("sign_weapon", """
.......ww.
......ww..
.....ww...
.E..ww....
..Eww.....
..NE......
.N..E.....
""")

sign("sign_armor", """
..wwwwww..
..wRRRRw..
..wReeRw..
..wReeRw..
...wRRw...
....ww....
..........
""")

sign("sign_inn", """
....ee....
...ee.....
...ee..W..
...ee.WWW.
....ee.W..
.....eeE..
..........
""")

sign("sign_healer", """
....rr....
....rr....
..rrrrrr..
..rrrrrr..
....rr....
....rr....
..........
""")

sign("sign_tavern", """
..WWWWW...
..eeeee...
..eeeeeEE.
..eeeee.E.
..eeeeeEE.
..eeeee...
..EEEEE...
""")

sign("sign_outfitter", """
..........
....n.....
....n.....
.N..n...N.
.NNNNNNNN.
..NnnnnN..
..........
""")

sign("sign_mage", """
....e.....
....e.....
..eeeee...
...eee....
...e.e....
..e...e...
..........
""")

tile("inukshuk", """
gggggggggggggggg
ggggggSSSSgggggg
ggggggswwSgggggg
ggggggSSSSgggggg
ggSSSSSSSSSSSSgg
ggswwwwwwwwwwSgg
ggSSSSSSSSSSSSgg
gggggSSSSSSggggg
gggggswwwwSggggg
gggggSSSSSSggggg
ggggSSSggSSSgggg
ggggswSggswSgggg
ggggSSSggSSSgggg
ggggswSggswSgggg
gggSSSSggSSSSggg
gggggggggggggggg
""")

# ── Dungeon ──────────────────────────────────────────────────────────────────

tile("dwall", """
SSSSSSSKsSSSSSSK
SsssssSKSsssssSK
SsssssSKSsssssSK
SSSSSSSKSSSSSSSK
KKKKKKKKKKKKKKKK
SSSKsSSSSSSKsSSS
ssSKSsssssSKSsss
ssSKSsssssSKSsss
SSSKSSSSSSSKSSSS
KKKKKKKKKKKKKKKK
SSSSSSSKsSSSSSSK
SsssssSKSsssssSK
SsssssSKSsssssSK
SSSSSSSKSSSSSSSK
KKKKKKKKKKKKKKKK
SSSKsSSSSSSKsSSS
""")

tile("dfloor", """
dddddddddddddddd
dDdddddddddddddd
ddddddddddKddddd
dddddddddKdddddd
ddddDdddddddddDd
dddddddddddddddd
dKdddddddddddddd
ddKddddddDdddddd
dddddddddddddddd
dddddddddddddKdd
ddddDddddddddddd
dddddddKdddddddd
ddddddddKddddddd
dddddddddddDdddd
dDdddddddddddddd
dddddddddddddddd
""")

tile("stairs_down", """
dddddddddddddddd
dSSSSSSSSSSSSSSd
dSwwwwwwwwwwwwSd
dSsssssssssssSSd
dSKKKKKKKKKKKKSd
dSwwwwwwwwwwwSSd
dSssssssssssSKSd
dSKKKKKKKKKKKKSd
dSwwwwwwwwwSSKSd
dSsssssssssSKKSd
dSKKKKKKKKKKKKSd
dSwwwwwwwSSKKKSd
dSsssssssSKKKKSd
dSkkkkkkkkkkkkSd
dSSSSSSSSSSSSSSd
dddddddddddddddd
""")

tile("stairs_up", """
dddddddddddddddd
ddddddddddnNdddd
ddddddddddnNdddd
dddddddnnnnNdddd
dddddddnNNNNdddd
dddddddnNddddddd
ddddnnnnNddddddd
ddddnNNNNddddddd
ddddnNdddddddddd
dnnnnNdddddddddd
dnNNNNdddddddddd
dnNddddddddddddd
dnNddddddddddddd
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
""")

tile("chest", """
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
dddNNNNNNNNNNddd
ddNooooooooooNdd
dNooooooooooooNd
dNEEEEEEEEEEEENd
dNnnnnnEEnnnnnNd
dNnnnnEkkEnnnnNd
dNnnnnnEEnnnnnNd
dNnnnnnnnnnnnnNd
dNEEEEEEEEEEEENd
dNNNNNNNNNNNNNNd
dddddddddddddddd
dddddddddddddddd
dddddddddddddddd
""")

# ── People ───────────────────────────────────────────────────────────────────

tile("avatar", """
................
......NNNN......
.....NNNNNN.....
.....NffffN...w.
.....fkffkf...w.
.....ffffff...w.
......frrf....w.
....BBBBBBBB..w.
...BBBBBBBBBBfE.
...fBBBeeBBB.E..
...f.BBBBBB.....
.....BBBBBB.....
.....NNNNNN.....
.....BB..BB.....
.....BB..BB.....
....NNN..NNN....
""")

tile("lord", """
....e.e..e.e....
....eeeeeeee....
....eReeeeRe....
....ffffffff....
....fkffffkf....
....ffffffff....
....WWWffWWW....
.....WWWWWW.....
...rrrrWWrrrr...
..rrrrrrrrrrrr..
..frrrrWWrrrrf..
..frrWWWWWWrrf..
...rrrWWWWrrr...
...rrrrWWrrrr...
...rrrrrrrrrr...
....NNN..NNN....
""")

tile("guard", """
.......nn.......
......nnnn......
...nnnnnnnnnn...
......ffff......
......kffk......
......ffff......
.......ff.....s.
....rrrrrrrr..s.
...rrrreerrrr.s.
...frrrrrrrrffs.
...f.rrrrrr...s.
.....kkekkk...s.
.....bebbeb...s.
.....bebbeb...s.
.....bb..bb.....
....kkk..kkk....
""")

tile("man", """
................
......NNNN......
.....NNNNNN.....
.....NffffN.....
.....fkffkf.....
.....ffffff.....
......ffff......
....gggggggg....
...gggggggggg...
...fggggggggf...
...f.gggggg.f...
.....nnnnnn.....
.....gggggg.....
.....NN..NN.....
.....NN..NN.....
....kkk..kkk....
""")

tile("woman", """
................
......eeee......
.....eeeeee.....
.....effffe.....
....efkffkfe....
....effffffe....
....e.ffff.e....
.....uuuuuu.....
....uuuuuuuu....
...fuuuuuuuuf...
...f.uuuuuu.f...
....uuuuuuuu....
...uuuuuuuuuu...
...uuuuuuuuuu...
..uuuuuuuuuuuu..
.....kk..kk.....
""")

tile("merchant", """
................
......ffff......
.....ffffff.....
.....fkffkf.....
.....ffffff.....
.....fNNNNf.....
......NNNN......
....oooooooo....
...ooWWWWWWoo...
...fWWWWWWWWf...
...f.WWWWWW.f...
.....WWWWWW.....
.....WWWWWW.....
.....SS..SS.....
.....SS..SS.....
....kkk..kkk....
""")

tile("jester", """
...e........e...
...rr......uu...
....rrr..uuu....
.....rrrruu.....
.....ffffff.....
.....fkffkf.....
.....frrrrf.....
......ffff......
....rrrruuuu....
...rrrrruuuuu...
...frrrruuuuf...
...f.rrruuu.f...
.....uuurrr.....
.....uu..rr.....
.....uu..rr.....
....eee..eee....
""")

# ── Monsters ─────────────────────────────────────────────────────────────────

tile("rat", """
................
................
................
................
................
................
................
....ww..........
...wsssssss.....
..kssssssssss...
.sssssssssssss..
psssssssssssss..
.ssssssssssss.pp
....s.s..s.s...p
................
................
""")

tile("bat", """
................
................
................
.....U....U.....
UU...UU..UU...UU
UUU..UUUUUU..UUU
UUUUUUrUUrUUUUUU
UUUUUUUUUUUUUUUU
.UUUUUUWWUUUUUU.
..UUUUUUUUUUUU..
..U.UUUUUUUU.U..
.....U.UU.U.....
.......UU.......
................
................
................
""")

tile("snake", """
................
................
................
................
.........gggg...
........gggggg..
........gkggkg..
........gggggg..
.........gggg.r.
..gggg...ggg..r.
.gGGGGg..ggg....
gGgggggGgggg....
gGg....gGgg.....
.gGgggggGg......
..gGGGGGg.......
...ggggg........
""")

tile("slime", """
................
................
................
................
................
.......ll.......
......llll......
....llllllll....
...lWWllllllll..
..lWlllllllllll.
..llkkllllkklll.
.lllkkllllkkllll
.lllllllllllllll
.gllllllllllllg.
..gggggggggggg..
................
""")

tile("wolf", """
................
................
................
................
..s.s...........
..sss...........
.ssksss.........
sssssssssssss...
.wsssssssssssss.
..ssssssssssss.s
...sssssssssss..
...ss.ss..ss.ss.
...ss.ss..ss.ss.
...kk.kk..kk.kk.
................
................
""")

tile("goblin", """
................
................
................
..l..........l..
..lll.llll.lll..
....llllllll....
....lrllllrl....
....llllllll....
.....lkkkkl.....
......llll....w.
....NNNNNNNN..w.
...lNNNNNNNNl.w.
...l.NNNNNN..ll.
.....NN..NN.....
.....ll..ll.....
....kkk..kkk....
""")

tile("orc", """
.....GGGGGG.....
....GGGGGGGG....
....GrGGGGrG....
....GGGGGGGG....
....GWGGGGWG....
.....GGGGGG.....
..sSSSSSSSSSSs..
.GSSSSSSSSSSSSG.
.GGSSSSSSSSSSGG.
.GG.SSSSSSSS.GGs
.GG.NNNNNNNN.GGs
....NNNNNNNN..ns
....NNN..NNN..n.
....GGG..GGG..n.
....GGG..GGG....
...kkkk..kkkk...
""")

tile("skeleton", """
......wwww......
.....wwwwww.....
.....kkwwkk.....
.....wwwwww.....
......wkkw......
.......ww.......
....wwwwwwww....
...w..wwww..w...
...w.wwwwww.w...
...w..wwww..w...
......wwww......
.....ww..ww.....
.....w....w.....
.....w....w.....
.....w....w.....
....ww....ww....
""")

tile("spider", """
................
................
................
.k..k......k..k.
..k..k....k..k..
...k..kkkk..k...
....kkkkkkkk....
.kkkkkrkkrkkkkk.
k...kkkkkkkk...k
...kkkkRRkkkk...
..k..kkRRkk..k..
.k..k.kkkk.k..k.
.k.k...kk...k.k.
k..k........k..k
................
................
""")

tile("troll", """
....aaaaaa......
...aaaaaaaa...n.
...araaaaraa..nn
...aaaaaaaa..nnn
...aaWWWWaa..nn.
....aaaaaa..an..
.aaaaaaaaaaaaa..
aaaaaaaaaaaaa...
aa.aaaaaaaaa....
aa.NNNNNNNNN....
aa.NNNNNNNNN....
...NNNN.NNNN....
...aaaa.aaaa....
...aaa...aaa....
...aaa...aaa....
..kkkk...kkkk...
""")

tile("ghost", """
................
.....wwwwww.....
....wwwwwwww....
...wwwwwwwwww...
...wwkkwwkkww...
...wwkkwwkkww...
...wwwwwwwwww...
...wwwwkkwwww...
...wwwwkkwwww...
...wwwwwwwwww...
...wwwwwwwwww...
...wwwwwwwwww...
...wwwwwwwwww...
...ww.www.www...
...w...w...w....
................
""")

tile("daemon", """
..w..........w..
..w...rrrr...w..
...w.rrrrrr.w...
....rreRReerr...
.....rrrrrr.....
RR...rWWWWr...RR
RRR.rrrrrrrr.RRR
RRRrrrrrrrrrrRRR
RRRrrrrrrrrrrRRR
.RR.rrrrrrrr.RR.
....rrrrrrrr....
.....rr..rr.....
.....rr..rr...r.
.....rr..rr..r..
....kkk..kkkr...
................
""")

tile("dragon", """
..........RR....
.........RRRR...
........RReRRt..
........RRRRRtt.
.R.....RRRRR..t.
.RR...RRRR......
.RRR.rrRRRRR....
.RRRRrrrrRRRR...
..RRrrrrrrRRRR..
...RrrrrrrrRRR..
....RrrrrrrRRR..
.....RRR..RRR..R
.....RR....RR.R.
....kkk...kkkR..
................
................
""")

tile("serpent", """
................
................
..........ggg...
.........gggggg.
.........gkggg..
.........gggg...
........ggg..r..
.......ggg......
..ggg..ggg......
.ggGgg.gGg......
gg...ggGgg......
g.....ggg.......
................
................
................
................
""")

tile("witch", """
.......U........
......UUU.......
.....UUUUU......
...UUUUUUUUU....
.....lllll...g..
.....kllkll..gg.
.....lllll...n..
......lll....n..
....GGGGGGG..n..
...GGGGGGGGGGn..
...lGGGGGGG..n..
....GGGGGGG..n..
...GGGGGGGGG.n..
...GGGGGGGGG.n..
..GGGGGGGGGGGn..
....NN...NN.....
""")

tile("beaver", """
................
................
................
................
................
.....nnnn.......
....nnnnnn......
...nknnnnnn.....
..Nnnnnnnnnn....
..WWnnnnnnnnn...
...nnnnnnnnnnn..
....nnnnnnnnnNNN
....nnnnnnnnNNNN
....nn.nn..NNNN.
....NN.NN.......
................
""")

tile("moosedain", """
nn..nn....nn..nn
.nnnn......nnnn.
..nnnn....nnnn..
....nnNNNNnn....
......NNNN......
.....NrNNrN.....
.....NNNNNN.....
......NNNN...e..
......NkkN...E..
....uuuuuuuu.n..
...uuuuuuuuuun..
...Nuuuuuuuu.n..
...N.uuuuuu..n..
....uuuuuuuu.n..
...uuuuuuuuuun..
...uuuuuuuuuu...
""")

# ── Effects ──────────────────────────────────────────────────────────────────

tile("canoe", """
................
................
................
......NNNN......
.....NNNNNN.....
.....NffffN.....
.....fkffkf.....
......ffff....n.
....BBBBBBBB.n..
...fBBBBBBBBfn..
...fBBBBBBBBn...
oNNNNNNNNNNNNNNo
.onnnnnnnnnnnno.
..oooooooooooo..
................
................
""")

tile("wizard", """
.......B........
......BeB.......
.....BBBBB......
...BBBBBBBBB....
.....fffff...c..
.....kffkff..cc.
.....WWWWW...n..
......WWW....n..
....BBBBBBB..n..
...BBBBBBBBBBn..
...fBBeBBBB..n..
....BBBBBBB..n..
...BBBBBeBBB.n..
...BBBBBBBBB.n..
..BBBBBBBBBBBn..
....NN...NN.....
""")

tile("puck", """
................
................
................
................
................
................
.....kkkkkk.....
....kKKKKKKk....
....kkkkkkkk....
.....kkkkkk.....
................
................
................
................
................
................
""")

tile("frost", """
................
................
................
.....cccc.......
....ccWWccc.....
...ccWWWWWcc....
...cWWWWWWc.....
...cWWWWWWc.....
...ccWWWWWcc....
....ccWWccc.....
.....cccc.......
................
................
................
................
................
""")

tile("hit", """
................
.......e........
...e...e...e....
....e..e..e.....
.....e.W.e......
......WWW.......
.eeeeWWWWWeeee..
......WWW.......
.....e.W.e......
....e..e..e.....
...e...e...e....
.......e........
................
................
................
................
""")

tile("bolt", """
................
................
................
.....tttt.......
....tteettt.....
...tteWWeett....
...teWWWWet.....
...teWWWWet.....
...tteWWeett....
....tteettt.....
.....tttt.......
................
................
................
................
................
""")


# ── PNG output ───────────────────────────────────────────────────────────────

def png(width, height, pixel):
    """PNG bytes; pixel(x, y) returns an (r, g, b) tuple or None."""
    raw = bytearray()
    for y in range(height):
        raw.append(0)
        for x in range(width):
            c = pixel(x, y)
            raw += bytes((c[0], c[1], c[2], 255)) if c else b"\0\0\0\0"

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff))
    return (b"\x89PNG\r\n\x1a\n" +
            chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6,
                                       0, 0, 0)) +
            chunk(b"IDAT", zlib.compress(bytes(raw), 9)) +
            chunk(b"IEND", b""))


def tile_png(rows):
    return png(16, 16, lambda x, y: PALETTE[rows[y][x]])


def b64_lines(data, indent):
    s = base64.b64encode(data).decode()
    return [indent + '"%s"' % s[i:i + 72] for i in range(0, len(s), 72)]


def tile_block():
    out = ["TILE_PNG = {"]
    for name, rows in TILES.items():
        out.append('    "%s": (' % name)
        out += b64_lines(tile_png(rows), "        ")
        out.append("    ),")
    out.append("}")
    return "\n".join(out)


def icon_block():
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "icon.png")
        subprocess.run([sys.executable, PROGRAM, "--icon-png", "128", path],
                       check=True)
        with open(path, "rb") as fh:
            data = fh.read()
    return "\n".join(["ICON_PNG = ("] + b64_lines(data, "    ") + [")"])


def splice(text, begin, end, block):
    pat = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    if not pat.search(text):
        raise SystemExit("markers %r not found in penultimate" % begin)
    return pat.sub(lambda m: begin + "\n" + block + "\n" + end, text)


def write_sheet(path, cols=10, scale=4):
    names = list(TILES)
    rows = (len(names) + cols - 1) // cols
    cell = 16 * scale + 4

    def pixel(x, y):
        i = (y // cell) * cols + x // cell
        px, py = (x % cell) - 2, (y % cell) - 2
        if i >= len(names) or not (0 <= px < 16 * scale and
                                   0 <= py < 16 * scale):
            return (255, 0, 255)
        c = PALETTE[TILES[names[i]][py // scale][px // scale]]
        return c or (((px // 8 + py // 8) % 2) and (90, 90, 90)
                     or (60, 60, 60))
    with open(path, "wb") as fh:
        fh.write(png(cols * cell, rows * cell, pixel))
    for r in range(rows):
        print(" ".join(names[r * cols:(r + 1) * cols]))


def main():
    args = sys.argv[1:]
    if args[:1] == ["--sheet"]:
        write_sheet(args[1] if len(args) > 1 else "sheet.png")
    with open(PROGRAM) as fh:
        text = fh.read()
    text = splice(text, "# ── TILE DATA BEGIN", "# ── TILE DATA END",
                  tile_block())
    with open(PROGRAM, "w") as fh:
        fh.write(text)
    text = splice(text, "# ── ICON DATA BEGIN", "# ── ICON DATA END",
                  icon_block())
    with open(PROGRAM, "w") as fh:
        fh.write(text)
    print("updated %s: %d tiles" % (PROGRAM, len(TILES)))


if __name__ == "__main__":
    main()
