# Blockers

## [날짜: 2025-02-10] - 환경 설정 필요

### 문제 설명
서버 실행을 위해 사용자가 직접 설정해야 하는 환경변수 및 인프라가 있습니다.

### 필요한 정보/결정

#### 1. Google OAuth 2.0 설정 (필수)
Google Cloud Console에서 OAuth 2.0 클라이언트를 생성해야 합니다.

1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. 새 프로젝트 생성 또는 기존 프로젝트 선택
3. **APIs & Services** → **OAuth consent screen** 설정
   - User Type: External
   - App name, User support email 입력
   - Scopes: `email`, `profile`, `openid` 추가
4. **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
   - Application type: **Web application**
   - Authorized redirect URIs: `http://localhost:8000/api/v1/auth/google/callback`
5. Client ID와 Client Secret 복사

#### 2. backend/.env 파일 생성 (필수)
```bash
cd backend
cp .env.example .env
```

그리고 `.env` 파일을 열어 다음 값들을 설정:

```bash
# Database - Docker Compose 사용 시 기본값 그대로 OK
DATABASE_URL=postgresql://admin:password@localhost:5432/llm_platform

# 보안 키 생성 (터미널에서 실행)
# python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=<생성된 값>

# Fernet 키 생성 (터미널에서 실행)
# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
ENCRYPTION_KEY=<생성된 값>

# Google OAuth (위에서 받은 값)
GOOGLE_CLIENT_ID=<your-client-id>
GOOGLE_CLIENT_SECRET=<your-client-secret>

# Admin 이메일 (본인 이메일)
ADMIN_EMAILS=<your-email@gmail.com>
```

#### 3. PostgreSQL 실행 (필수)
```bash
# 프로젝트 루트에서
docker-compose up -d postgres
```

#### 4. 데이터베이스 마이그레이션 (첫 실행 시)
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
```

#### 5. frontend/.env 파일 생성 (필수)
```bash
cd frontend
cp .env.example .env
```

기본값 사용 시 수정 불필요:
```bash
VITE_API_URL=http://localhost:8000
```

### 대안 방안
사용자 응답 전까지 진행 가능한 작업:
- [x] Model CRUD API 코드 작성 (DB 연결 없이 코드만)
- [x] Prompt CRUD API 코드 작성
- [x] Test Execution API 코드 작성
- [x] Frontend 프로젝트 초기화
- [x] Frontend API 클라이언트 작성
- [ ] Frontend UI 컴포넌트 (진행 중)

### 상태
**Partially Blocked** - 코드 작성은 계속 가능하나, 실제 테스트는 환경 설정 필요

---

## 요약: 사용자 액션 필요

| 항목 | 필수 여부 | 상태 |
|------|-----------|------|
| Google OAuth 설정 | 필수 | ⏳ 대기 |
| backend/.env 생성 | 필수 | ⏳ 대기 |
| frontend/.env 생성 | 필수 | ⏳ 대기 |
| Docker (PostgreSQL) | 필수 | ⏳ 대기 |
| Alembic 마이그레이션 | 필수 | ⏳ 대기 |
