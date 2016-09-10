
#include "data.hpp"

// Some physical constants
const double rho = rho_ice * (1 - rho_ice / rho_water);
const double temp = 263.15;
const double delta_temp = 5.0;
const double A = pow(rho * gravity / 4, 3) * icepack::rate_factor(temp);

const double u0 = 100.0;
const double length = 20000.0, width = 20000.0;
const double h0 = 600.0;
const double delta_h = 300.0;


Tensor<1, 2> Velocity::value(const Point<2>& x) const
{
  const double q = 1 - pow(1 - delta_h * x[0] / (length * h0), 4);

  Tensor<1, 2> v; v[1] = 0.0;
  v[0] = u0 + 0.25 * A * q * length * pow(h0, 4) / delta_h;

  return v;
}


double Thickness::value(const Point<2>& x, const unsigned int) const
{
  const double X = x[0] / length;
  return h0 - delta_h * X;
}

double Temperature::value(const Point<2>& x, const unsigned int) const
{
  const double X = x[0] / length;
  const double Y = x[1] / width;
  double q = 0.0;
  if (0.25 < X and X < 0.75 and
      0.25 < Y and Y < 0.75)
    q = 256 * (X - 0.25) * (0.75 - X) * (Y - 0.25) * (0.75 - Y);
  return temp + q * delta_temp;
}

