import React, { useState } from 'react';
import { Card, List, Checkbox, Button, Space, Tag, message, Typography } from 'antd';
import { CheckCircleOutlined, PlusOutlined, StarOutlined, StarFilled } from '@ant-design/icons';

const { Title } = Typography;

interface ActionItemsProps {
  items: string[];
  onSaveToNote?: (item: string, index: number) => void;
}

export const ActionItems: React.FC<ActionItemsProps> = ({ items, onSaveToNote }) => {
  const [checkedItems, setCheckedItems] = useState<Set<number>>(new Set());
  const [savedItems, setSavedItems] = useState<Set<number>>(new Set());

  const handleCheck = (index: number) => {
    setCheckedItems((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(index)) {
        newSet.delete(index);
      } else {
        newSet.add(index);
      }
      return newSet;
    });
  };

  const handleSave = (item: string, index: number) => {
    setSavedItems((prev) => new Set(prev).add(index));
    message.success('업무 노트에 저장되었습니다!');
    if (onSaveToNote) {
      onSaveToNote(item, index);
    }
  };

  if (items.length === 0) {
    return null;
  }

  return (
    <Card
      style={{
        borderLeft: '4px solid #ff9a9e',
      }}
      title={
        <Space>
          <CheckCircleOutlined style={{ fontSize: 20, color: '#ff9a9e' }} />
          <span style={{ fontSize: 18, fontWeight: 600 }}>
            추천 액션 아이템
          </span>
          <Tag color="#ffe4e6" style={{ color: '#ff6b9d' }}>{items.length}개</Tag>
        </Space>
      }
      extra={
        <Tag color="#fff0f1" style={{ fontSize: 13, color: '#ff6b9d', borderColor: '#ffc0cb' }}>
          ⭐ 선택하여 내 업무 노트에 추가하세요
        </Tag>
      }
    >
      <List
        dataSource={items}
        renderItem={(item, index) => (
          <List.Item
            style={{
              padding: '16px 0',
              border: 'none',
              borderBottom: index === items.length - 1 ? 'none' : '1px solid #f0f0f0',
            }}
          >
            <div style={{ width: '100%', display: 'flex', alignItems: 'center', gap: 12 }}>
              <Checkbox
                checked={checkedItems.has(index)}
                onChange={() => handleCheck(index)}
              >
                <span
                  style={{
                    textDecoration: checkedItems.has(index) ? 'line-through' : 'none',
                    opacity: checkedItems.has(index) ? 0.5 : 1,
                    transition: 'all 0.3s',
                    fontSize: 15,
                  }}
                >
                  {index + 1}. {item}
                </span>
              </Checkbox>
              
              <Button
                type="text"
                size="small"
                icon={savedItems.has(index) ? <StarFilled /> : <StarOutlined />}
                onClick={() => handleSave(item, index)}
                disabled={savedItems.has(index)}
                style={{
                  marginLeft: 'auto',
                  color: savedItems.has(index) ? '#faad14' : undefined,
                }}
              >
                {savedItems.has(index) ? '저장됨' : '노트에 추가'}
              </Button>
            </div>
          </List.Item>
        )}
      />
    </Card>
  );
};


