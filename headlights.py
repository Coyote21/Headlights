import os
import sys
import time

# Add path to Sphero SDK for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from sphero_sdk import RvrStreamingServices
from sphero_sdk import SpheroRvrObserver
from sphero_sdk import RvrLedGroups

rvr = SpheroRvrObserver()

SCALAR = 0.002125           # Scalar to map sensor data to RGB values
ambient_light_data = 0.0
headlight_brightness = 0

# Ambient Light Sensor Data Handler
def scan(ambient_light_data):
    print('Ambient light sensor data response: ', ambient_light_data)
    
# Calculate Headlight Brightness
def think():
    headlight_brightness = 255 - int(ambient_light_data*SCALAR)
    print('Headlight brightness:', headlight_brightness)

# Set the Headlight Brightness
def act():
    rgb_tuple = [headlight_brightness, 
                 headlight_brightness, 
                 headlight_brightness]
    
    # Set Left Headlight
    rvr.set_all_leds(
        led_group=RvrLedGroups.headlight_left.value,
        led_brightness_values=rgb_tuple
    )
    # Set Right Headlight
    rvr.set_all_leds(
        led_group=RvrLedGroups.headlight_right.value,
        led_brightness_values=rgb_tuple
    )

def main():

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        # Assign ambient light sensor to handler
        rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.ambient_light,
            handler=scan
        )

        # Start reading sensor data @ 300ms intervals
        rvr.sensor_control.start(interval=300)

        while True:
            # Delay to allow RVR to stream ambient light sensor data
            time.sleep(0.3)
            think()
            act()

    # End loop/program with Ctrl+c, Ctrl+z or Delete
    except KeyboardInterrupt:       
        print('\n Program Terminated.')

    finally:
        # Un-assign Sensors
        rvr.sensor_control.clear()

        # Delay to allow RVR issue command before closing
        time.sleep(0.5)
        
        rvr.close()


if __name__ == '__main__':
    main()