# Meshgen

Meshgen is Python module using Ctypes to wrap the Advancing Front Surface Reconstruction algorithm (AFSR) from the C++-based library [CGAL](https://doc.cgal.org/latest/Advancing_front_surface_reconstruction/index.html). AFSR permits to obtain a triangulated surface from a 3D set of points as a Numpy array. The algorithm is valid for both convex and non-convex surfaces, as well as for open and closed surfaces. Importantly, the resulting triangulation is oriented.
Cesar L. Pastrana, 2022


## Installation

The only non-vanilla Python module required by Meshgen is Numpy. Matplotlib is used for ploting the surface, but is not strictly necessary.

The C++ libary is included as a Linux-based pre-compiled shared libary `meshgen.so` in the folder `clib`. For other Unix-based operative systems, the library can be recompiled using the `Makefile` included by simply runing `make`. MinGW can be used in Windows.

It is necessary, both for compilation and execution of the module, to have CGAL and its dependencies installed on the system.


## Function calling and Execution
First import the module, for instance via `from meshgen import gentrimesh`.

For a set of $N$ points defining the surface and organised as a numpy array `r` of $N\times 3 (with $x, y$ and $z$ in columns), the triangulation is obtained as:

```
tri, n_tri = gentrimesh(r)
```

Here `tri` is an `int` array of `n_tri`x3, where the three columns indicate the indices in `r` defining a triangle. Example files for different shapes are provided, and the main function of the module shows the usage.

The AFSR takes benefict of OMP parallelisation. Then, it is convenient to specify in the terminal the desired number of threads to use: `export OMP_NUM_THREADS=12` will use 12 threads.





