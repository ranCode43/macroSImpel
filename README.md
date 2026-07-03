# USB macropad — mute / volume buttons + RGB volume bar

A USB macropad built on a Raspberry Pi Pico running CircuitPython: three
buttons (mute, volume down, volume up) and an 8-pixel RGB LED strip that
acts as a live volume-level bar. No firmware compiling — just Python files
on a USB drive.

## Parts

| Part | Notes |
|---|---|
| Raspberry Pi Pico (or Pico H) | Any RP2040 Pico works |
| 3x momentary push buttons | Mute / Volume down / Volume up |
| 1x NeoPixel Stick, 8x WS2812 | Used as a volume-level bar |
| Male-to-male jumper wires | ~4 needed (Pico power/data + spares) |
| Alligator-clip-to-male-jumper leads | ~7 needed — used instead of a breadboard, see wiring below |
| USB cable (data-capable) | Micro-USB or USB-C depending on your Pico |

No breadboard required — every connection below is direct point-to-point
wiring using alligator clips instead of a shared rail.

## 1. Wiring (no breadboard — alligator clips)

Every part connects straight to the Pico with an alligator-clip-to-male-jumper
lead: clip end onto the component's leg/pad, male jumper end straight into
the Pico's GPIO pin header.

**Buttons** — each has 2 legs: one clips to a GPIO pin, the other clips to
GND. Internal pull-ups handle the logic, no resistors needed.

| Button | Pico pin | Function |
|---|---|---|
| 1 | GP2 | Mute |
| 2 | GP3 | Volume down |
| 3 | GP4 | Volume up |

**RGB LED bar (NeoPixel Stick, 8x WS2812)** — 3 wires:

| Stick pin | Pico pin |
|---|---|
| DIN (data) | GP0 |
| VCC | 3V3 or 5V |
| GND | GND |

The 8 LEDs work as a volume-level bar: more pixels light up (green → amber
→ red) as volume goes up, and all 8 turn solid red when muted.

**Grounding tip:** you'll have 4 separate GND connections (3 buttons + the
NeoPixel stick) but only one GND pin on the Pico. Clip all 4 GND leads onto
one shared alligator clip, then run a single jumper from that clip to the
Pico's GND pin — effectively building your own tiny ground rail without a
breadboard.

## 2. Flash CircuitPython onto the Pico

1. Download the latest **CircuitPython UF2** for Raspberry Pi Pico from
   circuitpython.org/board/raspberry_pi_pico/.
2. Hold **BOOTSEL**, plug the Pico into USB, release BOOTSEL.
3. Drag the `.uf2` onto the `RPI-RP2` drive that appears.
4. It reboots into a `CIRCUITPY` drive automatically.

## 3. Install libraries

Download the **Adafruit CircuitPython Bundle** (version matched to your
CircuitPython version) from circuitpython.org/libraries, unzip it, and copy
these into a `lib` folder on `CIRCUITPY`:

- `adafruit_hid/` (folder)
- `neopixel.mpy`

```
CIRCUITPY/
  lib/
    adafruit_hid/
    neopixel.mpy
  code.py
```

## 4. Copy the code

Copy `code.py` from this repo onto the root of `CIRCUITPY`, overwriting the
existing one.

Save and it auto-runs:
- Press mute -> mute toggles, bar goes solid red / restores to volume level.
- Press volume down/up -> fewer/more pixels light up (green -> amber -> red
  as it climbs).

## Changing behavior

- Button pins or colors: edit the constants near the top of `code.py`.
- LED too bright/dim: change `brightness=0.3` in the `neopixel.NeoPixel(...)`
  line (0.0-1.0).

## Case

Cardboard works for v1 - cut holes for the 3 buttons and a slot for the
8-pixel LED strip. Hot glue or tape the Pico down inside the case first so
the alligator-clip leads have something stable to connect to, then wire up
the buttons and LED strip.

## Repo structure

```
macropad/
  code.py       # runs on the Pico
  README.md     # this file
  BOM.csv       # full parts list with estimated prices
  JOURNAL.md    # build log - decisions, problems, history
  LICENSE       # MIT license
  .gitignore
```

See `BOM.csv` for the full parts list and `JOURNAL.md` for the build history
and a template to log your own progress as you go.
