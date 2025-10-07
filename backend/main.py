"""
FastAPI 백엔드 메인 서버 (RAG 통합)
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.service.rag_service import RAGService

app = FastAPI(title="Kite API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RAG 서비스 초기화 (전역)
try:
    rag_service = RAGService()
    print("✅ RAG 서비스 초기화 완료")
except Exception as e:
    print(f"⚠️ RAG 서비스 초기화 실패: {str(e)}")
    rag_service = None


@app.get("/")
def read_root():
    return {
        "service": "Kite API",
        "status": "running",
        "version": "1.0.0",
        "features": [
            "RAG (Retrieval-Augmented Generation)",
            "Azure Blob Storage Integration",
            "Auto Indexer (5min interval)",
            "Hybrid Search (Keyword + Vector)"
        ]
    }


@app.post("/analyze")
async def analyze_query(request: Request):
    """
    업무 질문 분석 엔드포인트 (RAG 적용)
    """
    try:
        data = await request.json()
        query = data.get("query", "")
        
        if not query:
            return {
                "error": "query 파라미터가 필요합니다",
                "query": "",
                "summary": "",
                "documents": [],
                "action_items": []
            }
        
        if not rag_service:
            return {
                "error": "RAG 서비스가 초기화되지 않았습니다",
                "query": query,
                "summary": "",
                "documents": [],
                "action_items": []
            }
        
        # 1. RAG로 관련 문서 검색
        print(f"🔍 검색 쿼리: {query}")
        documents = rag_service.search_relevant_documents(query, top=5)
        
        # 2. AI로 맥락 요약 생성
        print(f"🤖 AI 요약 생성 중... (문서 {len(documents)}개)")
        summary = rag_service.generate_context_aware_summary(query, documents)
        
        # 3. 액션 아이템 추출
        print(f"✅ 액션 아이템 생성 중...")
        action_items = rag_service.generate_action_items(query, documents)
        
        return {
            "query": query,
            "summary": summary,
            "documents": documents,
            "action_items": action_items,
            "metadata": {
                "documents_found": len(documents),
                "search_method": "hybrid (keyword + vector)",
                "ai_model": "gpt-4"
            }
        }
    
    except Exception as e:
        print(f"❌ 분석 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            "error": str(e),
            "query": query if 'query' in locals() else "",
            "summary": "",
            "documents": [],
            "action_items": []
        }


@app.get("/health")
def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "rag_service": "ready" if rag_service else "not initialized"
    }


@app.get("/indexer/status")
async def get_indexer_status():
    """인덱서 상태 조회"""
    try:
        from backend.service.azure_search import AzureSearchService
        
        search_service = AzureSearchService()
        status = search_service.get_indexer_status()
        
        return {
            "indexer": "kite-auto-indexer",
            "status": status
        }
    except Exception as e:
        return {
            "error": str(e)
        }


@app.post("/indexer/run")
async def run_indexer():
    """인덱서 수동 실행"""
    try:
        from backend.service.azure_search import AzureSearchService
        
        search_service = AzureSearchService()
        
        if search_service.run_indexer():
            return {
                "message": "인덱서 실행 시작",
                "estimated_time": "1-2분"
            }
        else:
            return {
                "error": "인덱서 실행 실패"
            }
    except Exception as e:
        return {
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)