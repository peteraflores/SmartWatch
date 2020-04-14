# -*- coding: utf-8 -*-
import Tkinter
from PIL import Image, ImageTk
import datetime
import threading
import requests, json 
import os.path, time
from os import path
import pyowm
from playsound import playsound

root = Tkinter.Tk()

# Other settings
showNav = False
showSettings = False
degree_sign= u'\N{DEGREE SIGN}'
gifIndex = -1
gifCount = 47
fontcolor = "#ffaec9"



def kelvin_to_f(temp_k):
    return (((temp_k - 273.15) * 9) / 5) + 32

def unix_time_millis(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    return (dt - epoch).total_seconds()

def exitCallBack():
    root.destroy()


# Settings Menu
def toggleSettings():
    global showSettings
    if showSettings:
        showSettings = False
        settingsFrame.place_forget()
        settingsBanner.place_forget()

    else:
        showSettings = True
        settingsFrame.place(relheight = 0.85, relwidth = 1, relx = 0, rely = 0.15)
        settingsFrame.lift()
        cb_militaryTime.pack(side = "bottom", expand = True, fill = "both")
        cb_displaySeconds.pack(side = "bottom", expand = True, fill = "both")
        cb_displayDate.pack(side = "bottom", expand = True, fill = "both")
        settingsBanner.place(relheight = 0.15, relwidth = 1, relx = 0, rely = 0)
        settingsBanner.lift()
        settingsCloseButton.pack(side = "left", expand = True, fill = "both")
        settingsLabel.pack(side = "left", expand = True, fill = "both")


settingsFrame = Tkinter.Frame(root)
s_militaryTime = Tkinter.IntVar()
s_militaryTime.set(1)

s_displaySeconds = Tkinter.IntVar()
s_displaySeconds.set(0)

s_displayDate = Tkinter.IntVar()
s_displayDate.set(0)

cb_militaryTime = Tkinter.Checkbutton(settingsFrame, text = "24 Hour Clock", \
                variable = s_militaryTime, onvalue = 1, offvalue = 0, fg = fontcolor, bg = "black")
cb_displaySeconds = Tkinter.Checkbutton(settingsFrame, text = "Display Seconds", \
                variable = s_displaySeconds, onvalue = 1, offvalue = 0, fg = fontcolor, bg = "black")
cb_displayDate = Tkinter.Checkbutton(settingsFrame, text = "Display Date", \
                variable = s_displayDate, onvalue = 1, offvalue = 0, fg = fontcolor, bg = "black")

settingsBanner = Tkinter.Frame(root, relief = "raised", bd = 1)
settingsCloseButton = Tkinter.Button(settingsBanner, text = "Close", command = toggleSettings, font = ("Helvetica", 40), highlightbackground = fontcolor, highlightcolor = fontcolor, bg = "black", fg = fontcolor)
settingsLabel = Tkinter.Label(settingsBanner, text = "Settings", font = ("Helvetica", 40))


# Nav arrows

def displayNavArrows():
    global showNav
    if showNav:
        showNav = False
        leftButton.place_forget()
        rightButton.place_forget()
    else:
        showNav = True
        
        leftButton.place(relheight = 0.1, relwidth = 0.1, relx = 0, rely = 0.5)
        rightButton.place(relheight = 0.1, relwidth = 0.1, relx = 1 - 0.1, rely = 0.5)
        leftButton.lift()
        rightButton.lift()

def leftPress():
    changeScreen(-1)
    

def rightPress():
    changeScreen(1)

def changeScreen(val):
    global var_screenMode
    global var_navLabel


    previousMode = var_screenMode.get()
    var_screenMode.set((val + var_screenMode.get()) % 3)

    if previousMode == 0:
        hideClock()
    elif previousMode == 1:
        hideAlarms()
    elif previousMode == 2:
        hideWeather()


    if var_screenMode.get() == 0:
        var_navLabel.set("Watch")
        displayClock()
    elif var_screenMode.get() == 1:
        var_navLabel.set("Alarms")
        displayAlarms()
    elif var_screenMode.get() == 2:
        var_navLabel.set("Weather")
        displayWeather()
    try:
        navBar.lift()
    except:
        pass

var_screenMode = Tkinter.IntVar()
leftButton = Tkinter.Button(root, text = "<", command = leftPress, font = ("Helvetica", 20), highlightbackground = fontcolor, highlightcolor = fontcolor, bg = "black", fg = fontcolor)
rightButton = Tkinter.Button(root, text = ">", command = rightPress, font = ("Helvetica", 20), highlightbackground = fontcolor, highlightcolor = fontcolor, bg = "black", fg = fontcolor)


# Nav Bar

def displayNavBar():
    navBar.place(relheight = 0.15, relwidth = 1, relx = 0, rely = 0)
    navBar.lift()
    hideButton.pack(side = "left", expand = True, fill = "both")
    settingsButton.pack(side = "left", expand = True, fill = "both")
    l_navBar.pack(side = "left", expand = True, fill = "both")



var_navLabel = Tkinter.StringVar()
var_navLabel.set("Watch")
navBar = Tkinter.Frame(root, relief = "raised", bd = 1)
hideButton = Tkinter.Button(navBar, text = "Hide", command = displayNavArrows, font = ("Helvetica", 40), highlightbackground = fontcolor, highlightcolor = fontcolor, bg = "black", fg = fontcolor)
settingsButton = Tkinter.Button(navBar, text = "Settings", command = toggleSettings, font = ("Helvetica", 40), highlightbackground = fontcolor, highlightcolor = fontcolor, bg = "black", fg = fontcolor)
l_navBar = Tkinter.Label(navBar, textvariable = var_navLabel, font = ("Helvetica", 40), highlightbackground = fontcolor, highlightcolor = fontcolor, bg = "black", fg = fontcolor)
root.attributes('-fullscreen', True)


# Weather Menu

def queryWeather():
    # import required modules 
    import requests, json 
    
    # Enter your API key here 
    api_key = "21dcf30c39ec9ab0737b260a22629bf4"
    
    # base_url variable to store url 
    base_url = "https://api.openweathermap.org/data/2.5/forecast?"
    
    # Give city name 
    city_zip = "07960"
    
    # complete_url variable to store 
    # complete url address 
    complete_url = base_url + "appid=" + api_key + "&zip=" + city_zip
    
    # get method of requests module 
    # return response object 
    response = requests.get(complete_url) 
    # json method of response object  
    # convert json format data into 
    # python format data 
    x = response.json()
    with open('data.json', 'w') as outfile:
        json.dump(x, outfile)

def getWeather():
    #Check if weather data is too old
    if  not path.exists("data.json"):
        queryWeather()
    elif os.path.getctime("data.json") >= 10800 + unix_time_millis(datetime.datetime.now()):
        queryWeather()
    with open('data.json') as f:
        data = json.load(f)
    return data

def hideWeather():
    f_weatherBG.place_forget()

def getWeatherNear(date,data):

    weatherList = data["list"]
    for i in weatherList:
        if i["dt"] < unix_time_millis(date) + 5400 and i["dt"] > unix_time_millis(date) - 5400:
            return i
    return weatherList[0]


def displayWeather():
    global var_weatherData
    global degree_sign
    temp_timeNow = datetime.datetime.now()
    temp_epochTimeNow = unix_time_millis(temp_timeNow)
    var_weatherData = getWeather()
    weatherNow = getWeatherNear(temp_timeNow,var_weatherData)
    var_weatherAndLoc.set("%d%sF\n%s" % (kelvin_to_f(weatherNow["main"]["temp"]), degree_sign, var_weatherData["city"]["name"]))
    f_weatherBG.place(relheight = 0.85, relwidth = 1, relx = 0, rely = 0.15)
    f_weatherMainStage.place(relheight = 0.5, relwidth = 0.7, relx = 0.15, rely = 0.1)
    f_forecast.place(relheight = 0.3, relwidth = 0.9, relx = 0.05, rely = 0.65)
    l_weatherTodayWeatherAndLoc.configure(image = weatherImages[weatherNow["weather"][0]["main"]])
    l_weatherTodayWeatherAndLoc.pack(side = "top", fill = "x")

    for i in range(4):
        temp_epochTime = temp_epochTimeNow + 86400*i
        temp_time = datetime.datetime.fromtimestamp(temp_epochTime)
        temp_weather = getWeatherNear(temp_time, var_weatherData)
        temp_day = temp_time.strftime("%a")

        var_forecastDict["forecast%d" % (i)].configure(image = weatherImages[temp_weather["weather"][0]["main"]])
        var_forecastDict["forecast%d" % (i)].pack(side = "left", expand = True, fill = "both")
        temp_text = "%d%sF\n%s" % (int(kelvin_to_f(temp_weather["main"]["temp"])), degree_sign, temp_day )
        var_forecastDict["var%d" % (i)].set(temp_text)
        var_forecastDict["label%d" % (i)].pack(side = "top", fill = "both")


var_weatherData = getWeather()
var_weatherAndLoc = Tkinter.StringVar()


f_weatherBG = Tkinter.Frame(root, bg = "black", highlightbackground = fontcolor)
f_weatherMainStage = Tkinter.Frame(f_weatherBG, bd = 1, relief = "sunken", bg = fontcolor, highlightbackground = fontcolor, highlightcolor = fontcolor)
f_forecast = Tkinter.Frame(f_weatherBG, bd = 1, relief = "sunken", bg = "black", highlightbackground = fontcolor, highlightcolor = fontcolor)
l_weatherTodayWeatherAndLoc = Tkinter.Label(f_weatherMainStage, textvariable = var_weatherAndLoc, font = ("Helvetica", 40), fg = "black", bg = fontcolor, compound = "bottom")
var_forecastDict = {}
for i in range(4):
    var_forecastDict["forecast%d" % (i)] = Tkinter.Label(f_forecast, bd = 1, relief = "raised", bg = fontcolor, highlightbackground = "black", highlightcolor = fontcolor, fg = "black", compound = "bottom")
    var_forecastDict["var%d" % (i)] = Tkinter.StringVar()
    var_forecastDict["label%d" % (i)] = Tkinter.Label(var_forecastDict["forecast%d" % (i)], font = ("Helvetica", 15), textvariable = var_forecastDict["var%d" % (i)], bg = fontcolor, highlightbackground = fontcolor, highlightcolor = fontcolor, fg = "black")

weatherImages = {}
weatherH = 50
weatherW = 50
weatherImages["Clear"] =        ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-49_5896925.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Clouds"] =       ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-41_5896917.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Thunderstorm"] = ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-08_5896885.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Drizzle"] =      ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-03_5896879.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Rain"] =         ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-02_5896922.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Snow"] =         ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-21_5896896.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Mist"] =         ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-17_5896895.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Smoke"] =        ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-17_5896895.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Haze"] =         ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-17_5896895.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Dust"] =         ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-17_5896895.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Fog"] =          ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-17_5896895.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Sand"] =         ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-17_5896895.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Ash"] =          ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-17_5896895.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Squall"] =       ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-17_5896895.png").resize((weatherW, weatherH), Image.ANTIALIAS))
weatherImages["Tornado"] =      ImageTk.PhotoImage(Image.open("icons/iconfinder_weather_cloud_sun_moon_rain-17_5896895.png").resize((weatherW, weatherH), Image.ANTIALIAS))
root.weatherImages = weatherImages

