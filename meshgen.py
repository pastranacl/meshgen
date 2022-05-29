"""
 This module uses ctypes to wrap the CGAL function Advancing Front Surface reconstruction
 into Python. Returns an oriented triangulation from a set of points.
 
 Cesar L. Pastrana, 2022
"""

import os
import numpy as np
from ctypes import cdll, c_double, c_int, POINTER


def afsr_cgal_lib():
    """
        Loads the C library.
        Returns the getmesh function that calls CGAL and freemem to free the memory of 
        the 1D array after being used
    """
    
    LIB_FOLDER = 'clib'
    LIB_NAME = 'meshgen.so'
    lib_path = os.path.join(os.path.join(os.path.dirname(__file__),LIB_FOLDER), LIB_NAME)
    cesgal_so = cdll.LoadLibrary(lib_path)
    
    getmesh = cesgal_so.get_mesh 
    freemem = cesgal_so.free_ivector
    
    # (ndpointer permits pass/return by reference)
    getmesh.argtypes = [np.ctypeslib.ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS'),
                        c_int,
                        np.ctypeslib.ndpointer(dtype=np.int32, ndim=1, flags='C_CONTIGUOUS')]
    
    getmesh.restype = POINTER(c_int)
 
 
    freemem.argtypes = [POINTER(c_int)]
    freemem.restype = None
    
    return getmesh, freemem



def gentrimesh(r):
    """
        This function is wrapper to obtain a triangulation from a set of vertices
        using CGAL's Advancing Front Surface Reconstruction
        
        Input:  r = Nx3 double numpy array of the N coordinates and x,y,z values in 3D

        Output: tri    = n_tri x 3 numpy array with the triangulation (int)
                n_tri  = Total number of triangles 
    """
    getmesh, freemem = afsr_cgal_lib()
   
    # Converts to 1D array
    nvertices = len(r)
    rflat = np.reshape(r, (nvertices*3) )
    
    # Call the C++ library and retrieve mesh and n_tri
    n_trip = np.zeros((1,), dtype=np.int32)
    triflat = getmesh(rflat, nvertices, n_trip)
    n_tri = n_trip[0]
    
    # Converts 1D tri to 2D numpy array
    tri = np.zeros((n_tri,3), dtype=int)
    for i in range(0,n_tri):
        tri[i,0] = triflat[i*3+0]
        tri[i,1] = triflat[i*3+1]
        tri[i,2] = triflat[i*3+2]

    # Free memory
    freemem(triflat)

    return tri, n_tri




def plot_tri(r, tri):
    """
        Plots the triangulated mesh (just for checks)
        
        Input:  r   =  Nx3 double numpy array of the N coordinates and x,y,z values in 3D
                tri =  n_tri x 3 numpy array with the triangulation (int)
    """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
            
    x=r[:,0]
    y=r[:,1]
    z=r[:,2]
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(x, y, z, triangles=tri, 
                    color=(0.5,0.5,0.5,1.0), 
                    edgecolor=(0.0,0.0,0.0, 1.0),
                    linewidth=0.5,
                    antialiased=True,
                    shade=False)
    plt.show()
    
    

if __name__ == '__main__':
    """
        Example of usage, loading of coordinates from file
    """
    r = np.loadtxt("init_coords.dat", delimiter="\t")
    tri, n_tri = gentrimesh(r)
    plot_tri(r, tri)
    
    
    
