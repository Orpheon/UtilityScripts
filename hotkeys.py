import subprocess
import pynput
import time

def execute(command):
  try:
    return subprocess.check_output(command).decode("utf-8").strip()
  except subprocess.CalledProcessError:
    pass

class HotkeyMonitor:
  def __init__(self):
    self.modifiers = {
      "ctrl": 0,
      "alt": 0
    }
    self.hotkeys = {
      pynput.keyboard.KeyCode.from_char("1"): self.open_google,
      pynput.keyboard.KeyCode.from_char("2"): self.open_youtube,
      pynput.keyboard.KeyCode.from_char("3"): self.open_google_scholar
    }

    self.keywatcher = pynput.keyboard.Listener(
      on_press=self.on_keypress,
      on_release=self.on_keyrelease
    )
    self.keywatcher.start()
    self.keycontroller = pynput.keyboard.Controller()

  def on_keypress(self, key):
    if key in (pynput.keyboard.Key.ctrl, pynput.keyboard.Key.ctrl_l, pynput.keyboard.Key.ctrl_r):
      self.modifiers["ctrl"] = 1
    elif key in (pynput.keyboard.Key.alt, pynput.keyboard.Key.alt_l, pynput.keyboard.Key.alt_r):
      self.modifiers["alt"] = 1
    elif key in self.hotkeys.keys():
      if sum(self.modifiers.values()) == len(self.modifiers):
        self.hotkeys[key]()

  def on_keyrelease(self, key):
    if key in (pynput.keyboard.Key.ctrl, pynput.keyboard.Key.ctrl_l, pynput.keyboard.Key.ctrl_r):
      self.modifiers["ctrl"] = 0
    elif key in (pynput.keyboard.Key.alt, pynput.keyboard.Key.alt_l, pynput.keyboard.Key.alt_r):
      self.modifiers["alt"] = 0

  def tap_keys(self, keys):
    for key in keys:
      self.keycontroller.press(key)
    for key in reversed(keys):
      self.keycontroller.release(key)
    time.sleep(0.1)

  def open_private_ff_window(self):
    query = execute(["wmctrl", "-l"])
    firefoxes = [line for line in query.split("\n") if "Mozilla Firefox" in line]
    private = [line for line in firefoxes if "Mozilla Firefox (Private Browsing)" in line]
    if len(private) == 0:
      id = firefoxes[0].split()[0]
      execute(["wmctrl", "-ia", id])
      self.tap_keys((pynput.keyboard.Key.ctrl, pynput.keyboard.Key.shift, pynput.keyboard.KeyCode.from_char("p")))
      time.sleep(0.4)
    else:
      id = private[0].split()[0]
      execute(["wmctrl", "-ia", id])
      self.tap_keys((pynput.keyboard.Key.ctrl, pynput.keyboard.KeyCode.from_char("t")))

  def open_google(self):
    self.open_private_ff_window()
    self.tap_keys((pynput.keyboard.Key.ctrl, pynput.keyboard.KeyCode.from_char("l")))
    execute(["xdotool", "type", "google.com"])
    self.tap_keys([pynput.keyboard.Key.enter])

  def open_youtube(self):
    self.open_private_ff_window()
    self.tap_keys((pynput.keyboard.Key.alt, pynput.keyboard.KeyCode.from_char("1")))
    title = execute(["xdotool", "getactivewindow", "getwindowname"])
    while not title:
      time.sleep(0.2)
      title = execute(["xdotool", "getactivewindow", "getwindowname"])
    if "YouTube" not in title:
      self.tap_keys((pynput.keyboard.Key.ctrl, pynput.keyboard.KeyCode.from_char("t")))
      execute(["xdotool", "type", "youtube.com"])
      self.tap_keys([pynput.keyboard.Key.enter])

      self.keycontroller.press(pynput.keyboard.Key.ctrl)
      self.keycontroller.press(pynput.keyboard.Key.shift)
      for i in range(25):
        self.keycontroller.press(pynput.keyboard.Key.page_up)
        self.keycontroller.release(pynput.keyboard.Key.page_up)
      self.keycontroller.release(pynput.keyboard.Key.ctrl)
      self.keycontroller.release(pynput.keyboard.Key.shift)

  def open_google_scholar(self):
    self.open_private_ff_window()
    self.tap_keys((pynput.keyboard.Key.ctrl, pynput.keyboard.KeyCode.from_char("l")))
    execute(["xdotool", "type", "scholar.google.com"])
    self.tap_keys([pynput.keyboard.Key.enter])