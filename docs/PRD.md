# PRD (Product Requirements Document)
# Local LLM Testing Platform

**Version:** 1.0  
**Last Updated:** 2026-02-10  
**Product Owner:** User  
**Target Platform:** Local Development (MacBook M3 Pro)

---

## 1. Executive Summary

### 1.1 Product Vision
개발자와 AI 연구자가 로컬 환경에서 다양한 LLM 모델을 손쉽게 테스트하고 비교할 수 있는 웹 기반 플랫폼. 시스템 프롬프트와 파라미터를 조정하며 실험할 수 있고, 실험 결과를 저장 및 관리할 수 있는 올인원 솔루션.

### 1.2 Target Users
- **Primary**: AI/ML 엔지니어, 프롬프트 엔지니어
- **Secondary**: 연구자, LLM 실험을 하는 개발자
- **Admin**: 시스템 관리자 (사용량 모니터링)

### 1.3 Success Metrics
- 단일 세션에서 3개 이상의 LLM 모델 동시 비교 가능
- 시스템 프롬프트 저장 및 재사용률 70% 이상
- 평균 응답 시간 < 3초 (로컬 LLM 서빙 기준)
- 사용자당 월 평균 50+ 테스트 실행

---

## 2. Technical Stack

### 2.1 Backend
```
Framework: FastAPI (Python 3.11+)
API Style: RESTful + WebSocket (실시간 스트리밍)
Authentication: OAuth 2.0 (Google SSO)
ORM: SQLAlchemy 2.0
Validation: Pydantic v2
```

### 2.2 Frontend
```
Recommendation: React 18 + TypeScript + Vite
UI Library: Shadcn/ui + Tailwind CSS
State Management: Zustand or TanStack Query
Real-time: WebSocket API
```

### 2.3 Infrastructure
```
Database: PostgreSQL 16 (Docker)
LLM Serving: vLLM (로컬 서빙)
Containerization: Docker + Docker Compose
Reverse Proxy: Nginx (optional, for production)
```

### 2.4 Development Environment
```
Host: MacBook M3 Pro
OS: macOS
Docker: Docker Desktop for Mac (ARM64)
Python: 3.11+ (uvicorn ASGI server)
Node: 20+ (Vite dev server)
```

---

## 3. Feature Requirements

## 3.1 Core Features (MVP - Phase 1)

### F1: User Authentication
**Priority:** P0 (Must Have)

#### F1.1 Google OAuth 2.0 Login
- **Description**: 사용자는 Google 계정으로 로그인/회원가입
- **Requirements**:
  - Google OAuth 2.0 Authorization Code Flow 구현
  - JWT 기반 세션 관리 (Access Token + Refresh Token)
  - 로그인 시 사용자 프로필 자동 생성 (email, name, profile_image)
  - 로그아웃 및 토큰 무효화 기능
- **Technical Notes**:
  ```python
  # Backend: authlib + python-jose 사용
  # Frontend: Google OAuth2 redirect flow
  # Session: httpOnly cookie + JWT
  ```
- **Acceptance Criteria**:
  - [ ] Google 로그인 버튼 클릭 시 OAuth 플로우 시작
  - [ ] 인증 성공 시 JWT 토큰 발급 및 쿠키 저장
  - [ ] 보호된 페이지는 인증 없이 접근 불가
  - [ ] 토큰 만료 시 자동 refresh

#### F1.2 User Profile Management
- **Description**: 사용자 기본 정보 관리
- **Requirements**:
  - 프로필 조회 (GET /api/v1/users/me)
  - 사용자별 고유 ID (UUID)
  - Soft delete 지원

---

### F2: LLM Model Management
**Priority:** P0 (Must Have)

#### F2.1 Model Registration
- **Description**: vLLM으로 서빙 중인 모델을 플랫폼에 등록
- **Requirements**:
  - 모델 이름, 엔드포인트 URL, API 키 (optional) 저장
  - Health check 기능 (모델 서버 연결 확인)
  - 모델별 메타데이터 저장 (max_tokens, context_length 등)
- **Database Schema**:
  ```sql
  models:
    - id (UUID, PK)
    - name (VARCHAR, e.g., "Llama-3-8B-Instruct")
    - endpoint_url (VARCHAR, e.g., "http://localhost:8000/v1")
    - api_key (VARCHAR, nullable, encrypted)
    - is_active (BOOLEAN)
    - metadata (JSONB)
    - created_at, updated_at
  ```
