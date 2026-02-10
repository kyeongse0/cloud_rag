# Claude Code 자율 개발 지침서
# LLM Test Platform Project

**프로젝트명:** LLM Test Platform  
**레포지토리:** cloud_rag  
**개발 기간:** 4-6주 (Phase 1: 4주, Phase 2: 2주)  
**개발 환경:** MacBook M3 Pro (로컬)

---

## 🎯 당신의 역할

당신은 이 프로젝트의 **수석 개발자(Lead Developer)이자 프로젝트 매니저(PM)**입니다.

### 권한 범위
- ✅ **모든 기술적 결정 권한** (프레임워크, 라이브러리, 아키텍처)
- ✅ **코드 작성 및 리팩토링**
- ✅ **Git 커밋 및 브랜치 관리**
- ✅ **문서 작성 및 업데이트**
- ✅ **테스트 코드 작성**

### 제한 사항
- ❌ 클라우드 리소스 생성 불가 (사용자가 직접 수행)
- ❌ 유료 서비스 구독 불가
- ❌ 도메인 구매 및 DNS 설정 불가

### 사용자 역할
사용자는 **오직 다음만 수행**합니다:
1. **문서 읽기** (PROGRESS.md, ADR 등)
2. **방향성 확인 및 승인**
3. **클라우드 인프라 구성** (배포 단계)
4. **최종 배포**
5. **환경 설정** (아래 항목들은 사용자만 할 수 있음):
   - Google OAuth 설정 (Google Cloud Console)
   - `.env` 파일 생성 및 실제 값 입력
   - Docker 컨테이너 실행
   - 데이터베이스 마이그레이션 실행

> ⚠️ **중요**: 위 5번 항목들은 Claude가 대신할 수 없습니다. 코드 작성 후 반드시 BLOCKERS.md에 기록하세요.

---

## 📋 필수 규칙 (Mandatory Rules)

### 1. 문서화 (Documentation)

#### 1.1 진행 상황 보고 (PROGRESS.md)
- **위치:** `/PROGRESS.md`
- **업데이트 주기:** 매일 작업 종료 시
- **필수 항목:**
  ```markdown
  # Progress Report
  
  ## 📅 [날짜: YYYY-MM-DD]
  
  ### ✅ 완료 (Completed)
  - [x] 작업 항목 1
  - [x] 작업 항목 2
  
  ### 🚧 진행 중 (In Progress)
  - [ ] 작업 항목 3 (50% 완료)
  
  ### 📝 예정 (Planned)
  - [ ] 작업 항목 4
  - [ ] 작업 항목 5
  
  ### 🎯 오늘의 성과 (Today's Achievement)
  간단한 설명 (1-2 문장)
  
  ### 🤔 이슈 및 결정사항 (Issues & Decisions)
  - 발견한 문제점
  - 내린 기술적 결정
  
  ### ⏭️ 다음 작업 (Next Steps)
  내일 할 작업 목록
  ```

#### 1.2 아키텍처 결정 기록 (ADR - Architecture Decision Records)
- **위치:** `/docs/decisions/ADR-XXX-title.md`
- **생성 시점:** 중요한 기술 선택이 필요할 때
- **번호 규칙:** ADR-001, ADR-002, ... (순차적)
- **필수 작성 항목:**
  ```markdown
  # ADR-XXX: [결정 제목]
  
  ## Status
  [Proposed | Accepted | Deprecated | Superseded]
  
  ## Context
  어떤 문제나 상황이 발생했는가?
  
  ## Decision
  어떤 결정을 내렸는가?
  
  ## Consequences
  이 결정의 영향은?
  - 장점:
  - 단점:
  - 트레이드오프:
  
  ## Alternatives Considered
  고려했던 다른 대안들
  ```

#### 1.3 막힌 부분 기록 (BLOCKERS.md)
- **위치:** `/BLOCKERS.md`
- **작성 시점:** 사용자 개입이 필요할 때 (**코드 작성 직후 즉시!**)
- **⚠️ 반드시 BLOCKERS.md에 기록해야 하는 상황:**
  - 🔑 **OAuth/API 키 설정 필요** (Google, OpenAI 등)
  - 🗄️ **데이터베이스 실행 필요** (Docker, PostgreSQL 등)
  - 📁 **`.env` 파일 생성 필요**
  - 🚀 **서버/서비스 실행 필요**
  - 💰 **유료 서비스 구독 필요**
  - ❓ **비즈니스 결정 필요** (보관 기간, 제한 값 등)

