# LLM Test Platform - Frontend

React + TypeScript 기반 프론트엔드

## 기술 스택

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **UI Library**: Shadcn/ui + Tailwind CSS
- **State Management**: Zustand
- **Data Fetching**: TanStack Query

## 설치 및 실행

```bash
# 의존성 설치
npm install

# 환경변수 설정
cp .env.example .env.local
# .env.local 파일을 열어 실제 값으로 수정

# 개발 서버 실행
npm run dev
```

## 프로젝트 구조

```
frontend/
├── public/           # 정적 파일
├── src/
│   ├── pages/        # 페이지 컴포넌트
│   ├── components/   # 재사용 컴포넌트
│   ├── hooks/        # 커스텀 훅
│   ├── services/     # API 서비스
│   ├── store/        # 상태 관리
│   ├── types/        # TypeScript 타입
│   └── lib/          # 유틸리티
└── tests/            # 테스트
```

## 빌드

```bash
npm run build
```
