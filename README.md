# LLM Test Platform

로컬 환경에서 다양한 LLM 모델을 테스트하고 비교할 수 있는 웹 기반 플랫폼

## 주요 기능

- **Google OAuth 로그인**: 간편한 사용자 인증
- **LLM 모델 관리**: vLLM 서버 등록 및 관리
- **시스템 프롬프트 관리**: 재사용 가능한 프롬프트 템플릿
- **실시간 테스트**: 여러 모델 동시 비교 (WebSocket 스트리밍)
- **테스트 히스토리**: 과거 실험 결과 조회

## 기술 스택

| 영역 | 기술 |
|------|------|
| Backend | FastAPI, SQLAlchemy 2.0, PostgreSQL |
| Frontend | React 18, TypeScript, Vite, Tailwind CSS |
| Auth | Google OAuth 2.0, JWT |
| Infra | Docker, Docker Compose |

## 빠른 시작

```bash
# 1. 환경변수 설정
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
# .env 파일들을 열어 실제 값으로 수정

# 2. Docker Compose 실행
docker-compose up -d

# 3. 접속
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/docs
```

## 문서

- [PRD (Product Requirements)](docs/PRD.md)
- [개발 가이드](docs/CLAUDE.md)
- [API 문서](docs/API.md) (예정)

## 개발 현황

[PROGRESS.md](PROGRESS.md) 참조

## 라이선스

Private