# Alarms menu 

# used to convert reoccuring alarm to day list
def alarmToDayList(alarm):
    t_list = []
    if alarm[2]:
        t_list.append(6)
    if alarm[3]:
        t_list.append(0)
    if alarm[4]:
        t_list.append(1)
    if alarm[5]:
        t_list.append(2)
    if alarm[6]:
        t_list.append(3)
    if alarm[7]:
        t_list.append(4)
    if alarm[8]:
        t_list.append(5)
    return t_list   

def playAlarm():
    playsound("alarm.mp3")
    
    

def checkAlarms():
    global var_alarmsList
    for a in var_alarmsList:
        #Does the alarm repeat?
        if len(a) > 3:
            r_alarm = alarmToDayList(a)
            for d in r_alarm:
                currentDT = datetime.datetime.now()
                if d == int(currentDT.weekday()) and a[0] == int(currentDT.hour) and a[1] == int(currentDT.minute) and a[9] == False:
                    a[9] == True
                    #playAlarm()
                    t = threading.Thread(target=playAlarm, name='Ringing Alarm') 
                    t.daemon = True
                    t.start()
                elif a[0] == int(currentDT.hour) or a[1] == int(currentDT.minute):
                    a[9] = False
        else:
            #Check if alarm has run
            currentDT = datetime.datetime.now()
            if a[2] == False and a[0] == int(currentDT.hour) and a[1] == int(currentDT.minute):
                #playAlarm()
                a[2] = True
                t = threading.Thread(target=playAlarm, name='Ringing Alarm')
                t.daemon = True
                t.start()

    root.after(50,checkAlarms)

