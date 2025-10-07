"""
RAG 검색 테스트
"""
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.service.rag_service import RAGService


def main():
    print("🧪 RAG 검색 테스트 시작...\n")
    print("=" * 60)
    
    try:
        # RAG 서비스 초기화
        rag_service = RAGService()
        
        # 테스트 쿼리
        test_queries = [
            "Redis Stream 테이블 설계가 뭐야?",
            "CHUB 프로젝트에서 DBA는 누구야?",
            "마감일이 언제야?",
            "파티셔닝 전략은 뭐야?"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*60}")
            print(f"테스트 {i}/{len(test_queries)}: {query}")
            print("=" * 60)
            
            # 검색
            print("\n🔍 관련 문서 검색 중...")
            documents = rag_service.search_relevant_documents(query, top=3)
            
            print(f"✅ 검색 완료: {len(documents)}개 문서 발견\n")
            
            for j, doc in enumerate(documents, 1):
                print(f"  {j}. [{doc['source']}] {doc['title']}")
                print(f"     점수: {doc['score']:.4f}")
                print(f"     내용: {doc['content'][:100]}...\n")
            
            # AI 요약
            print("🤖 AI 요약 생성 중...")
            summary = rag_service.generate_context_aware_summary(query, documents)
            
            print("\n📋 요약:")
            print(summary[:500] + "..." if len(summary) > 500 else summary)
            
            # 액션 아이템
            print("\n✅ 액션 아이템:")
            action_items = rag_service.generate_action_items(query, documents)
            for item in action_items:
                print(f"  - {item}")
        
        print("\n" + "=" * 60)
        print("🎉 모든 테스트 완료!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ 테스트 실패: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)