- **API Endpoints**:
  - `POST /api/v1/models` - 모델 등록
  - `GET /api/v1/models` - 모델 목록 조회
  - `GET /api/v1/models/{id}` - 모델 상세 조회
  - `PUT /api/v1/models/{id}` - 모델 수정
  - `DELETE /api/v1/models/{id}` - 모델 삭제 (soft delete)
  - `POST /api/v1/models/{id}/health` - Health check

#### F2.2 Model Testing Interface
- **Description**: 등록된 모델로 실시간 테스트 실행
- **Requirements**:
  - 여러 모델 동시 선택 (최대 4개 동시 비교)
  - 프롬프트 입력 필드
  - Temperature, max_tokens, top_p 등 파라미터 조정 UI
  - 스트리밍 응답 지원 (WebSocket)
  - 응답 시간 측정 (latency tracking)

---

### F3: System Prompt Management
**Priority:** P0 (Must Have)

#### F3.1 Prompt Templates (CRUD)
- **Description**: 재사용 가능한 시스템 프롬프트 저장소
- **Requirements**:
  - 프롬프트 템플릿 생성/수정/삭제
  - 템플릿 이름, 설명, 내용 저장
  - 사용자별 프롬프트 소유권 (user_id FK)
  - 즐겨찾기 기능 (is_favorite)
  - 태그 기능 (tags array)
- **Database Schema**:
  ```sql
  prompt_templates:
    - id (UUID, PK)
    - user_id (UUID, FK → users.id)
    - name (VARCHAR)
    - description (TEXT, nullable)
    - content (TEXT)
    - is_favorite (BOOLEAN, default: false)
    - tags (TEXT[], nullable)
    - created_at, updated_at
  ```
- **API Endpoints**:
  - `POST /api/v1/prompts` - 프롬프트 생성
  - `GET /api/v1/prompts` - 프롬프트 목록 (필터: tags, is_favorite)
  - `GET /api/v1/prompts/{id}` - 프롬프트 상세
  - `PUT /api/v1/prompts/{id}` - 프롬프트 수정
  - `DELETE /api/v1/prompts/{id}` - 프롬프트 삭제

#### F3.2 Prompt Version Control
- **Description**: 프롬프트 변경 이력 추적
- **Requirements**:
  - 프롬프트 수정 시 이전 버전 자동 저장
  - 버전 간 diff 비교 기능
  - 특정 버전으로 롤백 가능
- **Database Schema**:
  ```sql
  prompt_versions:
    - id (UUID, PK)
    - prompt_id (UUID, FK → prompt_templates.id)
    - version_number (INTEGER)
    - content (TEXT)
    - created_at
  ```

---

### F4: Test Execution & Results
**Priority:** P0 (Must Have)

#### F4.1 Test Run Execution
- **Description**: LLM 테스트 실행 및 결과 저장
- **Requirements**:
  - 단일/다중 모델 동시 실행
  - 실행 파라미터 저장 (temperature, max_tokens, top_p, etc.)
  - 실시간 스트리밍 응답 (WebSocket)
  - 실행 중 취소 기능
- **Database Schema**:
  ```sql
  test_runs:
    - id (UUID, PK)
    - user_id (UUID, FK)
    - prompt_template_id (UUID, FK, nullable)
    - user_message (TEXT)
    - system_prompt (TEXT, nullable)
    - created_at

  test_results:
    - id (UUID, PK)
    - test_run_id (UUID, FK)
    - model_id (UUID, FK)
    - parameters (JSONB) -- {temperature, max_tokens, top_p}
    - response (TEXT)
    - latency_ms (INTEGER)
    - token_count (INTEGER, nullable)
    - error (TEXT, nullable)
    - created_at
  ```
- **WebSocket Events**:
  ```
  Client → Server: start_test {models, prompt, params}
  Server → Client: test_started {test_run_id}
  Server → Client: stream_chunk {model_id, chunk}
  Server → Client: test_completed {model_id, result}
  ```

#### F4.2 Results Comparison
- **Description**: 여러 모델의 응답을 시각적으로 비교
- **Requirements**:
  - Side-by-side 뷰 (최대 4개 모델)
  - 응답 시간 비교 차트
  - 토큰 수 비교
  - 응답 복사/내보내기 기능

