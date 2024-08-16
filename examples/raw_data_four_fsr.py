import asyncio
from queue import Empty, Queue
import time

from tqdm import tqdm

from voyage_touch.sensor import SensorType, TouchSensor, TouchSensorReader

NO_OF_SENSORS = 4

# Example for reading raw data from a queue using the TouchSensorReader class.

if __name__ == '__main__':
    sensor = TouchSensor('/dev/ttyACM0', num_fsrs=NO_OF_SENSORS, num_pzs=0)
    reader = TouchSensorReader(sensor)

    # initialise reader
    q = Queue()
    reader.register_listener(0, q)
    thread = asyncio.run(reader.start())
    time.sleep(1)

    # test reading a few values:
    val1 = reader.read(SensorType.FSR, 0)
    print(f"FRS 0 has value {val1}")
    val1 = reader.read(SensorType.FSR, 3)
    print(f"FRS 3 has value {val1}")

    # set up progress bars 
    progress_bars = []
    for i in range(NO_OF_SENSORS):
        progress_bars.append(tqdm(total=1000, desc=f'FSR {i+1}', ncols=100, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'))

    # do something
    while True:
        try:
            msg = q.get()

            sensor_id = msg.sensor_id
            value = msg.value
            value *= 1000

            progress_bars[sensor_id].n = value
            progress_bars[sensor_id].refresh()

        except Empty:
            pass

    # graceful shutdown
    reader.stop()
    thread.join()
