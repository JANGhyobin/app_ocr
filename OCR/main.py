import cv2
import numpy as np

# 원본 이미지 경로
img_path = "D:/DEV/workspace_python/OCR/origin.png"
mask_path = "D:/DEV/workspace_python/OCR/mask.png"

# 이미지 읽기
img = cv2.imread(img_path)

if img is None:
    print("❌ 원본 이미지를 불러올 수 없습니다.")
    exit()

# 그레이스케일 변환
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 임계값 적용 (텍스트 영역 검출)
_, mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# 마스크 저장
cv2.imwrite(mask_path, mask)

print(f"✅ 마스크 생성 완료: {mask_path}")
