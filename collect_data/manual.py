import asyncio
from queue import Empty, Queue
import sys
import termios
import time
from threading import Thread
import tty

from pynput import keyboard

NO_OF_FSRS = 3
NO_OF_PIEZOS = 3

from voyage_touch.sensor import SensorType, TouchSensor, TouchSensorReader

# Example for a manual data collection process.
# This example is for Markovian predictions and does not use time series measurement data

class EscapeException(Exception): pass

def on_press(key):
    if key == keyboard.Key.esc:
        raise EscapeException(key)
    if hasattr(key, 'char') and key.char in '123456789':
        print(f"Key {key.char} pressed")

def on_release(key):
    if hasattr(key, 'char') and key.char in '123456789':
        print(f"Key {key.char} released")

def disable_echo():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    return old_settings

def enable_echo(old_settings):
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def record_sensor_values(q: Queue):    
    while True:
        try:
            msg = q.get()
            if msg is False:
                # graceful shutdown
                return

            sensor_id = msg.sensor_id
            if msg.sensor_type is SensorType.PIEZO:
                sensor_id += NO_OF_FSRS

            # TODO: record reading

            display_value = msg.value
            if msg.sensor_type is SensorType.PIEZO:
                display_value *= 160
            else:
                display_value *= 1000


        except Empty:
            pass

if __name__ == '__main__':
    old_settings = disable_echo() 

    sensor = TouchSensor('/dev/ttyACM0')
    reader = TouchSensorReader(sensor)

    # initialise reader
    q = Queue()
    reader.register_listener(0, q)
    thread = asyncio.run(reader.start())
    time.sleep(1)

    # start sensor value recorder thread
    sensor_thread = Thread(target=lambda: asyncio.run(record_sensor_values(q)))
    sensor_thread.start()

    # thread 2
    # Run until exit
    with keyboard.Listener(
        on_press=on_press) as listener:
        while True:
            try:
                listener.join(0.01)
            except EscapeException as e:
                print('Terminating...')
                enable_echo(old_settings)

                reader.stop()
                thread.join()
                q.put(False)
                sensor_thread.join()

                exit()
