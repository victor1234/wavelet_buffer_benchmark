// Copyright 2020-2022 PANDA GmbH

#include <wavelet_buffer/wavelet.h>
#include <wavelet_buffer/primitives.h>
#include <wavelet_buffer/wavelet_buffer.h>
#include <wavelet_buffer/wavelet_parameters.h>
#include <wavelet_buffer/wavelet_utils.h>
#include <wavelet_buffer/denoise_algorithms.h>

#include <fstream>

#include <catch2/benchmark/catch_benchmark_all.hpp>
#include <catch2/catch_test_macros.hpp>
#include <catch2/generators/catch_generators_all.hpp>

#include "init.h"

using drift::DataType;
using drift::Signal1D;
using drift::SignalN2D;
using drift::WaveletBuffer;
using drift::wavelet::DaubechiesMat;
using drift::wavelet::dbwavf;
using drift::wavelet::Orthfilt;
using drift::utils::GetRandomSignal;

TEST_CASE("Wavelet algorithms benchmark 1D") {
  using drift::NullDenoiseAlgorithm;

  auto k = GENERATE(0.1, 1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50);

  const auto length = static_cast<size_t>(k * 48000);

  drift::WaveletParameters parameters = {
      .signal_shape = {length},
      .signal_number = 1,
      .decomposition_steps = 9,
      .wavelet_type = drift::WaveletTypes::kDB3};

  auto data_src = GetRandomSignal(length);

  WaveletBuffer buffer(parameters);
  BENCHMARK("Decompose " + std::to_string(length)) {
    buffer.Decompose(data_src, NullDenoiseAlgorithm<DataType>());
  };

}

TEST_CASE("Wavelet algorithms benchmark 2D") {
  using drift::NullDenoiseAlgorithm;
  using drift::SimpleDenoiseAlgorithm;

  const long s =
      GENERATE(200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000);

  drift::WaveletParameters parameters = {
      .signal_shape = {static_cast<unsigned long>(s),
                       static_cast<unsigned long>(s)},
      .signal_number = 1,
      .decomposition_steps = 4,
      .wavelet_type = drift::WaveletTypes::kDB3};

  auto data_src = GetRandomSignal(s, s);

  parameters.wavelet_type = drift::kDB3;
  WaveletBuffer buffer(parameters);

  BENCHMARK("Decompose s") {
    buffer.Decompose(data_src, NullDenoiseAlgorithm<DataType>());
  };
}
