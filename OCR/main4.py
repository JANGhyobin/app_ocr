import cv2
import numpy as np

# 마스크 이미지 읽기 (1채널로 변환)
mask_path = "D:/DEV/workspace_python/OCR/mask_4ch.png"
mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

if mask is None:
    print("❌ 마스크 이미지를 불러올 수 없습니다.")
    exit()

# 마스크 노이즈 제거 & 작은 영역 삭제
kernel = np.ones((5, 5), np.uint8)  # 작은 커널로 미세 조정
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # 작은 영역 제거

# 다시 저장
small_mask_path = "D:/DEV/workspace_python/OCR/mask_small.png"
cv2.imwrite(small_mask_path, mask)

print(f"✅ 축소된 마스크 저장 완료: {small_mask_path}")
