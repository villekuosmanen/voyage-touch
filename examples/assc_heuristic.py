import asyncio
import time

from voyage_touch.sensor import TouchSensor
from voyage_touch.assc import ASSC
from voyage_touch.assc.policies import FSRHeuristicPolicy

NO_OF_SENSORS = 3

# Example for using an ASSC with a heuristic model to predict touch or no touch events for every point in the sensor.

if __name__ == '__main__':
    sensor = TouchSensor('/dev/ttyACM0', num_fsrs=NO_OF_SENSORS, num_pzs=0)
    model = FSRHeuristicPolicy(NO_OF_SENSORS)
    assc = ASSC(model, sensor)

    # start ASSC reader thread
    thread = asyncio.run(assc.start())
    time.sleep(1)

    while True:
        res = assc.predict()
        print(res)
        time.sleep(0.2)
