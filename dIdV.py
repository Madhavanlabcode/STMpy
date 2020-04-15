import numpy as np
import matplotlib.pyplot as plt

print('├── STMpy.dIdV: getLinecut,plotLinecut,Linecut')


def getLinecut(dIdV,x1,y1,x2,y2,num):
    """
    input: 
        dIdV:  3d numpy array dIdV map
        x1,y1: start point
        x2,y2: stop point
        num:   number of spectra 
    return:
        lincut of 2D numpy array
        
    gives spectra linecut from (x1,y1) to (x2,y2) with num points
    """
    N = dIdV.shape[2]
    l = np.zeros((num,N))

    lx = np.linspace(x1,x2,num)
    ly = np.linspace(y1,y2,num)    
    
    for i in range(num):
        l[i,:] = dIdV[int(lx[i]),int(ly[i]),:]
    return l


def plotLinecut(linecut,bias,offset):

    """
    input:
        linecut: linecut of dIdV map
        bias(in mV): grid_map.signals.get("sweep_signal")*1000 
        offset: offset between diffrent energy when ploting linecut
    return:
        N/A
    plot the linecut from dIdV.getLinecut()
    """

    N = linecut.shape[0]
    for i in range(N):
        plt.plot(bias,linecut[i,:]+offset*i)
        
    plt.xlabel("Bias (mV)",size=15)
    plt.ylabel("dI/dV",size=15)
    plt.title('Line cut',size=15)
    plt.tight_layout()
    plt.show()


def gridLinecut(grid,x1,y1,x2,y2,num,offset):
    """
    input: grid map read from 3ds file
    return and plot linecut with more detail
    """
    lockin=grid.signals.get("Lockin X (V)")
    linecut = getLinecut(lockin,x1,y1,x2,y2,num)
    bias = grid.signals.get("sweep_signal")*1000 

    N = linecut.shape[0]
    for i in range(N):
        plt.plot(bias,linecut[i,:]+offset*i)
        
    plt.xlabel("Bias (mV)",size=15)
    plt.ylabel("dI/dV",size=15)
    plt.title('Line cut from (%d,%d) to (%d,%d), num = %d' % (x1,y1,x2,y2,num),size=15)
    plt.tight_layout()
    plt.show()
    return linecut
