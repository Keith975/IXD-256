# Implements a BLE HID mouse

import M5
from M5 import *
from hardware import *
from unit import IMUProUnit
import time
from unit import AngleUnit
import m5utils

#from machine import Pin
from hid_services import Mouse
from hid_ble_mouse import *



M5.begin()

# IMU Pro unit 
#i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=100000)  # AtomS3
#i2c0 = I2C(0, scl=Pin(21), sda=Pin(25), freq=100000)  # Atom Matrix P.A
i2c0 = I2C(0, scl=Pin(32), sda=Pin(26), freq=100000)  # connector next to USB
imupro_0 = IMUProUnit(i2c0)

#button = Pin(8, mode=Pin.IN)  # AtomS3
button = Pin(33, mode=Pin.IN)  # Atom Matrix
button_pressed = False

d = MouseDevice()



#motor：
motor = Pin(22, Pin.OUT)
motor.value(0)
motor_state = False
last_motortime = 0



if d.mouse.get_state() is Mouse.DEVICE_IDLE:
    d.mouse.start_advertising()

while True:
    M5.update()
    current_time = time.ticks_ms()

    
    imu_data = imupro_0.get_accelerometer()
    acc_x = imu_data[0]  
    acc_y = imu_data[1]  
    acc_z = imu_data[2]  

    # remap to 0 - 255 range:
    #acc_x = int(m5utils.remap(acc_x, -1, 1, 0, 255))  
    #acc_y = int(m5utils.remap(acc_y, -1, 1, 0, 255))
    
    acc_x = int(m5utils.remap(acc_x, -1, 1, 20, -20))
    acc_y = int(m5utils.remap(acc_y, -1, 1, -20, 20))
    
    
    if d.mouse.get_state() is Mouse.DEVICE_CONNECTED:
        d.mouse.set_axes(int(acc_x), int(acc_y))
        d.mouse.notify_hid_report()
        time.sleep_ms(10) 
    
    if not button_pressed:
        if not button.value():
            button_pressed = True
                
            if d.mouse.get_state() is Mouse.DEVICE_CONNECTED:
                # bluetooth left mouse button press:
                d.mouse.set_buttons(1)
                d.mouse.notify_hid_report()
            
    if button_pressed:
        if button.value():
            button_pressed = False
            print('button released..')
            
            
            if d.mouse.get_state() is Mouse.DEVICE_CONNECTED:
                # bluetooth left mouse button release:
                d.mouse.set_buttons()
                d.mouse.notify_hid_report()
                
    if button_pressed:
        if time.ticks_diff(current_time, last_motortime) >= 50:  # 0.3秒间隔
            motor_state = not motor_state
            motor.value(1 if motor_state else 0)
            last_motortime = current_time
    else:
        motor.value(0)
        motor_state = False




