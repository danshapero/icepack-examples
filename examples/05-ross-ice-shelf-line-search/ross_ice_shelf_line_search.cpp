
#include "data.hpp"

// In this example, we're going to show some of the guts of the inverse methods
// that we demonstrated in example 3, and we're going to do use real data for
// the Ross Ice Shelf like in example 4.
// Rather than run the optimization algorithm to convergence, this program is
// going to show what goes on inside a single step of that algorithm: picking a
// search direction and performing a line search in that direction.
// In example 3, I came up with some arbitrary convergence tolerances and
// everything just sort of worked out fine because it was a synthetic problem.
// With real data, the right convergence tolerances aren't always obvious, so
// it's helpful to execute just a single line search to see what a typical error
// magnitude is. You can then plan accordingly when you use BFGS.

int main(int argc, char ** argv)
{
  if (argc < 6) {
    std::cout << "Wrong number of args!" << std::endl;
    return 1;
  }

  // Read in some command-line arguments indicating where to find the mesh and
  // the input data.
  const std::string mesh_filename = argv[1];
  const std::string h_filename = argv[2];
  const std::string vx_filename = argv[3];
  const std::string vy_filename = argv[4];
  const std::string err_filename = argv[5];

  // Read in the mesh from a file.
  dealii::Triangulation<2> tria = icepack::read_gmsh_grid<2>(mesh_filename);

  // Read in the thickness, velocity, and error maps from files.
  const auto h_obs = readArcAsciiGrid(h_filename);
  const auto vx_obs = readArcAsciiGrid(vx_filename);
  const auto vy_obs = readArcAsciiGrid(vy_filename);
  const auto sigma_obs = readArcAsciiGrid(err_filename);

  // Create a model object and interpolate the measured data to the finite
  // element basis.
  IceShelf ice_shelf(tria, 1);

  const Field<2> h = ice_shelf.interpolate(h_obs);
  const VectorField<2> vo = ice_shelf.interpolate(vx_obs, vy_obs);
  const Field<2> sigma = ice_shelf.interpolate(sigma_obs);

  // Make a guess that the temperature is a constant -10C everywhere. In example
  // 4, we saw that this is not a very good guess!
  const Field<2> theta_guess =
    ice_shelf.interpolate(dealii::ConstantFunction<2>(263.15));

  // Solve the diagnostic equations with this temperature as input.
  VectorField<2> v_guess = ice_shelf.diagnostic_solve(h, theta_guess, vo);

  // Make some functions to pass to the optimization routines; this is just like
  // in example 3.
  const auto F =
    [&](const Field<2>& theta) -> double
    {
      VectorField<2> v = ice_shelf.diagnostic_solve(h, theta, v_guess);
      return icepack::inverse::square_error(v, vo, sigma);
    };

  const auto dF =
    [&](const Field<2>& theta) -> DualField<2>
    {
      const VectorField<2> v = ice_shelf.diagnostic_solve(h, theta, v_guess);
      const DualVectorField<2> dv = icepack::inverse::misfit(v, vo, sigma);
      const VectorField<2> lambda = ice_shelf.adjoint_solve(h, theta, v, dv);
      return icepack::inverse::gradient(ice_shelf, h, theta, v, lambda);
    };


  // Compute the value of the objective functional for our initial guess.
  Field<2> theta(theta_guess);
  double cost = F(theta);

  std::cout << "Initial cost:" << cost << std::endl;

  // Compute the gradient of the objective functional, and a search direction.
  DualField<2> df = dF(theta);
  Field<2> p = -transpose(df);

  std::cout << norm(p)/norm(theta) << std::endl;

  std::cout << "Cost of nearby value: " << F(theta + 0.25 * p) - cost << std::endl;
  p.write("p.ucd", "p");

  const auto f = [&](const double beta){ return F(theta_guess + beta * p); };

  const double beta_max =
    icepack::numerics::armijo(f, inner_product(df, p), 1.0e-4, 0.5);
  std::cout << beta_max << std::endl;

  return 0;
}
