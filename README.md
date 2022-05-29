# MESHGEN

Cesar L. Pastrana, 2022

## Introduction
This Python module uses Ctypes to wrap the Advancing Front Surface Reconstruction algorithm from the C++-based library [CGAL](https://doc.cgal.org/latest/Advancing_front_surface_reconstruction/index.html) to obtain a triangulation from a set of points. The algorithm is valid for both convex and non-convex surfaces , as well as for open and closed surfaces. The resulting triangulation is oriented.

## Calling
Import the module, for instance via `from meshgen import gentrimesh`. Then, for a set of *N* points defining the surface and organised as a numpy array `r` of *N*x3 (with *x, y* and *z* in columns), the triangulation is obtained as:

```
tri, n_tri = gentrimesh(r)```

Here `tri` is an `int` array of `n_tri`x3, where the three columns indicate the indices in `r` defining a triangle.



## Requirements
The libary is included as a Linux-based pre-compiled shared libary `meshgen.so` in the folder `clib`. For other operative systems, the libary can be recompiled using the `Makefile`. Both for compilation and execution, is necessary to have CGAL and its dependencies installed in the system.