def hideAlarmDialogue():
    f_alarmDialogBG.place_forget()
    refreshAlarmList()

def addAlarm():
    global var_alarmsList
    temp_listItem = []
    temp_listItem.append(var_alarmHours.get())
    temp_listItem.append(var_alarmMinute.get())
    
    if var_repeat.get():
        temp_listItem.append(var_rsun.get())
        temp_listItem.append(var_rmon.get())
        temp_listItem.append(var_rtue.get())
        temp_listItem.append(var_rwed.get())
        temp_listItem.append(var_rthu.get())
        temp_listItem.append(var_rfri.get())
        temp_listItem.append(var_rsat.get())
    
    temp_listItem.append(False)
    
    var_alarmsList.append(temp_listItem)
    hideAlarmDialogue()

def onAlarmListBoxSelect(evt):
    global var_alarmsList
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    if len(w.curselection()) > 0:
        index = int(w.curselection()[0])
        value = w.get(index)
        w.delete(index)
        var_alarmsList.pop(index)


def displayAlarmDialogue():
    f_alarmDialogBG.place(relheight = 1, relwidth = 1, relx = 0, rely = 0)
    f_alarmDialogBanner.place(relheight = 0.15, relwidth = 1, relx = 0, rely = 0)
    f_alarmDialogBottomBar.place(relheight = 0.15, relwidth = 0.70, relx = 0.15, rely = 0.7)
    f_alarmDialogBG.lift()
    l_alarmDialogTitle.pack(fill = "both", expand = True)
    b_alarmDialogueAdd.pack(side = "left", fill = "both", expand = True)
    b_alarmDialogueCancel.pack(side = "left", fill = "both", expand = True)
    
    f_alarmSpinboxFrame.place(relheight = 0.15, relwidth = 0.5, relx = 0.25, rely = 0.3)
    spinbox_hours.place(relheight = 1, relwidth = 0.4, relx = 0, rely = 0)
    l_spinboxColon.place(relheight = 1, relwidth = 0.2, relx = 0.4, rely = 0)
    spinbox_minutes.place(relheight = 1, relwidth = 0.4, relx = 0.6, rely = 0)

    f_alarmCalendar.place(relheight = 0.15, relwidth = 0.7, relx = 0.15, rely = 0.5)

    cb_repeatAlarm.pack(side = "left", fill = "both", expand = True)
    cb_sun.pack(side = "left", fill = "both", expand = True)
    cb_mon.pack(side = "left", fill = "both", expand = True)
    cb_tue.pack(side = "left", fill = "both", expand = True)
    cb_wed.pack(side = "left", fill = "both", expand = True)
    cb_thu.pack(side = "left", fill = "both", expand = True)
    cb_fri.pack(side = "left", fill = "both", expand = True)
    cb_sat.pack(side = "left", fill = "both", expand = True)


