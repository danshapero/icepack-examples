
#include <deal.II/base/function.h>
#include <deal.II/grid/grid_generator.h>

#include <icepack/physics/constants.hpp>
#include <icepack/physics/viscosity.hpp>
#include <icepack/glacier_models/ice_shelf.hpp>

using dealii::Tensor;
using dealii::Point;

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

// Type alias
template <int dim>
using Fn = dealii::ScalarFunctionFromFunctionObject<dim>;


class Velocity : public dealii::TensorFunction<1, 2>
{
public:
  Velocity() {}
  Tensor<1, 2> value(const Point<2>& x) const
  {
    const double q = 1 - pow(1 - delta_h * x[0] / (length * h0), 4);

    Tensor<1, 2> v; v[1] = 0.0;
    v[0] = u0 + 0.25 * A * q * length * pow(h0, 4) / delta_h;

    return v;
  }
};


int main()
{
  // First, we have to generate a mesh which discretizes the underlying
  // geometry. deal.II has a bunch of built-in functions for generating simple
  // meshes which we'll use here.
  dealii::Triangulation<2> mesh;
  const Point<2> p1(0.0, 0.0), p2(length, width);
  dealii::GridGenerator::hyper_rectangle(mesh, p1, p2);

  // Next, we need to mark the right-hand side of the geometry as belonging to
  // a different part of the boundary than the rest -- this is the ice front,
  // which has different boundary conditions.
  for (auto cell: mesh.active_cell_iterators())
    for (unsigned int face_number = 0;
         face_number < dealii::GeometryInfo<2>::faces_per_cell; ++face_number)
      if (cell->face(face_number)->center()(0) > length - 1.0)
        cell->face(face_number)->set_boundary_id(1);

  // Now refine the mesh a few times so that the solution is accurate enough.
  const unsigned int num_levels = 5;
  mesh.refine_global(num_levels);


  // Next we need to make some input data for the problem. The thickness is a
  // linear ramp which thins out towards the ice front.
  const Fn<2> thickness([&](const Point<2>& x)
                        {return h0 - delta_h/length * x[0];});
  const Velocity velocity;

  // To keep things interesting, we'll perturb the ice velocity a bit in the
  // center of the domain.
  const Fn<2> temperature([&](const Point<2>& x)
                          {
                            const bool inside =
                              (x[0] > length/4 && x[0] < 3*length/4 &&
                               x[1] > width/4  && x[1] < 3*width/4);
                            return temp + inside * delta_temp;
                          });

  // Create a model object which knows how to solve the solve the equations of
  // motion for glacier flow.
  icepack::IceShelf ice_shelf(mesh, 1);

  // Interpolate the exact input fields to the finite element basis.
  const Field<2> theta = ice_shelf.interpolate(temperature);
  const Field<2> h = ice_shelf.interpolate(thickness);
  const VectorField<2> u0 = ice_shelf.interpolate(velocity);

  // The model object's diagnostic solve procedure takes in the ice thickness,
  // temperature and an initial guess for the velocity and computes a solution
  // of the shallow shelf equations. The velocity initial guess has to have the
  // right Dirichlet boundary conditions.
  const VectorField<2> u = ice_shelf.diagnostic_solve(h, theta, u0);

  // Write out the finite element fields to file so that we can do some post-
  // processing, visualization, etc.
  u.write("u.ucd", "u");
  u0.write("u0.ucd", "u");

  return 0;
}
