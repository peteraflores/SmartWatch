# SmartWatch
This is my 2020 major project for CSH.

This a UI made in python TKinter that was intended to go onto a raspberry pi to be a smart watch.

## Features

### Watch Face
The watch face (the most important part) allows for the customization of time output. You can choose to have 24 hours time or 12
hour time, choose to display seconds, or choose to display the date. NTP must be installed to the system for times to be accurate.

### Alarms
Alarms can be set to play at certain times and can be configured to repeat at a certain day(s) every week. 

### Weather
View the current weather as well as the weather forecast up to 3 days. This is updated everyday and queries python's
openweatherapi to keep up to date.

### Sick animated background
The background MOOOOVES !!!!

### Python Packed Required to build.
Tkinter
PIL
ntp
playsound
pyowm
