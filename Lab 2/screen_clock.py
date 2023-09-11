import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
fontA = ImageFont.truetype("fonts/DejaVuSans.ttf", 30)
fontB = ImageFont.truetype("fonts/SuperMario256.ttf", 30)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Images
white_background_image = Image.open("images/white.jpg")
white_background_image = white_background_image.resize((width,height))
evening_image = Image.open("images/evening.jpg")
evening_image = evening_image.resize((width, height))
afternoon_image = Image.open("images/afternoon.jpg")
afternoon_image = afternoon_image.resize((width, height)) 

# Gifs
dog_gif = Image.open("gifs/dog.gif")
dog_gif_iter = ImageSequence.Iterator(dog_gif)
bones_gif = Image.open("gifs/bones.gif")
bones_gif_iter = ImageSequence.Iterator(bones_gif)

# Inital frames
dog_frame = dog_gif_iter
bone_frame = bones_gif_iter

pre_sec = cur_sec = 0

while True:
    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    # Time display
    # cur_time = strftime("%m/%d/%Y %H:%M:%S")
    cur_date = strftime("%m/%d/%Y")
    cur_time = strftime("%H:%M:%S") 
    cur_weekday = strftime("%A")  
    cur_sec = int(cur_time.split(':')[-1].split('.')[0])
    
    # button A is pressed, see screen_test.py
    if not buttonA.value:
        display_image = evening_image.copy()
        x, y = 40, 50  # Adjust the coordinates as needed.
        draw_on_image = ImageDraw.Draw(display_image)
        draw_on_image.text((x, y), cur_date, font=fontA, fill="#FFFFFF")
        # Display the modified images with the time on the screen
        disp.image(display_image, rotation)
        continue
    elif not buttonB.value:
        display_image = afternoon_image.copy()
        x, y = 65, 50  # Adjust the coordinates as needed.
        draw_on_image = ImageDraw.Draw(display_image)
        draw_on_image.text((x, y), cur_weekday, font=fontA, fill="#FFFFFF")
        # Display the modified images with the time on the screen
        disp.image(display_image, rotation)
        continue
        
    display_image = white_background_image.copy()
    
    # Bone frame:
    if cur_sec != pre_sec:
        try:
            bone_frame = next(bones_gif_iter)
            bone_frame = bone_frame.convert("RGBA").resize((150, 100))
        except StopIteration:
            bones_gif_iter = ImageSequence.Iterator(bones_gif)
            bone_frame = next(bones_gif_iter)
            bone_frame = bone_frame.convert("RGBA").resize((150, 100)) 
    
    display_image.paste(bone_frame, (120, 40), bone_frame)
    
    # Dog frame:
    try:
        dog_frame = next(dog_gif_iter)
        dog_frame = dog_frame.convert("RGBA").resize((150, 100))
    except StopIteration:
        dog_gif_iter = ImageSequence.Iterator(dog_gif)
        dog_frame = next(dog_gif_iter)
        dog_frame = dog_frame.convert("RGBA").resize((150, 100)) 
        
    display_image.paste(dog_frame, (-15, 30), dog_frame)
    
    
    # display_image.text((0, 0), cur_time, font=fontB, fill="#f41f1f")
    draw_on_image = ImageDraw.Draw(display_image)
    # draw_on_image.text((current_time_x, current_time_y), current_time, font=font2, fill="#f41f1f")  # Default color
    draw_on_image.text((55, 10), cur_time, font=fontB, fill="#f41f1f")  # Default color
    
    
    # Display image.
    disp.image(display_image, rotation)
    pre_sec = cur_sec
    
    time.sleep(0.1)
