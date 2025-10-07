"""
Azure OpenAI 서비스
"""
import os
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

# 프로토타입용: Azure 설정 전까지는 Mock 응답 사용
USE_MOCK = os.getenv("AZURE_OPENAI_KEY") == "your-api-key-here"

if not USE_MOCK:
    from openai import AzureOpenAI
    
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-02-01",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )


def get_ai_summary(query: str, documents: List[Dict]) -> str:
    """
    문서를 바탕으로 업무 맥락 요약 생성
    """
    if USE_MOCK:
        return generate_mock_summary(query, documents)
    
    # 문서 컨텍스트 생성
    context = "\n\n".join([
        f"[{doc['source']}] {doc['title']}\n{doc['content']}"
        for doc in documents
    ])
    
    prompt = f"""
당신은 업무 맥락을 분석하는 AI 도우미입니다.

사용자 질문: {query}

관련 문서:
{context}

위 문서들을 바탕으로 다음 내용을 작성해주세요:
1. 업무 배경 (왜 이 업무가 생겼는지)
2. 주요 내용 요약
3. 관련 이해관계자
4. 마감일 및 우선순위

간결하고 명확하게 작성해주세요.
"""
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": "당신은 업무 맥락 파악을 돕는 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ AI 응답 생성 중 오류 발생: {str(e)}"


def generate_action_items(query: str, documents: List[Dict]) -> List[str]:
    """
    액션 아이템 생성
    """
    if USE_MOCK:
        return [
            "DBA 김OO님께 ERD 검토 요청하기",
            "기존 테이블 정의서 참고하여 초안 작성",
            "Redis Stream 데이터 구조 확인 후 매핑",
            "금요일까지 ERD 완성 및 검토 요청"
        ]
    
    context = "\n\n".join([
        f"[{doc['source']}] {doc['title']}\n{doc['content']}"
        for doc in documents
    ])
    
    prompt = f"""
다음 업무 상황에서 해야 할 구체적인 액션 아이템을 3-5개 추출해주세요.

질문: {query}

관련 정보:
{context}

형식: 각 항목을 한 줄씩 작성
"""
    
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[
                {"role": "system", "content": "액션 아이템을 명확하고 실행 가능하게 작성합니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=300
        )
        
        items = response.choices[0].message.content.strip().split('\n')
        return [item.strip('- ').strip() for item in items if item.strip()]
    except Exception as e:
        return [f"⚠️ 액션 아이템 생성 실패: {str(e)}"]


def generate_mock_summary(query: str, documents: List[Dict]) -> str:
    """
    Mock 요약 생성 (Azure 연동 전 테스트용)
    """
    doc_count = len(documents)
    sources = ", ".join(set([doc["source"] for doc in documents]))
    
    return f"""
## 📋 업무 맥락 요약

**질문**: {query}

**배경**
CHUB 프로젝트에서 실시간 데이터 처리를 위해 Redis Stream을 도입했습니다. 
현재 Redis에 저장된 데이터를 영구 저장하고 분석하기 위해 데이터베이스 테이블 설계가 필요한 상황입니다.

**주요 내용**
- Redis Stream의 데이터 구조(timestamp, user_id, event_type, payload)를 DB 테이블로 매핑
- PostgreSQL 기반 테이블 스키마 정의
- 백엔드팀과 DBA의 협업 필요

**관련 이해관계자**
- PM: 김철수
- 백엔드 개발자: 박민수, 홍길동
- DBA: 김OO

**일정**
- 마감일: 이번 주 금요일 (2024-10-18)
- 우선순위: High

**참고 문서**: {doc_count}개 문서 발견 ({sources})
"""