# Implements a BLE HID keyboard


import M5
from M5 import *
from hardware import *
from machine import Pin
import time
from hid_services import Keyboard
from hid_ble_keyboard import *
import os, sys, io

from unit import IMUProUnit
import time
from unit import AngleUnit
import m5utils
from machine import Pin, ADC

# decidmal:    0 - 9, 10, 11, 12, 13, 14, 15
# hexadecimal: 0 - 9,  A,  B,  C,  D,  E,  F

'''
# key codes:
0x04 = Keyboard a and A
0x05 = Keyboard b and B
0x06 = Keyboard c and C
...
0x0A = Keyboard e and E
0x0B = Keyboard f and F
...
0x1D = Keyboard z and Z
0x1E = Keyboard 1 and !
0x1F = Keyboard 2 and @
0x20 = Keyboard 3 and #
0x21 = Keyboard 4 and $
0x22 = Keyboard 5 and %
0x23 = Keyboard 6 and ^
0x24 = Keyboard 7 and &
0x25 = Keyboard 8 and *
0x26 = Keyboard 9 and (
0x27 = Keyboard 0 and )
0x28 = Keyboard Return (ENTER)
0x29 = Keyboard ESCAPE
0x2A = Keyboard Delete (Backspace)
0x2B = Keyboard Tab
0x2C = Keyboard Spacebar
0x2D = Keyboard - and _ (underscore)
0x2E = Keyboard = and +
0x2F = Keyboard [ and {
0x30 = Keyboard ] and }
0x31 = Keyboard \ and |
0x32 = Keyboard Non-US # and ~
0x33 = Keyboard ; and :
0x34 = Keyboard ' and "
0x35 = Keyboard Grave Accent and Tilde
0x36 = Keyboard, and <
0x37 = Keyboard . and >
0x38 = Keyboard / and ?
0x39 = Keyboard Caps Lock
0x3A = Keyboard F1
0x3B = Keyboard F2
0x3C = Keyboard F3
0x3D = Keyboard F4
0x3E = Keyboard F5
0x3F = Keyboard F6
0x40 = Keyboard F7
0x41 = Keyboard F8
0x42 = Keyboard F9
0x43 = Keyboard F10
0x44 = Keyboard F11
0x45 = Keyboard F12
0x46 = Keyboard PrintScreen
0x47 = Keyboard Scroll Lock
0x48 = Keyboard Pause
0x49 = Keyboard Insert
0x4A = Keyboard Home
0x4B = Keyboard PageUp
0x4C = Keyboard Delete Forward
0x4D = Keyboard End
0x4E = Keyboard PageDown
0x4F = Keyboard RightArrow
0x50 = Keyboard LeftArrow
0x51 = Keyboard DownArrow
0x52 = Keyboard UpArrow
0x53 = Keypad Num Lock and Clear
0x54 = Keypad /
0x55 = Keypad *
0x56 = Keypad -
0x57 = Keypad +
0x58 = Keypad ENTER
0x59 = Keypad 1 and End
0x5A = Keypad 2 and Down Arrow
0x5B = Keypad 3 and PageDn
0x5C = Keypad 4 and Left Arrow
0x5D = Keypad 5
0x5E = Keypad 6 and Right Arrow
0x5F = Keypad 7 and Home
0x60 = Keypad 8 and Up Arrow
0x61 = Keypad 9 and PageUp
0x62 = Keypad 0 and Insert
0x63 = Keypad . and Delete
'''

print('BLE Keyboard Example')
print('Use Windows settings to add Bluetooth device..')

# PIN DIFFERENCES:
# AtomS3     Atom Matrix
# 1          32
# 2          26
# 

# initialize IMU Pro unit:
#button1 = Pin(8, mode=Pin.IN)  # AtomS3
button1 = Pin(33, mode=Pin.IN)  # Atom Matrix
#button2 = Pin(39, mode=Pin.IN)  # AtomS3
button2 = Pin(21, mode=Pin.IN)  # Atom Matrix

#adc1 = ADC(Pin(1), atten=ADC.ATTN_11DB)  # AtomS3
adc1 = ADC(Pin(32), atten=ADC.ATTN_11DB)  # Atom Matrix

#pwm1 = PWM(Pin(6))  # AtomS3
pwm1 = PWM(Pin(19))  # Atom Matrix

#configure PWM frequency at   50Hz for servo:
pwm1.freq(50)
#configer duty cycle to stop the servo:
duty_cycle = 75
pwm1.duty(duty_cycle)

#change duty cycle to move servo slowly clockwise:
pwm1.duty(0)


move_key =  None
reload_key = None
lens_key = False
led = 0
activate = 0
distance = None

# examples of obtaining the character code:
a_code = 0x04 + ord('a') - ord('a') 
print('code for a:', hex(a_code))

r_code = 0x04 + ord('r') - ord('a') 
print('code for r:', hex(r_code))


M5.begin()
d = KeyboardDevice()

if d.keyboard.get_state() is Keyboard.DEVICE_IDLE:
    d.keyboard.start_advertising()

while True:
  M5.update()
    
  distance = adc1.read()
  distance  = int(m5utils.remap(distance, 250, 2600, 0, 100))
  
 
  if not reload_key:
    if not button2.value():
      reload_key = True
      print('button2 pressed..')
      if d.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
          # send key press:
          #d.keyboard.set_keys(0x04)  # 'a'
          char_code = 0x04 + ord('r') - ord('a')  # get code for 'r'
          d.keyboard.set_keys(char_code)
          d.keyboard.notify_hid_report()
          time.sleep_ms(2)

  if reload_key:
    if button2.value():
      reload_key = False
      print('button2 released..')
      if d.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
        # send key release:
        d.keyboard.set_keys()
        d.keyboard.notify_hid_report()
        time.sleep_ms(2)

 
  time.sleep_ms(100)  # temporary delay REMOVE later
  
  if lens_key == False:
    if distance < 10:
      lens_key = True
      print('button2 pressed..')
      if d.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
          # send key press:
          char_code = 0x05
          d.keyboard.set_keys(char_code)
          d.keyboard.notify_hid_report()
          time.sleep_ms(2)

  if lens_key == True:
    if not distance < 10:
      lens_key = False
      print('button2 released..')
      if d.keyboard.get_state() is Keyboard.DEVICE_CONNECTED:
        # send key release:
        d.keyboard.set_keys()
        d.keyboard.notify_hid_report()
        time.sleep_ms(2)
    

  



