"""
Azure Speech Service 테스트 스크립트
"""
import os
from dotenv import load_dotenv
from service.azure_speech import AzureSpeechService
load_dotenv()


def test_speech_service():
    """Speech Service 기본 테스트"""
    print("=== Azure Speech Service 테스트 ===\n")
    
    try:
        # 서비스 초기화
        speech_service = AzureSpeechService()
        print("✅ Speech Service 초기화 성공\n")
        
        # 지원 언어 확인
        languages = speech_service.get_supported_languages()
        print("📋 지원하는 언어:")
        for lang in languages:
            print(f"  - {lang['name']} ({lang['code']})")
        
        print("\n테스트 완료!")
        print("실제 음성 인식은 프론트엔드에서 오디오 파일과 함께 테스트하세요.")
        
    except Exception as e:
        print(f"❌ 테스트 실패: {str(e)}")
        print("\n해결 방법:")
        print("1. .env 파일에 AZURE_SPEECH_KEY가 설정되어 있는지 확인")
        print("2. .env 파일에 AZURE_SPEECH_REGION이 설정되어 있는지 확인")
        print("3. Azure Portal에서 Speech Service 리소스가 생성되어 있는지 확인")


if __name__ == "__main__":
    test_speech_service()