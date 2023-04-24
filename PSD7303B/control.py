"""
Author: Ashutosh Singh
Date: 24th Apr'23
Short Desc: Control DC power Supply
##############################################################################################
Description: Python script to control scientific Programmable DC power supply (PSD7303B)
Current implementation uses USB to connect to the device. Network implementation
was avoided as the network might have multiple devices plugged in. 
##############################################################################################
Device uses SCPI command sequence. It is readily available in the datasheet
It requires a delay of about 20ms between successive commands. Query_delay is set
with the the module, however, read/write don't have a delay parameter, hence they
are put in manually. 
The commands are NOT case sensitive.
##############################################################################################
Features: 
read/write current, read/write voltage, turn on/off channel
##############################################################################################
"""

import pyvisa                      ##install NI visa
import time
def delay():
    time.sleep(0.02)
rm=pyvisa.ResourceManager()
print(rm.list_resources())         ## list of all NI instruments connected to the PC 


my_instrument = rm.open_resource("USB0::0x0483::0x7540::SPD3XIDD5R6197::INSTR")
my_instrument.write_termination = "\n"                                  # setting character termination
my_instrument.read_termination = "\n"   
my_instrument.query_delay=0.02                                          #delay = 20ms

#my_instrument.write('OUTP CH1,OFF')                                    #Turn OFF
my_instrument.write('OUTP CH2,ON')                                      #Turn ON
delay()


my_instrument.write('CH1:curr 2')                                       #Set current (max 3.2A)                           
delay()
print(my_instrument.query('CH1:CURR?'))                                 #Read current
delay()


my_instrument.write('CH1:VOLT 12.1')                                    #Write Voltage
delay()
print(my_instrument.query('CH1:VOLT?'))                                 #Read voltage


my_instrument.close()                                                   #close the instance