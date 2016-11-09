
#include "data.hpp"

// In this example, we're going to show some of the guts of the inverse methods
// that we demonstrated in example 3, and we're going to do use real data for
// the Ross Ice Shelf like in example 4.
// Rather than run the optimization algorithm to convergence, this program is
// going to show what goes on inside a single step of that algorithm: picking a
// search direction and performing a line search in that direction.

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

  // Make a guess that the temperature is a constant -15C everywhere.
  const Field<2> theta_guess =
    ice_shelf.interpolate(dealii::ConstantFunction<2>(258.15));

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
  double initial_cost = F(theta_guess);
  std::cout << "Initial cost: " << initial_cost << std::endl;

  // Compute the gradient of the objective functional and a search direction.
  DualField<2> df = dF(theta_guess);
  Field<2> p = -transpose(df);
  const double df_dot_p = inner_product(df, p);

  // We're going to look in the direction $p$ for a better guess for $\theta$,
  // but first we need to decide on how far out to look -- this is what the
  // Armijo rule does.
  const auto f = [&](const double beta){ return F(theta_guess + beta * p); };
  const double beta_max = numerics::armijo(f, df_dot_p, 1.0e-4, 0.5);
  std::cout << "Endpoint of interval for line search: " << beta_max << std::endl;

  // Now we're going to look for the minimum of the objective using
  // [golden section search](https://en.wikipedia.org/wiki/Golden_section_search).
  std::cout << "Finding minimum using line search..." << std::endl;

  const double phi = 0.5 * (std::sqrt(5.0) - 1);
  double a = 0.0, b = beta_max;
  double fa = f(a), fb = f(b);

  // Stop the iteration if the relative difference in errors at the endpoints
  // is small enough.
  while (std::abs(fa - fb)/fb > 1.0e-2) {
    const double L = b - a;
    const double A = a + L * (1 - phi);
    const double B = b - L * (1 - phi);

    // Evaluate the cost function at two points $A$, $B$ in the interior of the
    // interval. We will move one of the endpoints depending on where the
    // minimum lies.
    const double fA = f(A);
    const double fB = f(B);

    // Since $f$ is convex, there are only 4 possible orderings for $f(a)$,
    // $f(A)$, $f(B)$ and $f(b)$; these cases pick out whether the minimum is in
    // $[a, B]$ or in $[A, b]$.
    if (fA >= fB) {
      a = A;
      fa = fA;
    } else {
      b = B;
      fb = fB;
    }
  }

  const double beta = (a + b) / 2;

  Field<2> theta = theta_guess + beta * p;
  theta.write("theta.ucd", "theta");
  std::cout << "Final cost: " << F(theta) << std::endl;

  // Finally, we'd like to be sure that we actually found the minimum. To check
  // our results, generate a bunch of random points to sample in the search
  // interval and write them to a file along with the value obtained from the
  // golden section search.
  std::mt19937 rng;
  rng.seed(std::random_device()());
  std::uniform_real_distribution<double> U(0, beta_max);

  std::cout << "Sampling cost function in search interval..." << std::endl;

  std::ofstream file("costs.txt");
  file << df_dot_p << std::endl;
  file << beta << " " << f(beta) - initial_cost << std::endl;

  for (size_t k = 0; k < 100; ++k) {
    const double beta = U(rng);
    const double cost = f(beta);

    file << beta << " " << cost - initial_cost << std::endl;
  }

  // To see a plot of the values of the cost function that we just computed,
  // run the script `python postprocess.py`.
  return 0;
}
