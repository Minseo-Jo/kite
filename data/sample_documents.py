"""
업무 문서 Mock 데이터
"""

def get_sample_documents():
    """샘플 문서 목록 반환"""
    return [
        # ========== 기존 Redis Stream 관련 문서 ==========
        {
            "id": "doc_001",
            "title": "RE: RE: [CHUB] Redis Stream 테이블 설계 일정 문의",
            "content": """
안녕하세요, 백엔드 개발팀 홍길동입니다.

DBA 김영희님께 확인한 결과, Redis Stream 데이터 구조는 다음과 같습니다:

{
  "timestamp": "2025-10-05T14:30:00Z",
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
            "date": "2025-10-05",
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
            "date": "2025-10-05",
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
            "date": "2025-09-28",
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
- 2025-10-05: DBA와 파티셔닝 전략 논의 완료 (월별 파티셔닝)
- 2025-10-04: 데이터 볼륨 산정 완료 (월 4억 건)
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
        },
        
        # ========== KITE 프로젝트 관련 ==========
        {
            "id": "doc_006",
            "title": "[중요] KITE AI 프로젝트 킥오프 미팅 안내",
            "content": """
발신: 박기획 <ppm@company.com>
수신: 개발팀 전체
날짜: 2025.09.01 10:00

안녕하세요, PM 박기획입니다.

KITE AI 프로젝트 킥오프 미팅을 아래와 같이 진행합니다.

📅 일시: 2024.09.05 (목) 14:00 ~ 16:00
📍 장소: 본관 3층 대회의실
👥 참석자: 개발팀, AI팀, 디자인팀

## 안건
1. 프로젝트 목표 및 범위 공유
2. 기술 스택 확정
3. 역할 분담 및 일정 수립
4. Q&A

## 프로젝트 개요
AI 기반 업무 맥락 파악 시스템으로, 산재된 문서(메일, 위키, 슬랙)를 통합 분석하여 
신입 직원의 업무 적응 시간을 80% 단축하는 것이 목표입니다.

## 기술 스택
- Azure OpenAI GPT-4
- Azure AI Search (벡터 검색)
- FastAPI, React

감사합니다.
            """,
            "source": "메일",
            "date": "2024-09-01",
            "sender": "박기획"
        },
        {
            "id": "doc_007",
            "title": "KITE-001: 음성 인식 기능 구현",
            "content": """
[상태] In Progress
[우선순위] Medium
[담당자] 정인공
[리포터] 박기획

## Description
Azure Speech Services를 활용한 음성 질의응답 기능 구현

## Tasks
- [x] Azure Speech Service 리소스 생성
- [x] 백엔드 API 구현 (/api/speech-to-text)
- [ ] 프론트엔드 마이크 버튼 UI
- [ ] 실시간 텍스트 변환 표시
- [ ] 한글 음성 인식 테스트

## 기술 요구사항
- 한국어 음성 인식
- WebM/WAV 형식 지원
- 응답 시간 3초 이내

## Due Date
2025.10.15
            """,
            "source": "지라",
            "date": "2025-10-01",
            "sender": "박기획"
        },
        
        # ========== 사용자 인증 시스템 ==========
        {
            "id": "doc_008",
            "title": "[긴급] 사용자 인증 시스템 보안 취약점 발견",
            "content": """
발신: 최보안 <csecurity@company.com>
수신: 김개발, 이디비, CTO
날짜: 2025.08.15 09:30

긴급 보안 이슈입니다.

## 발견된 취약점
JWT 토큰 검증 로직에서 알고리즘 헤더 검증 누락으로 인한
'None' 알고리즘 공격 가능성 확인

## 영향 범위
- 전체 API 엔드포인트
- 약 50만 명의 사용자 계정

## 조치 사항
1. [긴급] JWT 라이브러리 최신 버전 업데이트 (완료)
2. 알고리즘 화이트리스트 검증 추가 (진행 중)
3. 기존 발급 토큰 전체 무효화 및 재발급 (예정)

## 배포 일정
- 핫픽스 배포: 오늘 (08.15) 18:00
- 사용자 재로그인 필요

즉시 대응 부탁드립니다.

---
최보안 | Security Engineer
            """,
            "source": "메일",
            "date": "2024-08-15",
            "sender": "최보안"
        },
        {
            "id": "doc_009",
            "title": "AUTH-567: OAuth 2.0 인증 시스템 설계",
            "content": """
[상태] Done
[우선순위] High
[담당자] 김개발

## Description
레거시 인증 시스템을 OAuth 2.0 기반으로 전환

## 구현 내용
- Authorization Code Flow
- Refresh Token 발급 (7일 만료)
- Access Token 발급 (30분 만료)
- Rate Limiting (분당 10회)

## 데이터베이스 설계
### users 테이블
- id: UUID (PK)
- email: VARCHAR(255) UNIQUE
- password_hash: VARCHAR(255)
- created_at: TIMESTAMP

### auth_sessions 테이블
- session_id: UUID (PK)
- user_id: UUID (FK)
- token: TEXT
- expires_at: TIMESTAMP

## 완료일
2025-09-30
            """,
            "source": "지라",
            "date": "2024-08-01",
            "sender": "김개발"
        },
        
        # ========== E-Commerce 시스템 ==========
        {
            "id": "doc_010",
            "title": "PERF-123: 주문 조회 API 응답 속도 개선",
            "content": """
[상태] In Progress
[우선순위] High
[담당자] 박백엔

## 문제
주문 조회 API의 P95 응답시간이 800ms로 SLA(200ms) 4배 초과

## 원인 분석
1. N+1 쿼리 문제 (order_items 조인)
2. 인덱스 미사용 (user_id 조건)
3. 불필요한 컬럼 조회

## 해결 방안
1. Eager Loading 적용
2. user_id + created_at 복합 인덱스 생성
3. DTO 필드 최소화
4. Redis 캐시 도입 (유저별 최근 주문 10건)

## 예상 개선
800ms → 150ms (81% 개선)

## 일정
- 개발: 08.20 ~ 08.22
- 리뷰: 08.23
- 배포: 08.24
            """,
            "source": "지라",
            "date": "2024-08-18",
            "sender": "박백엔"
        },
        {
            "id": "doc_011",
            "title": "#incident | 프로덕션 장애 대응",
            "content": """
[2025.09.15 18:30] ALERT: Prod API 5XX Error Rate 급증

정데브 (DevOps) [18:31]
🚨 프로덕션 API 장애 감지
- 5XX 에러율: 0.1% → 15%
- 영향 범위: 전체 API
- 발생 시간: 18:25

박백엔 [18:32]
확인 중입니다
DB 커넥션 풀이 고갈된 것 같습니다

이디비 [18:33]
DB 모니터링 확인 결과:
- Active Connections: 495/500 (MAX)
- Slow Query 다수 발견

김개발 [18:35]
방금 배포한 주문 조회 API가 문제인 것 같습니다
N+1 쿼리 이슈 있었는데 놓쳤습니다 😱

박백엔 [18:36]
즉시 롤백 진행합니다

정데브 [18:37]
롤백 완료했습니다
에러율 정상화 확인 ✅

박백엔 [18:40]
포스트모템 작성하겠습니다
근본 원인:
1. 코드 리뷰에서 N+1 쿼리 미발견
2. 스테이징 환경 데이터 부족
            """,
            "source": "슬랙",
            "date": "2024-09-15",
            "sender": "정데브, 박백엔, 김개발"
        },
        
        # ========== 코딩 가이드/문서 ==========
        {
            "id": "doc_012",
            "title": "Python 코딩 컨벤션",
            "content": """
# Python 코딩 컨벤션

## 기본 원칙
- PEP 8 준수
- Type Hints 필수
- Docstring 작성 (Google Style)

## 네이밍 규칙
### 변수/함수
- 스네이크 케이스 사용
- 동사 + 명사 조합
예: get_user_by_id, calculate_total_price

### 클래스
- 파스칼 케이스 사용
예: UserRepository, OrderService

## 파일 구조
```
project/
├── src/
│   ├── models/          # 데이터 모델
│   ├── repositories/    # DB 접근 계층
│   ├── services/        # 비즈니스 로직
│   └── api/            # API 라우터
├── tests/
└── docs/
```

## 에러 처리
```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Failed: {e}")
    raise
```

작성자: 김개발
최종 수정: 2024.08.01
            """,
            "source": "컨플루언스",
            "date": "2024-08-01",
            "sender": "김개발"
        },
        {
            "id": "doc_013",
            "title": "프로덕션 배포 가이드",
            "content": """
# 프로덕션 배포 가이드

## 배포 전 체크리스트
- [ ] 코드 리뷰 완료 (2명 이상 Approve)
- [ ] 단위 테스트 통과율 80% 이상
- [ ] E2E 테스트 통과
- [ ] 성능 테스트 완료
- [ ] 보안 스캔 통과

## 배포 절차
### 1. 준비 단계
```bash
git checkout -b release/v1.2.3
git tag -a v1.2.3 -m "Release v1.2.3"
docker build -t myapp:v1.2.3 .
```

### 2. 스테이징 배포
```bash
kubectl apply -f k8s/staging/
./scripts/smoke-test.sh staging
```

### 3. 프로덕션 배포
Blue-Green 배포 방식 사용
트래픽 전환: 10% → 50% → 100%

## 롤백 절차
```bash
kubectl rollout undo deployment/myapp
```

## 긴급 연락처
- DevOps 리드: 정데브 (010-9999-8888)
- 백엔드 리드: 박백엔 (010-8888-7777)

작성자: 정데브
최종 수정: 2025.09.01
            """,
            "source": "컨플루언스",
            "date": "2024-09-01",
            "sender": "정데브"
        },
        
        # ========== DB/인프라 관련 ==========
        {
            "id": "doc_014",
            "title": "#dev-backend | DB 마이그레이션 논의",
            "content": """
[2025.08.10]

이디비 (DBA) [09:30]
@박백엔 주문 테이블 파티셔닝 마이그레이션 일정 논의 필요합니다

박백엔 [09:35]
네, 언제가 좋으실까요? 이번 주 금요일은 어떠신가요?

이디비 [09:37]
금요일 14:00 괜찮습니다
안건:
1. 파티셔닝 전략 (월별 vs 분기별)
2. 다운타임 최소화 방안
3. 데이터 마이그레이션 스크립트 검토

박백엔 [09:40]
👍 회의실 예약하겠습니다

이디비 [09:45]
현재 orders 테이블이 5억 건 넘어서
쿼리 성능이 많이 저하된 상태입니다
파티셔닝 시급합니다 🔥

김개발 [10:00]
저도 참석 가능할까요? 주문 API 수정이 필요할 것 같아서요

박백엔 [10:05]
@김개발 물론이죠! 같이 논의해요
            """,
            "source": "슬랙",
            "date": "2024-08-10",
            "sender": "이디비, 박백엔, 김개발"
        },
        {
            "id": "doc_015",
            "title": "E-Commerce 주문 시스템 아키텍처",
            "content": """
# E-Commerce 주문 시스템 아키텍처

## 마이크로서비스 구성
1. 주문 서비스: 주문 생성/조회/취소
2. 결제 서비스: PG 연동, 결제 처리
3. 재고 서비스: 재고 관리, 예약
4. 배송 서비스: 배송 추적
5. 알림 서비스: 이메일, SMS

## 기술 스택
- API Gateway: Kong
- 메시지 큐: Kafka
- 데이터베이스: PostgreSQL, MongoDB
- 캐시: Redis Cluster
- 검색: Elasticsearch

## 성능 요구사항
- TPS: 최소 1,000
- 응답시간: P95 < 200ms
- 가용성: 99.9%

## 담당자
- 아키텍트: 김아키
- 백엔드 리드: 박백엔
- DevOps: 정데브
- DBA: 이디비

작성자: 김아키
최종 수정: 2025.07.15
            """,
            "source": "컨플루언스",
            "date": "2025-07-15",
            "sender": "김아키"
        }
    ]