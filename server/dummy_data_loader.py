# app_ocr/server/dummy_data_loader.py
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def load_dummy_data():
    # 기존 데이터
    redis_client.hset("850505-1234567", mapping={
        "ocr_fields_name": "김서연",
        "ocr_fields_rrn": "850505-1234567",
        "ocr_fields_issue_date": "20200115",
        "ocr_fields_issue_office": "대구광역시중구청장",
        "ocr_fields_type": "주민등록증"
    })
def load_dummy_data():
    # 기존 데이터
    redis_client.hset("850505-1234567", mapping={
        "ocr_fields_name": "김서연",
        "ocr_fields_rrn": "850505-1234567",
        "ocr_fields_issue_date": "20200775",
        "ocr_fields_issue_office": "대구광역시중구청장",
        "ocr_fields_type": "주민등록증"
    })

def load_dummy_data():
    # 기존 데이터
    redis_client.hset("850505-1234567", mapping={
        "ocr_fields_name": "김서연",
        "ocr_fields_rrn": "850505-1234567",
        "ocr_fields_issue_date": "20200113",
        "ocr_fields_issue_office": "대구광역시중구청장",
        "ocr_fields_type": "주민등록증"
    })

def load_dummy_data():
    # 기존 데이터
    redis_client.hset("850505-1234567", mapping={
        "ocr_fields_name": "김서연",
        "ocr_fields_rrn": "850505-1234567",
        "ocr_fields_issue_date": "20200775",
        "ocr_fields_issue_office": "대구광역시중구청장",
        "ocr_fields_type": "주민등록증"
    })

    print("더미 데이터 저장됨")

if __name__ == "__main__":
    load_dummy_data()