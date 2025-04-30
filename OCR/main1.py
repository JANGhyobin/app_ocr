import cv2
from pyinpaint import Inpaint

# Inpainting 실행
img_path = "D:/DEV/workspace_python/OCR/origin.png"
mask_path = "D:/DEV/workspace_python/OCR/mask_small.png"

inpaint = Inpaint(img_path, mask_path)
inpainted_img = inpaint()

# 결과 저장
result_path = "D:/DEV/workspace_python/OCR/inpainted_result.png"
cv2.imwrite(result_path, inpainted_img * 255)

print(f"✅ 복원된 이미지 저장 완료: {result_path}")
