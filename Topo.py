import numpy as np

print('├── STMpy.Topo: subtractMeanPlane')

def subtractMeanPlane(matrix): 
    """
    input: 2D nparray of original topography
    output: 2D nparray of topo subtracted backgroud
    """
    xdim,ydim = matrix.shape
    coordMatrix = np.zeros((xdim*ydim,3))
    zVector = np.zeros(xdim*ydim)
    for i in range(xdim):
        for j in range(ydim):
            coordMatrix[i*xdim+j] = [i,j,1]
            zVector[i*xdim+j] = matrix[i,j]
        
    zVector = np.matrix(zVector)
    coordMatrix = np.matrix(coordMatrix)
    planeVector = (coordMatrix.T * coordMatrix).I * coordMatrix.T * zVector.T
    planeMatrix = np.zeros((xdim,ydim)) 

    for i in range(xdim):
        for j in range(ydim): 
            planeMatrix[i,j] = i*planeVector[0]+j*planeVector[1]+planeVector[2]
    
    return(np.subtract(matrix,planeMatrix))


""" for later use: print all function in module """
# from inspect import getmembers, isfunction
# if __name__ == "__main__":
#     functions_list = [o[0] for o in getmembers(STMpy.Topo) if isfunction(o[1])]
#     # print('STMpy.dIdV')
#     print(functions_list)