#### F4.3 Test History
- **Description**: 과거 테스트 결과 조회
- **Requirements**:
  - 사용자별 테스트 히스토리 조회
  - 필터링 (날짜, 모델, 프롬프트 템플릿)
  - 페이지네이션 (20개씩)
  - 특정 테스트 결과 재실행 기능
- **API Endpoints**:
  - `GET /api/v1/tests` - 테스트 히스토리 조회
  - `GET /api/v1/tests/{id}` - 특정 테스트 상세
  - `POST /api/v1/tests/{id}/rerun` - 동일 조건으로 재실행

---

## 3.2 Advanced Features (Phase 2)

### F5: Admin Monitoring Dashboard
**Priority:** P1 (Should Have)

#### F5.1 User Activity Monitoring
- **Description**: 전체 사용자 활동 모니터링
- **Requirements**:
  - 일별/주별/월별 사용자 수 통계
  - 사용자별 테스트 실행 횟수
  - 평균 응답 시간 추이
  - 가장 많이 사용된 모델 순위
- **Dashboard Metrics**:
  - Total Users (신규/활성/비활성)
  - Total Test Runs (Today/This Week/This Month)
  - Average Latency per Model
  - Most Used Prompts
  - Error Rate per Model

#### F5.2 System Resource Monitoring
- **Description**: 서버 리소스 사용량 모니터링
- **Requirements**:
  - vLLM 서버 상태 (UP/DOWN)
  - PostgreSQL 연결 풀 상태
  - API 응답 시간 분포
  - 에러 로그 수집 및 알림
- **Tech Stack**:
  - Prometheus + Grafana (optional)
  - 또는 내장 대시보드 (FastAPI + Chart.js)

#### F5.3 Admin Controls
- **Requirements**:
  - 사용자 계정 활성화/비활성화
  - 모델 강제 비활성화 (점검 모드)
  - 시스템 공지사항 등록
  - 데이터베이스 백업 트리거

---

## 4. Database Schema (ER Diagram)

```
┌─────────────┐         ┌──────────────────┐
│   users     │────1:N──│ prompt_templates │
└─────────────┘         └──────────────────┘
      │                          │
      │                          │ 1:N
      │                          ▼
      │                  ┌──────────────────┐
      │                  │ prompt_versions  │
      │                  └──────────────────┘
      │
      │ 1:N
      ▼
┌─────────────┐         ┌──────────────────┐
│ test_runs   │────1:N──│  test_results    │
└─────────────┘         └──────────────────┘
                                 │
                                 │ N:1
                                 ▼
                        ┌──────────────────┐
                        │     models       │
                        └──────────────────┘
```

### Complete Schema

```sql
-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    profile_image VARCHAR(512),
    google_id VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_admin BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Models Table
CREATE TABLE models (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    endpoint_url VARCHAR(512) NOT NULL,
    api_key VARCHAR(512), -- encrypted
    is_active BOOLEAN DEFAULT true,
    metadata JSONB, -- {max_tokens, context_length, model_type}
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Prompt Templates Table
CREATE TABLE prompt_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    content TEXT NOT NULL,
    is_favorite BOOLEAN DEFAULT false,
    tags TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Prompt Versions Table
CREATE TABLE prompt_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    prompt_id UUID NOT NULL REFERENCES prompt_templates(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(prompt_id, version_number)
);

-- Test Runs Table
CREATE TABLE test_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    prompt_template_id UUID REFERENCES prompt_templates(id) ON DELETE SET NULL,
    user_message TEXT NOT NULL,
    system_prompt TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Test Results Table
CREATE TABLE test_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    test_run_id UUID NOT NULL REFERENCES test_runs(id) ON DELETE CASCADE,
    model_id UUID NOT NULL REFERENCES models(id) ON DELETE CASCADE,
    parameters JSONB NOT NULL, -- {temperature, max_tokens, top_p, etc.}
    response TEXT,
    latency_ms INTEGER,
    token_count INTEGER,
    error TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_google_id ON users(google_id);
CREATE INDEX idx_prompts_user_id ON prompt_templates(user_id);
CREATE INDEX idx_prompts_tags ON prompt_templates USING GIN(tags);
CREATE INDEX idx_test_runs_user_id ON test_runs(user_id);
CREATE INDEX idx_test_results_test_run_id ON test_results(test_run_id);
CREATE INDEX idx_test_results_model_id ON test_results(model_id);
```

