cmake_minimum_required(VERSION 3.15)

project(MonteCarloPricer)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Default to an optimized build: without a build type CMake passes no -O flag,
# which makes the engine roughly 4x slower.
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 CONFIG REQUIRED)
find_package(OpenMP REQUIRED)

# Put the built .so into build/python/
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/python)

pybind11_add_module(monte_carlo_pricer
    src/europeanOption.cpp
    bindings/module.cpp
)
target_link_libraries(monte_carlo_pricer PUBLIC OpenMP::OpenMP_CXX)

target_include_directories(monte_carlo_pricer PUBLIC
    ${PROJECT_SOURCE_DIR}/include
)