def refreshAlarmList():
    global var_alarmsList
    size = list_alarms.size()
    if size > 0:
        list_alarms.delete(0,size-1)
    for item in var_alarmsList:
        var_itemString = "Alarm at %02d:%02d"%(item[0],item[1])
        if len(item) > 3:
            var_itemString += " every"
            if item[2]: 
                var_itemString += " Sunday,"
            if item[3]:
                var_itemString += " Monday,"
            if item[4]:
                var_itemString += " Tuesday,"
            if item[5]:
                var_itemString += " Wednesday,"
            if item[6]:
                var_itemString += " Thursday,"
            if item[7]:
                var_itemString += " Friday,"
            if item[8]:
                var_itemString += " Saturday,"
        list_alarms.insert("end", var_itemString)

def displayAlarms():
    f_alarms.place(relheight = 1, relwidth = 1, relx = 0, rely = 0)
    f_subAlarms.place(relheight = 0.65, relwidth = 0.7, relx = 0.15, rely = 0.15)
    sb_alarms.pack(side = "right", fill = "y")
    list_alarms.pack(fill = "both", expand = True)
    refreshAlarmList()
    b_addAlarm.place(relheight = 0.15, relwidth = 0.6, relx = 0.2, rely = 0.82)

def hideAlarms():
    f_alarms.place_forget()

