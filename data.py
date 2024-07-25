from pynput import mouse, keyboard
import json
import time

mouse_data = []
keyboard_data = []

def on_move(x, y):
    mouse_data.append({'x': x, 'y': y, 'time': time.time()})

def on_click(x, y, button, pressed):
    mouse_data.append({'x': x, 'y': y, 'button': str(button), 'pressed': pressed, 'time': time.time()})

def on_scroll(x, y, dx, dy):
    mouse_data.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'time': time.time()})

def on_press(key):
    keyboard_data.append({'key': str(key), 'type': 'press', 'time': time.time()})

def on_release(key):
    keyboard_data.append({'key': str(key), 'type': 'release', 'time': time.time()})

# Collect events
mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

mouse_listener.start()
keyboard_listener.start()

# Run the listeners for a while then save data
time.sleep(60)
mouse_listener.stop()
keyboard_listener.stop()

# Save data to JSON
with open('mouse_data.json', 'w') as mouse_file:
    json.dump(mouse_data, mouse_file)

with open('keyboard_data.json', 'w') as keyboard_file:
    json.dump(keyboard_data, keyboard_file)
