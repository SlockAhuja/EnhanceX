#ifndef ENHANCEX_VIDEO_ENHANCER_HPP
#define ENHANCEX_VIDEO_ENHANCER_HPP

#include "image_enhancer.hpp"
#include "stabilizer.hpp"
#include "frame_interpolator.hpp"
#include <string>

namespace enhancex {

class VideoEnhancer {
public:
    VideoEnhancer() = default;

    bool enhance(const std::string& inputPath, const std::string& outputPath) {
        cv::VideoCapture cap(inputPath);
        if (!cap.isOpened()) return false;

        int width = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_WIDTH));
        int height = static_cast<int>(cap.get(cv::CAP_PROP_FRAME_HEIGHT));
        double fps = cap.get(cv::CAP_PROP_FPS);

        cv::VideoWriter writer(outputPath, cv::VideoWriter::fourcc('m', 'p', '4', 'v'), fps, cv::Size(width, height));
        ImageEnhancer enhancer;
        cv::Mat frame;
        while (cap.read(frame)) {
            cv::Mat enhanced = enhancer.sharpen(frame, 1.0f);
            writer.write(enhanced);
        }
        return true;
    }
};

} // namespace enhancex

#endif // ENHANCEX_VIDEO_ENHANCER_HPP
