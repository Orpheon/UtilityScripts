import os
import json
from collections import OrderedDict

def loadalllogs():
  logpath = "logs"
  data = {}
  for dirpath, dirname, files in os.walk(logpath):
    firstfile = sorted(files)[0].replace(".json", "")
    lastfile = sorted(files)[-1].replace(".json", "")
    print("{0} logfiles found, from {1} to {2}.".format(len(files), firstfile, lastfile))
    for file in files:
      with open(os.path.join(dirpath, file), "r") as f:
        data[file.replace(".json", "")] = json.load(f)
  return OrderedDict(sorted(data.items(), key=lambda x: x[0]))

def customround(x):
  return round(x, 2)

def printtotalstatistics(data):
  # This only counts days where ubuntu was on at least once
  ndays = len(data)
  totaltime = ndays*24*3600
  # Assuming 8 hours of sleeping on average per day
  totalawaketime = ndays*16*3600
  apptotal = {}
  days = []
  for day, apps in data.items():
    totaltimetoday = 0
    for app, windows in apps.items():
      if app not in apptotal:
        apptotal[app] = 0
      for title, time in windows.items():
        apptotal[app] += time
        totaltimetoday += time
    days.append(totaltimetoday)

  print("Overall statistics:")
  print("\tNumber of days tracked: {0} (days when the computer was never turned on are not counted)".format(len(days)))
  print("\tNumber of different apps used: {0}, {1} for more than an hour".format(len(apptotal),
                                                                                 len([1 for k,v in apptotal.items() if v > 3600])))
  print("\tTime spent on ubuntu:")
  print("\t\t{0} hours, {1} hours per day on average".format(customround(sum(days)/3600),
                                                             customround(sum(days)/3600/len(days))))
  print("\t\t{}% of time awake".format(customround(100*sum(days)/totalawaketime)))
  print("\t\t{}% of total time".format(customround(100*sum(days)/totaltime)))
  print("\tBy app (showing all those used more than an hour):")
  for app, time in sorted(apptotal.items(), key=lambda x: x[1], reverse=True):
    if time > 3600:
      print("\t\t{}".format(app))
      print("\t\t\t{0} total hours, {1} hours per day avg".format(customround(time/3600), customround(time/3600/len(days))))
      print("\t\t\t{}% of time awake".format(customround(100*time/totalawaketime)))
      print("\t\t\t{}% of total time".format(customround(100*time/totaltime)))



data = loadalllogs()
printtotalstatistics(data)