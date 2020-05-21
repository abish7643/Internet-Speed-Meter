import curses
import psutil
import time
import os

screen = curses.initscr()
height, width = screen.getmaxyx() #Getting Height and Width
title = "Quantitative Network Analysis"
footer = "Ctrl + C to Exit!"
start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
start_y = int((height // 2) - 5)
start_x = int(width // 2) - 20

#Color Combinations
curses.start_color()
curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

#Static Text
screen.addstr(start_y, start_x_title, title, curses.A_BOLD)
screen.addstr(start_y+3, start_x, "Download Speed")
screen.addstr(start_y+4, start_x, "Upload Speed")
screen.addstr(start_y+6, start_x, "Data Downloaded")
screen.addstr(start_y+7, start_x, "Data Uploaded")

#Footer Static Text
screen.attron(curses.color_pair(3))
screen.addstr(height-1, 0, footer)
screen.addstr(height-1, len(footer), " " * (width - len(footer) - 1))
screen.attroff(curses.color_pair(3))

#Height & Width At (0,0)
whRender = "W: {}, H: {}".format(width, height)
screen.addstr(0, 0, whRender, curses.color_pair(1))

#curses.napms(3000) Add Delay Before Refreshing Screen
#curses.endwin()

t0 = time.time()
uploadSpeed = 0
downloadSpeed = 0
upload = 0.00
download = 0.00
speed = (upload, download)
saveInitalData = False
sessionStartedTime = t0

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
        uploadSessionData = (upload-initialUpPackets)/1024/1024
        downloadSessionData = (download-initialDownPackets)/1024/1024
        uploadSessionDataAsString = '{:0.2f} MB'.format(uploadSessionData)
        downloadSessionDataAsString = '{:0.2f} MB'.format(downloadSessionData)

    if (saveInitalData == True):
        screen.attron(curses.color_pair(1))
        screen.addstr(start_y+3, start_x+20, downspeedAsString)
        screen.attroff(curses.color_pair(1))
        screen.addstr(start_y+4, start_x+20, upspeedAsString)
        
        if (downloadSessionData >= 500 or uploadSessionData >= 200):
            screen.attron(curses.color_pair(2))
            screen.addstr(start_y+6, start_x+20, downloadSessionDataAsString)
            screen.addstr(start_y+7, start_x+20, uploadSessionDataAsString)
            screen.attroff(curses.color_pair(2))
        else:
            screen.attron(curses.color_pair(1))
            screen.addstr(start_y+6, start_x+20, downloadSessionDataAsString)
            screen.attroff(curses.color_pair(1))
            screen.addstr(start_y+7, start_x+20, uploadSessionDataAsString)
        
        screen.refresh()