import React from 'react';
import { Layout, Space, Button } from 'antd';
import { RocketOutlined, FileTextOutlined, HistoryOutlined } from '@ant-design/icons';

const { Header: AntHeader } = Layout;

interface HeaderProps {
  currentTab: string;
  onTabChange: (tab: string) => void;
}

export const Header: React.FC<HeaderProps> = ({ currentTab, onTabChange }) => {
  return (
    <AntHeader
      style={{
        background: 'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
        padding: '0 50px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        boxShadow: '0 4px 12px rgba(252, 182, 159, 0.3)',
        height: 80,
        position: 'sticky',
        top: 0,
        zIndex: 100,
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
        <div
          style={{
            width: 56,
            height: 56,
            background: 'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
            borderRadius: 14,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 4px 16px rgba(255, 154, 158, 0.5)',
            flexShrink: 0,
          }}
        >
          <RocketOutlined style={{ fontSize: 32, color: '#fff' }} />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <h1
            style={{
              margin: 0,
              padding: 0,
              color: '#6b4f4f',
              fontSize: 32,
              fontWeight: 900,
              letterSpacing: '-1px',
              lineHeight: 1,
              marginBottom: 4,
            }}
          >
            Kite
          </h1>
          <p
            style={{
              margin: 0,
              padding: 0,
              color: '#8b6969',
              fontSize: 14,
              fontWeight: 500,
              lineHeight: 1,
            }}
          >
            업무 맥락을 한눈에 파악하세요
          </p>
        </div>
      </div>

      <Space size="large">
        <Button
          type={currentTab === 'search' ? 'primary' : 'text'}
          icon={<FileTextOutlined />}
          onClick={() => onTabChange('search')}
          size="large"
          style={{
            color: currentTab === 'search' ? '#fff' : '#6b4f4f',
            borderColor: currentTab === 'search' ? '#ff9a9e' : 'transparent',
            background: currentTab === 'search' ? '#ff9a9e' : 'transparent',
            fontWeight: 600,
            height: 44,
            padding: '0 24px',
            fontSize: 15,
          }}
        >
          업무 분석
        </Button>
        <Button
          type={currentTab === 'notes' ? 'primary' : 'text'}
          icon={<FileTextOutlined />}
          onClick={() => onTabChange('notes')}
          size="large"
          style={{
            color: currentTab === 'notes' ? '#fff' : '#6b4f4f',
            borderColor: currentTab === 'notes' ? '#ff9a9e' : 'transparent',
            background: currentTab === 'notes' ? '#ff9a9e' : 'transparent',
            fontWeight: 600,
            height: 44,
            padding: '0 24px',
            fontSize: 15,
          }}
        >
          내 업무 노트
        </Button>
        <Button
          type={currentTab === 'history' ? 'primary' : 'text'}
          icon={<HistoryOutlined />}
          onClick={() => onTabChange('history')}
          size="large"
          style={{
            color: currentTab === 'history' ? '#fff' : '#6b4f4f',
            borderColor: currentTab === 'history' ? '#ff9a9e' : 'transparent',
            background: currentTab === 'history' ? '#ff9a9e' : 'transparent',
            fontWeight: 600,
            height: 44,
            padding: '0 24px',
            fontSize: 15,
          }}
        >
          검색 이력
        </Button>
      </Space>
    </AntHeader>
  );
};