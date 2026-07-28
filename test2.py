import cv2

cap = cv2.VideoCapture("assets/sample_input.mp4")

print(cap.isOpened())

ret, frame = cap.read()

print(ret)

cap.release()