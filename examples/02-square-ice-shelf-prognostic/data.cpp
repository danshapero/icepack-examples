
#include "data.hpp"

const double rho = rho_ice * (1 - rho_ice / rho_water);
const double temp = 263.15;
const double delta_temp = -10.0;
const double A = pow(rho * gravity / 4, 3) * icepack::rate_factor(temp);

const double u0 = 100.0;
const double length = 20000.0, width = 20000.0;
const double h0 = 600.0;
const double delta_h = 300.0;


double Thickness::value(const Point<2>& x, const unsigned int) const
{
  return h0 - delta_h / length * x[0];
}

double DhDx::value(const Point<2>&, const unsigned int) const
{
  return -delta_h/length;
}

double Temperature::value(const Point<2>&, const unsigned int) const
{
  return temp;
}

Tensor<1, 2> Velocity::value(const Point<2>& x) const
{
  const double q = 1 - pow(1 - delta_h * x[0] / (length * h0), 4);

  Tensor<1, 2> v;
  v[0] = u0 + 0.25 * A * q * length * pow(h0, 4) / delta_h;
  v[1] = 0.0;

  return v;
}

double DuDx::value(const Point<2>& x, const unsigned int) const
{
  const double q = 1 - delta_h / h0 * x[0] / length;
  return A * pow(h0 * q, 3);
}

Accumulation::Accumulation(Thickness h, DhDx dh_dx, Velocity u, DuDx du_dx)
  : h(h), dh_dx(dh_dx), u(u), du_dx(du_dx)
{}

double Accumulation::value(const Point<2>& x, const unsigned int) const
{
  return h.value(x) * du_dx.value(x) + u.value(x)[0] * dh_dx.value(x);
}
