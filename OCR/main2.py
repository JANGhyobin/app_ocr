import cv2

# 마스크 이미지 읽기
mask_path = "D:/DEV/workspace_python/OCR/mask.png"
mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)  # 1채널(Grayscale)로 읽기

if mask is None:
    print("❌ 마스크 이미지를 불러올 수 없습니다.")
    exit()

# 마스크를 이진화 (0 또는 255 값만 가지도록 변환)
_, binary_mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

# 올바른 형식으로 마스크 저장
corrected_mask_path = "D:/DEV/workspace_python/OCR/mask_corrected.png"
cv2.imwrite(corrected_mask_path, binary_mask)

print(f"마스크 저장 완료: {corrected_mask_path}")
