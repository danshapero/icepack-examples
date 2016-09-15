
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
extern const double rho, temp, delta_temp, A, u0, length, width, h0, delta_h;


class Thickness : public Function<2>
{
public:
  Thickness() = default;
  double value(const Point<2>& x, const unsigned int = 0) const;
};

class DhDx : public Function<2>
{
public:
  DhDx() = default;
  double value(const Point<2>&, const unsigned int = 0) const;
};

class Temperature : public Function<2>
{
public:
  Temperature() = default;
  double value(const Point<2>&, const unsigned int = 0) const;
};

class Velocity : public TensorFunction<1, 2>
{
public:
  Velocity() = default;
  Tensor<1, 2> value(const Point<2>& x) const;
};

class DuDx : public Function<2>
{
public:
  DuDx() = default;
  double value(const Point<2>& x, const unsigned int = 0) const;
};

/**
 * an accumulation field for which the linear ice ramp is a steady state
 */
class Accumulation : public Function<2>
{
public:
  Accumulation(Thickness h, DhDx dh_dx, Velocity u, DuDx du_dx);
  double value(const Point<2>& x, const unsigned int = 0) const;

private:
  Thickness h;
  DhDx dh_dx;
  Velocity u;
  DuDx du_dx;
};
