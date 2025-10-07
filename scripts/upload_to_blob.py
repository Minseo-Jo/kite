"""
샘플 문서를 Azure Blob Storage에 업로드
"""
import sys
from pathlib import Path

# 경로 설정
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from backend.service.azure_blob import AzureBlobService
from data.sample_documents import get_sample_documents


def main():
    print("🚀 샘플 문서를 Blob Storage에 업로드 시작...\n")
    
    try:
        # Blob 서비스 초기화
        blob_service = AzureBlobService()
        
        # 샘플 문서 가져오기
        documents = get_sample_documents()
        print(f"📄 업로드할 문서: {len(documents)}개\n")
        
        # 문서 업로드
        print("🔄 업로드 진행 중...\n")
        success_count = blob_service.upload_documents(documents)
        
        if success_count == len(documents):
            print(f"\n🎉 모든 문서 업로드 완료! ({success_count}개)")
            print("\n📍 Azure Portal에서 확인:")
            print("   Storage Account > 컨테이너 > kite-documents")
            print("\n✅ 다음 단계: 인덱서가 자동으로 문서를 처리합니다 (최대 5분 소요)")
            return True
        else:
            print(f"\n⚠️ 일부 문서 업로드 실패: {success_count}/{len(documents)}개 성공")
            return False
            
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)