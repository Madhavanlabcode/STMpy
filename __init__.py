import numpy as np

# Please add import sentence if you decided to add a new *module*
import STMpy.dIdV
import STMpy.Topo
import STMpy.Spectra
import STMpy.IT
import STMpy.IV
import STMpy.IZ
import STMpy.FunnyCode
import STMpy.Noise

from inspect import getmembers, isfunction


# functions to automatic print functions in modules, need to test

# if __name__ == "__main__":     
# 	functions_list = [o[0] for o in getmembers(STMpy.dIdV) if isfunction(o[1])]
# 	print('STMpy.dIdV')
# 	# print(functions_list)
# 	# functions_list = [o[0] for o in getmembers(STMpy.Spectra) if isfunction(o[1])]
# 	# print('STMpy.dIdV')
# 	# print(functions_list)
