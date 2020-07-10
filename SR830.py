from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

import os.path
import sys
import array
import time
import serial

import matplotlib.pyplot as plt
import numpy as np

def setVol(ser,n):
    """
    input: 
        n:the modulation voltage in Volte
    output: 
        the modulation voltage after re-setting
    set the modulation voltage to n and return voltage at present
    """
    st='SLVL'+str(n)+'\n'
    ser.write(str.encode(st))
    ser.write(str.encode('SLVL?\n'))#return the modulation voltage after re-setting
    s = ser.read(256);
    return s

def cmdser(ser,cmd):
    """
    input:
        ser: your serial
        cmd: strings of command
            '*IDN?'= Queries the device identification
            'OUTP?1' = Queries the value of X (CH1)
            for other command, refer: http://users.df.uba.ar/dgrosz/material%20adicional/manual%20lock-in%20SR830.pdf from page 85.
    output:
        natural return
    giving command to SR830
    """
    print('Sending:', cmd)
    ser.write(str.encode(cmd+'\n'))#read output in channel 1
    s = ser.read(256);
    if len(s) > 0:
        print(s)


def Volbar(s):
    interact(setVol,s=fixed(ser),Vol=widgets.IntSlider(min=-30, max=30, step=1, value=0))

def plotOut(ser,timeout=0.3):
    o1=[]
    o2=[]
    while(True):
        a1 = cmdser(ser,'OUTP?1')
        a2 = cmdser(ser,'OUTP?2')
        a1.decode();
        a2.decode();
        b1 = float(a1[0:4]);
        b2 = float(a2[0:4]);
        
        o1.append(b1);
        o2.append(b2);

        # Limit o1 and o2 lists to 30 items
        o1=o1[-30:]
        o2=o2[-30:]
        
        plt.cla();
        plt.plot(o1,lable='Out1');
        plt.plot(o2,lable='Out2');
        plt.legend()
        time.sleep(timeout)
        plt.show()

def readOut1(ser,timeout=0.3):
    while True:
        a1 = cmdser(ser,'OUTP?1');
        print("\r"+"Out1="+o1,end="");
        time.sleep(timeout)

def readOut2(ser,timeout=0.3):
    while True:
        a2 = cmdser(ser,'OUTP?2');
        print("\r"+"Out2="+o1,end="");
        time.sleep(timeout)


from multiprocessing import Process

def runInParallel(*fns):
  proc = []
  for fn in fns:
    p = Process(target=fn)
    p.start()
    proc.append(p)
  for p in proc:
    p.join()

def guiAll(Port,timeout=0.3):
    """
    input:
        Port: string, Port number.
    use ser.close() after calling this function
    """
    ser = serial.Serial(Port, 9600, timeout=1)
    t = timeout;
    runInParallel(Volbar(ser),readOut1(ser,t),readOut2(ser,t),plotOut(ser,t))