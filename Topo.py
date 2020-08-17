import numpy as np

print('├── STMpy.Topo: subtractMeanPlane')
print('├── STMpy.Topo: fitPolySheet')
print('├── STMpy.Topo: fillExtremes')

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


# Polynomial sheet fit By Paddy Harrison
def fitPolySheet(z, kx=3, ky=3, order=None):
    '''
    Two dimensional polynomial fitting by least squares.
    Fits the functional form f(x,y) = z.

    Parameters
    ----------

    z: np.ndarray, 2d
        Surface to fit.
    kx, ky: int, default is 3
        Polynomial order in x and y, respectively.
    order: int or None, default is None
        If None, all coefficients up to maxiumum kx, ky, ie. up to and including x^kx*y^ky, are considered.
        If int, coefficients up to a maximum of kx+ky <= order are considered.

    Returns
    -------
    2d array of same size as z, containing the fit to z.

    '''
    
    #make x and y axies the size of the z array.
    x = np.linspace(0,1,num=len(z))
    y = np.linspace(0,1,num=len(z[1]))
    
    # grid coords
    x, y = np.meshgrid(x, y)
    # coefficient array, up to x^kx, y^ky
    coeffs = np.ones((kx+1, ky+1))

    # solve array
    a = np.zeros((coeffs.size, x.size))

    # for each coefficient produce array x^i, y^j
    for index, (j, i) in enumerate(np.ndindex(coeffs.shape)):
        # do not include powers greater than order
        if order is not None and i + j > order:
            arr = np.zeros_like(x)
        else:
            arr = coeffs[i, j] * x**i * y**j
        a[index] = arr.ravel()

    # do leastsq fitting and return matrix of leastsq result
    fit = np.linalg.lstsq(a.T, np.ravel(z), rcond=None)
    return np.polynomial.polynomial.polygrid2d(np.linspace(0,1,num=len(z)),np.linspace(0,1,num=len(z[1])),(fit[0]).reshape(kx+1,ky+1))


def fillExtremes(z, fBot=0.0, fTop=0.0, scale=4): 
    """
    Replace extreme pixels with local averages.
    
    input: z is 2D ndarray of original topography.
        the bottom fBot and the top fTop fractions of pixels are the extremes.
        scale sets the neighborhood, in pixels, around which things are averaged.
    output: 2D ndarray, with all the extremes replaced with local averages.
    """
    matrix = np.copy(z)
    
    xdim,ydim = matrix.shape
    
    #check that fBot and fTop are reasonable
    if fBot<0 or fTop<0 or fBot>=1 or fTop>=1:
        return None
    
    #calculate average and extreme values
    sorts = np.sort(matrix, axis=None)
    
    globalAvg = np.average(sorts)
    print(np.floor(xdim*ydim*fBot))
    zBot = sorts[int(np.floor(xdim*ydim*fBot))]
    zTop = sorts[int(np.ceil(xdim*ydim*(1-fTop)))-1]
    
    #use extreme values to locate all extremes
    extremes = np.zeros((xdim,ydim),dtype=bool) 
    for i in range(xdim):
        for j in range(ydim):
            if not zBot<=matrix[i,j]<=zTop:
                extremes[i,j]=True
    
    #replace all extremes with local average, biased very slightly towards the global average.
    for i in range(xdim):
        for j in range(ydim):
            if extremes[i,j]:
                localSum=globalAvg
                n=1
                #average over a box of size scale, but only inside the image
                for k in range(max(-scale,-i), min(scale+1, xdim-i)):
                    for l in range(max(-scale,-j), min(scale+1, ydim-j)):
                        if not extremes[i+k,j+l]:
                            localSum+=matrix[i+k,j+l]
                            n+=1
                matrix[i,j]=localSum/n
                
    return matrix


""" for later use: print all function in module """
# from inspect import getmembers, isfunction
# if __name__ == "__main__":
#     functions_list = [o[0] for o in getmembers(STMpy.Topo) if isfunction(o[1])]
#     # print('STMpy.dIdV')
#     print(functions_list)

