import React, { useState, useEffect } from 'react';
import { Card, List, Tag, Button, Empty, Space, Input } from 'antd';
import { ClockCircleOutlined, SearchOutlined, DeleteOutlined } from '@ant-design/icons';
import { SearchHistory } from '../types';

interface SearchHistoryPageProps {
  onSearchAgain?: (query: string) => void;
}

export const SearchHistoryPage: React.FC<SearchHistoryPageProps> = ({ onSearchAgain }) => {
  const [history, setHistory] = useState<SearchHistory[]>([]);
  const [searchText, setSearchText] = useState('');

  useEffect(() => {
    const savedHistory = localStorage.getItem('searchHistory');
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory));
    }
  }, []);

  const handleDelete = (id: string) => {
    const newHistory = history.filter((item) => item.id !== id);
    setHistory(newHistory);
    localStorage.setItem('searchHistory', JSON.stringify(newHistory));
  };

  const handleClearAll = () => {
    setHistory([]);
    localStorage.removeItem('searchHistory');
  };

  const filteredHistory = history.filter((item) =>
    item.query.toLowerCase().includes(searchText.toLowerCase())
  );

  return (
    <div style={{ padding: '24px 50px', background: '#fff5f7', minHeight: '100vh' }}>
      <div style={{ maxWidth: 1200, margin: '0 auto' }}>
        <Card 
          style={{ 
            marginBottom: 24,
            background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
            border: 'none',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h2 style={{ margin: 0, fontSize: 26, fontWeight: 800, color: '#6b4f4f' }}>
                🕐 검색 이력
              </h2>
              <p style={{ margin: '8px 0 0 0', color: '#8b6969', fontSize: 15 }}>
                과거에 검색한 업무들을 다시 확인하세요
              </p>
            </div>
            {history.length > 0 && (
              <Button 
                danger 
                onClick={handleClearAll}
                style={{
                  background: '#ff6b9d',
                  borderColor: '#ff6b9d',
                  color: '#fff',
                }}
              >
                전체 삭제
              </Button>
            )}
          </div>
        </Card>

        {history.length > 0 && (
          <Card style={{ marginBottom: 24 }}>
            <Input
              placeholder="검색 이력에서 찾기..."
              prefix={<SearchOutlined />}
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              allowClear
            />
          </Card>
        )}

        {filteredHistory.length === 0 ? (
          <Card>
            <Empty
              description="검색 이력이 없습니다."
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            />
          </Card>
        ) : (
          <List
            dataSource={filteredHistory}
            renderItem={(item) => (
              <Card
                style={{ marginBottom: 16 }}
                hoverable
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div style={{ flex: 1 }}>
                    <Space direction="vertical" size="small" style={{ width: '100%' }}>
                      <div>
                        <Tag icon={<ClockCircleOutlined />} color="blue">
                          {new Date(item.timestamp).toLocaleString()}
                        </Tag>
                        <Tag color="green">{item.documentsFound}개 문서 발견</Tag>
                      </div>
                      <h3 style={{ margin: 0, fontSize: 16 }}>
                        {item.query}
                      </h3>
                    </Space>
                  </div>
                  <Space>
                    <Button
                      type="primary"
                      icon={<SearchOutlined />}
                      onClick={() => onSearchAgain && onSearchAgain(item.query)}
                    >
                      다시 검색
                    </Button>
                    <Button
                      danger
                      icon={<DeleteOutlined />}
                      onClick={() => handleDelete(item.id)}
                    >
                      삭제
                    </Button>
                  </Space>
                </div>
              </Card>
            )}
          />
        )}
      </div>
    </div>
  );
};