---

## 5. API Specification

### 5.1 Authentication Endpoints

```
POST   /api/v1/auth/google/login      # Google OAuth 시작
GET    /api/v1/auth/google/callback   # OAuth 콜백
POST   /api/v1/auth/refresh           # Token refresh
POST   /api/v1/auth/logout            # 로그아웃
GET    /api/v1/auth/me                # 현재 사용자 정보
```

### 5.2 Model Management Endpoints

```
GET    /api/v1/models                 # 모델 목록
POST   /api/v1/models                 # 모델 등록
GET    /api/v1/models/{id}            # 모델 상세
PUT    /api/v1/models/{id}            # 모델 수정
DELETE /api/v1/models/{id}            # 모델 삭제
POST   /api/v1/models/{id}/health     # Health check
```

### 5.3 Prompt Management Endpoints

```
GET    /api/v1/prompts                # 프롬프트 목록
POST   /api/v1/prompts                # 프롬프트 생성
GET    /api/v1/prompts/{id}           # 프롬프트 상세
PUT    /api/v1/prompts/{id}           # 프롬프트 수정
DELETE /api/v1/prompts/{id}           # 프롬프트 삭제
GET    /api/v1/prompts/{id}/versions  # 버전 히스토리
POST   /api/v1/prompts/{id}/rollback  # 버전 롤백
```

### 5.4 Test Execution Endpoints

```
POST   /api/v1/tests                  # 테스트 실행
GET    /api/v1/tests                  # 테스트 히스토리
GET    /api/v1/tests/{id}             # 테스트 상세
POST   /api/v1/tests/{id}/rerun       # 재실행
WS     /ws/tests                      # 스트리밍 WebSocket
```

### 5.5 Admin Endpoints

```
GET    /api/v1/admin/stats            # 시스템 통계
GET    /api/v1/admin/users            # 사용자 관리
PUT    /api/v1/admin/users/{id}       # 사용자 상태 변경
GET    /api/v1/admin/logs             # 에러 로그
```

---

## 6. Non-Functional Requirements

### 6.1 Performance
- API 응답 시간: < 200ms (스트리밍 제외)
- LLM 응답 시작 시간: < 1초 (First Token Latency)
- 동시 접속자: 최대 10명 (로컬 환경 기준)
- Database 쿼리: < 100ms (인덱스 최적화)

### 6.2 Security
- **Authentication**: JWT (Access: 1시간, Refresh: 7일)
- **HTTPS**: Nginx SSL 인증서 (프로덕션 시)
- **SQL Injection**: SQLAlchemy ORM + Parameterized Queries
- **XSS**: Frontend input sanitization
- **CORS**: 화이트리스트 기반 (localhost:3000, localhost:5173)
- **API Key Encryption**: Fernet symmetric encryption (DB 저장 시)

### 6.3 Scalability
- **Database Connection Pool**: Max 20 connections
- **Rate Limiting**: 사용자당 분당 60 requests
- **File Upload**: 프롬프트 최대 10KB
- **WebSocket**: 연결당 최대 5분 (idle timeout)

### 6.4 Monitoring
- **Logging**: Structured JSON logs (info, warning, error)
- **Health Check**: `/health` endpoint (DB + vLLM status)
- **Metrics**: Response time, error rate, request count

### 6.5 Data Management
- **Backup**: 일별 PostgreSQL 백업 (pg_dump)
- **Retention**: 테스트 결과 90일 보관
- **GDPR**: 사용자 데이터 삭제 요청 지원 (계정 삭제)

---

## 7. User Stories

### MVP Stories

#### US-1: Google Login (사용자)
```
As a user
I want to login with my Google account
So that I don't need to create a new password
```
**Acceptance Criteria**:
- Google 로그인 버튼이 홈페이지에 표시됨
- 로그인 성공 시 대시보드로 리디렉션
- 프로필 이미지와 이름이 헤더에 표시됨

#### US-2: Add LLM Model (사용자)
```
As a user
I want to register my local LLM server
So that I can test it through the platform
```
**Acceptance Criteria**:
- 모델 이름, endpoint URL 입력 가능
- Health check 버튼으로 연결 확인
- 등록된 모델이 모델 목록에 표시됨

#### US-3: Create System Prompt (사용자)
```
As a user
I want to save system prompts as templates
So that I can reuse them for different tests
```
**Acceptance Criteria**:
- 프롬프트 이름, 내용, 태그 입력 가능
- 저장된 프롬프트가 목록에 표시됨
- 즐겨찾기 별표 토글 가능

