from enhancex import VideoEnhancer

enhancer = VideoEnhancer()

enhancer.enhance(
    "assets/sample_input.mp4",
    "demo_outputs/output.mp4"
)

print("Success")