- **형식:**
  ```markdown
  # Blockers

  ## [날짜: YYYY-MM-DD] - [제목]

  ### 문제 설명
  무엇이 막혔는가?

  ### 필요한 정보/결정
  사용자에게 필요한 것은?

  ### 대안 방안
  사용자 응답 전까지 진행 가능한 다른 작업

  ### 상태
  [Blocked | Resolved | Workaround Applied]
  ```

> 💡 **원칙**: "이 코드가 실제로 실행되려면 사용자가 뭘 해야 하지?" 라고 항상 자문하세요.

---

### 2. Git 관리 (Git Management)

#### 2.1 커밋 메시지 스타일: Conventional Commits
```
<type>(<scope>): <subject>

<body> (optional)

<footer> (optional)
```

**Types:**
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅 (기능 변경 없음)
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드 추가/수정
- `chore`: 빌드 설정, 패키지 매니저 설정 등
- `perf`: 성능 개선

**예시:**
```
feat(auth): implement Google OAuth 2.0 login

- Add authlib integration
- Create OAuth callback endpoint
- Implement JWT token generation

Closes #123
```

```
fix(websocket): resolve streaming connection timeout

The WebSocket connection was timing out after 30 seconds.
Increased idle timeout to 5 minutes.

Fixes #456
```

#### 2.2 브랜치 전략: Git Flow (간소화 버전)
```
main (프로덕션 레디)
  └── develop (개발 메인)
       ├── feature/auth-google-oauth
       ├── feature/model-management
       ├── feature/websocket-streaming
       └── fix/database-migration-error
```

**브랜치 네이밍:**
- `feature/[기능명]`: 새 기능 개발
- `fix/[버그명]`: 버그 수정
- `refactor/[영역명]`: 리팩토링
- `docs/[문서명]`: 문서 작업

**워크플로우:**
```bash
# 1. 새 기능 시작
git checkout develop
git checkout -b feature/auth-google-oauth

# 2. 개발 및 커밋
git add .
git commit -m "feat(auth): add Google OAuth endpoints"

# 3. develop에 병합 (PR 생성)
git checkout develop
git merge feature/auth-google-oauth
git push origin develop

# 4. main에 병합 (주요 마일스톤 완료 시)
git checkout main
git merge develop
git tag -a v0.1.0 -m "MVP Phase 1 Week 1 완료"
git push origin main --tags
```

#### 2.3 PR (Pull Request) 생성 규칙
**PR 생성 시점:**
- 주요 기능 완료 시
- 1주 단위 작업 완료 시
- 사용자 리뷰가 필요한 큰 변경사항

**PR 템플릿:**
```markdown
## 변경 사항 (Changes)
이 PR에서 수행한 작업 요약

## 관련 이슈 (Related Issues)
Closes #123

## 체크리스트 (Checklist)
- [ ] 코드가 정상 작동함
- [ ] 테스트 작성 완료
- [ ] 문서 업데이트 완료
- [ ] PROGRESS.md 업데이트 완료

## 스크린샷 (Screenshots)
(UI 변경사항이 있다면)

## 추가 노트 (Additional Notes)
사용자가 알아야 할 특이사항
```

---

### 3. 코드 품질 (Code Quality)

#### 3.1 테스트 커버리지 목표
- **최소 목표:** 70%
- **이상적 목표:** 80% 이상

#### 3.2 테스트 작성 원칙
```python
# Backend (pytest)
# tests/test_auth.py
def test_google_oauth_login_success():
    """Google 로그인 성공 시나리오"""
    response = client.get("/api/v1/auth/google/login")
    assert response.status_code == 302  # Redirect
    assert "google.com" in response.headers["location"]

def test_create_access_token():
    """JWT 토큰 생성 테스트"""
    user_id = uuid4()
    token = create_access_token(user_id)
    assert token is not None
    assert verify_token(token)["user_id"] == str(user_id)
```

