from pynput.keyboard import Controller

keyboard = Controller()

def press_key(key):
    if key:
        keyboard.press(key)
        keyboard.release(key)
