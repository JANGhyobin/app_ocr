main.py 실행하면된다 
easyocr==1.7.2
pytesseract==0.3.13
opencv-python==4.11.0.86
opencv-python-headless==4.11.0.86
Pillow==9.5.0
scikit-image==0.24.0
python-bidi==0.6.6
arabic-reshaper==2.1.3
trdg==1.8.0
ultralytics==8.3.102
torch==2.6.0
torchvision==0.21.0
위에거 설치하고  cd app_ocr 에서 python -m uvicorn main:app --host 0.0.0.0 --port 8888 --reload  하면 실행된다 

