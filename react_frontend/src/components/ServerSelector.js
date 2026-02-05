import React, { useState } from 'react';
import styled from 'styled-components';

const SelectorContainer = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 20px;
  margin: 20px 0;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
`;

const Select = styled.select`
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: none;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 16px;
  margin-top: 10px;
  backdrop-filter: blur(10px);

  option {
    background: #2c3e50;
    color: white;
  }
`;

function ServerSelector() {
  const [selectedServer, setSelectedServer] = useState('US-East');

  const servers = [
    { id: 'US-East', name: 'US-East (Нью-Йорк)', ping: 25 },
    { id: 'US-West', name: 'US-West (Лос-Анджелес)', ping: 45 },
    { id: 'Europe', name: 'Europe (Франкфурт)', ping: 80 },
    { id: 'Asia', name: 'Asia (Токио)', ping: 120 },
    { id: 'Australia', name: 'Australia (Сидней)', ping: 180 }
  ];

  const handleChange = (event) => {
    setSelectedServer(event.target.value);
  };

  return (
    <SelectorContainer>
      <h2>Выбор сервера</h2>
      <Select value={selectedServer} onChange={handleChange}>
        {servers.map(server => (
          <option key={server.id} value={server.id}>
            {server.name} (пинг: {server.ping}мс)
          </option>
        ))}
      </Select>
    </SelectorContainer>
  );
}

export default ServerSelector;