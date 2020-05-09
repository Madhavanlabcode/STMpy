import os.path
import sys
import array
import time
import serial
ser.close()
print('├── STMpy.SR830: cmdser, setVol,readSens,')
print('initialize with    ser = serial.Serial("COM4", 9600, timeout=1)')
print('read data with     ser.read(100) # read up to one hundred bytes ')

def setVol(ser,n):
    """
    input: 
        n:the modulation voltage in Volte
    output: 
        the modulation voltage after re-setting
    set the modulation voltage to n
    """    
    st='SLVL'+str(n)+'\n'
    ser.write(str.encode(st))
    ser.write(str.encode('SLVL?\n'))#return the modulation voltage after re-setting
    s = ser.read(256);
    print(s)


def cmdser(ser,cmd):
    """
    input:
        cmd: [string] command abbreviation
            '*IDN?'= Queries the device identification
            'OUTP?1' = Queries the value of X (CH1)
            for other command, refer: http://users.df.uba.ar/dgrosz/material%20adicional/manual%20lock-in%20SR830.pdf from page 85.
    output:
        read data
    """
    print('Sending:', cmd)
    ser.write(str.encode(cmd+'\n'))#read output in channel 1
    s = ser.read(256);
    if len(s) > 0:
        print(s)

def readSens(ser):
"""
read sensitivity: the returned number corresponding to...
i sensitivity   i sensitivity
0 2 nV/fA       13 50 µV/pA
1 5 nV/fA       14 100 µV/pA
2 10 nV/fA      15 200 µV/pA
3 20 nV/fA      16 500 µV/pA
4 50 nV/fA      17 1 mV/nA
5 100 nV/fA     18 2 mV/nA
6 200 nV/fA     19 5 mV/nA
7 500 nV/fA     20 10 mV/nA
8 1 µV/pA       21 20 mV/nA
9 2 µV/pA       22 50 mV/nA
10 5 µV/pA      23 100 mV/nA
11 10 µV/pA     24 200 mV/nA
12 20 µV/pA     25 500 mV/nA
26 1 V/µA
"""
    ser.write(str.encode('SENS?\n'))
    s = ser.read(256);
    print(s)

