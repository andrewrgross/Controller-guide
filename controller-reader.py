#############################
### controller-reader.py -- Andrew R Gross -- 2017-11-12 -- andrew@shrad.org
###
### This program will read input from a joystick or videogame controller, format it, 
### and then send it over a serial channel so an Arduino can receive it.
### Rows that should be customized are commented with '#-# '.
###

import serial
import pygame
import time

#############################
### 1: Identify the controller

pygame.init()                                     # Initiate the pygame functions
j = pygame.joystick.Joystick(0)                   # Define a joystick object to read from
j.init()                                          # Initiate the joystick or controller
print 'Detected controller : %s' % j.get_name()   # Print the name of any detected controllers

#############################
### 2: Open a Serial Channel to the Arduino

serial_is_on = False                            #-# Make 'True' to attempt a serial connection 
serial_port = '/dev/ttyUSB0'			        #-# Assign the location of the port that appears when the Arduino is plugged into the pi to a value
baud_rate = 9600					              # Assign the baudrate to a value

if serial_is_on == True:                          #Create an object that represents our open serial connection
    ser = serial.Serial(serial_port, baud_rate, timeout=1)	

#############################
### 3: Select which axes to check
   
axes_to_check = [1,3]		    		        #-# List the axes to check. Here, I want to check axis #1 and #3.
check_frequency = 5                             #~# Specify how many times a second to check for new values
breakout_button = 3                             #-# Specify which button stops the program

#############################
### 4: Begin reading the controller

while True:					                      # The program will check the button and joystick states until interrupted

    pygame.event.pump()			                  # The event.pump function refreshes knowledge of what events have changed (I think)
    recent_values = []		                      # Declare an empty list to store the values in before writing to serial
    for current_axis in axes_to_check:	          # Loop through the axes to check
        latest_value = j.get_axis(current_axis)	  # Store the current value of the axis
                                                  # If either axis isn't centered, the value will be reported
        if latest_value != 0.00: print 'Axis %i reads %.3f' % (current_axis, latest_value)
        #print(latest_value)                    #-# Uncomment to see all the raw values.  Spoiler alert: they'll mostly be zeros
                                                  # The value gets converted to an integer ranging from 0 - 200
        value_mod = int(round(latest_value*100,2)+100)
        value_mod = str(value_mod)                # The value gets converted to a string
        recent_values.append(value_mod)           # The string is added to the list of values to send over serial

    serial_output =','.join(recent_values) + ';'  # The list gets converted to a character string
    #print(serial_output)                       #-# Uncomment to see the character string that gets sent

    if serial_is_on == True:
        ser.write(serial_output)                  # The text string is sent over serial, one character at a time

    time.sleep(1/check_frequency)                 # The program waits the specified length before checking new values

    if j.get_button(breakout_button) == 1:        # If the breakout button is being held, the program ends
        break

