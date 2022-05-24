#ifndef MESHGEN
#define MESHGEN

#include <algorithm>
#include <CGAL/Simple_cartesian.h>
#include <CGAL/Advancing_front_surface_reconstruction.h>
#include <CGAL/tuple.h>



typedef CGAL::Simple_cartesian<double> K;
typedef K::Point_3  Point_3;
typedef CGAL::cpp11::array<std::size_t,3> Facet;


struct Perimeter {

  double bound;

  Perimeter(double bound)
    : bound(bound)
  {}

  template <typename AdvancingFront, typename Cell_handle>
  double operator() (const AdvancingFront& adv, Cell_handle& c,
                     const int& index) const
  {
    // bound == 0 is better than bound < infinity
    // as it avoids the distance computations
    if(bound == 0){
      return adv.smallest_radius_delaunay_sphere (c, index);
    }

    // If perimeter > bound, return infinity so that facet is not used
    double d  = 0;
    d = sqrt(squared_distance(c->vertex((index+1)%4)->point(),
                              c->vertex((index+2)%4)->point()));
    if(d>bound) return adv.infinity();
    d += sqrt(squared_distance(c->vertex((index+2)%4)->point(),
                               c->vertex((index+3)%4)->point()));
    if(d>bound) return adv.infinity();
    d += sqrt(squared_distance(c->vertex((index+1)%4)->point(),
                               c->vertex((index+3)%4)->point()));
    if(d>bound) return adv.infinity();

    // Otherwise, return usual priority value: smallest radius of
    // delaunay sphere
    return adv.smallest_radius_delaunay_sphere (c, index);
  }
};



extern "C" int *get_mesh(double *rvec, int np, int *ntrip);
std::vector<Facet> meshgen(std::vector<Point_3> r);

int *ivector(int M);
extern "C" void free_ivector(int *v);


#endif
