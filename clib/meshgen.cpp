/************************************************************************
  
    meshgen. This library uses CGAL's advancing front surface reconstruction
             from a 1d-based array to interface with Python.
            
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
    
************************************************************************/

#include "meshgen.hpp"


extern "C" int *get_mesh(double *rvec, int np, int *ntrip)
{
    // 1. Convert from 1D array to 2D array of coordinates for CGAL
    std::vector<Point_3> rarr(np);
    for(int i=0; i<np; i++) {
        double x,y,z;
        x = rvec[i*3 + 0];
        y = rvec[i*3 + 1];
        z = rvec[i*3 + 2];
        rarr[i] = Point_3(x,y,z);
    }
    

    //-------------------------------------------------------------
    
    // 2. Triangulation +++++++++++++++++++++++++++++++++++++++++++
    std::vector<Facet> facets;
    facets = meshgen(rarr);
    int n_tri = facets.size();
    
    
    //-------------------------------------------------------------
    
    // 3. Check if the volume is positive and correct it ++++++++++++++
    // 3.1 Calculate the volume
    
    double V = 0;
    #pragma omp parallel for reduction(+:V)
    for(int t = 0; t< n_tri; t++) {
        int v1,v2,v3;
        v1 = facets[t][0];
        v2 = facets[t][1];
        v3 = facets[t][2];
        V += ( rarr[v1].x()*( rarr[v2].y()*rarr[v3].z() - rarr[v3].y()*rarr[v2].z() ) + 
               rarr[v2].x()*( rarr[v3].y()*rarr[v1].z() - rarr[v1].y()*rarr[v3].z() ) + 
               rarr[v3].x()*( rarr[v1].y()*rarr[v2].z() - rarr[v2].y()*rarr[v1].z() ) );
    }
    V /= 6;
    
    // 3.2 Reorient the normal vectors to have positive volumes
    if(V<0){
        #pragma omp parallel for
        for(int t=0; t < n_tri; t++) {
            facets[t][1] = facets[t][1] + facets[t][2];
            facets[t][2] = facets[t][1] - facets[t][2];
            facets[t][1] = facets[t][1] - facets[t][2];
        }
    }
    
    //-------------------------------------------------------------

    // 4.  Converts 2D array triangulation to 1D array +++++++++++++++++++
    
    int *tri;
    tri = ivector(3*n_tri);
    for(int t=0; t<n_tri; t++) {
        tri[t*3 + 0] = facets[t][0];
        tri[t*3 + 1] = facets[t][1];
        tri[t*3 + 2] = facets[t][2];
    }
    //----------------------------------------------------------------
    
    *ntrip = n_tri;
    
    return tri;
}




/**************************************************************************/
/*                              meshgen                                   */
/*              This function returns the triaungulation                  */ 
/**************************************************************************/
std::vector<Facet> meshgen(std::vector<Point_3> r)
{
    double per = 0;
    std::vector<Facet> facets;
    Perimeter perimeter(per);
    CGAL::advancing_front_surface_reconstruction(r.begin(),
                                                 r.end(),
                                                 std::back_inserter(facets),
                                                 perimeter);
    return facets;
}



/**********************************************************************/
/*                               ivector                              */
/*  Allocate a int VE with subscript range   v[0...nc]                */                                                                 
/*                                                                    */
/**********************************************************************/
int *ivector(int M)
{
    int *v = new int [M];
    return v;
}



/************************************************************************/
/*                           free_ivector                               */
/* Free the memory of the vector allocated with dvector                 */
/************************************************************************/
extern "C" void free_ivector(int *v)
{
    delete[] v;
}
