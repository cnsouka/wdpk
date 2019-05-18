#!/usr/bin/env python
# encoding: utf-8

import time
import spidev
import curses

import bytearrays

# 0x00 0x01 ~ 0xFF...
# 0x66 ...

spi = spidev.SpiDev()

spi.open(0, 0)
spi.max_speed_hz = 100000
#spi.max_speed_hz = 15600000

data = [0x00,0x00,0x00,0x00]

print('running')

# a blank datasheet, use this to refresh
blank = ['00000000','00000000','00000000','00000000','00000000','00000000','00000000','00000000']
def blankit():
    
    for j in range(0,8):

        data[0] = ~int(blank[j],2)
        data[2] = 0xFF
        data[1] = 0xFF
        data[3] = 0x01 << j

        spi.xfer(data)

# run
def main(stdscr):

    nowmat = []

    stdscr.addstr(' _ _ _   _     _   \n')
    stdscr.addstr('| | | |_| |___| |_ \n')
    stdscr.addstr('| | | | . | . | ._|\n')
    stdscr.addstr('|_____|___|  _|_,_|\n')
    stdscr.addstr('          |_|      \n\n')
    stdscr.addstr('*** press any key to start... ***')

    stdscr.nodelay(1)
    while True:

        c = stdscr.getch()
        if c != -1:

            stdscr.move(6, 0)

            stdscr.addstr('*** Wdpk is Running, Press Ctrl+C to exit *** \n\n')  

            stdscr.addstr('now press: ' + str(c) + ' \n')
            stdscr.refresh()

            #map the keys
            if   c == 49:
                nowmat = bytearrays.testarrays[0]
            elif c == 50:
                nowmat = bytearrays.testarrays[1]
            elif c == 51:
                nowmat = bytearrays.testarrays[2]
            elif c == 52:
                nowmat = bytearrays.testarrays[3]
            elif c == 53:
                nowmat = bytearrays.testarrays[4]
            elif c == 54:
                nowmat = bytearrays.testarrays[5]

        # send
        '''
        if nowmat:
            for j in range(0,8):

                data[0] = ~int(nowmat[j],2) # reverse the data and convert to hex
                data[2] = 0xFF
                data[1] = 0xFF
                data[3] = 0x01 << j

                spi.xfer(data)
                # time.sleep(0.08)
        '''

        if nowmat:

            if len(nowmat) > 1:
                delay = 30 # increase this will delay the framerate
            else:
                delay = 1

            for mat in nowmat:

                for m in range(0,delay):

                    for j in range(0,8):

                        data[0] = ~int(mat[j],2) # reverse
                        data[2] = 0xFF
                        data[1] = 0xFF
                        data[3] = 0x01 << j

                        spi.xfer(data)
                        # time.sleep(0.08)

                        stdscr.move(9, 0)
                        stdscr.addstr( str(mat[0]) + ' in ' + str(len(nowmat)))
                        stdscr.refresh()


                blankit()
                #time.sleep(0) # between 2 frames

if __name__ == '__main__':
    curses.wrapper(main)