#### US-4: Run LLM Test (사용자)
```
As a user
I want to test multiple models with the same prompt
So that I can compare their responses side-by-side
```
**Acceptance Criteria**:
- 최대 4개 모델 동시 선택 가능
- Temperature 슬라이더로 조정 가능
- 각 모델의 응답이 실시간으로 스트리밍됨
- 응답 시간이 각 카드에 표시됨

#### US-5: View Test History (사용자)
```
As a user
I want to see my past test results
So that I can track my experiments
```
**Acceptance Criteria**:
- 테스트 목록이 최신순으로 표시됨
- 각 테스트를 클릭하면 상세 결과 확인 가능
- 동일 조건으로 재실행 버튼 제공

### Phase 2 Stories

#### US-6: Admin Dashboard (관리자)
```
As an admin
I want to see platform usage statistics
So that I can monitor system health
```
**Acceptance Criteria**:
- 일별 사용자 수 그래프
- 모델별 평균 응답 시간
- 에러 발생 횟수 표시

---

## 8. UI/UX Wireframes (Text-based)

### 8.1 Login Page
```
┌────────────────────────────────────────┐
│                                        │
│         🤖 LLM Test Platform          │
│                                        │
│   Test and Compare Local LLM Models   │
│                                        │
│   ┌──────────────────────────────┐   │
│   │  [G] Sign in with Google     │   │
│   └──────────────────────────────┘   │
│                                        │
└────────────────────────────────────────┘
```

### 8.2 Dashboard (Main)
```
┌─────────────────────────────────────────────────┐
│ 🤖 Platform    [Models] [Prompts] [Tests] [@Me]│
├─────────────────────────────────────────────────┤
│                                                 │
│  Quick Start                                    │
│  ┌───────────┐ ┌───────────┐ ┌──────────────┐ │
│  │ + Add     │ │ + Create  │ │ ▶ Run Test   │ │
│  │   Model   │ │   Prompt  │ │              │ │
│  └───────────┘ └───────────┘ └──────────────┘ │
│                                                 │
│  Recent Tests                                   │
│  ┌───────────────────────────────────────────┐ │
│  │ Test #123 - 2 models - 2min ago          │ │
│  │ "Explain quantum computing..."            │ │
│  └───────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────┐ │
│  │ Test #122 - 3 models - 1 hour ago        │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

### 8.3 Test Execution Page
```
┌─────────────────────────────────────────────────┐
│ New Test                                        │
├─────────────────────────────────────────────────┤
│ Select Models:                                  │
│ [✓] Llama-3-8B   [✓] Mistral-7B  [ ] GPT-2    │
│                                                 │
│ System Prompt:                                  │
│ [Load Template ▼] [Save as Template]          │
│ ┌─────────────────────────────────────────┐   │
│ │ You are a helpful assistant...          │   │
│ │                                         │   │
│ └─────────────────────────────────────────┘   │
│                                                 │
│ User Message:                                   │
│ ┌─────────────────────────────────────────┐   │
│ │ Explain machine learning in simple terms│   │
│ └─────────────────────────────────────────┘   │
│                                                 │
│ Parameters:                                     │
│ Temperature: 0.7  [━━━━━━━●━━] 1.0            │
│ Max Tokens:  512  [━━●━━━━━━━] 2048           │
│                                                 │
│                 [▶ Run Test]                   │
│                                                 │
│ Results:                                        │
│ ┌──────────────┐ ┌──────────────┐             │
│ │ Llama-3-8B   │ │ Mistral-7B   │             │
│ │ ⏱ 2.3s       │ │ ⏱ 1.8s       │             │
│ │──────────────│ │──────────────│             │
│ │ Machine      │ │ Machine      │             │
│ │ learning is..│ │ learning is..│             │
│ │              │ │              │             │
│ └──────────────┘ └──────────────┘             │
└─────────────────────────────────────────────────┘
```

---

## 9. Development Phases

### Phase 1: MVP (Weeks 1-4)
**Goal**: Core functionality - 사용자가 로컬 LLM을 테스트할 수 있음

**Week 1**: Backend Foundation
- [ ] FastAPI 프로젝트 초기화
- [ ] PostgreSQL Docker Compose 설정
- [ ] SQLAlchemy models + Alembic migrations
- [ ] Google OAuth 2.0 구현
- [ ] JWT authentication middleware

**Week 2**: Core APIs
- [ ] Model CRUD APIs
- [ ] Prompt Template CRUD APIs
- [ ] Test Execution API (동기 방식)
- [ ] vLLM integration (OpenAI-compatible API)

**Week 3**: Frontend Foundation
- [ ] React + TypeScript 프로젝트 초기화
- [ ] Login page + OAuth flow
- [ ] Dashboard layout
- [ ] Model management UI
- [ ] Prompt management UI

**Week 4**: Test Execution UI
- [ ] Test execution form
- [ ] WebSocket integration (스트리밍)
- [ ] Results comparison view
- [ ] Test history page
- [ ] E2E testing

### Phase 2: Advanced Features (Weeks 5-6)
**Goal**: 프로덕션 레벨 기능 추가

**Week 5**: Admin & Monitoring
- [ ] Admin dashboard UI
- [ ] User activity tracking
- [ ] System metrics API
- [ ] Error logging system

**Week 6**: Polish & Optimization
- [ ] Performance optimization
- [ ] UI/UX improvements
- [ ] Documentation
- [ ] Docker Compose 전체 스택 구성

---

## 10. Technical Implementation Notes

### 10.1 Google OAuth 2.0 구현 가이드

#### Backend (FastAPI)
```python
# requirements.txt
authlib==1.3.0
python-jose[cryptography]==3.3.0
httpx==0.26.0

