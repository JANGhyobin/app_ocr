# app_ocr/server/ocr_engine.py
import cv2
import easyocr
from ultralytics import YOLO
import numpy as np
import re

print("ocr_engine.py 동기 버전 실행 중 ")

# 학습된 모델 로드
model = YOLO("D:/DEV/workspace_python/app_ocr/server/yoloV8/runs/detect/train3/weights/best.pt")

# EasyOCR 리더 로드
reader = easyocr.Reader(['ko'], gpu=False)

def process_ocr(file_path: str):
    try:
        # 이미지 로드
        image = cv2.imread(file_path)
        if image is None:
            raise Exception("이미지를 로드할 수 없습니다.")

        # YOLOv8로 객체 탐지
        results = model(image)

        # 탐지된 객체에서 텍스트 추출
        extracted_data = {}
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls)
                class_name = result.names[class_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # 해당 영역 크롭
                cropped = image[y1:y2, x1:x2]

                # 이미지 전처리: 대비 조절 및 그레이스케일 변환
                cropped = cv2.convertScaleAbs(cropped, alpha=1.5, beta=0)
                cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

                # OCR로 텍스트 추출
                ocr_result = reader.readtext(cropped, detail=0, paragraph=True, min_size=10)
                text = " ".join(ocr_result) if ocr_result else ""

                # 텍스트 후처리
                text = re.sub(r'\s+', '', text)
                if class_name == 'ocr_fields_rrn':
                    if len(text) == 12:
                        text = text[:6] + '-' + text[6:]
                if class_name == 'ocr_fields_address':
                    text = text.replace('', '')

                extracted_data[class_name] = text

        # 추출된 데이터에 타입 추가
        extracted_data["ocr_fields_type"] = "주민등록증"

        return extracted_data

    except Exception as e:
        raise Exception(f"이미지 처리 실패: {str(e)}")