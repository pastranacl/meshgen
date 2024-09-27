"""

    meshgen: This module uses ctypes to wrap the CGAL function
             Advancing Front Surface Reconstruction into Python, returning
             an oriented triangulation from a set of points IN R^3.
 
    Copyright (C) 2022,  Cesar L. Pastrana
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
"""

import os
import numpy as np
from ctypes import cdll, c_double, c_int, POINTER




def gentrimesh(r):
    """
        This function is wrapper to obtain a triangulation from a set of vertices
        using CGAL's Advancing Front Surface Reconstruction
        
        Input:  r = Nx3 double numpy array of the N coordinates and x,y,z values in 3D

        Output: tri    = n_tri x 3 numpy array with the triangulation (int)
                n_tri  = Total number of triangles 
    """

    def _afsr_cgal_lib():
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


    getmesh, freemem = _afsr_cgal_lib()
   
    # Transform the coordinates in 2D to a 1D array (a requirement for the C-library)
    nvertices = len(r)
    rflat = np.reshape(r, (3*nvertices) )
    
    # Call the C++ library and retrieve mesh and n_tri
    n_trip = np.zeros((1,), dtype=np.int32)
    triflat = getmesh(rflat, nvertices, n_trip)
    n_tri = n_trip[0]
    

    # Convert the triangulated 1D array to 2D numpy array ++++
    # i. First the 1d triflat array is converted to a numpy array
    triflat_np = np.ctypeslib.as_array(triflat, shape=(3*n_tri,))

    # ii. Reshape tri from 1D -> 2D (np.reshape not working)
    tri = np.zeros((n_tri,3), dtype=int)
    tri[:,0] = triflat_np[0::3]
    tri[:,1] = triflat_np[1::3]
    tri[:,2] = triflat_np[2::3]


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

    shapes = {
                "sphere": "./examples/sphere.dat",
                "torus": "./examples/torus.dat",
                "spherocylinder": "./examples/spherocylinder.dat",
                "icosahedron": "./examples/icosahedron.dat"
            }

    r = np.loadtxt(shapes['icosahedron'], delimiter="\t")

    tri, n_tri = gentrimesh(r)
    plot_tri(r, tri)
    
    
    
