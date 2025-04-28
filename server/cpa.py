import cv2
import numpy as np

cap_no = 0

cap = cv2.VideoCapture(cap_no) # 0=내장 웹캠 1=USB 외장웹캠 2=가상 카메라 소프트웨어
fps = cap.get(cv2.CAP_PROP_FPS)
print('fps'+ str(fps))

roi_width,roi_height= 1000,700

while True:
    ret, frame = cap.read()
    if not ret:
        break
    h, w, _ = frame.shape
    center_x, center_y = w// 2, h// 2

x1 = center_x - roi_width //2
y1 = center_y - roi_height //2
x2 = center_x - roi_width //2
y2 = center_y - roi_height //2

mask = np.zeros_like(frame)

mask[y1:y2, x1:x2] = frame[y1:y2, x1:x2]

cv2.rectangle(mask,(x1,y1), (x2,y2), (0,255,0),3 )

cv2.imshow("관심 영역",mask)