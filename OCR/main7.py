import cv2
import numpy as np

# 원본 이미지 경로
image_path = 'test.png'  # 이미지 파일명 입력
image = cv2.imread(image_path)
mask = np.zeros(image.shape[:2], dtype=np.uint8)

drawing = False  # 마우스를 누르고 있는 상태
ix, iy = -1, -1

# 마우스 이벤트 콜백 함수
def draw_mask(event, x, y, flags, param):
    global ix, iy, drawing, mask

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(mask, (ix, iy), (x, y), 255, thickness=10)
            cv2.line(image, (ix, iy), (x, y), (0, 0, 255), thickness=10)
            ix, iy = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(mask, (ix, iy), (x, y), 255, thickness=10)
        cv2.line(image, (ix, iy), (x, y), (0, 0, 255), thickness=10)

cv2.namedWindow('Draw mask - Press s to save')
cv2.setMouseCallback('Draw mask - Press s to save', draw_mask)

while True:
    cv2.imshow('Draw mask - Press s to save', image)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('s'):  # s키 누르면 저장
        cv2.imwrite('mask.png', mask)
        print('Mask saved as mask.png')
        break
    elif k == 27:  # ESC 키로 종료
        break

cv2.destroyAllWindows()
