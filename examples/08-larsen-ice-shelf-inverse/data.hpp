
#include <icepack/read_mesh.hpp>
#include <icepack/grid_data.hpp>
#include <icepack/glacier_models/ice_shelf.hpp>
#include <icepack/numerics/optimization.hpp>
#include <icepack/inverse/error_functionals.hpp>
#include <icepack/inverse/regularization.hpp>
#include <icepack/inverse/ice_shelf.hpp>

using icepack::Field;
using icepack::DualField;
using icepack::VectorField;
using icepack::DualVectorField;
using icepack::readArcAsciiGrid;

namespace numerics = icepack::numerics;
namespace inverse = icepack::inverse;