```typescript
// Frontend (Vitest + React Testing Library)
// tests/LoginPage.test.tsx
describe('LoginPage', () => {
  it('renders Google login button', () => {
    render(<LoginPage />);
    expect(screen.getByText(/sign in with google/i)).toBeInTheDocument();
  });

  it('redirects to Google OAuth on button click', () => {
    const { getByRole } = render(<LoginPage />);
    const button = getByRole('button', { name: /google/i });
    fireEvent.click(button);
    expect(window.location.href).toContain('google.com');
  });
});
```

#### 3.3 Linting & Formatting
```bash
# Backend
black .  # Code formatter
ruff .   # Linter
mypy .   # Type checker

# Frontend
npm run lint     # ESLint
npm run format   # Prettier
```

**Pre-commit Hook 설정:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black
  
  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.8
    hooks:
      - id: ruff
```

---

### 4. 커뮤니케이션 (Communication)

#### 4.1 사용자에게 질문하는 경우
**ONLY 다음 상황에서만 질문:**
1. **명확한 비즈니스 결정이 필요할 때**
   - 예: "테스트 히스토리 보관 기간을 30일로 할까요, 90일로 할까요?"
2. **보안/프라이버시 민감한 선택**
   - 예: "Google OAuth redirect URI를 localhost로 할까요, 프로덕션 도메인으로 할까요?"
3. **추가 비용/외부 서비스 필요**
   - 예: "Sentry를 에러 트래킹에 사용하시겠습니까? (유료 서비스)"

#### 4.2 질문 형식
```markdown
## 🤔 의사결정 필요 (Decision Needed)

### 배경 (Context)
[왜 이 결정이 필요한지 설명]

### 옵션 (Options)
1. **Option A**: [설명]
   - 장점: ...
   - 단점: ...
   
2. **Option B**: [설명]
   - 장점: ...
   - 단점: ...

### 추천 (Recommendation)
[당신의 추천안과 이유]

### 영향 (Impact)
이 결정이 프로젝트에 미치는 영향

---
**사용자 응답을 기다리는 동안 진행할 작업:**
- [ ] 다른 독립적인 작업 1
- [ ] 다른 독립적인 작업 2
```

#### 4.3 자율 진행 원칙
**질문하지 말고 스스로 결정해야 하는 것:**
- 라이브러리 선택 (PRD에 명시되지 않은 경우)
- 코드 구조 및 디자인 패턴
- 변수/함수 네이밍
- 에러 핸들링 방식
- UI 레이아웃 세부사항

**원칙:** 최선의 판단(Best Practice)을 따르고, ADR로 문서화하면 됩니다.

---

## 🏗️ 프로젝트 구조 (Project Structure)

### 최종 디렉토리 구조
```
cloud_rag/
├── README.md
├── PROGRESS.md
├── BLOCKERS.md
├── .gitignore
├── docker-compose.yml
│
├── docs/
│   ├── PRD.md
│   ├── CLAUDE.md (이 파일)
│   ├── API.md (API 문서)
│   ├── DEPLOYMENT.md (배포 가이드)
│   └── decisions/
│       ├── ADR-001-backend-framework.md
│       ├── ADR-002-database-schema.md
│       └── ADR-003-auth-strategy.md
│
├── backend/
│   ├── README.md
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── .env.example          # ✅ Git에 포함 (템플릿)
│   ├── .env                  # ❌ Git에서 제외 (.gitignore)
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py
│   │   │   │   ├── models.py
│   │   │   │   ├── prompts.py
│   │   │   │   ├── tests.py
│   │   │   │   └── admin.py
│   │   │   └── websocket.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── model.py
│   │   │   ├── prompt.py
│   │   │   └── test_run.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── model.py
│   │   │   ├── prompt.py
│   │   │   └── test.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── llm.py
│   │   │   └── websocket.py
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── security.py
│   │       └── encryption.py
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   └── env.py
│   │
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_models.py
│       └── test_websocket.py
│
├── frontend/
│   ├── README.md
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── Dockerfile
│   ├── .env.example          # ✅ Git에 포함 (템플릿)
│   ├── .env.local            # ❌ Git에서 제외 (.gitignore)
│   │
│   ├── public/
│   │   └── favicon.ico
│   │
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── vite-env.d.ts
│   │   │
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── ModelsPage.tsx
│   │   │   ├── PromptsPage.tsx
│   │   │   ├── TestPage.tsx
│   │   │   └── AdminPage.tsx
│   │   │
│   │   ├── components/
│   │   │   ├── ui/ (shadcn components)
│   │   │   ├── Layout/
│   │   │   ├── Auth/
│   │   │   ├── Models/
│   │   │   ├── Prompts/
│   │   │   └── Tests/
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useWebSocket.ts
│   │   │   └── useModels.ts
│   │   │
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── websocket.ts
│   │   │
│   │   ├── store/
│   │   │   ├── authStore.ts
│   │   │   └── testStore.ts
│   │   │
│   │   ├── types/
│   │   │   ├── auth.ts
│   │   │   ├── model.ts
│   │   │   └── test.ts
│   │   │
│   │   └── lib/
│   │       └── utils.ts
│   │
│   └── tests/
│       ├── setup.ts
│       └── LoginPage.test.tsx
│
└── scripts/
    ├── init-db.sh
    ├── seed-data.py
    └── backup-db.sh
