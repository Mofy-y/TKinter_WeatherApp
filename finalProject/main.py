from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

root = Tk()
root.title("WEATHERAPP☁️byGeorge")
root.geometry("900x500+300+200")
root.resizable(False, False)


def get_weather():
    city = textfield.get()

    if not city:
        messagebox.showerror("Error", "Please enter a city")
        return

    try:
        geolocator = Nominatim(user_agent="MyGeocoder/1.0")
        location = geolocator.geocode(city, timeout=10)  # Increase the timeout to 10 seconds
        if location is None:
            messagebox.showerror("Error", "Location not found")
            return
    except GeocoderTimedOut as e:
        messagebox.showerror("Error", f"Geocoding error: {e}")
        return

    try:
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)
    except AttributeError:
        messagebox.showerror("Error", "Location data incomplete")
        return

    home = pytz.timezone(result)
    local_time = datetime.now(home)
    current_time = local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    name.config(text="CURRENT TIME")

    # weather
    api = "http://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=287f49ee6d240066dd63202f2da8bfe0"

    json_data = requests.get(api).json()

    # Print the JSON data to help identify the structure
    print(json_data)

    # Check if 'weather' key exists in the JSON response
    if 'weather' in json_data:
        # Check if 'description' key exists within the 'weather' object
        if len(json_data['weather']) > 0 and 'description' in json_data['weather'][0]:
            description = json_data['weather'][0]['description']
        else:
            description = "N/A"
    else:
        messagebox.showerror("Error", "Weather data not found")
        return

    # Continue with the rest of your code
    temp = int(json_data['main']['temp'] - 273.15)
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind = json_data['wind']['speed']

    t.config(text=(temp, "°"))
    c.config(text=("N/A", "|", "FEELS", "LIKE", temp, "°"))  # You can set condition to "N/A" in case it's missing

    w.config(text=wind)
    h.config(text=humidity)
    d.config(text=description)
    p.config(text=pressure)
image_icon = PhotoImage(file="logo2.png")
root.iconphoto(False, image_icon)


# search
search_image = PhotoImage(file="search.png")
myimage = Label(image=search_image)
myimage.place(x=20, y=20)

textfield = tk.Entry(root, justify="center", width=17, font=("poppins", 25, "bold"), bg="#404040", border=0, fg="white")
textfield.place(x=50, y=40)
textfield.focus()

search_icon = PhotoImage(file="search icon.png")
myimage_icon = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", command=get_weather)
myimage_icon.place(x=400, y=34)

# Logo
logo_image = PhotoImage(file="logo2.png")
logo = Label(image=logo_image)
logo.place(x=150, y=100)

# Bottom Box
Frame_box = PhotoImage(file="box.png")
Frame_image = Label(image=Frame_box)
Frame_image.pack(padx=5, pady=5, side=BOTTOM)

# time
name = Label(root, font=("arial", 15, "bold", "italic"))
name.place(x=30, y=100)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)


# Label
label1 = Label(root, text="WIND(KM/H)", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label1.place(x=115, y=400)

label2 = Label(root, text="HUMIDITY", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label2.place(x=250, y=400)

label3 = Label(root, text="DESCRIPTION", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label3.place(x=430, y=400)

label4 = Label(root, text="PRESSURE(hPa)", font=("Helvetica", 15, 'bold'), fg="white", bg="#1ab5ef")
label4.place(x=650, y=400)

t = Label(font=('poppins', 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)
c = Label(font=('arial', 15, "bold"))
c.place(x=400, y=250)

w = Label(text="......", font=("arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)
h = Label(text="......", font=("arial", 20, "bold"), bg="#1ab5ef")
h.place(x=260, y=430)
d = Label(text="......", font=("arial", 20, "bold"), bg="#1ab5ef")
d.place(x=445, y=430)
p = Label(text="......", font=("arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)


root.mainloop()
