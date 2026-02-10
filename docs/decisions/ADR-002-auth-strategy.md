# ADR-002: 인증 전략 (Authentication Strategy)

## Status
Accepted

## Context
LLM Test Platform은 사용자 인증이 필요합니다. 요구사항:
- 간편한 로그인 (비밀번호 관리 부담 없음)
- 안전한 세션 관리
- API와 WebSocket 모두에서 인증 지원
- 토큰 갱신 메커니즘

## Decision
**Google OAuth 2.0 + JWT** 조합을 사용합니다.

### 인증 흐름
```
1. 사용자 → Frontend → "Google 로그인" 클릭
2. Frontend → Google OAuth 서버로 리다이렉트
3. Google → 사용자 동의 → Authorization Code 발급
4. Google → Backend 콜백 URL로 리다이렉트 (code 포함)
5. Backend → Google Token 엔드포인트에서 Access Token 획득
6. Backend → Google UserInfo에서 사용자 정보 획득
7. Backend → DB에 사용자 생성 또는 조회
8. Backend → JWT (Access + Refresh) 발급
9. Backend → Frontend로 리다이렉트 (httpOnly 쿠키에 토큰 저장)
```

### JWT 설정
- **Access Token**: 1시간 만료, HS256 알고리즘
- **Refresh Token**: 7일 만료
- **저장**: httpOnly, Secure, SameSite=Lax 쿠키

### 라이브러리
- **authlib**: Google OAuth 2.0 클라이언트
- **python-jose**: JWT 생성/검증

## Consequences

### 장점
- 비밀번호 관리 불필요 (보안 부담 감소)
- Google의 보안 인프라 활용
- JWT로 stateless 인증 (확장성)
- httpOnly 쿠키로 XSS 방지

### 단점
- Google 서비스 의존성
- OAuth 설정 복잡도 (Google Cloud Console)
- 오프라인 환경에서 신규 로그인 불가

### 트레이드오프
- Session 기반 인증 대신 JWT 선택: DB 조회 없이 토큰 검증 가능
- LocalStorage 대신 httpOnly 쿠키: XSS 공격에 더 안전

## Alternatives Considered

### 1. 이메일/비밀번호 인증
- 장점: 외부 의존성 없음
- 단점: 비밀번호 해싱, 재설정 로직 구현 필요

### 2. Magic Link (이메일 링크 로그인)
- 장점: 비밀번호 없음
- 단점: 이메일 서비스 설정 필요

### 3. 다중 OAuth (Google + GitHub + etc.)
- 장점: 사용자 선택권
- 단점: 복잡도 증가, MVP에서는 과도함
