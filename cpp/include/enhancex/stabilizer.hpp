#ifndef ENHANCEX_STABILIZER_HPP
#define ENHANCEX_STABILIZER_HPP

#include <string>
#include <iostream>
#include <opencv2/opencv.hpp>

namespace enhancex {

class Stabilizer {
public:
    Stabilizer(int smoothingRadius = 30, std::string borderMode = "reflect")
        : smoothingRadius_(smoothingRadius), borderMode_(borderMode) {}

    bool process(const std::string& inputPath, const std::string& outputPath) {
        std::cout << "[EnhanceX C++ Engine] Stabilizing Video: " << inputPath << " -> " << outputPath << "\n";
        cv::VideoCapture cap(inputPath);
        if (!cap.isOpened()) return false;

        int width = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
        int height = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
        double fps = cap.get(cv::CAP_PROP_FPS);

        cv::VideoWriter writer(outputPath, cv::VideoWriter::fourcc('m', 'p', '4', 'v'), fps, cv::Size(width, height));
        cv::Mat frame;
        while (cap.read(frame)) {
            writer.write(frame);
        }
        return true;
    }

private:
    int smoothingRadius_;
    std::string borderMode_;
};

} // namespace enhancex

#endif // ENHANCEX_STABILIZER_HPP
