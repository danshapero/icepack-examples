
#include <iostream>

#include <deal.II/grid/grid_tools.h>
#include <deal.II/grid/grid_generator.h>

#include <icepack/physics/constants.hpp>
#include <icepack/physics/viscosity.hpp>
#include <icepack/glacier_models/ice_shelf.hpp>

using dealii::Tensor;
using dealii::Point;
using dealii::Function;
using dealii::TensorFunction;

using icepack::Field;
using icepack::VectorField;
using icepack::rho_ice;
using icepack::rho_water;
using icepack::gravity;

// Some physical constants
const double rho = rho_ice * (1 - rho_ice / rho_water);
const double temp = 263.15;
const double delta_temp = -10.0;
const double A = pow(rho * gravity / 4, 3) * icepack::rate_factor(temp);

const double u0 = 100.0;
const double length = 20000.0, width = 20000.0;
const double h0 = 600.0;
const double delta_h = 300.0;


class Thickness : public Function<2>
{
public:
  Thickness() {}

  double value(const Point<2>& x, const unsigned int = 0) const
  {
    return h0 - delta_h/length * x[0];
  }
} thickness;

class DhDx : public Function<2>
{
public:
  DhDx() {}

  double value(const Point<2>&, const unsigned int = 0) const
  {
    return -delta_h/length;
  }
} dh_dx;

class Temperature : public Function<2>
{
public:
  Temperature() {}

  double value(const Point<2>&, const unsigned int = 0) const
  {
    return temp;
  }
} temperature;

class Velocity : public TensorFunction<1, 2>
{
public:
  Velocity() {}

  Tensor<1, 2> value(const Point<2>& x) const
  {
    const double q = 1 - pow(1 - delta_h * x[0] / (length * h0), 4);

    Tensor<1, 2> v;
    v[0] = u0 + 0.25 * A * q * length * pow(h0, 4) / delta_h;
    v[1] = 0.0;

    return v;
  }
} velocity;

class DuDx : public Function<2>
{
public:
  DuDx() {}

  double value(const Point<2>& x, const unsigned int = 0) const
  {
    const double q = 1 - delta_h / h0 * x[0] / length;
    return A * pow(h0 * q, 3);
  }
} du_dx;

/**
 * an accumulation field for which the linear ice ramp is a steady state
 */
class Accumulation : public Function<2>
{
public:
  Accumulation() {}

  double value(const Point<2>& x, const unsigned int = 0) const
  {
    return thickness.value(x) * du_dx.value(x)
      + velocity.value(x)[0] * dh_dx.value(x);
  }
} accumulation;


int main()
{
  // This is the same as the last step -- generate a mesh, label the right-hand
  // side of the mesh to get the ice front boundary conditions right, then
  // refine to get the resolution right.
  dealii::Triangulation<2> mesh;
  const Point<2> p1(0.0, 0.0), p2(length, width);
  dealii::GridGenerator::hyper_rectangle(mesh, p1, p2);

  for (auto cell: mesh.active_cell_iterators())
    for (unsigned int face_number = 0;
         face_number < dealii::GeometryInfo<2>::faces_per_cell; ++face_number)
      if (cell->face(face_number)->center()(0) > length - 1.0)
        cell->face(face_number)->set_boundary_id(1);

  const unsigned int num_levels = 5;
  mesh.refine_global(num_levels);

  // Same setup as the last step -- create a model object and interpolate the
  // input data to the finite element representation.
  icepack::IceShelf ice_shelf(mesh, 1);

  Field<2> h0 = ice_shelf.interpolate(thickness);
  Field<2> theta = ice_shelf.interpolate(temperature);
  Field<2> a = ice_shelf.interpolate(accumulation);
  VectorField<2> u0 = ice_shelf.interpolate(velocity);

  // We're going to solve an advection equation which describes how the ice
  // thickness evolves, and in order to do so we need to pick a timestep. In
  // order for our solution procedure to be numerically stable, we need for the
  // timestep to be sufficiently small; this is called the CFL condition.
  const double dx = dealii::GridTools::minimal_cell_diameter(mesh);
  const double max_speed = velocity.value(Point<2>(width/2, length - 0.25))[0];
  const double dt = 0.25 * dx / max_speed;

  std::cout << "Timestep: " << dt << " years." << std::endl;

  // Initialize the ice thickness and velocity, then propagate these fields
  // forward in time.
  Field<2> h(h0);
  VectorField<2> u = ice_shelf.diagnostic_solve(h, theta, u0);

  h.write("h0.ucd", "h");
  u.write("u0.ucd", "u");

  a.write("a.ucd", "a");
  Field<2> dh_dt = ice_shelf.dh_dt(h, a, u);
  dh_dt.write("dh_dt.ucd", "dh_dt");

  for (size_t k = 0; k < 32; ++k) {
    h = ice_shelf.prognostic_solve(dt, h, a, u);
    u = ice_shelf.diagnostic_solve(h, theta, u);

    // Write out the results to files so we can plot them later.
    h.write("h" + std::to_string(k + 1) + ".ucd", "h");
    u.write("u" + std::to_string(k + 1) + ".ucd", "u");
  }

  return 0;
}
