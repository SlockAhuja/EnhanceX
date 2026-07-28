#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "enhancex/enhancex.hpp"

namespace py = pybind11;

PYBIND11_MODULE(enhancex_bindings, m) {
    m.doc() = "EnhanceX C++ Core Engine Pybind11 Module";

    py::class_<enhancex::GPUManager>(m, "GPUManager")
        .def_static("get_instance", &enhancex::GPUManager::getInstance, py::return_value_policy::reference)
        .def("is_cuda_available", &enhancex::GPUManager::isCUDAAvailable)
        .def("get_device_name", &enhancex::GPUManager::getDeviceName);

    py::class_<enhancex::ModelManager>(m, "ModelManager")
        .def(py::init<>())
        .def("load_model", &enhancex::ModelManager::loadModel)
        .def("get_model_path", &enhancex::ModelManager::getModelPath);

    py::class_<enhancex::ImageEnhancer>(m, "ImageEnhancer")
        .def(py::init<>());

    py::class_<enhancex::Stabilizer>(m, "Stabilizer")
        .def(py::init<int, std::string>(), py::arg("smoothing_radius") = 30, py::arg("border_mode") = "reflect")
        .def("process", &enhancex::Stabilizer::process);

    py::class_<enhancex::FrameInterpolator>(m, "FrameInterpolator")
        .def(py::init<std::string>(), py::arg("engine") = "rife");

    py::class_<enhancex::VideoEnhancer>(m, "VideoEnhancer")
        .def(py::init<>())
        .def("enhance", &enhancex::VideoEnhancer::enhance);
}