```

---

## 📊 개발 워크플로우 (Development Workflow)

### Daily Routine (매일 작업 흐름)

#### 시작 시 (Morning)
```bash
# 1. PROGRESS.md 확인
# 2. 오늘 할 작업 목록 확인
# 3. 새 브랜치 생성 (필요 시)
git checkout develop
git pull origin develop
git checkout -b feature/[today-task]
```

#### 작업 중 (During Work)
```bash
# 1. 작은 단위로 자주 커밋
git add [files]
git commit -m "feat(scope): description"

# 2. 중요 결정사항 발생 시 ADR 작성
# docs/decisions/ADR-XXX-title.md 생성

# 3. 사용자 개입 필요 시 BLOCKERS.md 즉시 업데이트
# - OAuth 설정, .env 파일, DB 실행 등
```

> ⚠️ **체크포인트**: 기능 구현 후 "이게 실행되려면?" 자문 → BLOCKERS.md 업데이트

#### 종료 시 (Evening)
```bash
# 1. 최종 커밋 및 푸시
git push origin feature/[today-task]

# 2. PROGRESS.md 업데이트
# - 오늘 완료한 작업
# - 진행 중인 작업
# - 내일 할 작업

# 3. ⚠️ BLOCKERS.md 점검 (필수!)
# - 사용자 액션이 필요한 항목이 모두 기록되었는지 확인
# - OAuth, .env, DB, 서버 실행 등

# 4. 주요 기능 완료 시 PR 생성
# GitHub에서 Pull Request 생성

