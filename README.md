# Voyage Touch

**Open source tactile sensing library for robots.**

Voyage Touch is a Python library for interacting with tactile sensors built using force sensitive resistors, or piezoelectronic sensors. It provides methods for reading raw sensor data, as well as an interface for an **artificial somatosensory cortex** - a model for predicting touch events from raw data.

Voyage Touch is built and maintained by [Voyage Robotics](https://www.voyagerobotics.com/).

## ASSC model

An ASSC is a foundation model for tactile sensing, converting raw sensor data into features such as touch contact (1 or 0), magnitude of force, or the direction of the force vector. A pre-trained ASSC is designed to be used as an input to other machine learning policies, allowing an easy integration of tactile sensing without the need to retrain the policy.

Currently, only a heuristic ASSC model that supports force-sensing resistors is provided, but the goal is to provide pre-trained models for a common set of sensor configurations and hardware devices you could build at home. 

## Installation

### Firmware

1. Open the `arduino` package in the [Arduino IDE](https://www.arduino.cc/en/software).
2. Ensure your Arduino board is connected to your computer
3. Flash the firmware to your Arduino board using the Arduino IDE.

Your touch sensor should now be ready to use with the Voyage Touch library! 

### Library

```
pip install voyage-touch
```

The Voyage Touch API is still experimental and may change in the future.



## Supported sensor types

We're planning Voyage Touch to be compatable with various types of tactile sensors to allow developers to explore different, inventive ways to integrate tactile sensing to their robot.

- ✅ Force sensing resistors
- 🚧 Piezoelectric sensors (also known as contact microphones)
    - supports raw data but no support in the ASSC yet. Still working on the most effective way to make use of these.
- 👀 Magnetic sensors

✅: fully supported
🚧: working on support
👀: support planned for the future

## Hardware design

Voyage Touch sensors can be built using an Arduino board and some sensors. Reference circuit designs and lists of hardware components to buy will be published in due course.

## Supported robots

Voyage Touch Sensors will have dedicated support for particular robot grippers  in the form of 3D printed designs and pre-trained ASSC models, allowing the integration of tactile sensing out of the box.

Contact us via Issues for a robot arm or gripper you'd like to use Voyage Touch with!

## Example usage

[Example with raw data](examples/raw_data.py).

[Example with a heuristic ASSC](examples/assc_heuristic.py).
