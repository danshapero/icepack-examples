
#include "data.hpp"

#include <deal.II/grid/grid_generator.h>
#include <icepack/physics/constants.hpp>

namespace data {

  dealii::Triangulation<2>
  make_rectangular_glacier(const double length, const double width)
  {
    dealii::Triangulation<2> mesh;
    const Point<2> p1(0.0, 0.0), p2(length, width);
    dealii::GridGenerator::hyper_rectangle(mesh, p1, p2);

    for (auto cell: mesh.active_cell_iterators())
      for (unsigned int face_number = 0;
           face_number < dealii::GeometryInfo<2>::faces_per_cell;
           ++face_number)
        if (cell->face(face_number)->center()(0) > length - 1.0)
          cell->face(face_number)->set_boundary_id(1);

    const unsigned int num_refinement_levels = 5;
    mesh.refine_global(num_refinement_levels);

    return mesh;
  }

  Thickness::Thickness(double length, double width, double h0, double dh)
    : length(length), width(width), h0(h0), dh(dh)
  {}

  double Thickness::value(const Point<2>& x, const unsigned int) const
  {
    return h0 - dh / length * x[0];
  }

  Velocity::Velocity(
    double length, double width, double v_in,
    const Thickness& h, const Temperature& theta
  ) : length(length), width(width), v_in(v_in), h(h), theta(theta)
  {}

  using icepack::rho_ice;
  const double rho = rho_ice * (1 - rho_ice / icepack::rho_water);

  Tensor<1, 2> Velocity::value(const Point<2>& x) const
  {
    const double dh =h.dh, h0 = h.h0;
    const double q = 1 - std::pow(1 - dh * x[0] / (length * h0), 4);
    const double A = icepack::rate_factor(theta.T0);
    const double Z = std::pow(rho * icepack::gravity / 4, 3) * A;

    Tensor<1, 2> v({v_in + 0.25 * Z * q * length * pow(h0, 4) / dh, 0.0});
    return v;
  }

  Temperature::Temperature(double length, double width, double T0, double dT)
    : length(length), width(width), T0(T0), dT(dT)
  {}

  double Temperature::value(const Point<2>& x, const unsigned int) const
  {
    const double X = x[0] / length;
    const double Y = x[1] / width;
    const double qx = std::max(0.0, (X - 0.25) * (0.75 - X));
    const double qy = std::max(0.0, (Y - 0.25) * (0.75 - Y));

    return T0 + 256 * qx * qy * dT;
  }

}

