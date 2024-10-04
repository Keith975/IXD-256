## Assignment1  
Assignment 1 description  
[assignment1](Project1.py) 
Code snipped for changing states in the program: 

```Python
import os, sys, io
import M5
from M5 import *
from hardware import *
import time

M5.begin()

pin6 = Pin(6, mode=Pin.OUT)  
pin8 = Pin(8, mode=Pin.OUT)  
pin5 = Pin(5, mode=Pin.IN, pull=Pin.PULL_UP)  
pin7 = Pin(7, mode=Pin.IN, pull=Pin.PULL_UP)  

rgb2 = RGB(io=2, n=15, type="SK6812")
rgb2.fill((0, 0, 0))

program_state = 'inactive'

def get_rgb_color(r, g, b):
    rgb_color = (r << 16) | (g << 8) | b
    return rgb_color

def rgb_blink_red():
    rgb2.fill_color(get_rgb_color(255, 0, 0))
    time.sleep_ms(500)
    rgb2.fill_color(get_rgb_color(0, 0, 0))
    time.sleep_ms(500)

def rgb_cycle_colors():
    while not pin5.value() and not pin7.value():
        for i in range(256):
            if pin5.value() or pin7.value():
                return
            rgb2.fill_color(get_rgb_color(0, i, 255 - i))
            time.sleep_ms(10)
        for i in range(256):
            if pin5.value() or pin7.value():
                return
            rgb2.fill_color(get_rgb_color(i, 255, 0))
            time.sleep_ms(10)
        for i in range(256):
            if pin5.value() or pin7.value():
                return
            rgb2.fill_color(get_rgb_color(255 - i, 255 - i, i))
            time.sleep_ms(10)

while True:
    M5.update()

    if not pin5.value() and program_state == 'inactive':
        program_state = 'active'
        print('active')
       

    if program_state == 'active':
        input_pin5_active = not pin5.value()
        input_pin7_active = not pin7.value()

        if input_pin5_active and input_pin7_active:
            pin6.off()
            pin8.off()
            rgb_cycle_colors()
        elif input_pin5_active or input_pin7_active:
            pin6.on()
            pin8.off()
            rgb_blink_red() 
            pin6.off()
            pin8.on()
            rgb_blink_red()
        else:
            pin6.on()   
            pin8.off()
            rgb2.fill((0, 0, 0))
    else:
        pin6.off()
        pin8.off()
        rgb2.fill((0, 0, 0))

    time.sleep_ms(10)
```
Image link example:  
![assignment1](image_35.png)
