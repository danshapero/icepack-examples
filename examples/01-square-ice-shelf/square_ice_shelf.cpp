// In this example, we'll see how to use the basic functionality of icepack --
// creating a mesh, creating some scalar and vector fields, and solving the
// diagnostic equations for the velocity of an ice shelf.

// This file contains a bunch of import statements, definitions of physical
// constants, etc. -- it's not too relevant, so we've put it in a separate
// file.
#include "data.hpp"

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

  // Now refine the mesh a few times so that our solution will be decently
  // accurate.
  const unsigned int num_levels = 5;
  mesh.refine_global(num_levels);


  // Next we need to make some input data for the problem. The thickness is a
  // linear ramp which thins out towards the ice front.
  const Fn<2> thickness([&](const Point<2>& x)
                        {return h0 - delta_h/length * x[0];});

  // The velocity is defined in the data file -- it's the exact solution of the
  // diagnostic equations with the thickness above and a constant temperature
  // of -10C.
  const Velocity velocity;

  // But to keep things interesting, we'll perturb the temperature a bit in the
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
