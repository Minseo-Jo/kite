import React, { useState, useEffect } from 'react';
import {
  Card,
  List,
  Button,
  Tag,
  Space,
  Select,
  Input,
  Modal,
  Form,
  Radio,
  Empty,
  Collapse,
  Checkbox,
} from 'antd';
import {
  PlusOutlined,
  DeleteOutlined,
  EditOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  SyncOutlined,
  QuestionCircleOutlined,
} from '@ant-design/icons';
import { WorkNote } from '../types';

const { TextArea } = Input;
const { Panel } = Collapse;

interface NotesByQuery {
  [query: string]: WorkNote[];
}

export const WorkNotesPage: React.FC = () => {
  const [notes, setNotes] = useState<WorkNote[]>([]);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterPriority, setFilterPriority] = useState<string>('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingNote, setEditingNote] = useState<WorkNote | null>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    const savedNotes = localStorage.getItem('workNotes');
    if (savedNotes) {
      setNotes(JSON.parse(savedNotes));
    }
  }, []);

  const saveNotes = (newNotes: WorkNote[]) => {
    setNotes(newNotes);
    localStorage.setItem('workNotes', JSON.stringify(newNotes));
  };

  const handleSaveNote = (values: any) => {
    if (editingNote) {
      const updatedNotes = notes.map((note) =>
        note.id === editingNote.id
          ? { ...note, ...values, updatedAt: new Date().toISOString() }
          : note
      );
      saveNotes(updatedNotes);
    } else {
      const newNote: WorkNote = {
        id: Date.now().toString(),
        ...values,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        tags: [],
      };
      saveNotes([newNote, ...notes]);
    }
    setIsModalOpen(false);
    setEditingNote(null);
    form.resetFields();
  };

  const handleDeleteNote = (id: string) => {
    saveNotes(notes.filter((note) => note.id !== id));
  };

  const handleStatusChange = (id: string, checked: boolean) => {
    const updatedNotes = notes.map((note) =>
      note.id === id
        ? {
            ...note,
            status: checked ? ('done' as const) : ('todo' as const),
            updatedAt: new Date().toISOString(),
          }
        : note
    );
    saveNotes(updatedNotes);
  };

  // 필터링된 노트
  const filteredNotes = notes.filter((note) => {
    if (filterStatus !== 'all' && note.status !== filterStatus) return false;
    if (filterPriority !== 'all' && note.priority !== filterPriority) return false;
    return true;
  });

  // 질문별로 그룹화
  const notesByQuery: NotesByQuery = filteredNotes.reduce((acc, note) => {
    const query = note.relatedQuery || '기타';
    if (!acc[query]) {
      acc[query] = [];
    }
    acc[query].push(note);
    return acc;
  }, {} as NotesByQuery);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return '#ff6b9d';
      case 'medium':
        return '#ffa07a';
      case 'low':
        return '#98d8c8';
      default:
        return 'default';
    }
  };

  const getPriorityText = (priority: string) => {
    switch (priority) {
      case 'high':
        return '높음';
      case 'medium':
        return '보통';
      case 'low':
        return '낮음';
      default:
        return '';
    }
  };

  return (
    <div style={{ padding: '24px 50px', background: '#fff5f7', minHeight: '100vh' }}>
      <div style={{ maxWidth: 1200, margin: '0 auto' }}>
        {/* 헤더 */}
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
                📝 내 업무 노트
              </h2>
              <p style={{ margin: '8px 0 0 0', color: '#8b6969', fontSize: 15 }}>
                AI가 추천한 액션 아이템을 질문별로 정리하고 관리하세요
              </p>
            </div>
            <Button
              type="primary"
              icon={<PlusOutlined />}
              size="large"
              onClick={() => {
                setEditingNote(null);
                form.resetFields();
                setIsModalOpen(true);
              }}
              style={{
                background: '#ff9a9e',
                borderColor: '#ff9a9e',
                height: 44,
                fontWeight: 600,
              }}
            >
              새 노트 추가
            </Button>
          </div>
        </Card>

        {/* 필터 */}
        <Card style={{ marginBottom: 24 }}>
          <Space size="large">
            <Space>
              <span style={{ fontWeight: 600 }}>상태:</span>
              <Select
                value={filterStatus}
                onChange={setFilterStatus}
                style={{ width: 120 }}
                options={[
                  { label: '전체', value: 'all' },
                  { label: '예정', value: 'todo' },
                  { label: '진행중', value: 'in-progress' },
                  { label: '완료', value: 'done' },
                ]}
              />
            </Space>
            <Space>
              <span style={{ fontWeight: 600 }}>우선순위:</span>
              <Select
                value={filterPriority}
                onChange={setFilterPriority}
                style={{ width: 120 }}
                options={[
                  { label: '전체', value: 'all' },
                  { label: '높음', value: 'high' },
                  { label: '보통', value: 'medium' },
                  { label: '낮음', value: 'low' },
                ]}
              />
            </Space>
            <Tag color="blue" style={{ fontSize: 13, padding: '4px 12px' }}>
              총 {filteredNotes.length}개 업무
            </Tag>
          </Space>
        </Card>

        {/* 질문별 그룹 노트 */}
        {Object.keys(notesByQuery).length === 0 ? (
          <Card>
            <Empty
              description="업무 노트가 없습니다. 업무 분석 페이지에서 액션 아이템을 추가해보세요!"
              image={Empty.PRESENTED_IMAGE_SIMPLE}
            />
          </Card>
        ) : (
          <Collapse
            defaultActiveKey={Object.keys(notesByQuery)}
            style={{ background: 'transparent', border: 'none' }}
          >
            {Object.entries(notesByQuery).map(([query, queryNotes]) => {
              const completedCount = queryNotes.filter((n) => n.status === 'done').length;
              const totalCount = queryNotes.length;
              const progress = Math.round((completedCount / totalCount) * 100);

              return (
                <Panel
                  header={
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                      <Space>
                        <QuestionCircleOutlined style={{ fontSize: 18, color: '#ff9a9e' }} />
                        <span style={{ fontSize: 16, fontWeight: 600 }}>
                          {query}
                        </span>
                      </Space>
                      <Space>
                        <Tag color="green">
                          {completedCount}/{totalCount} 완료
                        </Tag>
                        <Tag color={progress === 100 ? 'success' : 'processing'}>
                          {progress}%
                        </Tag>
                      </Space>
                    </div>
                  }
                  key={query}
                  style={{
                    marginBottom: 16,
                    background: '#fff',
                    borderRadius: 8,
                    border: '1px solid #ffe4e6',
                  }}
                >
                  <List
                    dataSource={queryNotes}
                    renderItem={(note) => (
                      <List.Item
                        style={{
                          padding: '16px 0',
                          borderBottom: '1px solid #fff0f1',
                        }}
                      >
                        <div style={{ width: '100%' }}>
                          <div style={{ display: 'flex', alignItems: 'flex-start', gap: 12 }}>
                            <Checkbox
                              checked={note.status === 'done'}
                              onChange={(e) => handleStatusChange(note.id, e.target.checked)}
                              style={{ marginTop: 4 }}
                            />
                            <div style={{ flex: 1 }}>
                              <div style={{ marginBottom: 8 }}>
                                <Tag
                                  color={getPriorityColor(note.priority)}
                                  style={{ marginRight: 8 }}
                                >
                                  {getPriorityText(note.priority)}
                                </Tag>
                                <span
                                  style={{
                                    fontSize: 15,
                                    fontWeight: 600,
                                    textDecoration:
                                      note.status === 'done' ? 'line-through' : 'none',
                                    opacity: note.status === 'done' ? 0.5 : 1,
                                  }}
                                >
                                  {note.title}
                                </span>
                              </div>
                              <p
                                style={{
                                  margin: '8px 0',
                                  color: '#666',
                                  fontSize: 14,
                                  textDecoration:
                                    note.status === 'done' ? 'line-through' : 'none',
                                  opacity: note.status === 'done' ? 0.5 : 1,
                                }}
                              >
                                {note.content}
                              </p>
                              <div style={{ fontSize: 12, color: '#999' }}>
                                수정: {new Date(note.updatedAt).toLocaleString()}
                              </div>
                            </div>
                            <Space>
                              <Button
                                type="text"
                                icon={<EditOutlined />}
                                size="small"
                                onClick={() => {
                                  setEditingNote(note);
                                  form.setFieldsValue(note);
                                  setIsModalOpen(true);
                                }}
                              >
                                수정
                              </Button>
                              <Button
                                type="text"
                                danger
                                icon={<DeleteOutlined />}
                                size="small"
                                onClick={() => handleDeleteNote(note.id)}
                              >
                                삭제
                              </Button>
                            </Space>
                          </div>
                        </div>
                      </List.Item>
                    )}
                  />
                </Panel>
              );
            })}
          </Collapse>
        )}
      </div>

      {/* 노트 추가/수정 모달 */}
      <Modal
        title={editingNote ? '노트 수정' : '새 노트 추가'}
        open={isModalOpen}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingNote(null);
          form.resetFields();
        }}
        onOk={() => form.submit()}
        width={600}
        okText="저장"
        cancelText="취소"
        okButtonProps={{
          style: { background: '#ff9a9e', borderColor: '#ff9a9e' },
        }}
      >
        <Form form={form} layout="vertical" onFinish={handleSaveNote}>
          <Form.Item
            label="제목"
            name="title"
            rules={[{ required: true, message: '제목을 입력하세요' }]}
          >
            <Input placeholder="예: ERD 작성하기" size="large" />
          </Form.Item>

          <Form.Item
            label="내용"
            name="content"
            rules={[{ required: true, message: '내용을 입력하세요' }]}
          >
            <TextArea rows={4} placeholder="세부 내용을 입력하세요" />
          </Form.Item>

          <Form.Item
            label="우선순위"
            name="priority"
            initialValue="medium"
            rules={[{ required: true }]}
          >
            <Radio.Group>
              <Radio.Button value="high">높음</Radio.Button>
              <Radio.Button value="medium">보통</Radio.Button>
              <Radio.Button value="low">낮음</Radio.Button>
            </Radio.Group>
          </Form.Item>

          <Form.Item label="상태" name="status" initialValue="todo" rules={[{ required: true }]}>
            <Radio.Group>
              <Radio.Button value="todo">예정</Radio.Button>
              <Radio.Button value="in-progress">진행중</Radio.Button>
              <Radio.Button value="done">완료</Radio.Button>
            </Radio.Group>
          </Form.Item>

          <Form.Item label="연관 질문 (선택)" name="relatedQuery">
            <Input placeholder="예: Redis Stream 테이블 설계란?" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};