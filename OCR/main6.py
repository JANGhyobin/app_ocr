import cv2
import numpy as np

# 파일 경로 설정
original_path = "D:/DEV/workspace_python/OCR/origin.png"   # 원본 이미지
mask_path = "D:/DEV/workspace_python/OCR/mask.png"      # 마스크 이미지

# 이미지 로드
original = cv2.imread(original_path)
mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

# 마스크가 제대로 로드되었는지 확인
if original is None:
    raise FileNotFoundError(f"❌ 원본 이미지 로드 실패: {original_path}")
if mask is None:
    raise FileNotFoundError(f"❌ 마스크 이미지 로드 실패: {mask_path}")

# 마스크 이진화 (0 or 255)
_, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

# Inpainting 적용
inpainted = cv2.inpaint(original, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

# 결과 저장
output_path = "D:/DEV/workspace_python/OCR/EX3.png"
cv2.imwrite(output_path, inpainted)

# 결과 경로 출력
output_path
