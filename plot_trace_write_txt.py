"""

This Python example shows how to transfer waveform data from Rohde & Schwarz Oscilloscope

Author: Ashutosh Kumar Singh
Date: 20 May'22

Enter the timescale in line#38;
This code is for channel 2, which can be changed for channel 1
"""

from RsInstrument.RsInstrument import RsInstrument
import matplotlib.pyplot as plt
from time import time
import numpy as np
from datetime import datetime

rth = None
try:
    
    rth = RsInstrument('TCPIP::172.16.0.92::INSTR', True, False)
    #rth = RsInstrument('TCPIP::169.254.253.36::INSTR', True, False)
    rth.visa_timeout = 10000  # Timeout for VISA Read Operations
    rth.opc_timeout = 10000  # Timeout for opc-synchronised operations
    rth.instrument_status_checking = True  # Error check after each command
except Exception as ex:
    print('Error initializing the instrument session:\n' + ex.args[0])
    exit()
    
print(f'Device IDN: {rth.idn_string}')
print(f'Device Options: {",".join(rth.instrument_options)}\n')

rth.clear_status()
rth.reset()

rth.write_str("CHAN:TYPE HRES")     # Switching high res
rth.write_str("CHAN1:STAT OFF")     # Switch Channel 1 OFF
rth.write_str("CHAN2:STAT ON")      # Switch Channel 2 ON

tmscale= 1E-8                              #enter the timescae
timescale = 'TIM:SCAL '+ str(tmscale)
rth.write_str((timescale))          #timescale


rth.write_str("CHAN2:SCAL 0.5")     #scale
rth.write_str("CHAN2:POS 0")        #position 
#rth.write_str("CHAN1:COUP DCL")    #1Mohm termination resistance
rth.write_str("CHAN2:COUP DC")      #50ohm termination resistance
rth.write_str("TRIG:A:SOUR CH2")    #trigger channel
rth.write_str("TRIG:A:TYPE RIS")    #rising edge rigger
#rth.write_str("TRIG:A:EDGE:SLOP NEG")


start = time()
rth.write_str("FORM:DATA ASC")
rth.data_chunk_size = 1000000  # transfer in blocks of 100k bytes (default)
data_asc = rth.query_bin_or_ascii_float_list("CHAN2:DATA?")

##writing data in file
data=np.array(data_asc)
now = datetime.now()
f = open('run_file'+str(now), 'a')
for i in range(len(data)):
    f.write(f"{data[i]}\n")
print(f'ASCII waveform transfer elapsed time: {time() - start:.3f}sec')


plt.figure(2)
plt.plot(data_asc)
plt.title('waveform; Timescale:'+str(tmscale)) 
plt.grid()
plt.show()
rth.close()
f.close()