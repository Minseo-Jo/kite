// 문서 타입
export interface Document {
  id: string;
  title: string;
  content: string;
  source: string;
  date: string;
  sender?: string;
  score?: number;
}

// API 응답 타입
export interface AnalyzeResponse {
  query: string;
  summary: string;
  documents: Document[];
  action_items: string[];
  metadata?: {
    documents_found: number;
    search_method: string;
    ai_model: string;
  };
  error?: string;
}

// 검색 요청 타입
export interface AnalyzeRequest {
  query: string;
}

// 업무 노트 타입
export interface WorkNote {
  id: string;
  title: string;
  content: string;
  priority: 'high' | 'medium' | 'low';
  status: 'todo' | 'in-progress' | 'done';
  createdAt: string;
  updatedAt: string;
  relatedQuery?: string;
  tags: string[];
}

// 검색 이력 타입
export interface SearchHistory {
  id: string;
  query: string;
  timestamp: string;
  documentsFound: number;
}