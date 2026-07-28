#ifndef ENHANCEX_IMAGE_ENHANCER_HPP
#define ENHANCEX_IMAGE_ENHANCER_HPP

#include <opencv2/opencv.hpp>
#include <string>

namespace enhancex {

class ImageEnhancer {
public:
    ImageEnhancer() = default;

    cv::Mat sharpen(const cv::Mat& input, float strength = 1.0f) {
        cv::Mat blurred, result;
        cv::GaussianBlur(input, blurred, cv::Size(3, 3), 1.0);
        cv::addWeighted(input, 1.0f + strength, blurred, -strength, 0, result);
        return result;
    }

    cv::Mat denoise(const cv::Mat& input, float h = 10.0f) {
        cv::Mat result;
        if (input.channels() == 1) {
            cv::fastNlMeansDenoising(input, result, h);
        } else {
            cv::fastNlMeansDenoisingColored(input, result, h, h);
        }
        return result;
    }

    cv::Mat applyCLAHE(const cv::Mat& input, double clipLimit = 2.0) {
        cv::Mat result;
        cv::Ptr<cv::CLAHE> clahe = cv::createCLAHE(clipLimit, cv::Size(8, 8));
        if (input.channels() == 1) {
            clahe->apply(input, result);
        } else {
            cv::Mat lab;
            cv::cvtColor(input, lab, cv::COLOR_BGR2Lab);
            std::vector<cv::Mat> channels;
            cv::split(lab, channels);
            clahe->apply(channels[0], channels[0]);
            cv::merge(channels, lab);
            cv::cvtColor(lab, result, cv::COLOR_Lab2BGR);
        }
        return result;
    }
};

} // namespace enhancex

#endif // ENHANCEX_IMAGE_ENHANCER_HPP
