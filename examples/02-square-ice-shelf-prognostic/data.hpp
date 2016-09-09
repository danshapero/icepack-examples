
#include <iostream>

#include <deal.II/grid/grid_tools.h>
#include <deal.II/grid/grid_generator.h>

#include <icepack/physics/constants.hpp>
#include <icepack/physics/viscosity.hpp>
#include <icepack/glacier_models/ice_shelf.hpp>

using dealii::Tensor;
using dealii::Point;
using dealii::Function;
using dealii::TensorFunction;

using icepack::Field;
using icepack::VectorField;
using icepack::rho_ice;
using icepack::rho_water;
using icepack::gravity;

// Some physical constants
const double rho = rho_ice * (1 - rho_ice / rho_water);
const double temp = 263.15;
const double delta_temp = -10.0;
const double A = pow(rho * gravity / 4, 3) * icepack::rate_factor(temp);

const double u0 = 100.0;
const double length = 20000.0, width = 20000.0;
const double h0 = 600.0;
const double delta_h = 300.0;


class Thickness : public Function<2>
{
public:
  Thickness() {}

  double value(const Point<2>& x, const unsigned int = 0) const
  {
    return h0 - delta_h/length * x[0];
  }
};

class DhDx : public Function<2>
{
public:
  DhDx() {}

  double value(const Point<2>&, const unsigned int = 0) const
  {
    return -delta_h/length;
  }
};

class Temperature : public Function<2>
{
public:
  Temperature() {}

  double value(const Point<2>&, const unsigned int = 0) const
  {
    return temp;
  }
};

class Velocity : public TensorFunction<1, 2>
{
public:
  Velocity() {}

  Tensor<1, 2> value(const Point<2>& x) const
  {
    const double q = 1 - pow(1 - delta_h * x[0] / (length * h0), 4);

    Tensor<1, 2> v;
    v[0] = u0 + 0.25 * A * q * length * pow(h0, 4) / delta_h;
    v[1] = 0.0;

    return v;
  }
};

class DuDx : public Function<2>
{
public:
  DuDx() {}

  double value(const Point<2>& x, const unsigned int = 0) const
  {
    const double q = 1 - delta_h / h0 * x[0] / length;
    return A * pow(h0 * q, 3);
  }
};

/**
 * an accumulation field for which the linear ice ramp is a steady state
 */
class Accumulation : public Function<2>
{
public:
  Accumulation(Thickness h, DhDx dh_dx, Velocity u, DuDx du_dx)
    : h(h), dh_dx(dh_dx), u(u), du_dx(du_dx)
  {}

  double value(const Point<2>& x, const unsigned int = 0) const
  {
    return h.value(x) * du_dx.value(x) + u.value(x)[0] * dh_dx.value(x);
  }

  Thickness h;
  DhDx dh_dx;
  Velocity u;
  DuDx du_dx;
};