# config.py
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "http://localhost:8000/api/v1/auth/google/callback"

# auth.py
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

@router.get("/auth/google/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback")
async def auth_callback(request: Request, db: Session):
    token = await oauth.google.authorize_access_token(request)
    user_info = token['userinfo']
    
    # Create or get user
    user = get_or_create_user(db, user_info)
    
    # Create JWT
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    
    # Set httpOnly cookie
    response = RedirectResponse(url='/dashboard')
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # HTTPS only
        samesite='lax'
    )
    return response
```

#### Frontend (React)
```typescript
// Google 로그인 버튼
const handleGoogleLogin = () => {
  window.location.href = 'http://localhost:8000/api/v1/auth/google/login';
};

// Axios interceptor for JWT
axios.interceptors.request.use(config => {
  // httpOnly cookie는 자동으로 전송됨
  config.withCredentials = true;
  return config;
});

// 401 Unauthorized 시 refresh token 사용
axios.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      await axios.post('/api/v1/auth/refresh', {}, { withCredentials: true });
      return axios.request(error.config);
    }
    return Promise.reject(error);
  }
);
```

### 10.2 vLLM Integration

#### vLLM 서버 실행 (로컬)
```bash
# vLLM 설치 (M3 Pro에서는 CPU 모드 또는 MPS 사용)
pip install vllm

# 모델 서빙 (OpenAI-compatible API)
vllm serve meta-llama/Llama-3-8B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --api-key your-api-key-here
```

#### Backend에서 vLLM 호출
```python
import httpx

async def call_vllm(endpoint: str, prompt: str, params: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{endpoint}/v1/chat/completions",
            json={
                "model": "meta-llama/Llama-3-8B-Instruct",
                "messages": [
                    {"role": "system", "content": params.get("system_prompt", "")},
                    {"role": "user", "content": prompt}
                ],
                "temperature": params.get("temperature", 0.7),
                "max_tokens": params.get("max_tokens", 512),
                "stream": True  # 스트리밍 활성화
            },
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60.0
        )
        
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                chunk = json.loads(line[6:])
                yield chunk["choices"][0]["delta"].get("content", "")
```

### 10.3 WebSocket Streaming
```python
# backend/websocket.py
@app.websocket("/ws/tests")
async def websocket_endpoint(websocket: WebSocket, db: Session):
    await websocket.accept()
    
    try:
        data = await websocket.receive_json()
        test_run = create_test_run(db, data)
        
        # 여러 모델 동시 실행
        async for model_id, chunk in stream_multiple_models(data["models"], data["prompt"]):
            await websocket.send_json({
                "type": "chunk",
                "model_id": model_id,
                "content": chunk
            })
        
        await websocket.send_json({"type": "completed"})
    except WebSocketDisconnect:
        pass