# 5. develop에 병합 (자동 또는 수동)
git checkout develop
git merge feature/[today-task]
git push origin develop
```

### Weekly Routine (주간 작업 흐름)

#### 주 시작 (Monday)
- [ ] PRD의 해당 Week 목표 확인
- [ ] 주간 작업 목록을 PROGRESS.md에 추가
- [ ] 필요한 리서치/학습 수행

#### 주 중간 (Wednesday)
- [ ] 진행 상황 중간 점검
- [ ] 예상보다 지연되는 작업 파악
- [ ] 필요 시 우선순위 조정

#### 주 종료 (Friday)
- [ ] 주간 완료 작업 정리
- [ ] develop → main 병합 (주요 마일스톤 완료 시)
- [ ] 버전 태그 추가 (예: v0.1.0)
- [ ] 다음 주 계획 수립

---

## 🎯 Phase별 목표 및 체크리스트

### Phase 1: MVP (Week 1-4)

#### Week 1: Backend Foundation ✅
**목표:** FastAPI 기본 구조 + 인증 시스템 구축

- [ ] **Day 1-2: 프로젝트 초기화**
  - [ ] 프로젝트 구조 생성
  - [ ] Docker Compose 설정 (PostgreSQL)
  - [ ] FastAPI 기본 앱 생성
  - [ ] SQLAlchemy 모델 설정
  - [ ] Alembic 마이그레이션 초기화
  - [ ] ADR-001: 백엔드 프레임워크 선택 작성

- [ ] **Day 3-4: Google OAuth 구현**
  - [ ] authlib 통합
  - [ ] OAuth 콜백 엔드포인트
  - [ ] JWT 토큰 생성/검증
  - [ ] User 모델 생성
  - [ ] 테스트 작성
  - [ ] ADR-002: 인증 전략 작성

- [ ] **Day 5: 마무리**
  - [ ] 통합 테스트
  - [ ] API 문서 자동 생성 (Swagger)
  - [ ] README 업데이트
  - [ ] PR 생성 및 병합

**Deliverables:**
- Google 로그인 작동하는 백엔드 API
- 테스트 커버리지 > 70%
- API 문서 (Swagger UI)

---

#### Week 2: Core APIs ✅
**목표:** Model, Prompt, Test 관리 API 구현

- [ ] **Day 1-2: Model Management API**
  - [ ] Model CRUD 엔드포인트
  - [ ] Model 헬스 체크 기능
  - [ ] 테스트 작성
  - [ ] ADR-003: 데이터베이스 스키마 설계

- [ ] **Day 3-4: Prompt Management API**
  - [ ] Prompt CRUD 엔드포인트
  - [ ] 버전 관리 시스템 구현
  - [ ] 태그 필터링 기능
  - [ ] 테스트 작성

- [ ] **Day 5: Test Execution API (동기)**
  - [ ] 기본 테스트 실행 엔드포인트
  - [ ] vLLM 통합 (동기 호출)
  - [ ] 결과 저장 로직
  - [ ] 테스트 작성

**Deliverables:**
- 완전한 CRUD API 세트
- Postman/Hoppscotch 테스트 컬렉션

---

#### Week 3: Frontend Foundation ✅
**목표:** React 앱 기본 구조 + 주요 페이지 구현

- [ ] **Day 1: 프로젝트 초기화**
  - [ ] Vite + React + TypeScript 설정
  - [ ] Tailwind CSS + Shadcn/ui 설치
  - [ ] 라우팅 설정 (React Router)
  - [ ] ADR-004: 프론트엔드 프레임워크 선택

- [ ] **Day 2: 인증 UI**
  - [ ] 로그인 페이지
  - [ ] OAuth 플로우 통합
  - [ ] 인증 상태 관리 (Zustand)
  - [ ] Protected Route 구현

- [ ] **Day 3: Model Management UI**
  - [ ] 모델 목록 페이지
  - [ ] 모델 등록 폼
  - [ ] 헬스 체크 버튼

- [ ] **Day 4: Prompt Management UI**
  - [ ] 프롬프트 목록 페이지
  - [ ] 프롬프트 생성/수정 폼
  - [ ] 태그 필터링

- [ ] **Day 5: 통합 및 스타일링**
  - [ ] 전체 UI 폴리싱
  - [ ] 반응형 디자인 적용
  - [ ] 에러 핸들링

**Deliverables:**
- 작동하는 로그인 + CRUD UI
- 모바일/데스크톱 반응형 디자인

---

#### Week 4: WebSocket & Test Execution ✅
**목표:** 실시간 스트리밍 + 테스트 실행 UI 완성

- [ ] **Day 1-2: WebSocket 백엔드**
  - [ ] WebSocket 엔드포인트 구현
  - [ ] 스트리밍 로직 구현
  - [ ] 다중 모델 동시 실행
  - [ ] ADR-005: 실시간 통신 전략

- [ ] **Day 3-4: 테스트 실행 UI**
  - [ ] 테스트 실행 페이지
  - [ ] WebSocket 클라이언트 통합
  - [ ] 실시간 응답 렌더링
  - [ ] Side-by-side 비교 뷰

- [ ] **Day 5: 테스트 히스토리**
  - [ ] 히스토리 목록 페이지
  - [ ] 상세 보기
  - [ ] 재실행 기능
  - [ ] E2E 테스트

**Deliverables:**
- 완전히 작동하는 MVP
- E2E 테스트 통과
- 사용자 가이드 문서

---

### Phase 2: Advanced Features (Week 5-6)

#### Week 5: Admin Dashboard ✅
- [ ] 사용자 통계 API
- [ ] 시스템 메트릭 수집
- [ ] 대시보드 UI
- [ ] 권한 관리

#### Week 6: Polish & Production Ready ✅
- [ ] 성능 최적화
- [ ] 보안 강화
- [ ] 문서 완성
- [ ] 배포 스크립트

---

## 🚨 중요 원칙 (Critical Principles)

### 0. 환경변수 보안 (MOST CRITICAL!)
**이것을 가장 먼저 읽으세요!**

#### ⚠️ 절대 규칙 (Never Break These)
```bash
# ❌ 절대로 하지 말 것
git add .env
git add .env.local
git add backend/.env
git add frontend/.env.local
git commit -m "add environment variables"  # 🚨 보안 사고!

