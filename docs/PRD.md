# PRD (Product Requirements Document)
# Local LLM Testing Platform

**Version:** 1.1
**Last Updated:** 2026-02-11

---

## 1. Executive Summary

### 1.1 Product Vision
로컬 환경에서 다양한 LLM 모델을 테스트하고 비교할 수 있는 웹 기반 플랫폼.

### 1.2 Target Users
- **Primary**: AI/ML 엔지니어, 프롬프트 엔지니어
- **Secondary**: 연구자, LLM 실험 개발자
- **Admin**: 시스템 관리자

### 1.3 Success Metrics
- 3개 이상 LLM 모델 동시 비교
- 시스템 프롬프트 재사용률 70%+
- 평균 응답 시간 < 3초

---

## 2. Technical Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, SQLAlchemy 2.0, Pydantic v2 |
| Frontend | React 18 + TypeScript + Vite |
| UI | Shadcn/ui + Tailwind CSS |
| State | Zustand |
| Auth | Google OAuth 2.0 + JWT |
| Database | PostgreSQL 16 |
| LLM | vLLM (OpenAI-compatible API) |

---

## 3. Feature Requirements

### F1: User Authentication (P0)
- Google OAuth 2.0 로그인
- JWT 세션 관리 (httpOnly cookie)
- 자동 토큰 리프레시

### F2: Model Management (P0)
- 모델 CRUD (이름, endpoint URL, API key)
- Health check 기능
- 최대 4개 모델 동시 비교

### F3: Prompt Management (P0)
- 프롬프트 템플릿 CRUD
- 버전 관리 (자동 저장, 롤백)
- 즐겨찾기, 태그 기능

### F4: Test Execution (P0)
- 다중 모델 동시 실행
- 실시간 스트리밍 (WebSocket)
- 파라미터 조정 (temperature, max_tokens, top_p)
- 결과 비교 (side-by-side)
- 테스트 히스토리 저장

### F5: Admin Dashboard (P1 - Phase 2)
- 사용자 활동 통계
- 모델별 성능 메트릭
- 시스템 모니터링

---

## 4. Database Schema

```
┌─────────────┐         ┌──────────────────┐
│   users     │────1:N──│ prompt_templates │
└─────────────┘         └──────────────────┘
      │                          │ 1:N
      │                          ▼
      │                  ┌──────────────────┐
      │                  │ prompt_versions  │
      │                  └──────────────────┘
      │ 1:N
      ▼
┌─────────────┐         ┌──────────────────┐
│ test_runs   │────1:N──│  test_results    │
└─────────────┘         └──────────────────┘
                                 │ N:1
                                 ▼
                        ┌──────────────────┐
                        │     models       │
                        └──────────────────┘
```

### Tables
- **users**: id, email, name, google_id, is_admin
- **models**: id, name, model_name, endpoint_url, api_key, is_active, metadata
- **prompt_templates**: id, user_id, name, content, tags, is_favorite
- **prompt_versions**: id, prompt_id, version_number, content
- **test_runs**: id, user_id, prompt_template_id, user_message, system_prompt
- **test_results**: id, test_run_id, model_id, parameters, response, latency_ms, error

---

## 5. API Endpoints

### Authentication
```
GET    /api/v1/auth/google/login
GET    /api/v1/auth/google/callback
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
GET    /api/v1/auth/me
```

### Models
```
GET    /api/v1/models
POST   /api/v1/models
GET    /api/v1/models/{id}
PUT    /api/v1/models/{id}
DELETE /api/v1/models/{id}
POST   /api/v1/models/{id}/health
```

### Prompts
```
GET    /api/v1/prompts
POST   /api/v1/prompts
GET    /api/v1/prompts/{id}
PUT    /api/v1/prompts/{id}
DELETE /api/v1/prompts/{id}
POST   /api/v1/prompts/{id}/favorite
GET    /api/v1/prompts/{id}/versions
POST   /api/v1/prompts/{id}/rollback
```

### Test Runs
```
POST   /api/v1/test-runs
GET    /api/v1/test-runs
GET    /api/v1/test-runs/{id}
DELETE /api/v1/test-runs/{id}
WS     /ws/tests (스트리밍)
```

---

## 6. Non-Functional Requirements

### Performance
- API 응답: < 200ms
- First Token Latency: < 1초
- 동시 접속: 10명

### Security
- JWT (Access: 1시간, Refresh: 7일)
- API Key 암호화 (Fernet)
- CORS 화이트리스트
- Rate Limiting: 60 req/min

---

## 7. Development Phases

### Phase 1: MVP (Week 1-4)
- **Week 1**: Backend Foundation + Google OAuth
- **Week 2**: Model, Prompt, Test APIs
- **Week 3**: Frontend Foundation + Auth UI
- **Week 4**: WebSocket 스트리밍 + Test UI

### Phase 2: Advanced (Week 5-6)
- **Week 5**: Admin Dashboard
- **Week 6**: Polish & Optimization

---

## 8. User Stories (MVP)

| ID | Story | Acceptance Criteria |
|----|-------|---------------------|
| US-1 | Google 로그인 | 로그인 버튼 → OAuth → 대시보드 리디렉션 |
| US-2 | 모델 등록 | 이름/URL 입력 → Health check → 목록 표시 |
| US-3 | 프롬프트 저장 | 이름/내용/태그 입력 → 저장 → 목록 표시 |
| US-4 | 테스트 실행 | 모델 선택 → 프롬프트 입력 → 실시간 스트리밍 |
| US-5 | 히스토리 조회 | 목록 표시 → 상세 보기 → 재실행 |

---

## 9. Success Criteria

### MVP 완료 기준
- [ ] Google 로그인 작동
- [ ] 모델 등록/관리 가능
- [ ] 프롬프트 CRUD + 버전 관리
- [ ] 2개+ 모델 동시 테스트 및 비교
- [ ] 스트리밍 응답 실시간 표시
- [ ] 테스트 히스토리 조회

---

**Document Version:** 1.1
**Status:** ✅ Development in Progress
