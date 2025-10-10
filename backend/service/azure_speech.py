"""
Azure Speech Service - 음성 인식
"""
import os
import io
import wave
import tempfile
from typing import Optional
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()


class AzureSpeechService:
    """Azure Speech 서비스"""
    
    def __init__(self):
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        speech_region = os.getenv("AZURE_SPEECH_REGION")
        
        if not speech_key or not speech_region:
            raise ValueError("AZURE_SPEECH_KEY와 AZURE_SPEECH_REGION을 .env에 설정해주세요")
        
        # Speech Config 설정
        self.speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region
        )
        
        # 한국어 설정
        self.speech_config.speech_recognition_language = "ko-KR"
        
        print("✅ Azure Speech Service 초기화 완료")
    
    def recognize_from_audio_data(self, audio_data: bytes) -> Optional[str]:
        """
        오디오 데이터에서 텍스트 추출
        
        Args:
            audio_data: WAV 형식의 오디오 바이트 데이터
            
        Returns:
            인식된 텍스트 또는 None
        """
        try:
            print(f"📊 수신된 오디오 크기: {len(audio_data)} bytes")
            
            # 임시 WAV 파일로 저장
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            try:
                # WAV 파일 정보 읽기
                with wave.open(temp_path, 'rb') as wav_file:
                    sample_rate = wav_file.getframerate()
                    channels = wav_file.getnchannels()
                    sample_width = wav_file.getsampwidth()
                    
                    print(f"📝 WAV 정보: {sample_rate}Hz, {channels}채널, {sample_width*8}bit")
                
                # 파일에서 직접 오디오 읽기
                audio_config = speechsdk.audio.AudioConfig(filename=temp_path)
                
                # Speech Recognizer 생성
                speech_recognizer = speechsdk.SpeechRecognizer(
                    speech_config=self.speech_config,
                    audio_config=audio_config
                )
                
                print("🎤 음성 인식 시작...")
                
                # 음성 인식 실행 (동기)
                result = speech_recognizer.recognize_once()
                
                # 결과 처리
                if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                    print(f"✅ 음성 인식 성공: {result.text}")
                    return result.text
                elif result.reason == speechsdk.ResultReason.NoMatch:
                    print("⚠️ 음성을 인식하지 못했습니다")
                    no_match = result.no_match_details
                    print(f"NoMatch 이유: {no_match.reason}")
                    return None
                elif result.reason == speechsdk.ResultReason.Canceled:
                    cancellation = result.cancellation_details
                    print(f"❌ 음성 인식 취소: {cancellation.reason}")
                    if cancellation.reason == speechsdk.CancellationReason.Error:
                        print(f"에러 코드: {cancellation.error_code}")
                        print(f"에러 상세: {cancellation.error_details}")
                    return None
                else:
                    print(f"⚠️ 알 수 없는 결과: {result.reason}")
                    return None
                    
            finally:
                # 임시 파일 삭제
                os.unlink(temp_path)
            
        except Exception as e:
            print(f"❌ 음성 인식 중 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_supported_languages(self) -> list:
        """지원하는 언어 목록"""
        return [
            {"code": "ko-KR", "name": "한국어"},
            {"code": "en-US", "name": "영어 (미국)"},
            {"code": "ja-JP", "name": "일본어"},
            {"code": "zh-CN", "name": "중국어 (간체)"}
        ]