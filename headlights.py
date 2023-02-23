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
headlight_brightness = 0

# Ambient Light Sensor Data Handler
def ambient_light_handler(ambient_light_data):
    print('Ambient light sensor data response: ', ambient_light_data)
    
    # Calculate Headlight Brightness
    headlight_brightness = 255 - int(ambient_light_data*SCALAR)
    print('Headlight brightness:', headlight_brightness)
    
    # Set the Headlight Brightness
    rvr.set_all_leds(
        led_group=RvrLedGroups.headlight_left.value,
        led_brightness_values=[
            headlight_brightness, 
            headlight_brightness, 
            headlight_brightness
            ]
    )
    rvr.set_all_leds(
        led_group=RvrLedGroups.headlight_right.value,
        led_brightness_values=[
            headlight_brightness, 
            headlight_brightness, 
            headlight_brightness
            ]
    )

def main():

    try:
        rvr.wake()

        # Give RVR time to wake up
        time.sleep(2)

        # Assign Ambient Light Sensor to Handler
        rvr.sensor_control.add_sensor_data_handler(
            service=RvrStreamingServices.ambient_light,
            handler=ambient_light_handler
        )

        # Start reading Sensor Data @ 250ms intervals
        rvr.sensor_control.start(interval=250)

        while True:
            # Delay to allow RVR to stream sensor data
            time.sleep(1)

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