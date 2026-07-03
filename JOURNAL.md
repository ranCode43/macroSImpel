# Build journal

A running log of decisions, problems, and fixes for this project. Add a new
dated entry each time you work on it.

---

## Entry template (copy this for new entries)

```
## YYYY-MM-DD

**Did today:**
-

**Problems hit:**
-

**Fixes / decisions:**
-

**Next step:**
-
```

---

## Project history so far

### Attempt 1 — Seeed XIAO RP2040 + custom PCB + QMK
- Started from a KiCad PCB/schematic zip for a 3-key macropad on a Seeed
  XIAO RP2040. Direct-pin wiring (no matrix): D8→GP2, D9→GP4, D10→GP3.
- Built a custom `hackpad3` QMK keyboard folder for direct pin matrix mode.
- Hit repeated QMK CLI errors:
  - `invalid keyboard_folder_or_all value: 'hackpad3'` — traced to
    `qmk_home` being unset.
  - After setting `qmk_home`, hit `invalid choice: 'compile'` — meant the
    QMK CLI install itself was incomplete/missing the compile subcommand.
- **Decision:** parked this — too much toolchain friction for a same-day
  build.

### Attempt 2 — Pico H + breadboard + alligator clips
- Started a hardware store run for a simpler breadboard build.
- Cart mistakes caught before checkout:
  - F-F (female-female) jumper wires don't plug into a breadboard — need
    M-M (male-male).
  - "Perma-Proto" board looked like a breadboard but is solder-only, not
    solderless.
- Couldn't find tactile buttons in-store — fell back to panel-mount push
  buttons + alligator clip leads.
- **Decision:** scrapped this too — decided it was getting overcomplicated
  with too many part swaps and a design that had drifted from anything
  documented.

### Attempt 3 (current) — Pico + CircuitPython + OLED
- Reset to a simple, achievable scope: Pico, 3 direct-wired buttons, no
  matrix, no PCB.
- Switched firmware approach entirely: **CircuitPython instead of QMK.**
  No compiling — `code.py` runs directly off the board's USB drive. This
  sidesteps every QMK CLI issue from attempt 1.
- Base version: 3 buttons → Mute / Volume down / Volume up via
  `adafruit_hid.consumer_control`.
- Added an SSD1306 I2C OLED display for status feedback (last button
  pressed + a locally-tracked volume percentage, since USB HID can send
  volume commands but can't read the OS's actual volume back).
- **Status:** code and docs written, not yet physically wired/tested.

---

## Known open items
- [ ] Confirm OLED I2C address (0x3C vs 0x3D) once the physical board is in
      hand — check the sticker/silkscreen on the module or scan the bus.
- [ ] Physically wire per `README.md` and test each button + the display.
- [ ] Push repo to GitHub.
- [ ] Cardboard case cutout for 3 buttons + OLED window.

---

## Update: dropped the OLED, added rotary encoder + RGB LED

The SSD1306 OLED (128x32 I2C) is out. It was cosmetic-only anyway -
CircuitPython can't read back the real OS volume over USB HID, so the
on-screen number was just a local counter, not the real level.

Swapped in:
- **Rotary encoder** (KY-040 style, CLK/DT/SW/+/GND) replaces the separate
  Volume Up / Volume Down buttons. Turning it sends volume up/down via
  `rotaryio.IncrementalEncoder`; pressing the knob in sends Play/Pause.
- **Single WS2812/NeoPixel RGB LED** replaces the screen for feedback - dim
  blue when idle, green/cyan flash on volume turns, red when muted, purple
  flash on play/pause.

New pinout:
- GP2 -> Mute button
- GP3 -> Encoder CLK
- GP4 -> Encoder DT
- GP5 -> Encoder push switch (SW)
- GP0 -> NeoPixel data in

Net result: fewer parts than the OLED version (no display, no displayio
dependencies to fight with), and the feedback is more glanceable - a color
change vs. reading small OLED text.

## Updated open items
- [ ] Physically wire per `README.md` and test mute button + encoder + LED.
- [ ] Confirm encoder rotation direction matches expectation (swap CLK/DT
      pins in `code.py` if reversed).
