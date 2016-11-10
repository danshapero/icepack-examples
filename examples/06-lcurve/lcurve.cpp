
#include "data.hpp"

int main(int argc, char ** argv)
{
  const double length = 20e3, width = 20e3;
  dealii::Triangulation<2> mesh = data::make_rectangular_glacier(length, width);

  icepack::IceShelf ice_shelf(mesh, 1);
  const auto& discretization = ice_shelf.get_discretization();

  const double stddev = 10.0;
  const data::Thickness thickness(length, width, 600.0, 300.0);
  const data::Temperature temperature(length, width, 258.15, 7.5);
  const Field<2>
    h = ice_shelf.interpolate(thickness),
    theta_true = ice_shelf.interpolate(temperature),
    sigma = ice_shelf.interpolate(dealii::ConstantFunction<2>(stddev));

  Field<2> theta_guess =
    ice_shelf.interpolate(dealii::ConstantFunction<2>(temperature.T0));

  theta_true.write("theta_true.ucd", "theta");

  const double v_in = 100.0;
  const data::Velocity velocity(length, width, v_in, thickness, temperature);
  const VectorField<2>
    u_guess = ice_shelf.interpolate(velocity),
    u_true = ice_shelf.diagnostic_solve(h, theta_true, u_guess),
    u_obs = data::add_noise(u_true, stddev);

  u_true.write("u_true.ucd", "u");

  const double theta_scale = 10.0;
  double length_scale = 0.0;
  double alpha = length_scale / theta_scale;
  auto regularizer = inverse::SquareGradient<2>(discretization, alpha);

  const auto F =
    [&](const Field<2>& theta) -> double
    {
      const VectorField<2> u = ice_shelf.diagnostic_solve(h, theta, u_guess);
      return inverse::square_error(u, u_obs, sigma) + regularizer(theta);
    };

  const auto dF =
    [&](const Field<2>& theta) -> DualField<2>
    {
      const VectorField<2> u = ice_shelf.diagnostic_solve(h, theta, u_guess);
      const DualVectorField<2> du = inverse::misfit(u, u_obs, sigma);
      const VectorField<2> lambda = ice_shelf.adjoint_solve(h, theta, u, du);
      const DualField<2>
        dE = inverse::gradient(ice_shelf, h, theta, u_obs, lambda),
        dR = regularizer.derivative(theta);
      return dE + dR;
    };

  std::ofstream file("lcurve.txt");

  const double dx = dealii::GridTools::minimal_cell_diameter(mesh);
  const double area = dealii::GridTools::volume(mesh);
  const double tolerance = 5.0e-3;
  for (length_scale = length/2; length_scale > dx; length_scale *= 0.95) {
    alpha = length_scale / theta_scale;
    regularizer = inverse::SquareGradient<2>(discretization, alpha);
    Field<2> theta = icepack::numerics::lbfgs(F, dF, theta_guess, 6, tolerance);
    VectorField<2> u = ice_shelf.diagnostic_solve(h, theta, u_guess);

    file << alpha << " "
         << inverse::square_error(u, u_obs, sigma) / area << " "
         << regularizer(theta) / std::pow(alpha, 2) << std::endl;

    theta_guess = theta;
  }

  return 0;
}