var_alarmsList = []
f_alarms = Tkinter.Frame(root, bg = "black")
f_subAlarms = Tkinter.Frame(f_alarms, relief = "sunken", bd = 1, bg = "black", highlightbackground = fontcolor)
sb_alarms = Tkinter.Scrollbar(f_subAlarms, bg = "black", highlightbackground = fontcolor, highlightcolor = fontcolor, troughcolor = fontcolor)
list_alarms = Tkinter.Listbox(f_subAlarms, yscrollcommand = sb_alarms.set , bg = "black", highlightbackground = fontcolor, highlightcolor = fontcolor, fg = fontcolor, font = ("Helvetica", 15))
list_alarms.bind('<<ListboxSelect>>', onAlarmListBoxSelect)
b_addAlarm = Tkinter.Button(f_alarms, text = "Add Alarm", command = displayAlarmDialogue, font = ("Helvetica", 40), highlightbackground = fontcolor, highlightcolor = fontcolor, bg = "black", fg = fontcolor)

f_alarmDialogBG = Tkinter.Frame(root, bg = "black")
f_alarmDialogBanner = Tkinter.Frame(f_alarmDialogBG, bd = 1, relief = "raised", bg = "black", highlightbackground = fontcolor, highlightcolor = fontcolor)
l_alarmDialogTitle = Tkinter.Label(f_alarmDialogBanner, text = "Add alarm", font = ("Helvetica", 40), bg = "black", fg = fontcolor, highlightbackground = fontcolor, highlightcolor = fontcolor)
f_alarmDialogBottomBar = Tkinter.Frame(f_alarmDialogBG, bd = 1, relief = "sunken", bg = "black")
b_alarmDialogueCancel = Tkinter.Button(f_alarmDialogBottomBar, text = "Cancel", command = hideAlarmDialogue, font = ("Helvetica", 40), highlightbackground = fontcolor, highlightcolor = fontcolor, bg = "black", fg = fontcolor)
b_alarmDialogueAdd = Tkinter.Button(f_alarmDialogBottomBar, text = "Add", command = addAlarm, font = ("Helvetica", 40), highlightbackground = fontcolor, highlightcolor = fontcolor, bg = "black", fg = fontcolor)

var_alarmHours = Tkinter.IntVar()
var_alarmMinute = Tkinter.IntVar()
f_alarmSpinboxFrame = Tkinter.Frame(f_alarmDialogBG, bd = 1, relief = "sunken", bg = "black", highlightbackground = fontcolor, highlightcolor = fontcolor)
l_spinboxColon = Tkinter.Label(f_alarmSpinboxFrame, font = ("Helvetica", 50), text = ":", bg = "black", fg = fontcolor)
spinbox_hours = Tkinter.Spinbox(f_alarmSpinboxFrame, font = ("Helvetica", 60),\
    from_ = 0, to = 23, wrap = True, format = "%02.0f", state = "readonly", textvariable = var_alarmHours, bg = "black", highlightbackground = fontcolor, highlightcolor = fontcolor, fg = fontcolor, buttonbackground = "black", background = "black")
spinbox_minutes = Tkinter.Spinbox(f_alarmSpinboxFrame, font = ("Helvetica", 60),\
    from_ = 0, to = 59, wrap = True, format = "%02.0f", state = "readonly", textvariable = var_alarmMinute, bg = "black", highlightbackground = fontcolor, highlightcolor = fontcolor, fg = fontcolor, buttonbackground = "black", background = "black")
f_alarmCalendar = Tkinter.Frame(f_alarmDialogBG, bd = 1, relief = "sunken", bg = "black")

