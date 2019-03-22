import subprocess
import os
import datetime

def execute(command):
  try:
    return subprocess.check_output(command).decode("utf-8").strip()
  except subprocess.CalledProcessError:
    pass

class Monitor:
  chatapps = [
    "discord",
    "telegram",
    "hexchat"
  ]
  CHAT_KILL_CD = 10 * 60 # in seconds

  def __init__(self):
    self.appusagecooldown = {c: 0 for c in self.chatapps}

  def get_apps(self):
    return self.chatapps

  def kill(self, app):
    execute(["killall", app.lower()])
    execute(["killall", app.capitalize()])
    self.appusagecooldown[app.lower()] = 0

  def reset(self, app):
    self.appusagecooldown[app.lower()] = 0

  def step(self, period):
    if os.path.exists("run_chatdisc") and (datetime.datetime.now().hour % 22) < 7:
      pids = [p for p in os.listdir("/proc") if p.isdigit()]
      data = ""
      for pid in pids:
        try:
          data += open(os.path.join("/proc", pid, "cmdline"), "r").read().split("\0")[0]
        except IOError:
          continue
      for app in self.chatapps:
        if app in data or app.capitalize() in data:
          self.appusagecooldown[app] += period
          if self.appusagecooldown[app] >= self.CHAT_KILL_CD:
            self.kill(app)
