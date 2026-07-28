#ifndef ENHANCEX_SDK_HPP
#define ENHANCEX_SDK_HPP

#include "enhancex.hpp"
#include <memory>
#include <string>

namespace enhancex {
namespace sdk {

/**
 * Enterprise C++ SDK Client Interface for EnhanceX.
 */
class EnhanceXSDK {
public:
    EnhanceXSDK() {
        gpu_mgr_ = &GPUManager::getInstance();
        model_mgr_ = std::make_unique<ModelManager>();
        image_enhancer_ = std::make_unique<ImageEnhancer>();
        video_enhancer_ = std::make_unique<VideoEnhancer>();
        stabilizer_ = std::make_unique<Stabilizer>();
    }

    [[nodiscard]] std::string getDeviceName() const {
        return gpu_mgr_->getDeviceName();
    }

    [[nodiscard]] bool isCUDAAvailable() const noexcept {
        return gpu_mgr_->isCUDAAvailable();
    }

    cv::Mat enhanceImage(const cv::Mat& input, float sharpen = 1.0f, double claheClip = 2.0) {
        cv::Mat res = image_enhancer_->sharpen(input, sharpen);
        return image_enhancer_->applyCLAHE(res, claheClip);
    }

    bool enhanceVideo(const std::string& inputPath, const std::string& outputPath) {
        return video_enhancer_->enhance(inputPath, outputPath);
    }

    bool stabilizeVideo(const std::string& inputPath, const std::string& outputPath, int smoothingRadius = 30) {
        Stabilizer stab(smoothingRadius);
        return stab.process(inputPath, outputPath);
    }

private:
    GPUManager* gpu_mgr_;
    std::unique_ptr<ModelManager> model_mgr_;
    std::unique_ptr<ImageEnhancer> image_enhancer_;
    std::unique_ptr<VideoEnhancer> video_enhancer_;
    std::unique_ptr<Stabilizer> stabilizer_;
};

} // namespace sdk
} // namespace enhancex

#endif // ENHANCEX_SDK_HPP
