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

#### Week 1 Day 3: Model & Prompt CRUD APIs
- [x] Model 스키마 (schemas/model.py)
  - ModelCreate, ModelUpdate, ModelResponse
  - ModelHealthCheck, ModelListResponse
- [x] Model 서비스 (services/model.py)
  - CRUD 기능 (생성, 조회, 수정, 삭제)
  - 소프트 삭제 패턴 (is_active)
  - 페이지네이션 지원
  - 헬스 체크 기능 (httpx)
- [x] Model 라우터 (api/v1/models.py)
  - GET/POST /api/v1/models
  - GET/PUT/DELETE /api/v1/models/{id}
  - POST /api/v1/models/{id}/health
- [x] Prompt 스키마 (schemas/prompt.py)
  - PromptCreate, PromptUpdate, PromptResponse
  - PromptVersionResponse, PromptListResponse
- [x] Prompt 서비스 (services/prompt.py)
  - CRUD 기능
  - 자동 버전 관리 (content 변경 시)
  - 롤백 기능
  - 즐겨찾기 토글
- [x] Prompt 라우터 (api/v1/prompts.py)
  - GET/POST /api/v1/prompts
  - GET/PUT/DELETE /api/v1/prompts/{id}
  - POST /api/v1/prompts/{id}/favorite
  - GET /api/v1/prompts/{id}/versions
  - POST /api/v1/prompts/{id}/rollback
- [x] 테스트 작성 (test_models.py, test_prompts.py)

#### Week 1 Day 4-5: Test Execution API
- [x] TestRun 스키마 (schemas/test_run.py)
  - ModelTestConfig, TestRunCreate, TestRunResponse
  - TestResultResponse, TestRunListResponse
  - TestRunSummary, TestRunListSummaryResponse
- [x] LLM 클라이언트 유틸리티 (utils/llm_client.py)
  - vLLM/OpenAI compatible API 지원
  - 비동기 HTTP 요청 (httpx)
  - 타임아웃 및 에러 처리
- [x] TestRun 서비스 (services/test_run.py)
  - 테스트 생성 및 실행
  - 다중 모델 동시 호출 (asyncio.gather)
  - 결과 저장 및 조회
  - 페이지네이션 지원
- [x] TestRun 라우터 (api/v1/test_runs.py)
  - POST /api/v1/test-runs (테스트 실행)
  - GET /api/v1/test-runs (목록 조회)
  - GET /api/v1/test-runs/{id} (상세 조회)
  - DELETE /api/v1/test-runs/{id} (삭제)
- [x] Model에 model_name 필드 추가 (API 모델 이름)
- [x] 테스트 작성 (test_test_runs.py)

### 🚧 진행 중 (In Progress)
- [ ] Week 2: Frontend 개발

### 📝 예정 (Planned)
- [ ] React + Vite 프로젝트 설정
- [ ] TailwindCSS + Shadcn UI 설정
- [ ] 라우팅 및 레이아웃
- [ ] 인증 UI (Google 로그인)

### 🎯 오늘의 성과 (Today's Achievement)
Week 1 완료! 백엔드 API 모두 완성:
- Google OAuth 2.0 인증
- Model/Prompt CRUD
- Test Execution (vLLM 동기 호출)

### 🤔 이슈 및 결정사항 (Issues & Decisions)
- ADR-001: FastAPI 선택 (async 지원, WebSocket, Pydantic 통합)
- ADR-002: Google OAuth + JWT (httpOnly 쿠키, 1시간/7일 만료)
- 테스트에 SQLite+aiosqlite 사용
- Model은 소프트 삭제 패턴 사용 (is_active 플래그)
- Prompt는 content 변경 시 자동 버전 생성
- LLM 호출은 OpenAI compatible API 사용 (vLLM 호환)
- 다중 모델 테스트는 asyncio.gather로 동시 실행

### ⏭️ 다음 작업 (Next Steps)
1. Week 2 Day 1: React + Vite + TailwindCSS 설정
2. Week 2 Day 2: 인증 UI 구현
3. Week 2 Day 3: 모델/프롬프트 관리 UI
4. Week 2 Day 4-5: 테스트 실행 UI
