# LLM Test Platform - Backend

FastAPI 기반 백엔드 서버

## 기술 스택

- **Framework**: FastAPI
- **Database**: PostgreSQL 16
- **ORM**: SQLAlchemy 2.0
- **Migration**: Alembic
- **Authentication**: Google OAuth 2.0 + JWT

## 설치 및 실행

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 열어 실제 값으로 수정

# 데이터베이스 마이그레이션
alembic upgrade head

# 개발 서버 실행
uvicorn app.main:app --reload --port 8000
```

## 프로젝트 구조

```
backend/
├── app/
│   ├── api/v1/       # API 엔드포인트
│   ├── models/       # SQLAlchemy 모델
│   ├── schemas/      # Pydantic 스키마
│   ├── services/     # 비즈니스 로직
│   ├── db/           # 데이터베이스 설정
│   └── utils/        # 유틸리티
├── alembic/          # 마이그레이션
└── tests/            # 테스트
```

## API 문서

서버 실행 후: http://localhost:8000/docs
