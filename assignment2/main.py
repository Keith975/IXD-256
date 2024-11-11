import js as p5
from js import document

img1 = p5.loadImage('rightcontrol.png')
img2 = p5.loadImage('leftcontrol.png')
img3 = p5.loadImage('rightcontrol2.png')
img4 = p5.loadImage('leftcontrol2.png')
largecircle = p5.loadImage('largecircle.png')
smallcircle = p5.loadImage('smallcircle.png')
centerlinevertical = p5.loadImage('centervertical.png')
centerlinehorizontal  = p5.loadImage('centerhorizontal.png')
redborder = p5.loadImage('activated.png')

imu_data = [0, 0, 0]

acc_x = 0
acc_x_last = 0
acc_y = 0
acc_y_last = 0

controls_speed_y = -2
controls_y = 0
controls_x = 0

controls_speed_x = 0

rotate_speed = 2
rotate_angle = 0

circle_x = 0
circle_y = 0

activated = 0

activated_prev = 0   # 新增
activated_time = 0   # 新增

def setup():
  p5.createCanvas(300, 300)
  # draw images from center:
  p5.imageMode(p5.CENTER)
  
def draw():
  global acc_x, acc_x_last
  global acc_y, acc_y_last
  global controls_speed_x, controls_speed_y
  global controls_y
  global rotate_speed
  global rotate_angle
  global circle_x, circle_y, controls_x, activated
  global activated_prev, activated_time


  p5.background(0)

  data = document.getElementById("data").innerText
  
  # assign content of "data" div on index.html page to variable:
  data_string = document.getElementById("data").innerText

  # split data_string by comma, making a list:
  data_list = data_string.split(',')

  p5.fill(255)
  # p5.text(data_list[0], 10, 20)
  # p5.text(data_list[1], 10, 32)

  # p5.text('circle_x = ' + str(circle_x), 10, 44)
  # p5.text('circle_y = ' + str(circle_y), 10, 56)

  # p5.text('controls_speed_y = ' + str(controls_speed_y), 10, 68)

  
  controls_speed_x = float(data_list[0])
  controls_speed_x = p5.map(controls_speed_x, -1.0, 1.0, -3.0, 3.0)

  controls_speed_y = float(data_list[1])
  controls_speed_y = p5.map(controls_speed_y, -1.0, 1.0, -3.0, 3.0)

  rotate_speed = float(data_list[0])
  rotate_speed = p5.map(rotate_speed, -1.0, 1.0, -0.05, 0.05)

  activated = float(data_list[2])
  #controls_x += controls_speed_x


  if activated_prev == 0 and activated == 1:
    activated_time = p5.millis()  # 记录激活的时间

  activated_prev = activated  # 更新前一帧的激活状态
  



  
  
  
  update_controls()

  #draw small circle
  p5.push()
  #p5.translate(controls_x, controls_y)
  p5.translate(p5.width/2, p5.height/2)
  p5.translate(circle_x, circle_y)
  p5.image(smallcircle, 0, 0,smallcircle.width*0.5, smallcircle.height*0.5)
  p5.pop()

  p5.translate(p5.width/2, p5.height/2)

  #Draw rightline
  p5.push()
  p5.translate(-120, controls_y)
  p5.image(img1, 0, 0,img1.width*0.5, img1.height*0.5)
  p5.pop()

  #Draw left line2
  p5.push()
  p5.translate(-60, controls_y*0.25)
  p5.image(img3, 0, 0,img3.width*0.3, img3.height*0.5)
  p5.pop()
  
  #Draw rightline1
  p5.push()
  p5.translate(60, controls_y*0.25)
  p5.image(img4, 0, 0,img4.width*0.3, img4.height*0.5)
  p5.pop()
  
  #draw rightline 2
  p5.push()
  p5.translate(120, controls_y)
  p5.image(img2, 0, 0,img2.width*0.5, img2.height*0.5)
  p5.pop()
  
  p5.push()
  p5.rotate(rotate_angle)

  #draw centerline vertical
  p5.push()
  p5.translate(0, 0)
  p5.image(centerlinevertical, 0, 0,centerlinevertical.width*0.5, centerlinevertical.height*0.5)
  p5.pop()

   #draw centerline horizontal
  p5.push()
  p5.translate(0, 0)
  p5.image(centerlinehorizontal, 0, 0, centerlinehorizontal.width*0.5, centerlinehorizontal.height*0.5)
  p5.pop()
  p5.pop()

  

  #draw big circle
  p5.push()
  p5.translate(0, 0)
  p5.image(largecircle, 0, 0,largecircle.width*0.5, largecircle.height*0.5)
  p5.pop()

  current_time = p5.millis() - activated_time

  # p5.push()
  # p5.translate(0, 0)
  # p5.image(redborder, 0, 0, redborder.width*0.33, redborder.height*0.33)
  # p5.pop()

  if current_time < 1000:
      if int(current_time / 200) % 2 == 0:
        p5.push()
        p5.image(redborder, 0, 0, redborder.width*0.33, redborder.height*0.33)
        p5.pop()

  

def update_controls():
  global controls_speed_y
  global controls_y
  global rotate_speed
  global rotate_angle, controls_x
  global circle_x, circle_y


  if (p5.abs(controls_speed_x) < 0.5):
    if (circle_x < 0):
      circle_x += 1
    elif (circle_x > 0):
      circle_x -= 1

  if (p5.abs(controls_speed_y) < 0.5):
    if (circle_y < 0):
      circle_y += 1
    elif (circle_y > 0):
      circle_y -= 1

  else:

    if (controls_speed_y > 0) and (controls_y < 150):
        controls_y += controls_speed_y
        circle_y += controls_speed_y
        
    if (controls_speed_x > 0) and (controls_x < 150):
        controls_x += controls_speed_x
        circle_x += controls_speed_x

    if (controls_speed_y < 0) and (controls_y > -150):
      controls_y += controls_speed_y
      circle_y += controls_speed_y
      
    if (controls_speed_x < 0) and (controls_x > -150):
      controls_x += controls_speed_x
      circle_x += controls_speed_x

  if (rotate_speed > 0):
    if (rotate_angle < 1):
      rotate_angle += rotate_speed
  elif (rotate_speed < 0) and (rotate_angle > -1):
    rotate_angle += rotate_speed

    


  #if (controls_y > p5.height):
  #  controls_y = 0