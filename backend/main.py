"""
FastAPI 백엔드 메인 서버 (RAG 통합)
"""
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import io
import tempfile
import os
import ffmpeg

from service.rag_service import RAGService
from service.azure_speech import AzureSpeechService

app = FastAPI(title="Kite API", version="1.0.0")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서비스 초기화
try:
    rag_service = RAGService()
    print("✅ RAG 서비스 초기화 완료")
except Exception as e:
    print(f"⚠️ RAG 서비스 초기화 실패: {str(e)}")
    rag_service = None

try:
    speech_service = AzureSpeechService()
    print("✅ Speech Service 초기화 완료")
except Exception as e:
    print(f"⚠️ Speech Service 초기화 실패: {e}")
    speech_service = None


# 요청/응답 모델
class QueryRequest(BaseModel):
    query: str


class AnalyzeResponse(BaseModel):
    query: str
    summary: str
    documents: List[Dict]
    action_items: List[str]
    estimated_time: str
    difficulty: str


def convert_audio_to_wav(audio_data: bytes, input_format: str = "webm") -> bytes:
    """오디오를 Azure Speech가 인식 가능한 WAV 형식으로 변환"""
    try:
        print(f"🔄 오디오 변환 시작 ({input_format} → WAV PCM 16-bit)...")
        
        # 임시 입력 파일
        with tempfile.NamedTemporaryFile(suffix=f".{input_format}", delete=False) as temp_input:
            temp_input.write(audio_data)
            input_path = temp_input.name
        
        # 임시 출력 파일
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_output:
            output_path = temp_output.name
        
        try:
            # ffmpeg로 변환
            stream = ffmpeg.input(input_path)
            stream = ffmpeg.output(
                stream,
                output_path,
                ar=16000,
                ac=1,
                acodec='pcm_s16le',
                format='wav'
            )
            ffmpeg.run(stream, overwrite_output=True, quiet=True)
            
            # 변환된 파일 읽기
            with open(output_path, 'rb') as f:
                wav_data = f.read()
            
            print(f"✅ 변환 완료: {len(audio_data)} bytes → {len(wav_data)} bytes")
            return wav_data
            
        finally:
            if os.path.exists(input_path):
                os.unlink(input_path)
            if os.path.exists(output_path):
                os.unlink(output_path)
        
    except Exception as e:
        print(f"❌ 오디오 변환 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"오디오 변환 중 오류: {str(e)}")


@app.get("/")
def read_root():
    return {
        "service": "Kite API",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "analyze": ["/api/analyze", "/analyze"],
            "speech": "/api/speech-to-text",
            "health": "/health"
        }
    }


async def _analyze_query_logic(request: QueryRequest) -> AnalyzeResponse:
    """업무 맥락 분석 로직 (공통)"""
    if not rag_service:
        raise HTTPException(status_code=503, detail="RAG Service를 사용할 수 없습니다")
    
    try:
        query = request.query
        
        # 1. 관련 문서 검색 (최소 점수 0.03)
        documents = rag_service.search_relevant_documents(query, top=5, min_score=0.03)
        
        # 2. AI 요약 생성
        summary = rag_service.generate_context_aware_summary(query, documents)
        
        # 3. ⭐ 문서가 있을 때만 액션 아이템 생성
        if documents and len(documents) > 0:
            action_items = rag_service.generate_action_items(query, documents)
            estimated_time = "2-3일"
            difficulty = "중"
        else:
            # 문서가 없으면 빈 액션 아이템
            action_items = []
            estimated_time = "N/A"
            difficulty = "N/A"
        
        return AnalyzeResponse(
            query=query,
            summary=summary,
            documents=documents,
            action_items=action_items,
            estimated_time=estimated_time,
            difficulty=difficulty
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_query_api(request: QueryRequest):
    """업무 맥락 분석 API (표준 경로)"""
    return await _analyze_query_logic(request)


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_query_legacy(request: QueryRequest):
    """업무 맥락 분석 API (레거시 경로 - 프론트엔드 호환)"""
    return await _analyze_query_logic(request)


@app.post("/api/speech-to-text")
async def speech_to_text(audio: UploadFile = File(...)):
    """음성을 텍스트로 변환하는 API"""
    print(f"📥 음성 파일 수신: {audio.filename}, 타입: {audio.content_type}")
    
    if not speech_service:
        raise HTTPException(
            status_code=503, 
            detail="Speech Service를 사용할 수 없습니다. Azure Speech 설정을 확인하세요."
        )
    
    try:
        # 오디오 파일 읽기
        audio_data = await audio.read()
        print(f"📊 원본 오디오 크기: {len(audio_data)} bytes")
        
        # 오디오 형식 변환
        print("🔄 오디오 형식 변환 중...")
        if "webm" in (audio.content_type or "").lower() or "webm" in (audio.filename or "").lower():
            audio_data = convert_audio_to_wav(audio_data, "webm")
        else:
            audio_data = convert_audio_to_wav(audio_data, "wav")
        
        # 음성 인식
        print("🎤 음성 인식 시작...")
        recognized_text = speech_service.recognize_from_audio_data(audio_data)
        
        if recognized_text is None or not recognized_text.strip():
            print("⚠️ 음성 인식 실패 또는 빈 결과")
            raise HTTPException(
                status_code=400,
                detail="음성을 인식할 수 없습니다. 더 크고 명확하게 말씀해주세요."
            )
        
        print(f"✅ 음성 인식 성공: {recognized_text}")
        return {"text": recognized_text}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ 음성 인식 중 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"음성 인식 중 오류: {str(e)}")


@app.get("/api/speech/languages")
async def get_supported_languages():
    """지원하는 언어 목록"""
    if not speech_service:
        raise HTTPException(status_code=503, detail="Speech Service를 사용할 수 없습니다")
    
    try:
        return {"languages": speech_service.get_supported_languages()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "services": {
            "rag": "ok" if rag_service else "error",
            "speech": "ok" if speech_service else "error"
        }
    }


@app.get("/indexer/status")
async def get_indexer_status():
    """인덱서 상태 조회"""
    try:
        from service.azure_search import AzureSearchService
        search_service = AzureSearchService()
        status = search_service.get_indexer_status()
        return {"indexer": "kite-auto-indexer", "status": status}
    except Exception as e:
        return {"error": str(e)}


@app.post("/indexer/run")
async def run_indexer():
    """인덱서 수동 실행"""
    try:
        from service.azure_search import AzureSearchService
        search_service = AzureSearchService()
        
        if search_service.run_indexer():
            return {"message": "인덱서 실행 시작", "estimated_time": "1-2분"}
        else:
            return {"error": "인덱서 실행 실패"}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)