- [ ] Push repo to GitHub.
- [ ] Cardboard case cutout for button, encoder shaft, and LED window.

---

## Update: single NeoPixel -> 8-pixel NeoPixel Stick, volume bar

Swapped the single RGB LED for an 8x WS2812 NeoPixel Stick to put the extra
pixels to use as an actual volume-level bar instead of just a status flash.

Behavior now:
- Idle: pixel count lit = volume/100 * 8, color ramps green -> amber -> red
  as level rises.
- Muted: all 8 pixels solid red.
- Play/pause: whole bar flashes purple briefly, then restores to the
  volume-bar display.
- Turning the encoder implicitly un-mutes (matches how most OS volume
  controls behave).

Wiring unchanged from the single-pixel version - still just DIN/VCC/GND on
GP0/3V3(or 5V)/GND. Code changed from `neopixel.NeoPixel(board.GP0, 1, ...)`
to `neopixel.NeoPixel(board.GP0, 8, ...)` plus the bar-fill logic in
`refresh_bar()`.

## Updated open items
- [ ] Physically wire per `README.md` and test mute button + encoder + bar.
- [ ] Confirm encoder rotation direction matches expectation (swap CLK/DT
      pins in `code.py` if reversed).
- [ ] Push repo to GitHub.
- [ ] Cardboard case cutout for button, encoder shaft, and LED strip slot.

---

## Update: dropped the rotary encoder, back to 3 buttons

The rotary encoder module (KY-040 style) turned out to be a pain to source
locally - Micro Center only carries one listing (Inland KS0013), and it was
out of stock / effectively ship-only anyway. Rather than wait on shipping,
reverted to the original 3-button approach (Mute / Volume down / Volume up)
from the very first CircuitPython version, but kept the 8-pixel NeoPixel
volume bar from the encoder version - it works exactly the same whether
volume changes come from a knob or a button.

New pinout:
- GP2 -> Mute button
- GP3 -> Volume down button
- GP4 -> Volume up button
- GP0 -> NeoPixel Stick data in

Play/pause (which was tied to the encoder's push switch) is dropped for now
- see "options to add" for ways to bring it back with a 4th button instead.

## Updated open items
- [ ] Physically wire per `README.md` and test all 3 buttons + LED bar.
- [ ] Push repo to GitHub.
- [ ] Cardboard case cutout for 3 buttons and LED strip slot.

---

## Update: sourced everything, dropped the breadboard, went alligator clips

Couldn't find a solderless breadboard in stock anywhere nearby (Micro Center
Rockville, Fairfax - all out). Since this build is just direct point-to-point
wiring (no need for a breadboard's shared rails except for grounding), swapped
in an Adafruit alligator-clip-to-male-jumper bundle instead - clip end grabs
the button legs/NeoPixel pads, jumper end plugs straight into the Pico's GPIO
header. All 4 GND connections (3 buttons + NeoPixel) get bundled onto one
shared clip, then a single jumper runs from that clip to the Pico's GND pin.

Full order picked up at Micro Center Rockville:
- Pico H (SKU 412213) - $3.99
- USB 2.0 Type-A to Micro-USB cable (SKU 402008) - $5.99
- 6x6mm tactile push button assortment (SKU 221788) - $9.99
- Male-to-male jumper wires, 40-pack (SKU 847178) - $7.99
- NeoPixel Stick, 8x WS2812 (SKU 493114) - $5.95
- Alligator clip to male jumper bundle, 12pc (SKU 758128) - $8.99

Total: $42.90. Every part is now in hand - no more sourcing needed.

## Final open items
- [ ] Flash CircuitPython onto the Pico H.
- [ ] Wire per README.md (buttons on GP2/GP3/GP4, NeoPixel on GP0, shared
      GND clip).
- [ ] Confirm all 3 buttons and the LED bar work as expected.
- [ ] Push repo to GitHub.
- [ ] Cardboard case cutout for 3 buttons and LED strip slot.
