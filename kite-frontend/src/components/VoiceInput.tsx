import React, { useState, useRef, useEffect } from 'react';
import { Button, message } from 'antd';
import { AudioOutlined, LoadingOutlined } from '@ant-design/icons';

interface VoiceInputProps {
  onTranscript: (text: string) => void;
  disabled?: boolean;
}

export const VoiceInput: React.FC<VoiceInputProps> = ({ onTranscript, disabled }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // 키보드 단축키: Ctrl+Shift+M
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.ctrlKey && e.shiftKey && e.key === 'M') {
        e.preventDefault();
        if (!disabled && !isProcessing) {
          isRecording ? stopRecording() : startRecording();
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [isRecording, disabled, isProcessing]);

  const startRecording = async () => {
    try {
      // 마이크 권한 요청
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100,
        } 
      });
      
      // MediaRecorder 생성
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm',
      });
      
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      // 데이터 수집
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      // 녹음 종료 시 처리
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await sendAudioToAPI(audioBlob);
        
        // 스트림 정리
        stream.getTracks().forEach(track => track.stop());
      };

      // 녹음 시작
      mediaRecorder.start();
      setIsRecording(true);
      message.info({
        content: '🎤 음성 인식 중... 말씀해주세요',
        duration: 0,
        key: 'recording',
      });

    } catch (error) {
      console.error('녹음 시작 실패:', error);
      if (error instanceof Error && error.name === 'NotAllowedError') {
        message.error('마이크 접근 권한이 필요합니다. 브라우저 설정을 확인해주세요.');
      } else {
        message.error('마이크를 사용할 수 없습니다. 마이크가 연결되어 있는지 확인해주세요.');
      }
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      message.destroy('recording');
      message.loading({
        content: '음성 분석 중...',
        duration: 0,
        key: 'processing',
      });
      setIsProcessing(true);
    }
  };

  const sendAudioToAPI = async (audioBlob: Blob) => {
    try {
      // WebM을 WAV로 변환
      const wavBlob = await convertToWav(audioBlob);
      
      // FormData 생성
      const formData = new FormData();
      formData.append('audio', wavBlob, 'recording.wav');

      // API 호출
      const response = await fetch('http://localhost:8000/api/speech-to-text', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || '음성 인식 실패');
      }

      const data = await response.json();
      
      message.destroy('processing');
      
      if (data.text && data.text.trim()) {
        message.success('✅ 음성 인식 완료!');
        onTranscript(data.text);
      } else {
        message.warning('음성을 인식하지 못했습니다. 다시 시도해주세요.');
      }

    } catch (error) {
      console.error('음성 전송 실패:', error);
      message.destroy('processing');
      message.error(
        error instanceof Error 
          ? error.message 
          : '음성 인식 중 오류가 발생했습니다. 네트워크 연결을 확인해주세요.'
      );
    } finally {
      setIsProcessing(false);
    }
  };

  // WebM을 WAV로 변환
  const convertToWav = async (webmBlob: Blob): Promise<Blob> => {
    try {
      const audioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
      const arrayBuffer = await webmBlob.arrayBuffer();
      const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);
      
      // WAV 인코딩
      const wavBuffer = audioBufferToWav(audioBuffer);
      return new Blob([wavBuffer], { type: 'audio/wav' });
    } catch (error) {
      console.error('오디오 변환 실패:', error);
      // 변환 실패 시 원본 반환
      return webmBlob;
    }
  };

  // AudioBuffer를 WAV 형식으로 변환
  const audioBufferToWav = (buffer: AudioBuffer): ArrayBuffer => {
    const length = buffer.length * buffer.numberOfChannels * 2;
    const arrayBuffer = new ArrayBuffer(44 + length);
    const view = new DataView(arrayBuffer);

    // WAV 헤더 작성
    const writeString = (offset: number, string: string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };

    writeString(0, 'RIFF');
    view.setUint32(4, 36 + length, true);
    writeString(8, 'WAVE');
    writeString(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, buffer.numberOfChannels, true);
    view.setUint32(24, buffer.sampleRate, true);
    view.setUint32(28, buffer.sampleRate * buffer.numberOfChannels * 2, true);
    view.setUint16(32, buffer.numberOfChannels * 2, true);
    view.setUint16(34, 16, true);
    writeString(36, 'data');
    view.setUint32(40, length, true);

    // PCM 데이터 작성
    const channelData = buffer.getChannelData(0);
    let offset = 44;
    for (let i = 0; i < channelData.length; i++) {
      const sample = Math.max(-1, Math.min(1, channelData[i]));
      view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
      offset += 2;
    }

    return arrayBuffer;
  };

  return (
    <Button
      type={isRecording ? 'primary' : 'default'}
      danger={isRecording}
      icon={isProcessing ? <LoadingOutlined spin /> : <AudioOutlined />}
      onClick={isRecording ? stopRecording : startRecording}
      disabled={disabled || isProcessing}
      size="large"
      aria-label={isRecording ? '녹음 중지' : '음성 녹음 시작'}
      aria-pressed={isRecording}
      style={{
        borderRadius: '8px',
        width: '48px',
        height: '48px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        transition: 'all 0.3s ease',
        ...(isRecording && {
          animation: 'pulse 1.5s infinite',
        }),
      }}
    >
      <style>{`
        @keyframes pulse {
          0%, 100% {
            transform: scale(1);
            box-shadow: 0 0 0 0 rgba(255, 77, 79, 0.7);
          }
          50% {
            transform: scale(1.05);
            box-shadow: 0 0 0 10px rgba(255, 77, 79, 0);
          }
        }
      `}</style>
    </Button>
  );
};