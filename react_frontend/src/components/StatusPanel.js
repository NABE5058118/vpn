import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

const StatusContainer = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 20px;
  margin: 20px 0;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
`;

const StatusItem = styled.div`
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);

  &:last-child {
    border-bottom: none;
  }
`;

const StatusLabel = styled.span`
  font-weight: 600;
  color: #a0aec0;
`;

const StatusValue = styled.span`
  font-weight: 600;
  color: #fff;
`;

function StatusPanel() {
  const [status, setStatus] = useState({
    connected: false,
    server: 'N/A',
    ip: 'N/A',
    connectionTime: 'N/A'
  });

  // Имитация обновления статуса
  useEffect(() => {
    const interval = setInterval(() => {
      // В реальном приложении здесь будет запрос к API
      setStatus(prev => ({
        ...prev,
        connected: Math.random() > 0.5 // Имитация изменения статуса
      }));
    }, 10000); // Обновление каждые 10 секунд

    return () => clearInterval(interval);
  }, []);

  return (
    <StatusContainer>
      <h2>Статус подключения</h2>
      
      <StatusItem>
        <StatusLabel>Подключен:</StatusLabel>
        <StatusValue style={{ color: status.connected ? '#2ecc71' : '#e74c3c' }}>
          {status.connected ? '✅ Да' : '❌ Нет'}
        </StatusValue>
      </StatusItem>
      
      <StatusItem>
        <StatusLabel>Сервер:</StatusLabel>
        <StatusValue>{status.server}</StatusValue>
      </StatusItem>
      
      <StatusItem>
        <StatusLabel>IP-адрес:</StatusLabel>
        <StatusValue>{status.ip}</StatusValue>
      </StatusItem>
      
      <StatusItem>
        <StatusLabel>Время подключения:</StatusLabel>
        <StatusValue>{status.connectionTime}</StatusValue>
      </StatusItem>
    </StatusContainer>
  );
}

export default StatusPanel;