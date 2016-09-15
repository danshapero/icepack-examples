
#include <iostream>

#include <icepack/read_mesh.hpp>
#include <icepack/grid_data.hpp>
#include <icepack/glacier_models/ice_shelf.hpp>

using icepack::Field;
using icepack::VectorField;
using icepack::DualVectorField;
using icepack::IceShelf;
using icepack::readArcAsciiGrid;


int main(int argc, char ** argv)
{
  // Read in some command-line arguments indicating where to find the mesh and
  // the input data.
  const std::string mesh_filename = argv[1];
  const std::string h_filename = argv[2];
  const std::string vx_filename = argv[3];
  const std::string vy_filename = argv[4];

  // Read in the mesh from a file.
  dealii::Triangulation<2> tria = icepack::read_gmsh_grid<2>(mesh_filename);

  // Read in the thickness and velocity data from files.
  const auto h_obs = readArcAsciiGrid(h_filename);
  const auto vx_obs = readArcAsciiGrid(vx_filename);
  const auto vy_obs = readArcAsciiGrid(vy_filename);

  // Create a model object and interpolate the measured data to the finite
  // element basis.
  IceShelf ice_shelf(tria, 1);

  const Field<2> h = ice_shelf.interpolate(h_obs);
  const VectorField<2> vo = ice_shelf.interpolate(vx_obs, vy_obs);

  // Make a guess that the temperature is a constant -10C everywhere, and
  // compute what the residual is for this temperature.
  const Field<2> theta =
      ice_shelf.interpolate(dealii::ConstantFunction<2>(263.15));
  const DualVectorField<2> tau_d = ice_shelf.driving_stress(h);
  const DualVectorField<2> r = ice_shelf.residual(h, theta, vo, tau_d);

  std::cout << "Initial residual: " << norm(r) << std::endl;

  // Solve the diagnostic equations for the ice velocity we would get with this
  // temperature.
  const VectorField<2> v = ice_shelf.diagnostic_solve(h, theta, vo);

  // Write out the results to a file.
  v.write("v.ucd", "v");
  vo.write("vo.ucd", "v");

  return 0;
}
