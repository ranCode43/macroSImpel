"""
3-button USB media macropad with OLED status display
Raspberry Pi Pico + CircuitPython + adafruit_hid + adafruit_displayio_ssd1306

Buttons (each wired to GPIO + shared GND, using internal pull-ups):
  GP2 -> Mute
  GP3 -> Volume down
  GP4 -> Volume up

OLED (I2C):
  GP0 -> SDA
  GP1 -> SCL
  3V3 -> VCC
  GND -> GND
"""

import time
import board
import busio
import digitalio
import displayio
import terminalio
import usb_hid
from adafruit_display_text import label
import adafruit_displayio_ssd1306
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

# ---------- Display setup ----------

displayio.release_displays()
i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=32)

splash = displayio.Group()
display.root_group = splash

status_label = label.Label(terminalio.FONT, text="Macropad ready", x=4, y=6)
volume_label = label.Label(terminalio.FONT, text="Vol: 50", x=4, y=20)
splash.append(status_label)
splash.append(volume_label)

# Purely local, cosmetic volume tracker for the screen -- CircuitPython can't
# read the real OS volume back over USB HID, so this just mirrors button
# presses so the screen has something meaningful to show.
volume = 50
muted = False

def refresh_display():
    volume_label.text = "MUTED" if muted else "Vol: {}".format(volume)

refresh_display()

LAST_ACTION_DISPLAY_SEC = 1.5
last_action_time = 0

# ---------- Main loop ----------

while True:
    now = time.monotonic()

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

            status_label.text = b["name"]
            refresh_display()
            last_action_time = now

            time.sleep(DEBOUNCE_SEC)

        b["was_pressed"] = pressed

    # Clear the "last action" text back to idle after a short delay
    if status_label.text != "Macropad ready" and (now - last_action_time) > LAST_ACTION_DISPLAY_SEC:
        status_label.text = "Macropad ready"

    time.sleep(0.01)
