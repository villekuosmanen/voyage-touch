import time 

import serial 
from tqdm import tqdm

NO_OF_SENSORS = 3

def write_read(x): 
    arduino.read(bytes(x, 'utf-8')) 
    time.sleep(0.05) 
    data = arduino.readline() 
    return data

arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1) 
print("initialising serial connection...")
time.sleep(0.5)  # Wait for the serial connection to initialize
# throw away the first line:
arduino.readline()
time.sleep(0.5)

progress_bars = []
for i in range(NO_OF_SENSORS):
    progress_bars.append(tqdm(total=1000, desc=f'FSR {i+1}', ncols=100, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'))
for i in range(NO_OF_SENSORS):
    progress_bars.append(tqdm(total=100, desc=f'PZ {i+1}', ncols=100, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}'))

success = False
while i in range(10):
    line = arduino.readline()
    try:
        line = line.decode('utf-8').strip()
        tokens = line.split(',')
        if len(tokens) != 3:
            continue
        
        # initialised successfully
        success = True
        break
    except:
        continue

if not success:
    print(f"failed to initialise serial connection")
    exit()

while True:
    if arduino.in_waiting > 0:
        line = arduino.readline().decode('utf-8').strip()
        tokens = line.split(',')
        if len(tokens) != 3:
            print(f"invalid format received via serial: {line}\n")
            continue
        try:
            if tokens[0] == "FSR":
                sensor_id = int(tokens[1])

                # Convert FSR value to an integer
                fsr_value = int(tokens[2])
                # Clamp the value between 0 and 1000
                fsr_value = max(0, min(1000, fsr_value))
                # Update the progress bar
                progress_bars[sensor_id].n = fsr_value
                progress_bars[sensor_id].refresh()
            elif tokens[0] == "PZ":
                sensor_id = int(tokens[1])

                # Convert FSR value to an integer
                fsr_value = int(tokens[2])
                # Clamp the value between 0 and 1000
                fsr_value = max(0, min(100, fsr_value))
                # Update the progress bar
                progress_bars[NO_OF_SENSORS + sensor_id].n = fsr_value
                progress_bars[NO_OF_SENSORS + sensor_id].refresh()
            else:
                print(f"expected sensor type to be FSR, got {tokens[0]}\n")
                continue

        except ValueError:
            pass  # Ignore invalid values