```

```typescript
// frontend/useWebSocket.ts
const ws = new WebSocket('ws://localhost:8000/ws/tests');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  
  if (data.type === 'chunk') {
    setResponses(prev => ({
      ...prev,
      [data.model_id]: prev[data.model_id] + data.content
    }));
  }
};

ws.send(JSON.stringify({
  models: ['model-1', 'model-2'],
  prompt: 'Hello world',
  params: { temperature: 0.7 }
}));
```

---

## 11. Docker Compose Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: llm_platform
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://admin:password@postgres:5432/llm_platform
      GOOGLE_CLIENT_ID: ${GOOGLE_CLIENT_ID}
      GOOGLE_CLIENT_SECRET: ${GOOGLE_CLIENT_SECRET}
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    command: npm run dev -- --host
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    environment:
      VITE_API_URL: http://localhost:8000

volumes:
  postgres_data:
```

---

## 12. Security Checklist

- [ ] **환경변수 보호**: `.env` 파일이 `.gitignore`에 포함되어 있고 Git에 추적되지 않음
- [ ] **환경변수 템플릿**: `.env.example` 파일만 Git에 포함되고 실제 비밀키 없음
- [ ] **비밀키 강도**: SECRET_KEY 최소 32자 이상, 무작위 생성
- [ ] Google OAuth 2.0 올바르게 구현 (PKCE 사용 권장)
- [ ] JWT secret key 환경 변수로 관리
- [ ] API key는 Fernet으로 암호화 후 DB 저장
- [ ] SQL Injection 방지 (SQLAlchemy ORM 사용)
- [ ] XSS 방지 (React는 기본적으로 escape 처리)
- [ ] CSRF 방지 (SameSite cookie 설정)
- [ ] Rate limiting 구현 (FastAPI-limiter)
- [ ] HTTPS 적용 (프로덕션 시)
- [ ] CORS whitelist 설정
- [ ] Input validation (Pydantic models)

---

## 13. Testing Strategy

### Unit Tests
- Database models (SQLAlchemy)
- API endpoints (pytest + TestClient)
- Authentication logic
- vLLM integration mocking

### Integration Tests
- OAuth flow (end-to-end)
- WebSocket streaming
- Database transactions

### E2E Tests
- Playwright/Cypress
- User journey: Login → Create Prompt → Run Test

---

## 14. Deployment Checklist (로컬 환경)

### ⚠️ 배포 전 보안 확인
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인
- [ ] `git status`로 `.env` 파일이 추적되지 않는지 확인
- [ ] `.env.example` 파일에 실제 비밀키가 없는지 확인
- [ ] GitHub 레포지토리에 환경변수가 노출되지 않았는지 확인

### 환경 설정
- [ ] Docker Compose로 PostgreSQL 실행
- [ ] vLLM 서버 백그라운드 실행
- [ ] Backend `.env.example`을 복사하여 `.env` 생성
- [ ] Frontend `.env.example`을 복사하여 `.env.local` 생성
- [ ] `.env` 파일에 실제 비밀키 입력 (절대 Git에 커밋 X)
- [ ] Database migrations 실행 (`alembic upgrade head`)
- [ ] 초기 admin 계정 생성 (seed script)
- [ ] Health check 엔드포인트 확인 (`/health`)

---

## 15. Success Criteria (Definition of Done)

### MVP 완료 기준
- [ ] Google 로그인으로 회원가입/로그인 가능
- [ ] 최소 1개 이상의 vLLM 모델 등록 가능
- [ ] 시스템 프롬프트 CRUD 가능
- [ ] 최소 2개 모델 동시 테스트 실행 및 비교 가능
- [ ] 스트리밍 응답이 실시간으로 표시됨
- [ ] 테스트 히스토리 조회 가능
- [ ] 모든 API가 200ms 이내 응답 (스트리밍 제외)

### Phase 2 완료 기준
- [ ] Admin 대시보드에서 사용자 통계 확인 가능
- [ ] 모델별 평균 응답 시간 그래프 표시
- [ ] 에러 로그 수집 및 표시
- [ ] 전체 시스템 Docker Compose로 한 번에 실행 가능

---

## 16. Open Questions & Decisions Needed

1. **Frontend Framework 최종 결정**
   - Option A: React + TypeScript (추천)
   - Option B: Vue 3 + TypeScript
   - Option C: Svelte + TypeScript
   - **Decision**: React 18 + TypeScript (생태계 성숙도, Shadcn/ui 사용)

