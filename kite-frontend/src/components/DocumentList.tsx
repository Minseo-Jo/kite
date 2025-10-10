import React from 'react';
import { Card, Collapse, Tag, Typography, Space } from 'antd';
import { FileTextOutlined, CalendarOutlined, UserOutlined } from '@ant-design/icons';
import { Document } from '../types';

const { Panel } = Collapse;
const { Text, Title } = Typography;

interface DocumentListProps {
  documents: Document[];
}

const getSourceColor = (source: string): string => {
  const colors: Record<string, string> = {
    '메일': '#ff9a9e',
    '슬랙': '#c77dff',
    '지라': '#98d8c8',
    '컨플루언스': '#ffb5a7',
    '구글 캘린더': '#ffc8dd',
  };
  return colors[source] || '#fdb5c8';
};

export const DocumentList: React.FC<DocumentListProps> = ({ documents }) => {
  if (documents.length === 0) {
    return null;
  }

  return (
    <Card
      style={{ marginBottom: 24 }}
      title={
        <Title level={4} style={{ margin: 0 }}>
          <FileTextOutlined style={{ marginRight: 8 }} />
          관련 문서 ({documents.length}개 발견)
        </Title>
      }
    >
      <Collapse accordion>
        {documents.map((doc, index) => (
          <Panel
            header={
              <Space direction="vertical" size={0} style={{ width: '100%' }}>
                <Space>
                  <Tag color={getSourceColor(doc.source)}>{doc.source}</Tag>
                  <Text strong>{doc.title}</Text>
                </Space>
                <Space size="small">
                  <Text type="secondary" style={{ fontSize: 12 }}>
                    <CalendarOutlined /> {doc.date}
                  </Text>
                  {doc.sender && (
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      <UserOutlined /> {doc.sender}
                    </Text>
                  )}
                  {doc.score && (
                    <Tag color="gold" style={{ fontSize: 11 }}>
                      관련도: {(doc.score * 100).toFixed(0)}%
                    </Tag>
                  )}
                </Space>
              </Space>
            }
            key={index}
          >
            <div style={{ whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>
              {doc.content}
            </div>
          </Panel>
        ))}
      </Collapse>
    </Card>
  );
};