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
