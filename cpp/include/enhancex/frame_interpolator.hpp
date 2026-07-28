#ifndef ENHANCEX_FRAME_INTERPOLATOR_HPP
#define ENHANCEX_FRAME_INTERPOLATOR_HPP

#include <string>
#include <iostream>
#include <opencv2/opencv.hpp>

namespace enhancex {

class FrameInterpolator {
public:
    FrameInterpolator(const std::string& engine = "rife") : engine_(engine) {}

    cv::Mat interpolate(const cv::Mat& frame1, const cv::Mat& frame2, float alpha = 0.5f) {
        cv::Mat blended;
        cv::addWeighted(frame1, 1.0f - alpha, frame2, alpha, 0.0, blended);
        return blended;
    }

private:
    std::string engine_;
};

} // namespace enhancex

#endif // ENHANCEX_FRAME_INTERPOLATOR_HPP
