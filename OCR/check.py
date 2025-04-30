import cv2

# 마스크 이미지 읽기
mask_4ch = cv2.imread("mask_4ch.png", cv2.IMREAD_UNCHANGED)

# 마스크 형상 확인
print("마스크 형상:", mask_4ch.shape)

# 마스크 이미지 표시
cv2.imshow("4채널 마스크", mask_4ch)
cv2.waitKey(0)
cv2.destroyAllWindows()