#ifndef ENHANCEX_CUDA_KERNELS_HPP
#define ENHANCEX_CUDA_KERNELS_HPP

#include <cstddef>
#include <cstdint>

namespace enhancex {
namespace cuda {

/**
 * High-performance CUDA Kernels interface for parallel image operators.
 * Modern C++20 interface with explicit stream synchronization support.
 */

// CUDA kernel launcher for 2D Image Sharpening (3x3 Shared Memory Laplacian Filter)
void launch_sharpen_kernel(
    const uint8_t* d_input,
    uint8_t* d_output,
    int width,
    int height,
    int channels,
    float strength,
    void* stream = nullptr
);

// CUDA kernel launcher for Spatial Bilateral / Gaussian Denoising
void launch_denoise_kernel(
    const uint8_t* d_input,
    uint8_t* d_output,
    int width,
    int height,
    int channels,
    float sigma_spatial,
    float sigma_range,
    void* stream = nullptr
);

// CUDA kernel launcher for Color Space Transformations (RGB<->BGR, Grayscale)
void launch_color_transform_kernel(
    const uint8_t* d_input,
    uint8_t* d_output,
    int width,
    int height,
    int code,
    void* stream = nullptr
);

// CUDA kernel launcher for Parallel Bilinear Rescaling
void launch_bilinear_resize_kernel(
    const uint8_t* d_input,
    int in_w,
    int in_h,
    uint8_t* d_output,
    int out_w,
    int out_h,
    int channels,
    void* stream = nullptr
);

// CUDA kernel launcher for HDR Reinhard Tone Mapping
void launch_hdr_tonemap_kernel(
    const uint8_t* d_input,
    uint8_t* d_output,
    int width,
    int height,
    int channels,
    float gamma,
    void* stream = nullptr
);

// CUDA kernel launcher for Brightness & Contrast Adjustments
void launch_adjust_brightness_contrast_kernel(
    const uint8_t* d_input,
    uint8_t* d_output,
    int width,
    int height,
    int channels,
    float alpha,
    float beta,
    void* stream = nullptr
);

} // namespace cuda
} // namespace enhancex

#endif // ENHANCEX_CUDA_KERNELS_HPP
