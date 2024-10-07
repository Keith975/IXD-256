## Assignment1  
Link to the code: [assignment1](Project1.py)     
Description  
A book on a shelf with conductive material on the back. When the book is pushed back, the conductive part will make contact with a conductive backplate on the shelf, activating a hidden mechanism, like turning on a light.

Inspiration  
In many movies, bookshelves are filled with hidden secrets, like escape room puzzles or concealed toggles. Inspired by this, I want to create an installation that recreates this mysterious experience, turning an ordinary bookshelf into an interactive puzzle full of surprises and hidden mechanisms.  

![inspiration images](inspiration_images.png)

Sketches：  
![sketches](Sketch.png)

Material List:  
Basic Material:  
MDF, Books  
Basic Hardware:  
ESP 32, Bread board, conductive tape, wires  
Input：  
Books(with conductive tape)  
OutPut:  
LED lights 

Flowchart of high level logic:   
![digram](Flowchart.png)




Code snipped for definitions in the program: 

```Python
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
```

Main code in the program: 
```Python
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
Images of Prototype;
![Detail_Images](Detail_Images.png)

link to demo Video:  
https://drive.google.com/file/d/1uqaur7JPG99CNawr7ctLzb1RcDJ87BxB/view?usp=share_link

