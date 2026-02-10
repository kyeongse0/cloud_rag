# Progress Report

## 📅 [날짜: 2025-02-10]

### ✅ 완료 (Completed)
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
- [x] 모든 데이터베이스 모델 정의:
  - User (Google OAuth)
  - Model (LLM endpoints)
  - PromptTemplate & PromptVersion
  - TestRun & TestResult
- [x] FastAPI main.py 작성 (health check 포함)
- [x] Alembic 설정 (async migrations)

### 🚧 진행 중 (In Progress)
- [ ] Week 1 Day 2: Google OAuth 2.0 구현

### 📝 예정 (Planned)
- [ ] authlib 통합
- [ ] OAuth 콜백 엔드포인트
- [ ] JWT 토큰 생성/검증
- [ ] 인증 미들웨어 구현
- [ ] 테스트 작성

### 🎯 오늘의 성과 (Today's Achievement)
Week 1 Day 1 완료. FastAPI 백엔드 기반 구조와 모든 SQLAlchemy 모델 정의 완료.

### 🤔 이슈 및 결정사항 (Issues & Decisions)
- ADR-001 작성 완료: FastAPI 선택 (async 지원, WebSocket, Pydantic 통합)
- 데이터베이스 모델 설계 PRD 스키마 기반으로 구현

### ⏭️ 다음 작업 (Next Steps)
1. Google OAuth 2.0 구현 (authlib 사용)
2. JWT 토큰 생성 및 검증 로직
3. 인증 관련 테스트 작성
4. ADR-002 작성: 인증 전략
