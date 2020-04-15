print('├── STMpy.Spectra: getAverageSpec')

def getAverageSpec(Spec):
    """
    input:  3d numpy array of spectra
    output: 1d numpy array of mean value for each spectra
    
    returns the average value of spectra over plane at different energy
    """
    l = Spec.mean(axis=(0,1)) # take mean value of different (x,y) points
    return l
