import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import IMUProUnit
import time

print('imu example')

M5.begin()

# configure I2C on bottom connector of Atom Board:
#i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)

# configure I2C on PortA (red connector):
i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=100000)

# initialize IMU Pro unit:
imupro_0 = IMUProUnit(i2c0)

button = Pin(1, mode=Pin.IN)

acc_x = 0
acc_x_last = 0
button_pressed =  0
led = 0
activate = 0

# configure RGB strip connected to pin 2 with 10 LEDs enabled:
rgb_strip = RGB(io=5, n=30, type="SK6812")
rgb_strip.fill_color(0x000000)

while True:
  M5.update()
  imu_data = imupro_0.get_accelerometer()
  acc_x = imu_data[0] #Xacceleration value
  acc_y = imu_data[1]#yacceleration value
  acc_z = imu_data[2]#zacceleration value
  if not button.value():
      button_pressed = 1
  elif button.value():
      button_pressed = 0
      
  if button_pressed == 1 and led < 29:
    led += 1
    rgb_strip.set_color(led,0xff0000)
  elif led > 0 and button_pressed == 0:
    
    rgb_strip.set_color(led, 0x000000)  # 关闭对应的LED
    led  -= 1
    #rgb_strip.write()
    
  if led == 29:
    activate = 1
  else:
    activate = 0

      

      
      
  print(acc_x,',', acc_y,',',activate)
      
    
  
  
  

  time.sleep_ms(50)
