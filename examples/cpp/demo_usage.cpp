#include "enhancex/enhancex.hpp"
#include <iostream>

int main() {
    std::cout << "=== EnhanceX C++20 API Demonstration ===\n";

    auto& gpu = enhancex::GPUManager::getInstance();
    std::cout << "Active Device: " << gpu.getDeviceName() << "\n";

    enhancex::ImageEnhancer enhancer;
    cv::Mat input = cv::Mat::zeros(400, 400, CV_8UC3);
    cv::putText(input, "C++ EnhanceX", cv::Point(50, 200), cv::FONT_HERSHEY_SIMPLEX, 1.0, cv::Scalar(255, 255, 255), 2);

    cv::Mat sharpened = enhancer.sharpen(input, 1.5f);
    cv::Mat claheResult = enhancer.applyCLAHE(sharpened, 2.0);

    std::cout << "Successfully enhanced C++ frame: " << claheResult.cols << "x" << claheResult.rows << "\n";
    return 0;
}
