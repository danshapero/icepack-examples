
#include <random>

#include <icepack/numerics/optimization.hpp>
#include <icepack/glacier_models/ice_shelf.hpp>
#include <icepack/inverse/error_functionals.hpp>
#include <icepack/inverse/regularization.hpp>
#include <icepack/inverse/ice_shelf.hpp>

using dealii::Point;
using dealii::Tensor;

using icepack::Field;
using icepack::DualField;
using icepack::VectorField;
using icepack::DualVectorField;
using icepack::FieldType;

namespace inverse = icepack::inverse;

namespace data {

  dealii::Triangulation<2> make_rectangular_glacier(double length, double width);

  class Thickness : public dealii::Function<2>
  {
  public:
    Thickness(double length, double width, double h0 = 600, double dh = 300);
    double value(const Point<2>& x, unsigned int = 0) const;

    const double length, width, h0, dh;
  };

  class Temperature : public dealii::Function<2>
  {
  public:
    Temperature(double length, double width, double T0 = 258, double dT = 3);
    double value(const Point<2>& x, unsigned int = 0) const;

    const double length, width, T0, dT;
  };

  class Velocity : public dealii::TensorFunction<1, 2>
  {
  public:
    Velocity(
      double length, double width, double v_in,
      const Thickness& h, const Temperature& theta
    );
    Tensor<1, 2> value(const Point<2>& x) const;

    const double length, width, v_in;
    const Thickness& h;
    const Temperature& theta;
  };

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


}