var_repeat = Tkinter.IntVar()
var_rsun = Tkinter.IntVar()
var_rmon = Tkinter.IntVar()
var_rtue = Tkinter.IntVar()
var_rwed = Tkinter.IntVar()
var_rthu = Tkinter.IntVar()
var_rfri = Tkinter.IntVar()
var_rsat = Tkinter.IntVar()

cb_sun = Tkinter.Checkbutton(f_alarmCalendar, text = "Sun", variable = var_rsun, onvalue = 1, offvalue = 0, fg = fontcolor, bg = "black")
cb_mon = Tkinter.Checkbutton(f_alarmCalendar, text = "Mon", variable = var_rmon, onvalue = 1, offvalue = 0, fg = fontcolor, bg = "black")
cb_tue = Tkinter.Checkbutton(f_alarmCalendar, text = "Tue", variable = var_rtue, onvalue = 1, offvalue = 0, fg = fontcolor, bg = "black")
cb_wed = Tkinter.Checkbutton(f_alarmCalendar, text = "Wed", variable = var_rwed, onvalue = 1, offvalue = 0, fg = fontcolor, bg = "black")
cb_thu = Tkinter.Checkbutton(f_alarmCalendar, text = "Thu", variable = var_rthu, onvalue = 1, offvalue = 0, fg = fontcolor, bg = "black")
cb_fri = Tkinter.Checkbutton(f_alarmCalendar, text = "Fri", variable = var_rfri, onvalue = 1, offvalue = 0, fg = fontcolor, bg = "black")
cb_sat = Tkinter.Checkbutton(f_alarmCalendar, text = "Sat", variable = var_rsat, onvalue = 1, offvalue = 0, fg = fontcolor, bg = "black")
cb_repeatAlarm = Tkinter.Checkbutton(f_alarmCalendar, text = "Repeat", variable = var_repeat, onvalue = 1, offvalue = 0, fg = fontcolor, bg = "black")




# Watch Face

def playGif():
    global gifIndex
    global background_frames
    gifIndex = (gifIndex + 1) % gifCount
    try:
        if clock.winfo_exists():
            w = clock.winfo_width()
            h = clock.winfo_height()
            t_width, t_height = clock.background_frames[gifIndex].size
            if t_width != w and t_height != h:
                clock.background_frames[gifIndex] = clock.background_frames[gifIndex].resize((w, h), Image.ANTIALIAS)
            gif = ImageTk.PhotoImage(clock.background_frames[gifIndex])
            watchFace.image = gif
            watchFace.configure(image=gif)
            watchFace.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
    except Exception as ex:
        print ex
    root.after(50,playGif)

def displayClock():
    clock.place(relheight = 1, relwidth = 1, relx = 0, rely = 0)
    clock.update()
    playGif()


def hideClock():
    clock.place_forget()
    watchFace.place_forget()

def updateClock():
    global var_screenMode
    try:
        if var_screenMode.get() == 0:
            watchText = ""
            dateStr = ""
            currentDT = datetime.datetime.now()
            
            if s_militaryTime.get() == 1:
                if s_displaySeconds.get() == 1:
                    watchText = currentDT.strftime("%H:%M:%S")
                else:
                    watchText = currentDT.strftime("%H:%M")
            else:
                if s_displaySeconds.get() == 1:
                    watchText = currentDT.strftime("%I:%M:%S %p")
                else:
                    watchText = currentDT.strftime("%I:%M %p")

            if s_displayDate.get() == 1:
                watchText += "\n%s" % (currentDT.strftime("%a, %b %d, %Y"))
                watchFace.configure(font = ("Helvetica", 55))
            else:
                watchFace.configure(font = ("Helvetica", 110))
                
            clockText.set(watchText)
    except Exception as ex:
        print ex
    root.after(50, updateClock)


clock = Tkinter.Frame(root)
clockText = Tkinter.StringVar()
watchFace = Tkinter.Label(clock, textvariable = clockText, font = ("Helvetica", 110), compound = "center", fg = fontcolor)
background_frames = []


for i in range(gifCount):
    background_frames.append(Image.open("background/frame_%02d.gif" % i))

clock.background_frames = background_frames

# MAIN LOOP

displayClock()
displayNavArrows()
displayNavBar()

updateClock()
checkAlarms()
Tkinter.mainloop()