cmake_minimum_required(VERSION 3.20)
project(EnhanceX VERSION 2.0.0 LANGUAGES CXX C)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Build options
option(ENHANCEX_BUILD_TESTS "Build C++ unit tests" ON)
option(ENHANCEX_BUILD_EXAMPLES "Build C++ example applications" ON)
option(ENHANCEX_BUILD_BINDINGS "Build Python bindings via Pybind11" ON)
option(ENHANCEX_BUILD_CUDA "Enable CUDA Acceleration" OFF)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/cpp/include
)

# Core C++ Sources
file(GLOB_RECURSE ENHANCEX_SOURCES
    "cpp/src/core/*.cpp"
    "cpp/src/image/*.cpp"
    "cpp/src/video/*.cpp"
    "cpp/src/ai/*.cpp"
    "cpp/src/gpu/*.cpp"
)

# CUDA Support
if(ENHANCEX_BUILD_CUDA)
    enable_language(CUDA)
    find_package(CUDAToolkit REQUIRED)
    file(GLOB_RECURSE ENHANCEX_CUDA_SOURCES "cpp/src/gpu/*.cu")
    list(APPEND ENHANCEX_SOURCES ${ENHANCEX_CUDA_SOURCES})
    add_compile_definitions(ENHANCEX_ENABLE_CUDA=1)
endif()

# Build Shared Library
add_library(enhancex_cpp SHARED ${ENHANCEX_SOURCES})
target_include_directories(enhancex_cpp PUBLIC 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/cpp/include>
    $<INSTALL_INTERFACE:include>
)

# Build Static Library
add_library(enhancex_cpp_static STATIC ${ENHANCEX_SOURCES})
target_include_directories(enhancex_cpp_static PUBLIC 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/cpp/include>
    $<INSTALL_INTERFACE:include>
)

# Link Dependencies
find_package(OpenCV REQUIRED)
target_link_libraries(enhancex_cpp PRIVATE ${OpenCV_LIBS})
target_link_libraries(enhancex_cpp_static PRIVATE ${OpenCV_LIBS})

if(ENHANCEX_BUILD_CUDA)
    target_link_libraries(enhancex_cpp PRIVATE CUDA::cudart)
    target_link_libraries(enhancex_cpp_static PRIVATE CUDA::cudart)
endif()

# Build Pybind11 Bindings if enabled
if(ENHANCEX_BUILD_BINDINGS)
    find_package(pybind11 CONFIG QUIET)
    if(pybind11_FOUND)
        pybind11_add_module(enhancex_bindings cpp/bindings/pybind_module.cpp)
        target_link_libraries(enhancex_bindings PRIVATE enhancex_cpp)
    else()
        message(STATUS "Pybind11 not found; skipping binary C++ module creation.")
    endif()
endif()

# Installation rules
install(TARGETS enhancex_cpp enhancex_cpp_static DESTINATION lib)
install(DIRECTORY cpp/include/ DESTINATION include)
