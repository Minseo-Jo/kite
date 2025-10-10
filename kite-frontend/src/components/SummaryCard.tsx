import React from 'react';
import { Card, Typography } from 'antd';
import { BookOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown';

const { Title } = Typography;

interface SummaryCardProps {
  summary: string;
}

export const SummaryCard: React.FC<SummaryCardProps> = ({ summary }) => {
  return (
    <Card
      style={{ 
        marginBottom: 24,
        borderLeft: '4px solid #ff9a9e',
      }}
      title={
        <Title level={4} style={{ margin: 0 }}>
          <BookOutlined style={{ marginRight: 8, color: '#ff9a9e' }} />
          업무 맥락 요약
        </Title>
      }
    >
      <div className="markdown-content">
        <ReactMarkdown>{summary}</ReactMarkdown>
      </div>
    </Card>
  );
};