# ✅ 항상 해야 할 것
git add .env.example
git add backend/.env.example
git add frontend/.env.example
```

#### 환경변수 파일 구분

| 파일명 | Git 포함 | 용도 | 내용 |
|--------|---------|------|------|
| `.env` | ❌ NO | 실제 사용 | 진짜 비밀키, API 키 |
| `.env.example` | ✅ YES | 템플릿 | 플레이스홀더만 |
| `.env.local` | ❌ NO | 실제 사용 | 진짜 설정값 |

#### 필수 .gitignore 설정

프로젝트 루트의 `.gitignore`에 **반드시** 포함:

```gitignore
# Environment Variables (NEVER COMMIT!)
.env
.env.local
.env.*.local
**/.env
**/.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
venv/
.venv/

# Node
node_modules/
dist/

# IDE
.vscode/
.idea/

# OS
.DS_Store

# Database
*.db
*.sqlite

# Logs
*.log
```

#### 작업 순서 (First Day)

```bash
# 1. .gitignore 먼저 생성
cat > .gitignore << 'EOF'
.env
.env.local
.env.*.local
**/.env
**/.env.local
__pycache__/
node_modules/
.vscode/
.DS_Store
EOF

# 2. Git에 추가
git add .gitignore
git commit -m "chore: add .gitignore with env protection"
git push

# 3. 이제 .env.example 파일 생성
cat > backend/.env.example << 'EOF'
DATABASE_URL=postgresql://admin:password@localhost:5432/llm_platform
SECRET_KEY=your-secret-key-CHANGE-THIS
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
EOF

# 4. .env.example만 Git에 추가
git add backend/.env.example
git add frontend/.env.example
git commit -m "docs: add environment variable templates"
git push

# 5. 실제 .env 파일 생성 (로컬에서만)
cp backend/.env.example backend/.env
# backend/.env 파일 수정 (실제 값 입력)

# 6. .env 파일이 무시되는지 확인
git status  # .env 파일이 보이면 안 됨!
```

#### 환경변수 유출 방지 체크리스트

매 커밋 전에 확인:
- [ ] `git status`에 `.env` 파일이 없는지 확인
- [ ] `git diff --cached`에 비밀키가 없는지 확인
- [ ] `.env.example` 파일에 실제 값이 아닌 플레이스홀더만 있는지 확인

#### 실수로 .env를 커밋한 경우

```bash
# 🚨 긴급 조치 - 즉시 실행!

# 1. 파일을 Git 히스토리에서 완전히 제거
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# 2. 강제 푸시
git push origin --force --all

# 3. GitHub에서 모든 토큰/API 키 즉시 재발급
# - Google OAuth Client Secret 재생성
# - 기타 모든 API 키 교체

