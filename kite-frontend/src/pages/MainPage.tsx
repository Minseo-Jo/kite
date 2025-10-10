import React, { useState, useEffect } from 'react';
import { Layout, Spin, Alert, Card, Typography } from 'antd';
import { Header } from '../components/Header';
import { SearchInput } from '../components/SearchInput';
import { SummaryCard } from '../components/SummaryCard';
import { DocumentList } from '../components/DocumentList';
import { ActionItems } from '../components/ActionItems';
import { WorkNotesPage } from './WorkNotesPage';
import { SearchHistoryPage } from './SearchHistoryPage';
import { analyzeQuery } from '../services/api';
import { AnalyzeResponse, WorkNote, SearchHistory } from '../types';

const { Content } = Layout;
const { Paragraph } = Typography;

export const MainPage: React.FC = () => {
  const [currentTab, setCurrentTab] = useState<string>('search');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (query: string) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await analyzeQuery(query);
      setResult(response);

      // 검색 이력 저장
      const history: SearchHistory[] = JSON.parse(
        localStorage.getItem('searchHistory') || '[]'
      );
      const newHistoryItem: SearchHistory = {
        id: Date.now().toString(),
        query,
        timestamp: new Date().toISOString(),
        documentsFound: response.documents.length,
      };
      localStorage.setItem(
        'searchHistory',
        JSON.stringify([newHistoryItem, ...history.slice(0, 49)])
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : '알 수 없는 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleSaveToNote = (item: string, index: number) => {
    const notes: WorkNote[] = JSON.parse(localStorage.getItem('workNotes') || '[]');
    const newNote: WorkNote = {
      id: Date.now().toString(),
      title: item,
      content: `AI가 추천한 액션 아이템입니다.`,
      priority: 'medium',
      status: 'todo',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      relatedQuery: result?.query || '',
      tags: [],
    };
    localStorage.setItem('workNotes', JSON.stringify([newNote, ...notes]));
  };

  const handleSearchAgain = (query: string) => {
    setCurrentTab('search');
    setTimeout(() => handleSearch(query), 100);
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header currentTab={currentTab} onTabChange={setCurrentTab} />

      <Content>
        {currentTab === 'search' && (
          <div style={{ padding: '40px 50px', background: '#fff5f7', minHeight: 'calc(100vh - 80px)' }}>
            <div style={{ maxWidth: 1200, margin: '0 auto' }}>
              {/* 히어로 섹션 */}
              <Card
                style={{
                  marginBottom: 32,
                  background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
                  border: 'none',
                  boxShadow: '0 8px 24px rgba(252, 182, 159, 0.3)',
                }}
              >
                <div style={{ textAlign: 'center', padding: '30px 0' }}>
                  <h1
                    style={{
                      fontSize: 36,
                      fontWeight: 800,
                      color: '#6b4f4f',
                      margin: 0,
                      marginBottom: 12,
                      textShadow: '0 2px 4px rgba(0,0,0,0.05)',
                    }}
                  >
                    업무가 쉬워지는 공간, Kite
                  </h1>
                  <Paragraph
                    style={{
                      fontSize: 17,
                      color: '#8b6969',
                      margin: 0,
                      fontWeight: 500,
                    }}
                  >
                    산재된 문서를 한 번에 분석하고, AI가 업무 맥락을 정리해드립니다
                  </Paragraph>
                </div>
              </Card>

              <SearchInput onSearch={handleSearch} loading={loading} />

              {loading && (
                <div style={{ textAlign: 'center', padding: 80, background: '#fff', borderRadius: 8 }}>
                  <Spin size="large" />
                  <Paragraph style={{ marginTop: 24, fontSize: 16, color: '#666' }}>
                    🔎 관련 문서를 찾고 AI가 분석하고 있습니다...
                  </Paragraph>
                </div>
              )}

              {error && (
                <Alert
                  message="오류 발생"
                  description={error}
                  type="error"
                  showIcon
                  closable
                  onClose={() => setError(null)}
                  style={{ marginBottom: 24 }}
                />
              )}

              {result && !loading && (
                <>
                  <SummaryCard summary={result.summary} />
                  <DocumentList documents={result.documents} />
                  <ActionItems items={result.action_items} onSaveToNote={handleSaveToNote} />
                </>
              )}

              {!loading && !error && !result && (
                <Card style={{ textAlign: 'center', padding: 40 }}>
                  <div style={{ fontSize: 48, marginBottom: 16 }}>🪁</div>
                  <h3 style={{ fontSize: 18, color: '#666', fontWeight: 400 }}>
                    업무 관련 질문을 입력하면 AI가 맥락을 분석해드립니다
                  </h3>
                </Card>
              )}
            </div>
          </div>
        )}

        {currentTab === 'notes' && <WorkNotesPage />}

        {currentTab === 'history' && (
          <SearchHistoryPage onSearchAgain={handleSearchAgain} />
        )}
      </Content>
    </Layout>
  );
};