def find_min_dIdV(filename):
    """
    Input: Filename
    Output: Plot and Value of Minimum of dI/dV
    """

#Minimum of dI/dV can give approxiamte value of Dirac Point in topological insulators
#For example, in https://journals.aps.org/prb/abstract/10.1103/PhysRevB.79.205411
#Python script to plot dI/dV and find minimum
    import numpy as np; import matplotlib.pyplot as plt;
    file_vals=np.loadtxt(filename, skiprows=19); #Loading dI/dV Data
    bias_vals=file_vals[:,0];current_vals=file_vals[:,1];lockin_x_vals=file_vals[:,2];
    plt.plot(1000*bias_vals,lockin_x_vals,'b'); #Plot dI/dV
    plt.title('dI/dV'); plt.xlabel('Bias Voltage (mV)'); plt.ylabel('dI/dV (Arbitrary Units)'); #Plot title, axes labels
    min_ind=np.where(lockin_x_vals==min(lockin_x_vals)); #Finding index of minimum of dI/dV
    bias_min_mV=bias_vals[min_ind[0][0]]*1000; #Bias value of minimum
    print('Minimum of dI/dV is at',bias_min_mV,'mV.')