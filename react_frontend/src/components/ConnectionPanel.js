import React, { useState } from 'react';
import styled from 'styled-components';
import axios from 'axios';

const Panel = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 20px;
  margin: 20px 0;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
`;

const Button = styled.button`
  padding: 12px 24px;
  margin: 10px 5px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: ${(props) => (props.disabled ? 'not-allowed' : 'pointer')};
  opacity: ${(props) => (props.disabled ? 0.6 : 1)};
  transition: all 0.3s ease;
  min-width: 150px;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  }
`;

const ConnectButton = styled(Button)`
  background: #2ecc71;
  color: white;

  &:hover:not(:disabled) {
    background: #27ae60;
  }
`;

const DisconnectButton = styled(Button)`
  background: #e74c3c;
  color: white;

  &:hover:not(:disabled) {
    background: #c0392b;
  }
`;

const RefreshButton = styled(Button)`
  background: #3498db;
  color: white;

  &:hover:not(:disabled) {
    background: #2980b9;
  }
`;

function ConnectionPanel() {
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleConnect = async () => {
    setIsLoading(true);
    try {
      // Здесь будет вызов API для подключения
      await new Promise(resolve => setTimeout(resolve, 2000)); // Имитация API-вызова
      setIsConnected(true);
      alert('Успешно подключено к VPN!');
    } catch (error) {
      console.error('Ошибка подключения:', error);
      alert('Ошибка при подключении к VPN');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisconnect = async () => {
    setIsLoading(true);
    try {
      // Здесь будет вызов API для отключения
      await new Promise(resolve => setTimeout(resolve, 1000)); // Имитация API-вызова
      setIsConnected(false);
      alert('Успешно отключено от VPN');
    } catch (error) {
      console.error('Ошибка отключения:', error);
      alert('Ошибка при отключении от VPN');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRefresh = async () => {
    try {
      // Здесь будет вызов API для обновления статуса
      alert('Статус обновлен');
    } catch (error) {
      console.error('Ошибка обновления статуса:', error);
      alert('Ошибка при обновлении статуса');
    }
  };

  return (
    <Panel>
      <h2>Управление подключением</h2>
      
      <div style={{ display: 'flex', justifyContent: 'center', flexWrap: 'wrap' }}>
        <ConnectButton 
          onClick={handleConnect} 
          disabled={isConnected || isLoading}
        >
          🔌 Подключиться
        </ConnectButton>
        
        <DisconnectButton 
          onClick={handleDisconnect} 
          disabled={!isConnected || isLoading}
        >
          🔌 Отключиться
        </DisconnectButton>
      </div>
      
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '10px' }}>
        <RefreshButton onClick={handleRefresh}>
          🔄 Обновить статус
        </RefreshButton>
      </div>
    </Panel>
  );
}

export default ConnectionPanel;