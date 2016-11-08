
#include <random>

#include <deal.II/grid/grid_generator.h>

#include <icepack/physics/constants.hpp>
#include <icepack/physics/viscosity.hpp>
#include <icepack/numerics/optimization.hpp>
#include <icepack/glacier_models/ice_shelf.hpp>
#include <icepack/inverse/error_functionals.hpp>
#include <icepack/inverse/regularization.hpp>
#include <icepack/inverse/ice_shelf.hpp>

using dealii::Tensor;
using dealii::Point;
using dealii::Function;
using dealii::ConstantFunction;

using icepack::Discretization;
using icepack::FieldType;
using icepack::Field;
using icepack::DualField;
using icepack::VectorField;
using icepack::DualVectorField;
using icepack::rho_ice;
using icepack::rho_water;
using icepack::gravity;

namespace numerics = icepack::numerics;
namespace inverse = icepack::inverse;
using inverse::SquareGradient;

// Some physical constants
extern const double rho, temp, delta_temp, A, u0, length, width, h0, delta_h;


// A synthetic velocity field. This will be the initial guess for the velocity.
// It is the exact solution for the ice velocity when the ice thickness
// is linear and the ice temperature is constant. The true velocities will be
// synthesized by computing the velocity field for a non-constant temperature.
class Velocity : public dealii::TensorFunction<1, 2>
{
public:
  Velocity() = default;
  Tensor<1, 2> value(const Point<2>& x) const;
};


// A synthetic thickness field
class Thickness : public Function<2>
{
public:
  Thickness() = default;
  double value(const Point<2>& x, const unsigned int = 0) const;
};


// A smooth synthetic temperature profile which is parabolic in each direction.
// This temperature is easy to recover for using any regularization method.
class Temperature : public Function<2>
{
public:
  Temperature() = default;
  double value(const Point<2>& x, const unsigned int = 0) const;
};


// Perturb a field with Gaussian noise with standard deviation `sigma`
template <int rank, int dim>
FieldType<rank, dim>
add_noise(const FieldType<rank, dim>& phi, const double sigma)
{
  FieldType<rank, dim> psi(phi);

  std::random_device rd;
  std::mt19937 gen(rd());
  std::normal_distribution<> z(0.0, sigma);

  for (auto& v: psi.get_coefficients())
    v += z(gen);

  return psi;
}

