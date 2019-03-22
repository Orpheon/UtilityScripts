from pynput import mouse, keyboard
import sys
import time

class ClickRecorder:
  def __init__(self):
    self.clicks = []

  def click(self, x, y, button, press):
    if press and button == mouse.Button.left:
      self.clicks.append((x, y))
      print(x, y, button, press)
    elif press:
      print(self.clicks)
      raise IOError

class ClickOutput:
  telegram_icon = (30, 373)
  telegram_upload = (510, 1181)
  telegram_file = (852, 743)
  telegram_confirm = (1119, 844)
  images = [(828, 146), (821, 168), (829, 197), (828, 223), (826, 241), (827, 261), (818, 285), (824, 306), (822, 340), (824, 364), (826, 378), (826, 401), (828, 431), (828, 452), (829, 473), (830, 499), (830, 521), (830, 534), (829, 560), (828, 579), (828, 610), (832, 633), (830, 656), (829, 679), (829, 703), (829, 731), (829, 742), (829, 773), (827, 793), (825, 819), (829, 843), (826, 859), (824, 885), (824, 909), (824, 938), (821, 947), (829, 975), (827, 1002), (832, 1023), (840, 1041), (842, 1065), (849, 1095), (850, 1115)]

  def run(self):
    k = keyboard.Controller()
    m = mouse.Controller()

    m.position = self.telegram_icon
    m.click(mouse.Button.left)
    time.sleep(0.1)
    with k.pressed(keyboard.Key.shift):
      # American keyboards can fug off
      k.press('7')
      k.release('7')
    k.type("newpack")
    time.sleep(0.1)
    k.press(keyboard.Key.enter)
    k.release(keyboard.Key.enter)
    time.sleep(0.1)

    def wait_for_enter(key):
      if key == keyboard.Key.enter:
        return False
    with keyboard.Listener(
      on_release=wait_for_enter) as listener:
      listener.join()

    time.sleep(0.5)

    for image in self.images:
      m.position = self.telegram_upload
      m.click(mouse.Button.left)
      time.sleep(0.5)

      m.position = image
      time.sleep(0.1)
      m.click(mouse.Button.left, 2)
      time.sleep(0.2)

      m.position = self.telegram_file
      time.sleep(0.1)
      m.click(mouse.Button.left)
      time.sleep(0.4)

      k.press(keyboard.Key.enter)
      time.sleep(0.2)
      k.release(keyboard.Key.enter)
      time.sleep(2)

      with k.pressed(keyboard.Key.shift):
        k.press('.')
        k.release('.')
      k.type("heart")
      with k.pressed(keyboard.Key.shift):
        k.press('.')
        k.release('.')
      time.sleep(0.1)
      k.press(keyboard.Key.enter)
      k.release(keyboard.Key.enter)
      time.sleep(0.2)


# c = ClickRecorder()
# with mouse.Listener(
#     on_click=c.click) as listener:
#   try:
#     listener.join()
#   except IOError as e:
#     sys.exit(0)

c = ClickOutput()
c.run()