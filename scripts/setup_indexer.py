"""
Azure AI Search 인덱서 전체 설정
데이터 소스 → 인덱스 → 스킬셋 → 인덱서 순서로 생성
"""
import sys
from pathlib import Path
import time

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.service.azure_search import AzureSearchService


def main():
    print("🚀 Azure AI Search 인덱서 설정 시작...\n")
    print("=" * 60)
    
    try:
        search_service = AzureSearchService()
        
        # Step 1: 데이터 소스 생성
        print("\n📦 Step 1/4: 데이터 소스 생성 중...")
        if not search_service.create_data_source():
            print("❌ 데이터 소스 생성 실패")
            return False
        
        # Step 2: 인덱스 생성
        print("\n📋 Step 2/4: 인덱스 생성 중...")
        if not search_service.create_index():
            print("❌ 인덱스 생성 실패")
            return False
        
        # Step 3: 스킬셋 생성
        print("\n🧠 Step 3/4: 스킬셋 생성 중...")
        if not search_service.create_skillset():
            print("❌ 스킬셋 생성 실패")
            return False
        
        # Step 4: 인덱서 생성
        print("\n🤖 Step 4/4: 인덱서 생성 중...")
        if not search_service.create_indexer():
            print("❌ 인덱서 생성 실패")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 인덱서 설정 완료!")
        print("=" * 60)
        
        # Step 5: 인덱서 즉시 실행
        print("\n🔄 인덱서를 즉시 실행하시겠습니까? (y/n): ", end="")
        response = input().strip().lower()
        
        if response == 'y':
            print("\n⏳ 인덱서 실행 중...")
            if search_service.run_indexer():
                print("\n✅ 인덱서가 실행되었습니다!")
                print("⏰ 처리 시간: 약 1-2분 소요")
                print("\n📍 Azure Portal에서 진행 상황 확인:")
                print("   AI Search > 인덱서 > kite-auto-indexer")
                
                # 상태 확인
                print("\n⏳ 10초 후 상태 확인...")
                time.sleep(10)
                
                status = search_service.get_indexer_status()
                print(f"\n📊 현재 상태: {status.get('status', 'Unknown')}")
                print(f"   마지막 실행: {status.get('last_result', 'N/A')}")
        
        print("\n" + "=" * 60)
        print("✅ 설정 완료! 다음 단계:")
        print("=" * 60)
        print("\n1. Blob Storage에 문서 업로드:")
        print("   python scripts/upload_to_blob.py")
        print("\n2. 인덱서가 자동으로 처리 (5분마다)")
        print("   또는 즉시 실행: search_service.run_indexer()")
        print("\n3. 검색 테스트:")
        print("   python backend/main.py")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)