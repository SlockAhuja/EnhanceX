#ifndef ENHANCEX_GPU_MANAGER_HPP
#define ENHANCEX_GPU_MANAGER_HPP

#include <string>
#include <iostream>
#include <memory>

namespace enhancex {

class GPUManager {
public:
    // Singleton Access
    static GPUManager& getInstance() {
        static GPUManager instance;
        return instance;
    }

    // Modern C++20 non-copyable, non-movable singleton
    GPUManager(const GPUManager&) = delete;
    GPUManager& operator=(const GPUManager&) = delete;
    GPUManager(GPUManager&&) = delete;
    GPUManager& operator=(GPUManager&&) = delete;

    [[nodiscard]] bool isCUDAAvailable() const noexcept {
#ifdef ENHANCEX_ENABLE_CUDA
        return true;
#else
        return false;
#endif
    }

    [[nodiscard]] std::string getDeviceName() const {
        if (isCUDAAvailable()) {
            return "NVIDIA CUDA GPU (C++ Engine)";
        }
        return "CPU Fallback (C++ Engine)";
    }

    void synchronize() const noexcept {
        // Stream synchronization point
    }

private:
    GPUManager() = default;
    ~GPUManager() = default;
};

} // namespace enhancex

#endif // ENHANCEX_GPU_MANAGER_HPP
