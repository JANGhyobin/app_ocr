import cv2
import numpy as np

# 원본 이미지와 마스크 읽기
img = cv2.imread("origin.png", cv2.IMREAD_UNCHANGED)  # 4채널 이미지 읽기
mask = cv2.imread("mask.png", cv2.IMREAD_COLOR)       # 3채널 마스크 읽기

# 마스크를 4채널로 변환
if mask.shape[2] == 3:  # 마스크가 3채널일 경우
    alpha_channel = np.ones((mask.shape[0], mask.shape[1], 1), dtype=mask.dtype) * 255
    mask = np.concatenate((mask, alpha_channel), axis=2)  # 알파 채널 추가

# 변환된 마스크 저장
cv2.imwrite("mask_4ch.png", mask)

# pyinpaint 실행
# pyinpaint --org_img "origin.png" --mask "mask_4ch.png"