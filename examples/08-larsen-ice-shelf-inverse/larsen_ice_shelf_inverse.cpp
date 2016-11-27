
#include "data.hpp"

int main(int argc, char ** argv)
{
   // --------------------
  // Initialize everything

  if (argc < 6) {
    std::cout << "Wrong number of args!" << std::endl;
    return 1;
  }

  const std::string mesh_filename = argv[1];
  const std::string h_filename = argv[2];
  const std::string vx_filename = argv[3];
  const std::string vy_filename = argv[4];
  const std::string err_filename = argv[5];

  dealii::Triangulation<2> tria = icepack::read_gmsh_grid<2>(mesh_filename);
  tria.refine_global(1);

  const auto h_obs = readArcAsciiGrid(h_filename);
  const auto vx_obs = readArcAsciiGrid(vx_filename);
  const auto vy_obs = readArcAsciiGrid(vy_filename);
  const auto sigma_obs = readArcAsciiGrid(err_filename);

  icepack::IceShelf ice_shelf(tria, 1);

  const Field<2> h = ice_shelf.interpolate(h_obs);
  const VectorField<2> vo = ice_shelf.interpolate(vx_obs, vy_obs);
  const Field<2> sigma = ice_shelf.interpolate(sigma_obs);

  Field<2> theta_guess =
    ice_shelf.interpolate(dealii::ConstantFunction<2>(265.85));
  VectorField<2> v_guess =
    ice_shelf.diagnostic_solve(h, theta_guess, vo);

  vo.write("vo.ucd", "v");


   // ----------------------
  // Make some length scales

  const double Theta = 20.0;
  const double length = dealii::GridTools::diameter(tria);
  const double dx = dealii::GridTools::minimal_cell_diameter(tria);
  const double area = dealii::GridTools::volume(tria);
  double alpha = 0.0;


   // ------------------
  // Make some functions

  const auto regularizer =
    inverse::SquareGradient<2>(ice_shelf.get_discretization());
  // TODO: make this a conditional when we make TV an option
  const unsigned int p = 2;

  const auto F =
    [&](const Field<2>& theta) -> double
    {
      VectorField<2> v = ice_shelf.diagnostic_solve(h, theta, v_guess);
      const double
        E = inverse::square_error(v, vo, sigma),
        R = std::pow(alpha, p) * regularizer(theta);
      return E + R;
    };

  const auto dF =
    [&](const Field<2>& theta) -> DualField<2>
    {
      const VectorField<2> v = ice_shelf.diagnostic_solve(h, theta, v_guess);
      const DualVectorField<2> dv = inverse::misfit(v, vo, sigma);
      const VectorField<2> lambda = ice_shelf.adjoint_solve(h, theta, v, dv);
      const DualField<2>
        dE = inverse::gradient(ice_shelf, h, theta, vo, lambda),
        dR = std::pow(alpha, p) * regularizer.derivative(theta);
      return dE + dR;
    };


   // -------------------------
  // Solve the inverse problem!

  std::ofstream file("lcurve.txt");

  const double tolerance = 1.0e-2;
  for (double L = 4 * dx; L < length / 8; L *= 1.05) {
    alpha = L / Theta;
    Field<2> theta = icepack::numerics::lbfgs(F, dF, theta_guess, 6, tolerance);
    VectorField<2> v = ice_shelf.diagnostic_solve(h, theta, v_guess);

    v.write("v_" + std::to_string(L) + ".ucd", "v");
    theta.write("theta_" + std::to_string(L) + ".ucd", "theta");

    file << L << " "
         << inverse::square_error(v, vo, sigma) / area << " "
         << regularizer(theta) << std::endl;

    //TODO: make this work -- possibly by updating `v_guess`.
    //theta_guess = theta;
  }

  return 0;
}
