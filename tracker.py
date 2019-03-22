import subprocess
import datetime
import json
import os
import time

import mss
import pyocr
from PIL import Image

import chatdiscipline
import hotkeys

# Per second
SAMPLE_PERIOD = 1
SAVING_PERIOD = 60*10
CHAT_MONITOR_PERIOD = 5

sct = mss.mss()
tools = pyocr.get_available_tools()
tool = tools[0]

chatmonitor = chatdiscipline.Monitor()
hotkeymonitor = hotkeys.HotkeyMonitor()

def dump_to_file(data):
  logpath = os.path.join("logs", datetime.date.today().isoformat()+".json")
  if os.path.exists(logpath):
    with open(logpath, "r") as f:
      prev_data = json.load(f)

    for app,detail in prev_data.items():
      if app in data:
        for title,time in detail.items():
          if title in data[app]:
            data[app][title] += time
          else:
            data[app][title] = time
      else:
        data[app] = detail

  with open(logpath, "w") as f:
    json.dump(data, f, indent=4)

def execute(command):
  try:
    return subprocess.check_output(command).decode("utf-8").strip()
  except subprocess.CalledProcessError:
    pass

def beautify(app, title):
  app = app.lower()
  if app == "gnome-terminal-":
    app = "gnome-terminal"
  elif app == "discord":
    screenshot = sct.grab({"left": 137, "top": 64, "width": 213, "height": 48})
    img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
    img = img.resize((img.width*5, img.height*5))
    servername = tool.image_to_string(img)
    if servername == "raeled":
      servername = "/div/"
    elif servername == "lOT-Schweiz":
      servername = "IOT-Schweiz"
    channel = title.split()[0]
    title = servername + " - " + channel
  elif app == "firefox":
    idx = title.rfind(" - ")
    title = title[:idx]
  elif app == "java":
    if "PyCharm" in title:
      app = "pycharm"
      idx = title.rfind(" - ")
      title = title[:idx]
  elif app == "signal-desktop":
    app = "Signal"
    title = "Signal"
  elif app == "telegram":
    title = "Telegram"

  return app, title

def main():
  data = {}
  last_dump_time = datetime.datetime.now()
  last_chatmonitor_time = datetime.datetime.now()
  monitored_apps = chatmonitor.get_apps()
  while True:
    pid = execute(["xdotool", "getactivewindow", "getwindowpid"])
    title = execute(["xdotool", "getactivewindow", "getwindowname"])
    app = execute(["ps", "-p", pid, "-o", "comm="]) if pid != None else "Unknown"
    app, title = beautify(app, title)
    if app in monitored_apps:
      chatmonitor.reset(app)
    if app not in data:
      data[app] = { title: SAMPLE_PERIOD }
    else:
      if title not in data[app]:
        data[app][title] = SAMPLE_PERIOD
      else:
        data[app][title] += SAMPLE_PERIOD

    if datetime.datetime.now() - last_chatmonitor_time > datetime.timedelta(seconds=CHAT_MONITOR_PERIOD):
      chatmonitor.step(CHAT_MONITOR_PERIOD)
      last_chatmonitor_time = datetime.datetime.now()

    if datetime.datetime.now() - last_dump_time > datetime.timedelta(seconds=SAVING_PERIOD):
      dump_to_file(data)
      data = {}
      last_dump_time = datetime.datetime.now()

    time.sleep(SAMPLE_PERIOD)


if __name__ == "__main__":
  main()
