import threading
import time
from customtkinter import *
from PIL import Image, ImageTk
from functools import partial
import python_weather
import asyncio
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

config_path = resource_path('src/data_germany')
map_path = resource_path('src/map_ger.png')
icon_path = resource_path('src/logo.png')
print(config_path, map_path, icon_path)

curbut = None

client = python_weather.Client(unit=python_weather.METRIC)

set_appearance_mode('Dark')
set_default_color_theme('green')

app = CTk()
app.title('Weather Map')
app.resizable(False, False)
app.geometry('700x600')

try:
    icon = ImageTk.PhotoImage(file=icon_path)
    app.iconphoto(True, icon)
except Exception:
    pass

locvar  = StringVar()
tempvar = StringVar()
fcvar   = StringVar()

map_img = CTkImage(dark_image=Image.open(map_path), size=(450, 550))

#menu = CTkFrame(master=app, width=200, height=600, corner_radius=0, fg_color='#212121')
map_frame = CTkFrame(master=app, width=700, height=600, corner_radius=0)
map = CTkLabel(master=map_frame, width=300, height=300, image=map_img)
temperature = CTkLabel(master=map_frame, textvariable=tempvar, font=('system', 22))
location = CTkLabel(master=map_frame, textvariable=locvar, font=('system', 22))
forecast = CTkLabel(master=map_frame, textvariable=fcvar, font=('system', 22))

#menu.place(x=0,
#           y=0)
map_frame.place(x=0,
                y=0)
location.place(x=5,
               y=5)
temperature.place(x=5,
                  y=30)
forecast.place(x=5,
               y=60)
map.place(x=120,
          y=20)

with open(config_path, 'r') as file:
   data = file.readlines()


async def process_weather(dat, button):
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        # fetch a weather forecast from a city
        weather = await client.get(dat)

        tempvar.set(f'Temperature: {weather.temperature}°C')
        locvar.set(f'Location: {dat}')
        fcvar.set(f'Forecast: {weather.description}')

        button.configure(fg_color='green')
        while True:
            if dat == curbut:
                time.sleep(0.1)
            else:
                button.configure(fg_color='gray')
                break

def process(dat, button):
    global curbut
    print(dat)
    curbut = dat
    thrd = threading.Thread(target=partial(asyncio.run, process_weather(dat, button)))
    thrd.start()

for city in enumerate(data):
    cd = city[1].split('|')
    button = CTkButton(master=map_frame, text=cd[0], anchor='w', bg_color='transparent', fg_color='gray', corner_radius=0, width=30, height=20)
    button.configure(command=partial(process, cd[0], button))
    button.place(x=cd[1],
                 y=cd[2])

app.mainloop()