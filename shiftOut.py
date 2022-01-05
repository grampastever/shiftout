# The following program, written in micropython on Thonny, interfaces the RPi Pico with a 
#74HC595 8-bit shift register and displays the results on a 4 x 7-segment display. 
# Two buttons have been incorporated; a clear button and a count button. See readme file 
# for hardware details.

import machine
import utime

#setup each 7-seg enable pins and initialize. Since each 7-segment display is pulled to ground via a 1k resistor
#setting disp_n high will turn off the display and setting disp_n low will turn on the display.
disp_1 = machine.Pin(9, machine.Pin.OUT, value=1)
disp_2 = machine.Pin(8, machine.Pin.OUT, value=1)
disp_3 = machine.Pin(7, machine.Pin.OUT, value=1)
disp_4 = machine.Pin(6, machine.Pin.OUT, value=1)

#setup count and reset buttons
count_button = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_DOWN)
reset_button = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)

#define function shiftOut
def shiftOut(dataPin, clockPin, latchPin, bitOrder, val):
    
    #setup pins and initialize
    data = machine.Pin(dataPin, machine.Pin.OUT, value=0)
    clock = machine.Pin(clockPin, machine.Pin.OUT, value=0)
    latch = machine.Pin(latchPin, machine.Pin.OUT, value=0)
    
    #bit map of digital number to 7-seg display pinout where the bit order is 'abcdefgh'
    #which also maps to the output pins of the 74HC595 as 'QaQbQcQdQeQfQgQh'
    bit_map = ['11111100', '01100000', '11011010', '11110010', '01100110',
               '10110110', '00111110', '11100000', '11111110', '11100110']
    
    #convert the digital val to a corresponding binary string representation of that
    #number as it applies to the 7-segment display
    bin_num = bit_map[val]
    
#shift out per the pre-selected bit order
        
    if bitOrder == 0:  #MSB first
     
        #shift out bin_num MSB first
        for i in range(0, 8):
            a = bin_num[i:i+1]

            #"typecast" string value to integer
            if a == '0':
                data.value(0)
            elif a == '1':
                data.value(1)
            
            clock.value(1)
            clock.value(0)
            
        #display data from the serial register of the74HC595
        latch.value(1)   
        latch.value(0)

    elif bitOrder == 1: #LSB first
    
        #shift out bin_num LSB first
        for i in range(8, 0, -1):
            a = bin_num[i-1:i]
            
            if a == '0':
                data.value(0)
            elif a == '1':
                data.value(1)
                
            clock.value(1)
            clock.value(0)
    
        #display data from the serial register of the74HC595
        latch.value(1)   
        latch.value(0)
    
    else:
        
        #trap bit order error
        print("Bit order error. Must be either 0 = MSB first or 1 = LSB first")
        print("press cntl-c to end")
        while True:
            a = 0  #just a useless variable assignement to keep the while loop going
        
def display(number, bit_order):
    
    display_number = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    sleep_value = 0.004  #seems to be the best compromise between flicker and illumination
    
    for i in range(4):

        ones_digit = number%10
        x = number - ones_digit
        new_number = int(x/10) 
        number = new_number
        shiftOut(2, 4, 3, bit_order, display_number[ones_digit])  #shiftOut(dataPin, clockPin, latchPin, bitOrder 0=MSB first, val)
    
        if i == 0:
            disp_1.value(0)
            utime.sleep(sleep_value)
            disp_1.value(1)
        elif i == 1:
            disp_2.value(0)
            utime.sleep(sleep_value)
            disp_2.value(1)
        elif i == 2:
            disp_3.value(0)
            utime.sleep(sleep_value)
            disp_3.value(1)
        elif i == 3:
            disp_4.value(0)
            utime.sleep(sleep_value)
            disp_4.value(1)
    
#-----------------------
        
z = 0

while True:
    
#count button press program
    
    if count_button.value() == 1:          
        z = z + 1
        press_duration = 0
        # when count button pressed and held for a short period (press_duration < 30)
        #the system keeps displaying the same until press_duration >= 30 at which point the count increments
        #rapidly
        while count_button.value() == 1:
            press_duration = press_duration + 1
            if press_duration < 30:
                display(z, 1)
                
            else:
                display(z, 1)
                z = z + 1
    
    if reset_button.value() == 1:
        z = 0
        #if the reset button is pressed and held, the system keeps displaying '0000'
        while reset_button() == 1:
            display(z, 1)
        
   
    display(z, 1)
    
    



