
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
using icepack::IceShelf;
using icepack::readArcAsciiGrid;

namespace icepack {
  namespace inverse {

    DualField<2> gradient(
      const IceShelf& ice_shelf,
      const Field<2>& h,
      const Field<2>& theta,
      const VectorField<2>& u,
      const VectorField<2>& lambda
    );

  }
}
