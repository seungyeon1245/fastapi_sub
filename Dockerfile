# 베이스 이미지
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 파일 복사
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 포트 설정 (FastAPI 기본 포트는 8000)
EXPOSE 8000

# 컨테이너 실행 시 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
