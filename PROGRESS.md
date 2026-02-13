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

#### Week 3 Day 1: Frontend Foundation
- [x] ADR-003 작성: 프론트엔드 프레임워크 선택
- [x] Vite + React + TypeScript 프로젝트 초기화
- [x] Tailwind CSS v4 설정 (@tailwindcss/vite)
- [x] Shadcn/ui 기본 컴포넌트 설정
  - Button, Card, Input 컴포넌트
  - cn 유틸리티 함수
- [x] React Router v7 설정
  - Protected Route 구현
  - 라우팅 구조 설정
- [x] Zustand 상태 관리 설정
  - authStore (인증 상태)
  - persist middleware
- [x] MainLayout 컴포넌트 (사이드바 네비게이션)
- [x] 페이지 컴포넌트 스캐폴딩
  - LoginPage (Google 로그인 버튼)
  - DashboardPage (대시보드)
  - ModelsPage, PromptsPage, TestPage, HistoryPage
- [x] 경로 별칭 설정 (@/*)

#### Week 3 Day 2: Auth & API Integration
- [x] OAuth 콜백 페이지 (AuthCallbackPage)
  - 인증 완료 후 리다이렉트 처리
  - 에러 핸들링
- [x] API 클라이언트 (lib/api.ts)
  - Fetch wrapper with credentials
  - 자동 토큰 리프레시
  - 타입 안전 API 함수들
  - Models, Prompts, TestRuns API
- [x] authStore 개선
  - API 클라이언트 통합
  - 로딩/에러 상태 관리

#### Week 3 Day 3: Model & Prompt Management UI
- [x] UI 컴포넌트 추가
  - Label, Textarea 컴포넌트
  - Badge 컴포넌트 (success, warning, destructive variants)
  - Dialog 컴포넌트 (React Context 기반)
- [x] ModelsPage 구현
  - 모델 목록 (카드 그리드)
  - 모델 생성/수정 다이얼로그
  - 헬스 체크 (latency 표시)
  - 활성화/비활성화 토글
  - 삭제 기능
- [x] PromptsPage 구현
  - 프롬프트 목록 (카드 그리드)
  - 프롬프트 생성/수정 다이얼로그
  - 태그 관리 (comma-separated)
  - 즐겨찾기 토글
  - 버전 히스토리 다이얼로그
  - 롤백 기능

#### Week 3 Day 4-5: Test Execution & History UI
- [x] UI 컴포넌트 추가
  - Slider 컴포넌트 (파라미터 조절)
  - Checkbox 컴포넌트 (모델 선택)
  - Select 컴포넌트 (프롬프트 템플릿 선택)
- [x] TestPage 구현
  - 모델 선택 체크박스 (다중 선택)
  - 모델별 파라미터 조절 (temperature, max_tokens, top_p)
  - 시스템 프롬프트 (템플릿 선택 또는 커스텀)
  - 사용자 메시지 입력
  - 테스트 실행 및 결과 표시
  - 결과: 응답, latency, token count, 에러 표시
- [x] HistoryPage 구현
  - 테스트 실행 히스토리 목록
  - 상세 보기 다이얼로그
  - 삭제 기능
  - 결과 비교 뷰 (모델별 응답 비교)

#### Week 4: Dashboard & Polish
- [x] Dashboard 통계 구현
  - 실시간 API 데이터 연동
  - Stats 카드 (Models, Prompts, Tests 카운트)
  - 최근 테스트 목록 (최대 5개)
  - Quick Start 가이드
  - 각 섹션 링크 연결

#### Week 5: Deployment Configuration
- [x] Docker 설정
  - Backend Dockerfile (dev/prod 멀티스테이지)
  - Frontend Dockerfile (dev/prod with nginx)
  - nginx.conf (SPA 라우팅, API 프록시)
  - docker-compose.yml (개발용)
  - docker-compose.prod.yml (프로덕션용)
- [x] 인증 우회 환경변수화 (VITE_DEV_BYPASS_AUTH)

### 🚧 진행 중 (In Progress)
- [ ] OAuth 설정 대기 (사용자)

### 📝 예정 (Planned)
- [ ] E2E 통합 테스트 (OAuth 설정 후)
- [ ] 실제 배포 테스트

### 🎯 오늘의 성과 (Today's Achievement)
Week 5 배포 설정 완료!
- Docker 멀티스테이지 빌드 (개발/프로덕션)
- 인증 우회를 환경변수로 제어 가능

### 🤔 이슈 및 결정사항 (Issues & Decisions)
- ADR-001: FastAPI 선택 (async 지원, WebSocket, Pydantic 통합)
- ADR-002: Google OAuth + JWT (httpOnly 쿠키, 1시간/7일 만료)
- ADR-003: Vite + React + Tailwind + Shadcn + Zustand
- 테스트에 SQLite+aiosqlite 사용
- Model은 소프트 삭제 패턴 사용 (is_active 플래그)
- Prompt는 content 변경 시 자동 버전 생성
- LLM 호출은 OpenAI compatible API 사용 (vLLM 호환)
- 다중 모델 테스트는 asyncio.gather로 동시 실행
- Dialog 컴포넌트: Radix 대신 React Context 기반 커스텀 구현
- Slider/Checkbox/Select: 커스텀 구현 (의존성 최소화)

### ⏭️ 다음 작업 (Next Steps)
1. OAuth 설정 완료 (사용자)
2. 통합 테스트 (Backend + Frontend)
3. 실제 LLM 모델 연동 테스트
