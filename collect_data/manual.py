import asyncio
from queue import Empty, Queue
import sys
import termios
import time
from threading import Event, Thread
import tty
from typing import List

import numpy as np
from pynput import keyboard
from tqdm import tqdm

from voyage_touch.sensor import SensorType, TouchSensor, TouchSensorReader
from voyage_touch.assc.data import MarkovianDatapoint, store_markovian_data

NO_OF_FSRS = 3

current_values = [0]*NO_OF_FSRS
recorded_data = []

# Example for a manual data collection process.
# This example is for Markovian predictions and does not use time series measurement data

class EscapeException(Exception): pass

def on_press(key):
    if key == keyboard.Key.esc:
        raise EscapeException()
    if hasattr(key, 'char') and key.char in '123456789':
        id = int(key.char) - 1
        if id >= 0 and id < NO_OF_FSRS:
            current_values[id] = 1

def on_release(key):
    if hasattr(key, 'char') and key.char in '123456789':
        id = int(key.char) - 1
        if id >= 0 and id < NO_OF_FSRS:
            current_values[id] = 0

def disable_echo():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    return old_settings

def enable_echo(old_settings):
    fd = sys.stdin.fileno()
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def record_sensor_values(
        reader: TouchSensorReader,
        progress_bars: List[tqdm],
        stop_event: Event,
    ):    
    while not stop_event.is_set():
        readings = np.zeros(NO_OF_FSRS)

        for i in range(NO_OF_FSRS):
            reading = reader.read(SensorType.FSR, i)

            readings[i] = reading.value


            display_value = reading.value
            display_value *= 1000
            progress_bars[i].n = display_value
            progress_bars[i].refresh()
            
        datapoint = MarkovianDatapoint(readings=readings, labels=np.asarray(current_values))
        recorded_data.append(datapoint)

        time.sleep(0.1)
        # print(current_values)

if __name__ == '__main__':
    # old_settings = disable_echo() 

    sensor = TouchSensor('/dev/ttyACM0')
    reader = TouchSensorReader(sensor)

    # initialise reader
    thread = asyncio.run(reader.start())
    time.sleep(2)

    # set up progress bars 
    progress_bars = []
    for i in range(NO_OF_FSRS):
        progress_bars.append(tqdm(total=1000, desc=f'FSR {i+1}', ncols=100, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'))

    # start sensor value recorder thread
    stop_event = Event()
    sensor_thread = Thread(target=lambda: record_sensor_values(reader, progress_bars, stop_event))
    sensor_thread.start()

    # thread 2
    # Run until exit
    with keyboard.Listener(
        on_press=on_press,
        on_release=on_release,    
    ) as listener:
        while True:
            try:
                listener.join(0.01)
            except EscapeException as e:
                print('Terminating...')
                # enable_echo(old_settings)

                reader.stop()
                thread.join()
                stop_event.set()
                sensor_thread.join()

                store_markovian_data("data", recorded_data)

                exit()
