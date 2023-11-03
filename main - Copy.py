
import requests
import smtplib
from tkinter import *
from tkinter import messagebox

MY_EMAIL = ("YOUR MAIL")
PASSWORD = "YOUR APP PASSWORD"
TO_ADDRS = "RECIEVER'S MAIL"

OWM_Endpoint = "https://api.openweathermap.org/data/3.0/onecall"
API_KEY = "YOUR API KEY"

PARAMS = {
    "lat":"YOUR LATITUDE",
    "lon":"YOUR LONGITUDE",
    "appid": API_KEY,
    "exclude": "current,minutely",
}

def weather():
    response = requests.get(OWM_Endpoint, params=PARAMS)
    response.raise_for_status()
    data = response.json()
    weather_slice = data["hourly"][:12]
    weather_summary = data["daily"][0]["summary"]

    will_rain = False

    for hour_data in weather_slice:
        condition_code = hour_data["weather"][0]["id"]
        if int(condition_code) < 700:
            will_rain = True

    if will_rain:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login("YOUR EMAIL", password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=TO_ADDRS,
                                msg=f"Subject:Rain Alert\n\nThere'll be rain today please carry an Umbrella.\nThe weather "
                                    f"summary for today is: {weather_summary}")
            messagebox.showinfo(title="Report Delivered", message=f"Report sent to {TO_ADDRS}")
    else:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login("YOUR EMAIL", password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=TO_ADDRS,
                                msg=f"Subject:No Rain Today\n\nThere'll be no rain today.\nThe weather summary for today "
                                    f"is: {weather_summary}")
            messagebox.showinfo(title="Report Delivered", message=f"Report sent to {TO_ADDRS}")

window = Tk()
window.title("Rain Alert")
window.config(padx=50, pady=50, bg="#FF8080")

# IMAGE CANVAS
canvas = Canvas(height=200, width=200, bg="#FF8080", highlightthickness=0)
logo_img = PhotoImage(file="logo2.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# LABELS
weather_label = Label(text="Weather Report Generated!", bg="#FF8080")
weather_label.grid(row=1, column=1)

# BUTTONS
send_button = Button(text="Send Report", width=13, command=weather, bg="#EFB495")
send_button.grid(row=2, column=1)

window.mainloop()