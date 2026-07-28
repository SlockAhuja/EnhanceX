#include "enhancex/cuda_kernels.hpp"
#include <cuda_runtime.h>
#include <algorithm>
#include <cmath>

namespace enhancex {
namespace cuda {

// 2D CUDA Sharpening Kernel (3x3 Laplacian Unsharp Masking)
__global__ void sharpen_kernel(
    const uint8_t* __restrict__ input,
    uint8_t* __restrict__ output,
    int width,
    int height,
    int channels,
    float strength
) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x >= width || y >= height) return;

    for (int c = 0; c < channels; ++c) {
        int idx = (y * width + x) * channels + c;

        int x_left = max(x - 1, 0);
        int x_right = min(x + 1, width - 1);
        int y_up = max(y - 1, 0);
        int y_down = min(y + 1, height - 1);

        float center = static_cast<float>(input[idx]);
        float left = static_cast<float>(input[(y * width + x_left) * channels + c]);
        float right = static_cast<float>(input[(y * width + x_right) * channels + c]);
        float up = static_cast<float>(input[(y_up * width + x) * channels + c]);
        float down = static_cast<float>(input[(y_down * width + x) * channels + c]);

        float laplacian = 4.0f * center - (left + right + up + down);
        float sharpened = center + strength * laplacian;

        output[idx] = static_cast<uint8_t>(fminf(fmaxf(sharpened, 0.0f), 255.0f));
    }
}

// Spatial Gaussian / Bilateral Denoising CUDA Kernel
__global__ void denoise_kernel(
    const uint8_t* __restrict__ input,
    uint8_t* __restrict__ output,
    int width,
    int height,
    int channels,
    float sigma_spatial,
    float sigma_range
) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x >= width || y >= height) return;

    int radius = 2;
    for (int c = 0; c < channels; ++c) {
        int idx = (y * width + x) * channels + c;
        float center_val = static_cast<float>(input[idx]);

        float sum_weight = 0.0f;
        float sum_val = 0.0f;

        for (int dy = -radius; dy <= radius; ++dy) {
            for (int dx = -radius; dx <= radius; ++dx) {
                int nx = min(max(x + dx, 0), width - 1);
                int ny = min(max(y + dy, 0), height - 1);
                int n_idx = (ny * width + nx) * channels + c;

                float neighbor_val = static_cast<float>(input[n_idx]);
                float spatial_dist_sq = static_cast<float>(dx * dx + dy * dy);
                float range_dist_sq = (center_val - neighbor_val) * (center_val - neighbor_val);

                float w_spatial = __expf(-spatial_dist_sq / (2.0f * sigma_spatial * sigma_spatial));
                float w_range = __expf(-range_dist_sq / (2.0f * sigma_range * sigma_range));
                float weight = w_spatial * w_range;

                sum_val += neighbor_val * weight;
                sum_weight += weight;
            }
        }

        output[idx] = static_cast<uint8_t>(fminf(fmaxf(sum_val / (sum_weight + 1e-5f), 0.0f), 255.0f));
    }
}

// Color transform CUDA kernel (0: BGR2RGB, 1: BGR2GRAY)
__global__ void color_transform_kernel(
    const uint8_t* __restrict__ input,
    uint8_t* __restrict__ output,
    int width,
    int height,
    int code
) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x >= width || y >= height) return;

    int idx = (y * width + x) * 3;
    if (code == 0) {
        // Swap B and R
        output[idx] = input[idx + 2];
        output[idx + 1] = input[idx + 1];
        output[idx + 2] = input[idx];
    } else if (code == 1) {
        // Grayscale conversion
        float b = static_cast<float>(input[idx]);
        float g = static_cast<float>(input[idx + 1]);
        float r = static_cast<float>(input[idx + 2]);
        uint8_t gray = static_cast<uint8_t>(0.114f * b + 0.587f * g + 0.299f * r);
        output[y * width + x] = gray;
    }
}

// Bilinear resize CUDA kernel
__global__ void bilinear_resize_kernel(
    const uint8_t* __restrict__ input,
    int in_w,
    int in_h,
    uint8_t* __restrict__ output,
    int out_w,
    int out_h,
    int channels
) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x >= out_w || y >= out_h) return;

    float scale_x = static_cast<float>(in_w) / out_w;
    float scale_y = static_cast<float>(in_h) / out_h;

    float gx = (x + 0.5f) * scale_x - 0.5f;
    float gy = (y + 0.5f) * scale_y - 0.5f;

    int gxi = min(max(static_cast<int>(floorf(gx)), 0), in_w - 2);
    int gyi = min(max(static_cast<int>(floorf(gy)), 0), in_h - 2);

    float dx = gx - gxi;
    float dy = gy - gyi;

    for (int c = 0; c < channels; ++c) {
        float c00 = input[(gyi * in_w + gxi) * channels + c];
        float c10 = input[(gyi * in_w + (gxi + 1)) * channels + c];
        float c01 = input[((gyi + 1) * in_w + gxi) * channels + c];
        float c11 = input[((gyi + 1) * in_w + (gxi + 1)) * channels + c];

        float val = c00 * (1.0f - dx) * (1.0f - dy) +
                    c10 * dx * (1.0f - dy) +
                    c01 * (1.0f - dx) * dy +
                    c11 * dx * dy;

        output[(y * out_w + x) * channels + c] = static_cast<uint8_t>(fminf(fmaxf(val, 0.0f), 255.0f));
    }
}

