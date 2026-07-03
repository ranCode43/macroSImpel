# 3-button media macropad with OLED status display

A USB macropad built on a Raspberry Pi Pico running CircuitPython, with a
small I2C OLED screen showing the last button pressed and a locally-tracked
volume level. No firmware compiling — just Python files on a USB drive.

Buttons: **Mute / Volume down / Volume up**, with live feedback on screen.

## Parts

| Part | Notes |
|---|---|
| Raspberry Pi Pico (or Pico H) | Any RP2040 Pico works |
| Solderless breadboard | Not a "Perma-Proto" board — needs to be push-in |
| 3x momentary push buttons | Panel-mount or breadboard tactile, either works |
| SSD1306 OLED, 128x32, I2C | The 4-pin (VCC/GND/SDA/SCL) version, not SPI |
| Male-to-male jumper wires | ~10 needed (2 per button + 4 for the OLED) |
| USB cable (data-capable) | Micro-USB or USB-C depending on your Pico |

## 1. Wiring

**Buttons** — each connects one leg to a GPIO pin, the other leg to GND
(shared ground rail). Internal pull-ups handle debouncing logic, no
resistors needed.

| Button | Pico pin | Function |
|---|---|---|
| 1 | GP2 | Mute |
| 2 | GP3 | Volume down |
| 3 | GP4 | Volume up |

**OLED (I2C)** — 4 wires:

| OLED pin | Pico pin |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SDA | GP0 |
| SCL | GP1 |

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
- `adafruit_displayio_ssd1306.mpy`
- `adafruit_display_text/` (folder)

```
CIRCUITPY/
  lib/
    adafruit_hid/
    adafruit_displayio_ssd1306.mpy
    adafruit_display_text/
  code.py
```

## 4. Copy the code

Copy `code.py` from this repo onto the root of `CIRCUITPY`, overwriting the
existing one.

Save and it auto-runs. Press a button → your computer's volume responds
*and* the OLED shows which button you pressed plus a running local volume
percentage (0-100, ±5 per press). Mute toggles a "MUTED" display.

Note: the on-screen volume number is cosmetic — CircuitPython can send
volume-up/down/mute commands over USB HID, but it has no way to read back
your computer's actual system volume, so the screen tracks its own local
count starting at 50.

## Changing behavior

- Button functions: edit `BUTTON_MAP` at the top of `code.py`.
- Display layout/text: edit the `label.Label(...)` lines.
- OLED not showing anything: double check the I2C address — most SSD1306
  boards are `0x3C`, some are `0x3D`. Change `device_address=0x3C` in
  `code.py` if needed.

## Case

Cardboard works for v1 — cut holes for the 3 buttons and a window for the
OLED. Hot glue or tape the Pico/breadboard/OLED inside.

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
