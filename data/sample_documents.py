"""
샘플 업무 문서 데이터
실제 회사 문서처럼 보이는 현실적인 Mock 데이터
"""

def get_sample_documents():
    """샘플 문서 목록 반환"""
    return [
        {
            "id": "doc_001",
            "title": "RE: RE: [CHUB] Redis Stream 테이블 설계 일정 문의",
            "content": """
안녕하세요, 백엔드 개발팀 홍길동입니다.

DBA 김영희님께 확인한 결과, Redis Stream 데이터 구조는 다음과 같습니다:

{
  "timestamp": "2024-10-05T14:30:00Z",
  "user_id": "usr_12345",
  "event_type": "user_action",
  "payload": {
    "action": "click",
    "page": "/dashboard",
    "metadata": {...}
  }
}

이를 PostgreSQL 테이블로 매핑할 때 고려사항:
1. timestamp는 TIMESTAMPTZ 타입 사용
2. payload는 JSONB로 저장 (인덱싱 가능)
3. partition by timestamp (월별 파티셔닝 추천)

ERD 초안은 금요일 오전까지 작성 예정입니다.
검토 부탁드립니다.

---
홍길동
Backend Developer | CHUB Project
            """,
            "source": "메일",
            "date": "2024-10-05",
            "sender": "홍길동"
        },
        {
            "id": "doc_002",
            "title": "#chub-backend 채널 대화",
            "content": """
[14:20] 박민수: @홍길동 Redis Stream 데이터 초당 몇 건 정도 들어와?
[14:22] 홍길동: 피크 타임 기준 약 5000 TPS 예상
[14:23] 박민수: 그럼 파티셔닝 필수네. 월별로 할까 일별로 할까?
[14:25] 김영희(DBA): 월별 추천. 일별은 테이블 수 너무 많아짐
[14:27] 홍길동: 알겠습니다. 월별 파티셔닝으로 ERD 작성하겠습니다
            """,
            "source": "슬랙",
            "date": "2024-10-05",
            "sender": "박민수, 홍길동, 김영희"
        },
        {
            "id": "doc_003",
            "title": "CHUB 프로젝트 - Redis Stream 아키텍처",
            "content": """
# Redis Stream 데이터 파이프라인

## 개요
실시간 사용자 이벤트를 Redis Stream으로 수집 → Kafka Consumer → PostgreSQL 저장

## 데이터 플로우
1. Frontend → API Gateway → Redis Stream (Primary Buffer)
2. Stream Consumer → Data Validation
3. PostgreSQL Batch Insert (500건 단위)

## 테이블 설계 요구사항
- 최소 3개월 데이터 보관 (약 13억 건)
- 쿼리 성능: 특정 user_id 기준 1초 이내
- 백업: 매일 자정 S3 업로드

## 담당자
- 아키텍트: 이영희
- Backend: 홍길동, 박민수
- DBA: 김영희
            """,
            "source": "컨플루언스",
            "date": "2024-09-28",
            "sender": "이영희"
        },
        {
            "id": "doc_004",
            "title": "CHUB-1234: Redis Stream 데이터 영구 저장 테이블 설계",
            "content": """
[상태] In Progress
[우선순위] High
[담당자] 홍길동
[리포터] 김철수 (PM)

## Description
Redis Stream에 임시 저장된 이벤트 데이터를 PostgreSQL에 영구 저장하기 위한 테이블 스키마 설계

## Acceptance Criteria
- [ ] ERD 작성 (draw.io)
- [ ] 테이블 정의서 작성 (DDL 포함)
- [ ] DBA 검토 완료
- [ ] 인덱스 전략 수립

## Due Date
2024-10-18 (금)

## Comments
- 2024-10-05: DBA와 파티셔닝 전략 논의 완료 (월별 파티셔닝)
- 2024-10-04: 데이터 볼륨 산정 완료 (월 4억 건)
            """,
            "source": "지라",
            "date": "2024-10-02",
            "sender": "김철수"
        },
        {
            "id": "doc_005",
            "title": "CHUB DB 스키마 리뷰 미팅",
            "content": """
일시: 2024-10-18 (금) 14:00-15:00
장소: 회의실 A (Zoom 병행)

참석자:
- 홍길동 (발표자)
- 김영희 (DBA)
- 박민수 (Backend)
- 이영희 (Architect)
- 김철수 (PM)

안건:
1. Redis Stream 테이블 ERD 발표
2. 인덱스 전략 검토
3. 마이그레이션 계획 논의
            """,
            "source": "구글 캘린더",
            "date": "2024-10-18",
            "sender": "김철수"
        }
    ]