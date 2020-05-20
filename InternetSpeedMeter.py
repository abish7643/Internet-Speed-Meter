import curses
import psutil
import time
import os

screen = curses.initscr()

screen.addstr(0, 3, "Quantitative Network Analysis",curses.A_BOLD)
screen.addstr(3, 1, "Download Speed")
screen.addstr(4, 1, "Upload Speed")
screen.addstr(6, 1, "Session Data Downloaded")
screen.addstr(7, 1, "Session Data Uploaded")

#curses.napms(3000) Add Delay Before Refreshing Screen
#curses.endwin()

t0 = time.time()
uploadSpeed = 0
downloadSpeed = 0
upload = 0.00
download = 0.00
speed = (upload, download)
saveInitalData = False

while True:
    last_speed = speed
    upload = psutil.net_io_counters(pernic=True)['wlp2s0'][0]
    download = psutil.net_io_counters(pernic=True)['wlp2s0'][1]

    if (saveInitalData == False):
        initialUpPackets = upload
        initialDownPackets = download
        saveInitalData = True
    
    speed = (upload, download)
    t1 = time.time()
    
    try:
        uploadSpeed, downloadSpeed = [(now - last)/(t1 - t0)/1024.0 for now, last in zip(speed, last_speed)]
        t0 = time.time()
    except:
        pass

    if downloadSpeed > 0.1 or uploadSpeed >= 0.1:
        time.sleep(0.75)
        upspeedAsString = '{:0.2f} kB/s '.format(uploadSpeed)
        downspeedAsString = '{:0.2f} kB/s'.format(downloadSpeed)
        uploadSessionData = '{:0.2f} MB'.format((upload-initialUpPackets)/1024/1024)
        downloadSessionData = '{:0.2f} MB'.format((download-initialDownPackets)/1024/1024)

        if (saveInitalData == True):
            screen.addstr(3, 20, downspeedAsString)
            screen.addstr(4, 20, upspeedAsString)
            screen.addstr(6, 30, downloadSessionData)
            screen.addstr(7, 30, uploadSessionData)
            screen.refresh()
