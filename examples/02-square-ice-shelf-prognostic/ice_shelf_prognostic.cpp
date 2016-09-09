
#include "data.hpp"

// In this example program, we will demonstrate how to use the prognostic solve
// routine when modelling the flow of an ice shelf.
int main()
{
  // Generate a mesh and label the right-hand side as the ice front.
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

  // Create a model object and the exact data, then interpolate the exact data
  // to the finite element basis.
  icepack::IceShelf ice_shelf(mesh, 1);

  Thickness thickness;
  Temperature temperature;
  Velocity velocity;
  Accumulation accumulation(thickness, DhDx(), velocity, DuDx());

  Field<2> h0 = ice_shelf.interpolate(thickness);
  Field<2> theta = ice_shelf.interpolate(temperature);
  Field<2> a = ice_shelf.interpolate(accumulation);
  VectorField<2> u0 = ice_shelf.interpolate(velocity);

  // Now the interesting part!
  // We're going to solve an advection equation which describes how the ice
  // thickness evolves, so we need to pick a timestep. In order for our solution
  // procedure to be numerically stable, we need for the timestep to be
  // sufficiently small; this is called the CFL condition.
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
    // First, update the ice thickness using the prognostic equation:
    // $$\frac{\partial h}{\partial t} + \nabla\cdot hu = \dot a - \dot m$$
    h = ice_shelf.prognostic_solve(dt, h, a, u);

    // Now update the ice velocity for the new thickness.
    u = ice_shelf.diagnostic_solve(h, theta, u);

    // Write out the results to files so we can plot them later.
    h.write("h" + std::to_string(k + 1) + ".ucd", "h");
    u.write("u" + std::to_string(k + 1) + ".ucd", "u");
  }

  return 0;
}
