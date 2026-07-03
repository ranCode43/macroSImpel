"""
USB media macropad: mute / volume down / volume up buttons + RGB volume bar
Raspberry Pi Pico + CircuitPython + adafruit_hid + neopixel

Buttons (each wired to GPIO + shared GND, using internal pull-ups):
  GP2 -> Mute
  GP3 -> Volume down
  GP4 -> Volume up

RGB LED strip (NeoPixel Stick, 8x WS2812):
  GP0 -> DIN
  5V or 3V3 -> VCC (5V recommended if your Pico board breaks it out; 3V3 also works, just dimmer)
  GND -> GND
"""

import time
import board
import digitalio
import neopixel
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

# ---------- HID setup ----------

cc = ConsumerControl(usb_hid.devices)

BUTTON_MAP = {
    board.GP2: ("Mute", ConsumerControlCode.MUTE),
    board.GP3: ("Vol down", ConsumerControlCode.VOLUME_DECREMENT),
    board.GP4: ("Vol up", ConsumerControlCode.VOLUME_INCREMENT),
}

buttons = {}
for pin, (name, code) in BUTTON_MAP.items():
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.UP  # True = not pressed, False = pressed (shorted to GND)
    buttons[pin] = {"io": io, "name": name, "code": code, "was_pressed": False}

DEBOUNCE_SEC = 0.03

# ---------- RGB LED bar (8 pixels) ----------

NUM_PIXELS = 8
pixels = neopixel.NeoPixel(board.GP0, NUM_PIXELS, brightness=0.3, auto_write=False)

COLOR_OFF = (0, 0, 0)
COLOR_MUTE = (60, 0, 0)  # solid red across the whole bar

# Volume bar color ramps from green (low) -> amber (mid) -> red (high),
# so the bar itself gives a rough "how loud" read at a glance.
def bar_color_for_index(i):
    fraction = i / (NUM_PIXELS - 1)  # 0.0 .. 1.0
    if fraction < 0.5:
        t = fraction / 0.5
        r = int(20 + t * 40)
        g = 60
        b = 0
    else:
        t = (fraction - 0.5) / 0.5
        r = 60
        g = int(60 - t * 60)
        b = 0
    return (r, g, b)

# Purely local, cosmetic volume tracker for the LED bar -- CircuitPython
# can't read the real OS volume back over USB HID, so this mirrors button
# presses so the bar has something meaningful to show, starting at midpoint.
volume = 50  # 0-100
muted = False

def refresh_bar():
    if muted:
        pixels.fill(COLOR_MUTE)
        pixels.show()
        return
    lit = round((volume / 100) * NUM_PIXELS)
    for i in range(NUM_PIXELS):
        pixels[i] = bar_color_for_index(i) if i < lit else COLOR_OFF
    pixels.show()

refresh_bar()

# ---------- Main loop ----------

while True:
    for pin, b in buttons.items():
        pressed = not b["io"].value
        if pressed and not b["was_pressed"]:
            cc.send(b["code"])

            if b["name"] == "Mute":
                muted = not muted
            else:
                muted = False
                if b["name"] == "Vol down":
                    volume = max(0, volume - 5)
                elif b["name"] == "Vol up":
                    volume = min(100, volume + 5)

            refresh_bar()
            time.sleep(DEBOUNCE_SEC)

        b["was_pressed"] = pressed

    time.sleep(0.01)
