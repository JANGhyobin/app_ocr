import redis
import os
import shutil
import re
import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from ocr_engine import process_ocr
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Redis 연결 설정
try:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        db=int(os.getenv("REDIS_DB", 0)),
        decode_responses=True  # 자동으로 바이트를 문자열로 디코딩
    )
    # Redis 연결 테스트
    redis_client.ping()
    logger.info("Redis 연결 성공")
except redis.RedisError as e:
    logger.error(f"Redis 연결 실패: {str(e)}")
    raise HTTPException(status_code=500, detail=f"Redis 연결 실패: {str(e)}")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 환경 변수로 출처 지정 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 임시 파일 저장 디렉토리
TEMP_DIR = os.getenv("TEMP_DIR", "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "FastAPI OCR server 작동중"}

@app.options("/ocr")
async def options_ocr():
    """프리플라이트 요청 처리"""
    return JSONResponse(status_code=200, headers={
        "Access-Control-Allow-Origin": os.getenv("ALLOWED_ORIGINS", "*"),
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    })

# 날짜 형식 정규화 함수
def normalize_date(date_str: str) -> str:
    """날짜 형식 정규화"""
    if not date_str:
        return ""
    return ''.join(filter(str.isdigit, date_str))  # 예: "2020.01.15" -> "20200115"

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    try:
        # 파일 확장자 검증
        if not file.content_type.startswith("image/"):
            logger.warning(f"잘못된 파일 타입: {file.content_type}")
            raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

        # 파일 저장
        file_path = os.path.join(TEMP_DIR, file.filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info(f"파일 저장 완료: {file_path}")
        except Exception as e:
            logger.error(f"파일 저장 실패: {str(e)}")
            raise HTTPException(status_code=500, detail=f"파일 저장 실패: {str(e)}")

        # OCR 처리
        try:
            extracted_data = process_ocr(file_path)
            logger.info(f"추출된 데이터: {extracted_data}")
        except Exception as e:
            logger.error(f"OCR 처리 실패: {str(e)}")
            raise HTTPException(status_code=500, detail=f"OCR 처리 실패: {str(e)}")
        finally:
            # 임시 파일 삭제
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"임시 파일 삭제: {file_path}")

        # ocr_fields_type 확인
        type_value = re.sub(r'\s+', '', extracted_data.get("ocr_fields_type", ""))
        if type_value != "주민등록증":
            logger.warning("주민등록증이 아님")
            raise HTTPException(status_code=400, detail="주민등록증이 아닙니다.")

        # 주민번호로 Redis에서 데이터 조회
        rnn = extracted_data.get("ocr_fields_rrn")
        if not rnn:
            logger.warning("주민등록번호 없음")
            raise HTTPException(status_code=400, detail="주민등록번호가 없습니다.")

        try:
            stored_data = redis_client.hgetall(rnn)
            if not stored_data:
                logger.warning(f"등록되지 않은 주민번호: {rnn}")
                raise HTTPException(status_code=404, detail="등록되지 않은 주민번호입니다.")
        except redis.RedisError as e:
            logger.error(f"Redis 조회 실패: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Redis 조회 실패: {str(e)}")

        # 날짜 필드 정규화
        if "ocr_fields_issue_date" in extracted_data:
            extracted_data["ocr_fields_issue_date"] = normalize_date(extracted_data["ocr_fields_issue_date"])
        if "ocr_fields_issue_date" in stored_data:
            stored_data["ocr_fields_issue_date"] = normalize_date(stored_data["ocr_fields_issue_date"])

        # 비교할 필드 정의
        fields_to_compare = [
            "ocr_fields_name",
            "ocr_fields_rrn",
            "ocr_fields_issue_date",
            "ocr_fields_issue_office"
        ]

        # 필드 비교
        for field in fields_to_compare:
            if stored_data.get(field) != extracted_data.get(field):
                logger.warning(f"{field} 불일치: {stored_data.get(field)} != {extracted_data.get(field)}")
                raise HTTPException(status_code=400, detail=f"{field} 불일치")

        logger.info("인증 성공")
        return {"status": "success", "message": "인증 성공"}

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"서버 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
