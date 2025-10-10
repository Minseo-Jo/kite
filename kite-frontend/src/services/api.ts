import axios from 'axios';
import { AnalyzeRequest, AnalyzeResponse } from '../types';

// 백엔드 URL (환경변수로 관리)
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 업무 분석 API
export const analyzeQuery = async (query: string): Promise<AnalyzeResponse> => {
  try {
    const response = await api.post<AnalyzeResponse>('/analyze', {
      query,
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(
        error.response?.data?.error || '서버 연결에 실패했습니다.'
      );
    }
    throw error;
  }
};

// 헬스 체크 API
export const healthCheck = async (): Promise<boolean> => {
  try {
    const response = await api.get('/health');
    return response.status === 200;
  } catch {
    return false;
  }
};

export default api;