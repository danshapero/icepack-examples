
#include "data.hpp"

// In this example program, we will show how to use inverse methods to estimate
// the temperature of an ice shelf from the velocity and thickness.
int main()
{
  // Generate a mesh.
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

  // Create a model object and the exact data.
  icepack::IceShelf ice_shelf(mesh, 1);

  const double stddev = 10.0;
  const Field<2>
    h = ice_shelf.interpolate(Thickness()),
    theta_guess = ice_shelf.interpolate(ConstantFunction<2>(temp)),
    theta_true = ice_shelf.interpolate(Temperature()),
    sigma = ice_shelf.interpolate(ConstantFunction<2>(stddev));

  const VectorField<2>
    u_guess = ice_shelf.interpolate(Velocity()),
    u_true = ice_shelf.diagnostic_solve(h, theta_true, u_guess),
    u_obs = add_noise(u_true, stddev);

  // Now the interesting part!

  // Create a penalty functional
  // $$R(\theta) = \frac{\alpha^2}{2}\int_\Omega|\nabla\theta|^2dx$$
  // which regularizes the solution.
  const double theta_scale = 10.0;
  const double alpha = length / theta_scale;
  auto regularizer = SquareGradient<2>(ice_shelf.get_discretization());

  // The optimization routines expect to work with functions of a single real
  // variable, so we'll create some lambda functions that project out all the
  // other arguments.

  // First is the objective functional, which is the sum of the misfit with the
  // observed data and the regularization.
  const auto F =
    [&](const Field<2>& theta) -> double
    {
      const VectorField<2> u = ice_shelf.diagnostic_solve(h, theta, u_guess);
      const double
        E = inverse::square_error(u, u_obs, sigma),
        R = std::pow(alpha, 2) * regularizer(theta);
      return E + R;
    };

  // Next, we need the derivative of the objective functional so that we can
  // minimize it using some descent method.
  const auto dF =
    [&](const Field<2>& theta) -> DualField<2>
    {
      const VectorField<2> u = ice_shelf.diagnostic_solve(h, theta, u_guess);
      const DualVectorField<2> du = icepack::inverse::misfit(u, u_obs, sigma);
      const VectorField<2> lambda = ice_shelf.adjoint_solve(h, theta, u, du);
      const DualField<2>
        dE = inverse::gradient(ice_shelf, h, theta, u_obs, lambda),
        dR = std::pow(alpha, 2) * regularizer.derivative(theta);
      return dE + dR;
    };

  // Set a stopping criterion.
  const double tolerance = 1.0e-2;

  // Solve the inverse problem using LBFGS.
  Field<2> theta = numerics::lbfgs(F, dF, theta_guess, 6, tolerance);
  VectorField<2> u = ice_shelf.diagnostic_solve(h, theta, u_guess);

  // Write out the results for postprocessing.
  theta.write("theta.ucd", "theta");
  u.write("u.ucd", "u");

  return 0;
}
