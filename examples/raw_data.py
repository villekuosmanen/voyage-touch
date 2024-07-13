import asyncio
from queue import Empty, Queue
import time

from tqdm import tqdm

from voyage_touch.sensor import SensorType, TouchSensor, TouchSensorReader

NO_OF_SENSORS = 3

# Example for reading raw data from a queue using the TouchSensorReader class.

if __name__ == '__main__':
    sensor = TouchSensor('/dev/ttyACM0')
    reader = TouchSensorReader(sensor)

    # initialise reader
    q = Queue()
    reader.register_listener(0, q)
    thread = asyncio.run(reader.start())

    time.sleep(1)

    # test reading a few values:
    val1 = reader.read(SensorType.FSR, 0)
    print(f"FRS 0 has value {val1}")

    val2 = reader.read(SensorType.PIEZO, 2)
    print(f"Piezo 2 has value {val2}")

    # set up progress bars 
    progress_bars = []
    for i in range(NO_OF_SENSORS):
        progress_bars.append(tqdm(total=1000, desc=f'FSR {i+1}', ncols=100, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'))
    for i in range(NO_OF_SENSORS):
        progress_bars.append(tqdm(total=160, desc=f'PZ {i+1}', ncols=100, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'))

    # do something
    while True:
        try:
            msg = q.get()

            sensor_id = msg.sensor_id
            if msg.sensor_type is SensorType.PIEZO:
                sensor_id += NO_OF_SENSORS

            value = msg.value
            if msg.sensor_type is SensorType.PIEZO:
                value *= 160
            else:
                value *= 1000

            progress_bars[sensor_id].n = value
            progress_bars[sensor_id].refresh()

        except Empty:
            pass

    # graceful shutdown
    reader.stop()
    thread.join()