// HDR Reinhard Tone Mapping CUDA Kernel
__global__ void hdr_tonemap_kernel(
    const uint8_t* __restrict__ input,
    uint8_t* __restrict__ output,
    int width,
    int height,
    int channels,
    float gamma
) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x >= width || y >= height) return;

    for (int c = 0; c < channels; ++c) {
        int idx = (y * width + x) * channels + c;
        float val = static_cast<float>(input[idx]) / 255.0f;
        float mapped = val / (val + 1.0f);
        float corrected = powf(mapped, 1.0f / gamma);
        output[idx] = static_cast<uint8_t>(fminf(fmaxf(corrected * 255.0f, 0.0f), 255.0f));
    }
}

// Brightness & Contrast Adjustment CUDA Kernel
__global__ void adjust_brightness_contrast_kernel(
    const uint8_t* __restrict__ input,
    uint8_t* __restrict__ output,
    int width,
    int height,
    int channels,
    float alpha,
    float beta
) {
    int x = blockIdx.x * blockDim.x + threadIdx.x;
    int y = blockIdx.y * blockDim.y + threadIdx.y;

    if (x >= width || y >= height) return;

    for (int c = 0; c < channels; ++c) {
        int idx = (y * width + x) * channels + c;
        float val = static_cast<float>(input[idx]);
        float out_val = alpha * val + beta;
        output[idx] = static_cast<uint8_t>(fminf(fmaxf(out_val, 0.0f), 255.0f));
    }
}

void launch_sharpen_kernel(
    const uint8_t* d_input,
    uint8_t* d_output,
    int width,
    int height,
    int channels,
    float strength,
    void* stream
) {
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x, (height + block.y - 1) / block.y);
    cudaStream_t custream = static_cast<cudaStream_t>(stream);
    sharpen_kernel<<<grid, block, 0, custream>>>(d_input, d_output, width, height, channels, strength);
}

void launch_denoise_kernel(
    const uint8_t* d_input,
    uint8_t* d_output,
    int width,
    int height,
    int channels,
    float sigma_spatial,
    float sigma_range,
    void* stream
) {
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x, (height + block.y - 1) / block.y);
    cudaStream_t custream = static_cast<cudaStream_t>(stream);
    denoise_kernel<<<grid, block, 0, custream>>>(d_input, d_output, width, height, channels, sigma_spatial, sigma_range);
}

void launch_color_transform_kernel(
    const uint8_t* d_input,
    uint8_t* d_output,
    int width,
    int height,
    int code,
    void* stream
) {
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x, (height + block.y - 1) / block.y);
    cudaStream_t custream = static_cast<cudaStream_t>(stream);
    color_transform_kernel<<<grid, block, 0, custream>>>(d_input, d_output, width, height, code);
}

void launch_bilinear_resize_kernel(
    const uint8_t* d_input,
    int in_w,
    int in_h,
    uint8_t* d_output,
    int out_w,
    int out_h,
    int channels,
    void* stream
) {
    dim3 block(16, 16);
    dim3 grid((out_w + block.x - 1) / block.x, (out_h + block.y - 1) / block.y);
    cudaStream_t custream = static_cast<cudaStream_t>(stream);
    bilinear_resize_kernel<<<grid, block, 0, custream>>>(d_input, in_w, in_h, d_output, out_w, out_h, channels);
}

void launch_hdr_tonemap_kernel(
    const uint8_t* d_input,
    uint8_t* d_output,
    int width,
    int height,
    int channels,
    float gamma,
    void* stream
) {
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x, (height + block.y - 1) / block.y);
    cudaStream_t custream = static_cast<cudaStream_t>(stream);
    hdr_tonemap_kernel<<<grid, block, 0, custream>>>(d_input, d_output, width, height, channels, gamma);
}

void launch_adjust_brightness_contrast_kernel(
    const uint8_t* d_input,
    uint8_t* d_output,
    int width,
    int height,
    int channels,
    float alpha,
    float beta,
    void* stream
) {
    dim3 block(16, 16);
    dim3 grid((width + block.x - 1) / block.x, (height + block.y - 1) / block.y);
    cudaStream_t custream = static_cast<cudaStream_t>(stream);
    adjust_brightness_contrast_kernel<<<grid, block, 0, custream>>>(d_input, d_output, width, height, channels, alpha, beta);
}

} // namespace cuda
} // namespace enhancex
