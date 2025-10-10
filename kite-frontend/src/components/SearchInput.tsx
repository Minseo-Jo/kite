import React, { useState } from 'react';
import { Input, Button, Space, Typography, Tooltip } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { VoiceInput } from './VoiceInput';

const { Text } = Typography;

interface SearchInputProps {
  onSearch: (query: string) => void;
  loading: boolean;
}

export const SearchInput: React.FC<SearchInputProps> = ({
  onSearch,
  loading,
}) => {
  const [query, setQuery] = useState('');
  const [showTranscript, setShowTranscript] = useState(false);

  const handleSearch = () => {
    if (query.trim()) {
      onSearch(query);
    }
  };

  // ⭐ 음성 인식 결과 처리
  const handleVoiceTranscript = (text: string) => {
    setQuery(text);
    setShowTranscript(true);
    
    // 1.5초 후 자동으로 검색 실행
    setTimeout(() => {
      setShowTranscript(false);
      onSearch(text);
    }, 1500);
  };

  return (
    <div style={{ marginBottom: 24 }}>
      <Space direction="vertical" style={{ width: '100%' }} size="middle">
        {/* ⭐ 음성 인식 결과 표시 */}
        {showTranscript && (
          <div
            style={{
              padding: '12px 16px',
              background: 'linear-gradient(135deg, #e6f7ff 0%, #f0f5ff 100%)',
              borderRadius: '8px',
              border: '1px solid #91d5ff',
              animation: 'fadeIn 0.3s ease-in',
            }}
          >
            <Text type="secondary" style={{ fontSize: '12px', display: 'block', marginBottom: '4px' }}>
              🎤 음성 인식됨:
            </Text>
            <Text strong style={{ fontSize: '14px' }}>
              {query}
            </Text>
          </div>
        )}

        {/* 검색 입력 + 음성 버튼 */}
        <Space.Compact style={{ width: '100%' }}>
          <Input
            size="large"
            placeholder="업무 관련 질문을 입력하세요 (예: Redis Stream 테이블 설계가 뭐야?)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onPressEnter={handleSearch}
            disabled={loading}
            style={{ flex: 1 }}
          />
          
          {/* ⭐ 음성 입력 버튼 */}
          <Tooltip title="음성으로 질문하기 (Ctrl+Shift+M)">
            <div>
              <VoiceInput
                onTranscript={handleVoiceTranscript}
                disabled={loading}
              />
            </div>
          </Tooltip>
          
          {/* 기존 검색 버튼 */}
          <Button
            type="primary"
            size="large"
            icon={<SearchOutlined />}
            onClick={handleSearch}
            loading={loading}
            disabled={!query.trim()}
            style={{
              background: '#ff9a9e',
              borderColor: '#ff9a9e',
              fontWeight: 600,
              minWidth: '120px',
            }}
          >
            분석 시작
          </Button>
        </Space.Compact>

        {/* ⭐ 사용 팁 */}
        <div style={{ textAlign: 'center', marginTop: '4px' }}>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            💡 <strong>팁:</strong> 마이크 버튼을 눌러 음성으로 질문할 수 있습니다
          </Text>
        </div>
      </Space>

      {/* ⭐ 페이드인 애니메이션 CSS */}
      <style>{`
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};