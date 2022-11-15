cmake_minimum_required(VERSION 3.16)

project(wavelet_buffer_benchmark)

find_package(wavelet_buffer REQUIRED)
find_package(Catch2 REQUIRED)

add_executable(benchmark benchmark.cc init.cc)
target_link_libraries(benchmark wavelet_buffer::wavelet_buffer Catch2::Catch2WithMain)
