"""
Azure Blob Storage 클라이언트
문서 업로드 및 관리
"""
import os
import json
from typing import List, Dict
from azure.storage.blob import BlobServiceClient, BlobClient, ContentSettings
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)


class AzureBlobService:
    """Azure Blob Storage 서비스"""
    
    def __init__(self):
        """클라이언트 초기화"""
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        
        # Blob 서비스 클라이언트
        self.blob_service_client = BlobServiceClient.from_connection_string(
            self.connection_string
        )
        
        # 컨테이너 클라이언트
        self.container_client = self.blob_service_client.get_container_client(
            self.container_name
        )
        
        logger.info("✅ Azure Blob Storage 클라이언트 초기화 완료")
    
    def upload_document(self, document: Dict, blob_name: str = None) -> bool:
        """
        단일 문서를 Blob Storage에 업로드
        
        Args:
            document: 업로드할 문서 딕셔너리
            blob_name: Blob 파일명 (없으면 document['id'].json 사용)
        
        Returns:
            성공 여부
        """
        try:
            if blob_name is None:
                blob_name = f"{document['id']}.json"
            
            # JSON 문자열로 변환
            json_data = json.dumps(document, ensure_ascii=False, indent=2)
            
            # Blob 업로드
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.upload_blob(
                json_data,
                overwrite=True,
                content_settings=ContentSettings(content_type='application/json')
            )
            
            logger.info(f"✅ 문서 업로드 성공: {blob_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 문서 업로드 실패: {blob_name}, {str(e)}")
            return False
    
    def upload_documents(self, documents: List[Dict]) -> int:
        """
        여러 문서를 일괄 업로드
        
        Args:
            documents: 문서 리스트
        
        Returns:
            성공한 문서 개수
        """
        success_count = 0
        
        for doc in documents:
            if self.upload_document(doc):
                success_count += 1
        
        logger.info(f"📊 일괄 업로드 완료: {success_count}/{len(documents)}개 성공")
        return success_count
    
    def list_blobs(self) -> List[str]:
        """컨테이너 내 모든 Blob 목록 반환"""
        try:
            blobs = self.container_client.list_blobs()
            blob_names = [blob.name for blob in blobs]
            
            logger.info(f"📄 Blob 목록 조회: {len(blob_names)}개 발견")
            return blob_names
            
        except Exception as e:
            logger.error(f"❌ Blob 목록 조회 실패: {str(e)}")
            return []
    
    def download_blob(self, blob_name: str) -> Dict:
        """
        Blob 다운로드 및 JSON 파싱
        
        Args:
            blob_name: Blob 파일명
        
        Returns:
            파싱된 문서 딕셔너리
        """
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_data = blob_client.download_blob().readall()
            
            # JSON 파싱
            document = json.loads(blob_data)
            
            logger.info(f"✅ Blob 다운로드 성공: {blob_name}")
            return document
            
        except Exception as e:
            logger.error(f"❌ Blob 다운로드 실패: {blob_name}, {str(e)}")
            return {}
    
    def delete_blob(self, blob_name: str) -> bool:
        """Blob 삭제"""
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            blob_client.delete_blob()
            
            logger.info(f"✅ Blob 삭제 성공: {blob_name}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Blob 삭제 실패: {blob_name}, {str(e)}")
            return False
    
    def get_blob_url(self, blob_name: str) -> str:
        """Blob URL 반환 (디버깅용)"""
        blob_client = self.container_client.get_blob_client(blob_name)
        return blob_client.url


def test_blob_service():
    """Blob 서비스 테스트"""
    try:
        blob_service = AzureBlobService()
        
        # 테스트 문서
        test_doc = {
            "id": "test_001",
            "title": "테스트 문서",
            "content": "Azure Blob Storage 연결 테스트입니다.",
            "source": "테스트",
            "date": "2025-10-07"
        }
        
        print("🔄 테스트 문서 업로드 중...")
        if blob_service.upload_document(test_doc):
            print("✅ 업로드 성공!")
        
        print("\n🔄 Blob 목록 조회 중...")
        blobs = blob_service.list_blobs()
        print(f"📄 발견된 Blob: {blobs}")
        
        print("\n🔄 테스트 문서 다운로드 중...")
        downloaded = blob_service.download_blob("test_001.json")
        print(f"✅ 다운로드 성공: {downloaded['title']}")
        
        print("\n✅ Azure Blob Storage 테스트 완료!")
        return True
        
    except Exception as e:
        print(f"❌ 테스트 실패: {e}")
        import traceback
        print(traceback.format_exc())
        return False


if __name__ == "__main__":
    test_blob_service()