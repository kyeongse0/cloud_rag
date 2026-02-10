# Progress Report

## 📅 [날짜: 2025-02-10]

### ✅ 완료 (Completed)

#### Week 1 Day 1: Backend Foundation
- [x] 프로젝트 레포지토리 초기화
- [x] .gitignore 생성 (.env 보안 포함)
- [x] 프로젝트 구조 생성
- [x] PROGRESS.md 생성
- [x] docs/decisions/ 폴더 생성
- [x] backend/frontend 기본 구조 생성
- [x] docker-compose.yml 템플릿 생성
- [x] .env.example 파일 생성
- [x] ADR-001 작성: 백엔드 프레임워크 선택 (FastAPI)
- [x] FastAPI config.py 작성 (pydantic-settings)
- [x] SQLAlchemy 데이터베이스 설정 (async)
- [x] 모든 데이터베이스 모델 정의 (User, Model, Prompt, TestRun)
- [x] FastAPI main.py 작성 (health check 포함)
- [x] Alembic 설정 (async migrations)

#### Week 1 Day 2: Google OAuth 2.0
- [x] ADR-002 작성: 인증 전략 (Google OAuth + JWT)
- [x] JWT 토큰 유틸리티 (utils/security.py)
- [x] User Pydantic 스키마 (schemas/user.py)
- [x] 인증 서비스 (services/auth.py)
- [x] OAuth 라우터 (api/v1/auth.py)
  - GET /api/v1/auth/google/login
  - GET /api/v1/auth/google/callback
  - POST /api/v1/auth/refresh
  - POST /api/v1/auth/logout
  - GET /api/v1/auth/me
- [x] 인증 의존성 (api/deps.py)
- [x] 인증 테스트 작성 (tests/test_auth.py)

### 🚧 진행 중 (In Progress)
- [ ] Week 1 Day 3: Model Management API

### 📝 예정 (Planned)
- [ ] Model CRUD 엔드포인트
- [ ] Model 헬스 체크 기능
- [ ] Prompt CRUD 엔드포인트
- [ ] 버전 관리 시스템 구현

### 🎯 오늘의 성과 (Today's Achievement)
Week 1 Day 1-2 완료. FastAPI 백엔드 기반 + Google OAuth 2.0 인증 시스템 구현 완료.

### 🤔 이슈 및 결정사항 (Issues & Decisions)
- ADR-001: FastAPI 선택 (async 지원, WebSocket, Pydantic 통합)
- ADR-002: Google OAuth + JWT (httpOnly 쿠키, 1시간/7일 만료)
- 테스트에 SQLite+aiosqlite 사용

### ⏭️ 다음 작업 (Next Steps)
1. Model CRUD API 구현
2. Model 헬스 체크 기능
3. Prompt CRUD API 구현
4. ADR-003: 데이터베이스 스키마 설계 작성
