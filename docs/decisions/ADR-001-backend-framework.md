# ADR-001: Backend Framework 선택

## Status
Accepted

## Context
LLM Test Platform의 백엔드 프레임워크를 선택해야 합니다. 주요 요구사항:
- RESTful API + WebSocket 지원 (실시간 스트리밍)
- 비동기 처리 (여러 LLM 동시 호출)
- Python 기반 (vLLM, LangChain 통합)
- 빠른 개발 속도

## Decision
**FastAPI**를 백엔드 프레임워크로 선택합니다.

## Consequences

### 장점
- 네이티브 async/await 지원으로 동시성 처리 우수
- 내장 WebSocket 지원
- Pydantic 통합으로 자동 검증 및 문서화
- OpenAPI (Swagger) 자동 생성
- Python 생태계와 완벽 호환

### 단점
- Django 대비 내장 기능 적음 (ORM, Admin 등 별도 설정 필요)
- 대규모 프로젝트 구조화는 개발자 재량

### 트레이드오프
Django의 "batteries included" 접근법 대신 필요한 것만 선택하는 유연성 확보

## Alternatives Considered

### Django + Django REST Framework
- 장점: 풍부한 내장 기능, Admin 패널
- 단점: 동기 기반 (async 지원 제한적), WebSocket 설정 복잡

### Flask
- 장점: 미니멀, 유연
- 단점: 타입 힌트/문서화 추가 작업 필요, async 네이티브 아님
