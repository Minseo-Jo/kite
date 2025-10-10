"""
RAG (Retrieval-Augmented Generation) 서비스
검색된 문서를 기반으로 AI 응답 생성
"""
from typing import List, Dict
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

from service.azure_search import AzureSearchService
from service.query_preprocessor import QueryPreprocessor

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
        
        # ⭐ 쿼리 전처리기 추가
        self.preprocessor = QueryPreprocessor()
        
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
            return [0.0] * 1536
    
    def search_relevant_documents(
        self,
        query: str,
        top: int = 5,
        min_score: float = 0.5  # ⭐ 0.7에서 0.5로 낮춤
    ) -> List[Dict]:
        """
        쿼리에 관련된 문서 검색
        """
        # 쿼리 전처리 (한글 → 영어 변환)
        processed_query = self.preprocessor.preprocess(query)
        
        if processed_query != query:
            print(f"🔄 쿼리 전처리: '{query}' → '{processed_query}'")
        else:
            print(f"🔍 원본 쿼리 사용: '{query}'")
        
        # 전처리된 쿼리로 벡터 생성
        query_vector = self.get_embedding(processed_query)
        
        # 하이브리드 검색 실행
        documents = self.search_service.hybrid_search(
            query=processed_query,
            query_vector=query_vector,
            top=top
        )
        
        # ⭐ 검색된 모든 문서의 점수 출력
        print(f"📊 검색된 문서: {len(documents)}개")
        for i, doc in enumerate(documents[:3], 1):
            print(f"  {i}. [{doc.get('source', 'unknown')}] 점수: {doc.get('score', 0):.4f} - {doc.get('title', 'No title')[:50]}")
        
        # 점수 필터링
        filtered_docs = [
            doc for doc in documents 
            if doc.get('score', 0) >= min_score
        ]
        
        if filtered_docs:
            print(f"✅ 필터링 결과: {len(documents)}개 → {len(filtered_docs)}개 (최소 점수: {min_score})")
        else:
            print(f"⚠️ 관련성 높은 문서 없음 (모든 문서가 {min_score} 이하)")
            if documents:
                max_score = max([doc.get('score', 0) for doc in documents])
                print(f"   최고 점수: {max_score:.4f}")
        
        return filtered_docs
    
    def generate_context_aware_summary(
        self,
        query: str,
        documents: List[Dict]
    ) -> str:
        """
        검색된 문서를 기반으로 맥락 요약 생성
        """
        # ⭐ 문서가 없거나 관련성이 낮은 경우
        if not documents:
            return self._generate_no_result_message(query)
        
        # 문서 컨텍스트 생성
        context = "\n\n".join([
            f"[{doc['source']}] {doc['title']}\n작성일: {doc['date']}\n내용: {doc['content'][:500]}"
            for doc in documents[:3]
        ])
        
        # ⭐ AI에게 관련성 검증 요청
        system_prompt = """당신은 업무 맥락을 분석하는 AI 도우미입니다.

중요: 사용자의 질문과 제공된 문서가 관련이 없다면, 솔직하게 "관련 문서를 찾을 수 없습니다"라고 답변하세요.
문서의 내용을 억지로 질문에 맞추려 하지 마세요.

만약 질문과 문서가 관련이 있다면, 다음 형식으로 답변해주세요:

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

간결하고 구조화된 형태로 작성해주세요."""

        user_prompt = f"""
사용자 질문: {query}

관련 문서:
{context}

위 문서들이 사용자의 질문과 관련이 있나요? 
관련이 있다면 위 문서를 바탕으로 답변하고, 관련이 없다면 솔직하게 "관련 문서를 찾을 수 없습니다"라고 답변해주세요.
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
    
    def _generate_no_result_message(self, query: str) -> str:
        """관련 문서가 없을 때 메시지"""
        return f"""## 🔍 검색 결과 없음

죄송합니다. **"{query}"**와 관련된 업무 문서를 찾을 수 없습니다.

### 💡 도움말

다음과 같이 시도해보세요:

1. **구체적인 키워드 사용**
   - 예: "Redis Stream", "테이블 설계", "CHUB 프로젝트"

2. **업무 관련 질문**
   - 예: "○○ 프로젝트 일정이 언제야?"
   - 예: "△△ 담당자가 누구야?"

3. **문서가 업로드되어 있는지 확인**
   - Blob Storage에 관련 문서가 있는지 확인해주세요

현재 시스템에 업로드된 문서 내에서만 검색이 가능합니다."""
    
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
다음 업무 상황에서 해야 할 구체적인 액션 아이템을 3-4개 추출해주세요.

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