"""
RAG (Retrieval-Augmented Generation) 서비스
검색된 문서를 기반으로 AI 응답 생성
"""
from typing import List, Dict
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

from backend.service.azure_search import AzureSearchService

load_dotenv()


class RAGService:
    """RAG 서비스 - 검색 + 생성"""
    
    def __init__(self):
        # OpenAI 클라이언트
        self.openai_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        
        # Search 서비스
        self.search_service = AzureSearchService()
        
        print("✅ RAG 서비스 초기화 완료")
    
    def get_embedding(self, text: str) -> List[float]:
        """텍스트를 벡터로 변환"""
        try:
            response = self.openai_client.embeddings.create(
                model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"⚠️ 임베딩 생성 실패: {str(e)}")
            return [0.0] * 1536  # 더미 벡터
    
    def search_relevant_documents(
        self,
        query: str,
        top: int = 5
    ) -> List[Dict]:
        """
        쿼리에 관련된 문서 검색
        """
        # 쿼리를 벡터로 변환
        query_vector = self.get_embedding(query)
        
        # 하이브리드 검색 실행
        documents = self.search_service.hybrid_search(
            query=query,
            query_vector=query_vector,
            top=top
        )
        
        return documents
    
    def generate_context_aware_summary(
        self,
        query: str,
        documents: List[Dict]
    ) -> str:
        """
        검색된 문서를 기반으로 맥락 요약 생성
        """
        if not documents:
            return "관련 문서를 찾을 수 없습니다. 검색 키워드를 변경해보세요."
        
        # 문서 컨텍스트 생성
        context = "\n\n".join([
            f"[{doc['source']}] {doc['title']}\n작성일: {doc['date']}\n내용: {doc['content'][:500]}"
            for doc in documents[:3]  # 상위 3개만 사용
        ])
        
        # 프롬프트 생성
        system_prompt = """당신은 업무 맥락을 분석하는 AI 도우미입니다.
주어진 문서들을 바탕으로 사용자의 질문에 답변해주세요.

답변 형식:
## 📋 업무 맥락 분석 결과

### 🎯 핵심 요약
(한 문장으로 업무의 본질 설명)

### 📖 배경 및 목적
(왜 이 업무가 생겼는지)

### 👥 주요 이해관계자
(관련된 사람들과 역할)

### 📅 일정 및 우선순위
(마감일, 우선순위)

### 🔑 핵심 내용
(기술적 요구사항이나 중요 사항)

### ⚡ 현재 진행 상황
(진행 상태)

간결하고 구조화된 형태로 작성해주세요."""

        user_prompt = f"""
사용자 질문: {query}

관련 문서:
{context}

위 문서들을 바탕으로 사용자의 질문에 답변해주세요.
"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ AI 응답 생성 실패: {str(e)}")
            return "AI 응답 생성 중 오류가 발생했습니다."
    
    def generate_action_items(
        self,
        query: str,
        documents: List[Dict]
    ) -> List[str]:
        """액션 아이템 생성"""
        if not documents:
            return ["관련 문서가 없어 액션 아이템을 생성할 수 없습니다."]
        
        context = "\n".join([
            f"[{doc['source']}] {doc['content'][:300]}"
            for doc in documents[:2]
        ])
        
        prompt = f"""
다음 업무 상황에서 해야 할 구체적인 액션 아이템을 4-5개 추출해주세요.

질문: {query}

관련 정보:
{context}

각 항목은 한 줄로 작성하고, "- "로 시작해주세요.
"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
                messages=[
                    {"role": "system", "content": "액션 아이템을 명확하고 실행 가능하게 작성합니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=400
            )
            
            items = response.choices[0].message.content.strip().split('\n')
            return [item.strip('- ').strip() for item in items if item.strip() and item.strip().startswith('-')]
            
        except Exception as e:
            print(f"❌ 액션 아이템 생성 실패: {str(e)}")
            return ["액션 아이템 생성에 실패했습니다."]