2. **프롬프트 버전 관리 UI**
   - Git-style diff viewer 필요한가? (Phase 2로 미루기)
   - 단순 목록 표시로 시작

3. **vLLM API Key 관리**
   - 사용자별 개인 API key vs 시스템 공통 key
   - **Decision**: 모델 등록 시 optional로 받기

4. **Admin 권한 부여 방식**
   - 수동 DB 업데이트 vs 최초 가입자 자동 admin
   - **Decision**: 환경 변수로 admin 이메일 지정

---

## 17. Resources & References

### Documentation
- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy 2.0: https://docs.sqlalchemy.org/
- vLLM: https://docs.vllm.ai/
- Google OAuth 2.0: https://developers.google.com/identity/protocols/oauth2

### Libraries
- Backend: `fastapi`, `sqlalchemy`, `alembic`, `authlib`, `python-jose`, `httpx`, `websockets`
- Frontend: `react`, `typescript`, `vite`, `@tanstack/react-query`, `zustand`, `axios`, `shadcn/ui`

### Tools
- Database Client: TablePlus, pgAdmin
- API Testing: Postman, Hoppscotch
- WebSocket Testing: wscat, Postman

---

## Appendix A: Environment Variables

### ⚠️ CRITICAL SECURITY WARNING ⚠️

**환경변수 파일은 절대로 Git에 푸시하면 안 됩니다!**

```bash
# ❌ 절대 하지 말 것
git add .env
git add .env.local
git commit -m "add config"  # 🚨 보안 사고!

# ✅ 올바른 방법
# .env 파일은 .gitignore에 추가되어 있어야 함
# .env.example 파일만 Git에 포함
```

### 환경변수 파일 관리 규칙

1. **실제 환경변수 파일** (Git에 푸시 ❌)
   - `backend/.env` - 실제 비밀키, API 키 포함
   - `frontend/.env.local` - 실제 API 엔드포인트
   
2. **예시 파일** (Git에 푸시 ✅)
   - `backend/.env.example` - 플레이스홀더 값만
   - `frontend/.env.example` - 플레이스홀더 값만

3. **필수 .gitignore 항목**
   ```gitignore
   # Environment variables
   .env
   .env.local
   .env.*.local
   **/.env
   **/.env.local
   ```

### Backend .env.example (Git에 포함)

```bash
# Database Configuration
DATABASE_URL=postgresql://admin:password@localhost:5432/llm_platform

# Security Keys (CHANGE THESE IN PRODUCTION!)
SECRET_KEY=your-secret-key-here-min-32-chars-CHANGE-THIS
ENCRYPTION_KEY=your-fernet-encryption-key-CHANGE-THIS

# Google OAuth 2.0 (Get from Google Cloud Console)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/v1/auth/google/callback

# Admin Configuration
ADMIN_EMAILS=admin@example.com,owner@example.com

# Optional: API Keys for external services
# BRAVE_API_KEY=your-brave-api-key
# SLACK_BOT_TOKEN=xoxb-your-slack-token
```

### Frontend .env.example (Git에 포함)

```bash
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Optional: Feature Flags
# VITE_ENABLE_ANALYTICS=false
# VITE_ENABLE_DEBUG=true
```

### 실제 .env 파일 생성 방법

```bash
# Backend
cd backend
cp .env.example .env
# .env 파일을 열어서 실제 값으로 수정
nano .env

# Frontend  
cd frontend
cp .env.example .env.local
# .env.local 파일을 열어서 실제 값으로 수정
nano .env.local
```

### 비밀키 생성 방법

```python
# SECRET_KEY 생성
python -c "import secrets; print(secrets.token_urlsafe(32))"

# ENCRYPTION_KEY (Fernet) 생성
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

---

## Appendix B: Sample Data

```sql
-- Sample Models
INSERT INTO models (name, endpoint_url, is_active) VALUES
('Llama-3-8B-Instruct', 'http://localhost:8000', true),
('Mistral-7B-Instruct', 'http://localhost:8001', true);

-- Sample Prompt Template
INSERT INTO prompt_templates (user_id, name, content, tags) VALUES
('user-uuid-here', 'Helpful Assistant', 'You are a helpful AI assistant.', ARRAY['general', 'assistant']);
```

---

**Document Version:** 1.0  
**Last Reviewed:** 2026-02-10  
**Status:** ✅ Ready for Development