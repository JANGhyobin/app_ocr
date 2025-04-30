import cv2
import numpy as np

# 원본 이미지 경로 (215x137 크기)
img_path = "D:/DEV/workspace_python/OCR/origin.png"  # 파일명에 맞춰 조정할 것
mask_output_path = "D:/DEV/workspace_python/OCR/mask.png"  # 저장할 마스크 파일 경로

# 이미지 로드
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

if img is None:
    print("❌ 이미지 로드 실패")
    exit()

# 1. 블러 처리하여 노이즈 제거
blurred = cv2.GaussianBlur(img, (5, 5), 0)

# 2. 임계값 처리 (Thresholding)
_, mask = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY_INV)

# 3. 마스크 크기를 조정 (필요 시)
mask = cv2.resize(mask, (215, 137), interpolation=cv2.INTER_NEAREST)

# 4. 마스크 저장
cv2.imwrite(mask_output_path, mask)

print(f"✅ 마스크 생성 완료: {mask_output_path}")
