## Final Project 

Link to the code:  
[assignment3 Mouse code](Mouse.py)  
[assignment3 keyboard code](keyboard.py)     

##  Introduction


**Description**  
This project leverages a motion sensor to translate real human interactions into the game, enhancing the realism of the experience. By using the motion sensor, I can detect users' movements and synchronize them with the game character’s actions. Additionally, I aim to map interactions like reloading, shooting, and more. To heighten the immersive experience, I plan to add vibration feedback, making the gameplay even more lifelike.  

**Inspiration**  
The core of this project is to use a motion sensor to simulate the experience of flying a fighter jet. A HUD will display key information such as altitude, direction, and other essential data. This setup aims to create a realistic and immersive flight experience.  

![inspiration images](Inspiration.png)  

**Sketches：**  
![sketches](Sketch.png)  

## Implementation

**Material List:**  
Basic Material:  
MDF enclosure, MDF Reload component, Spring  
Basic Hardware:  
2 Atom Matrix/Atom S3, Extention module, 3-axis Motion Sensor, limit switch unit, reflective sensor  
Input：  
3-axis Motion Sensor, limit switch unit, reflective sensor  
Output:  
Bluetooth Mouse output, Bluetooth Keyboard output, viberation motor  

**Software:**  
Micro Phton  
Game: Project Strinova

##  Diagram  

**Prototype Line Sketch:**  

![sketches](LineSketch.png)  

**Prototype Teardown:**  

![sketches](Teardown.png)  

**Schematic Diagram:**  

![sketches](SchematicDiagram.png)  



##  Prototyping Process  

![sketches](PrototypeProcess.png)  

**Main code in Mouse Interaction:** 

```Python
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
    
    acc_x = int(m5utils.remap(acc_x, -1, 1, 10, -10))
    acc_y = int(m5utils.remap(acc_y, -1, 1, 10, -10))
    
    
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
```
**Code for viberation cycle** 

```Python       
if button_pressed:
    if time.ticks_diff(current_time, last_motortime) >= 50: 
        motor_state = not motor_state
        motor.value(1 if motor_state else 0)
        last_motortime = current_time
else:
    motor.value(0)
    motor_state = False
```

**Code for keyboard interaction** 

```Python       
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
```

**Images of Prototype:**
![Detail_Images](Images.png)

**link to demo Video:**  
https://drive.google.com/file/d/19_AIDiYw_o4snVoypcmCBq1djsGoEjB8/view?usp=share_link