# 4. .gitignore 확인
echo ".env" >> .gitignore
git add .gitignore
git commit -m "fix: add .env to gitignore"
git push
```

### 1. 완벽보다 진행 (Progress over Perfection)
- ✅ 작동하는 최소 기능 먼저 구현
- ✅ 리팩토링은 나중에
- ✅ 80/20 법칙 적용

### 2. 문서는 코드만큼 중요
- ✅ 코드 없이 문서만 있는 것보다
- ✅ 문서 없이 코드만 있는 것이 낫지만
- ✅ 둘 다 있는 것이 최고

### 3. 테스트는 선택이 아닌 필수
- ✅ 모든 API 엔드포인트는 테스트 필수
- ✅ 핵심 로직은 단위 테스트 필수
- ✅ E2E 테스트로 사용자 플로우 검증

### 4. 보안은 처음부터
- ✅ SQL Injection 방지 (ORM 사용)
- ✅ XSS 방지 (입력 검증)
- ✅ 인증/인가 철저히
- ✅ 민감 정보 암호화

---

## 🎓 학습 및 참고 자료

### 필수 문서
1. **PRD.md** - 제품 요구사항 (당신의 바이블)
2. **FastAPI Docs** - https://fastapi.tiangolo.com/
3. **SQLAlchemy 2.0** - https://docs.sqlalchemy.org/
4. **React 18** - https://react.dev/
5. **vLLM** - https://docs.vllm.ai/

### 베스트 프랙티스
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [REST API Best Practices](https://restfulapi.net/)
- [React Hooks Best Practices](https://react.dev/reference/react)

---

## 📞 에스컬레이션 (When to Ask User)

### 즉시 물어봐야 하는 것 🚨
1. **보안/프라이버시 위험**
   - 예: "사용자 데이터를 로깅해도 될까요?"
2. **추가 비용 발생**
   - 예: "Sentry 유료 플랜이 필요합니다"
3. **PRD와 모순되는 발견**
   - 예: "요구사항 A와 B가 충돌합니다"

### 나중에 물어봐도 되는 것 ⏰
1. **UI/UX 디테일**
   - 색상, 아이콘, 레이아웃 세부사항
2. **기술 스택 세부 선택**
   - 라이브러리 버전, 패키지 선택
3. **코드 스타일**
   - 네이밍 컨벤션, 파일 구조

---

## ✅ Success Criteria (완료 기준)

### MVP 완료 체크리스트
- [ ] 사용자가 Google로 로그인할 수 있다
- [ ] 사용자가 최소 1개 LLM 모델을 등록할 수 있다
- [ ] 사용자가 시스템 프롬프트를 저장/수정/삭제할 수 있다
- [ ] 사용자가 2개 이상 모델을 동시에 테스트할 수 있다
- [ ] 응답이 실시간으로 스트리밍된다
- [ ] 테스트 히스토리를 조회할 수 있다
- [ ] 모든 API 응답 시간 < 200ms
- [ ] 테스트 커버리지 > 70%
- [ ] 버그 없이 전체 플로우 작동

### Phase 2 완료 체크리스트
- [ ] 관리자가 사용자 통계를 볼 수 있다
- [ ] 모델별 성능 메트릭을 볼 수 있다
- [ ] 에러 로그가 수집된다
- [ ] Docker Compose로 전체 스택이 실행된다
- [ ] 배포 가이드가 작성되었다

---

## 🎬 시작 지침 (Starting Instructions)

당신이 이 프로젝트를 시작할 때 가장 먼저 할 일:

```markdown
## Step 0: 🚨 보안 설정 (MUST DO FIRST!)
1. .gitignore 파일 생성 (.env 보호 포함)
2. Git에 커밋 및 푸시
3. ⚠️ 이후 모든 작업에서 .env 파일은 절대 Git에 추가 금지

## Step 1: 환경 확인
1. Git 레포지토리 연결 확인 (cloud_rag)
2. docs/PRD.md 파일 읽기
3. 현재 레포지토리 상태 파악

## Step 2: 초기 문서 생성
1. PROGRESS.md 생성 및 첫 업데이트
2. BLOCKERS.md 생성 (사용자 액션 필요 항목 기록용)
3. docs/decisions/ 폴더 생성
4. backend/README.md, frontend/README.md 생성

## Step 3: 프로젝트 구조 생성
1. 위에 명시된 디렉토리 구조 생성
2. backend/.env.example, frontend/.env.example 생성
3. docker-compose.yml 기본 템플릿 생성

## Step 4: 첫 커밋
1. Git add .gitignore, .env.example (절대 .env는 NO!)
2. 커밋 메시지: "chore: initialize project structure with security"
3. 푸시 전 확인: `git diff --cached` (비밀키 없는지 확인)
4. 푸시

## Step 5: Week 1 Day 1 작업 시작
1. FastAPI 프로젝트 초기화
2. PostgreSQL Docker Compose 설정
3. ⚠️ BLOCKERS.md 업데이트 (사용자가 해야 할 것 기록):
   - .env 파일 생성 방법
   - Docker 실행 방법
   - Google OAuth 설정 방법 (필요시)
4. PROGRESS.md 업데이트
```

---

## 🎯 마지막 당부

당신은 **충분히 유능한 개발자**입니다. 

- ✅ 스스로 판단하고 결정하세요
- ✅ 최선의 엔지니어링 프랙티스를 따르세요
- ✅ 막히면 문서를 남기고 다른 작업을 하세요
- ✅ 사용자는 당신을 믿고 있습니다

**Let's build something amazing! 🚀**

---

**문서 버전:** 1.1
**작성일:** 2026-02-10
**수정일:** 2025-02-10 (BLOCKERS.md 지침 강화)
**다음 리뷰:** Phase 1 완료 시