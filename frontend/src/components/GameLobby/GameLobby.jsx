import React, { useState, useEffect } from 'react';
import { Card, Button, Input, Select, Space, Table, Tag, message, Modal, Form } from 'antd';
import { 
  PlusOutlined, 
  ReloadOutlined, 
  UserOutlined,
  RobotOutlined,
  SettingOutlined
} from '@ant-design/icons';
import { useNavigate } from 'react-router-dom';
import { useGameStore } from '../../store/gameStore';
import './GameLobby.css';

const { Option } = Select;

const GameLobby = () => {
  const navigate = useNavigate();
  const { createGame, joinGame, isLoading, error, clearError } = useGameStore();
  const [gameList, setGameList] = useState([]);
  const [createModalVisible, setCreateModalVisible] = useState(false);
  const [joinModalVisible, setJoinModalVisible] = useState(false);
  const [form] = Form.useForm();

  // 模拟游戏列表（实际应从API获取）
  useEffect(() => {
    const mockGames = [
      {
        id: 'ABC123',
        name: '新手场 #1',
        players: 2,
        maxPlayers: 6,
        status: 'waiting',
        aiDifficulty: 'easy',
        createdAt: '2024-01-01 10:00'
      },
      {
        id: 'DEF456',
        name: '进阶场 #2',
        players: 3,
        maxPlayers: 6,
        status: 'playing',
        aiDifficulty: 'medium',
        createdAt: '2024-01-01 09:30'
      },
      {
        id: 'GHI789',
        name: '高手场 #3',
        players: 4,
        maxPlayers: 6,
        status: 'waiting',
        aiDifficulty: 'hard',
        createdAt: '2024-01-01 09:00'
      }
    ];
    setGameList(mockGames);
  }, []);

  // 创建游戏
  const handleCreateGame = async (values) => {
    try {
      const result = await createGame(
        values.playerName || 'Player',
        values.aiDifficulty || 'medium'
      );
      setCreateModalVisible(false);
      form.resetFields();
      message.success('游戏创建成功！');
      navigate('/');
    } catch (error) {
      message.error('创建游戏失败：' + error.message);
    }
  };

  // 加入游戏
  const handleJoinGame = async (values) => {
    try {
      await joinGame(values.gameId, values.playerName || 'Player');
      setJoinModalVisible(false);
      form.resetFields();
      message.success('加入游戏成功！');
      navigate('/');
    } catch (error) {
      message.error('加入游戏失败：' + error.message);
    }
  };

  // 刷新列表
  const refreshGames = () => {
    message.loading('刷新中...');
    setTimeout(() => {
      message.success('刷新成功');
    }, 500);
  };

  const columns = [
    {
      title: '房间ID',
      dataIndex: 'id',
      key: 'id',
      render: (id) => <Tag color="purple">{id}</Tag>
    },
    {
      title: '房间名称',
      dataIndex: 'name',
      key: 'name'
    },
    {
      title: 'AI难度',
      dataIndex: 'aiDifficulty',
      key: 'aiDifficulty',
      render: (difficulty) => {
        const map = {
          easy: { color: 'green', label: '简单' },
          medium: { color: 'orange', label: '中等' },
          hard: { color: 'red', label: '困难' }
        };
        return <Tag color={map[difficulty]?.color}>{map[difficulty]?.label}</Tag>;
      }
    },
    {
      title: '玩家',
      dataIndex: 'players',
      key: 'players',
      render: (players, record) => (
        <span>{players} / {record.maxPlayers}</span>
      )
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={status === 'waiting' ? 'success' : 'processing'}>
          {status === 'waiting' ? '等待中' : '游戏中'}
        </Tag>
      )
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      key: 'createdAt'
    },
    {
      title: '操作',
      key: 'action',
      render: (_, record) => (
        <Button 
          type="primary" 
          size="small"
          disabled={record.status === 'playing'}
          onClick={() => {
            form.setFieldsValue({ gameId: record.id });
            setJoinModalVisible(true);
          }}
        >
          加入
        </Button>
      )
    }
  ];

  return (
    <div className="game-lobby">
      <div className="lobby-header">
        <h2>🎮 游戏大厅</h2>
        <Space>
          <Button 
            icon={<ReloadOutlined />} 
            onClick={refreshGames}
          >
            刷新
          </Button>
          <Button 
            type="primary" 
            icon={<PlusOutlined />}
            onClick={() => setCreateModalVisible(true)}
          >
            创建房间
          </Button>
        </Space>
      </div>

      <Card className="lobby-stats">
        <Space size="large">
          <div className="stat-item">
            <span className="stat-number">{gameList.length}</span>
            <span className="stat-label">总房间</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">
              {gameList.filter(g => g.status === 'waiting').length}
            </span>
            <span className="stat-label">等待中</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">
              {gameList.reduce((sum, g) => sum + g.players, 0)}
            </span>
            <span className="stat-label">在线玩家</span>
          </div>
        </Space>
      </Card>

      <Table 
        columns={columns} 
        dataSource={gameList}
        rowKey="id"
        className="lobby-table"
        pagination={{ pageSize: 10 }}
      />

      {/* 创建游戏弹窗 */}
      <Modal
        title="🎯 创建新游戏"
        open={createModalVisible}
        onCancel={() => setCreateModalVisible(false)}
        footer={null}
        className="lobby-modal"
      >
        <Form
          form={form}
          onFinish={handleCreateGame}
          layout="vertical"
          initialValues={{
            playerName: 'Player',
            aiDifficulty: 'medium'
          }}
        >
          <Form.Item
            name="playerName"
            label="玩家名称"
            rules={[{ required: true, message: '请输入玩家名称' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="输入你的名字" />
          </Form.Item>
          <Form.Item
            name="aiDifficulty"
            label="AI难度"
            rules={[{ required: true }]}
          >
            <Select>
              <Option value="easy">😊 简单</Option>
              <Option value="medium">🤔 中等</Option>
              <Option value="hard">😈 困难</Option>
            </Select>
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={isLoading} block>
              创建游戏
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      {/* 加入游戏弹窗 */}
      <Modal
        title="🔑 加入游戏"
        open={joinModalVisible}
        onCancel={() => setJoinModalVisible(false)}
        footer={null}
        className="lobby-modal"
      >
        <Form
          form={form}
          onFinish={handleJoinGame}
          layout="vertical"
          initialValues={{
            playerName: 'Player'
          }}
        >
          <Form.Item
            name="gameId"
            label="房间ID"
            rules={[{ required: true, message: '请输入房间ID' }]}
          >
            <Input placeholder="输入房间ID" />
          </Form.Item>
          <Form.Item
            name="playerName"
            label="玩家名称"
            rules={[{ required: true, message: '请输入玩家名称' }]}
          >
            <Input prefix={<UserOutlined />} placeholder="输入你的名字" />
          </Form.Item>
          <Form.Item>
            <Button type="primary" htmlType="submit" loading={isLoading} block>
              加入游戏
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default GameLobby;
