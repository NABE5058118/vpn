import React from 'react';
import styled from 'styled-components';
import MainContainer from './components/MainContainer';
import ConnectionPanel from './components/ConnectionPanel';
import ServerSelector from './components/ServerSelector';
import StatusPanel from './components/StatusPanel';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #1a2a6c, #2a4d69, #4b86b4);
  color: white;
  font-family: 'Arial', sans-serif;
`;

function App() {
  return (
    <AppContainer>
      <MainContainer>
        <h1>🚀 VPN Клиент</h1>
        <p>Безопасное подключение к интернету</p>
        
        <ServerSelector />
        <ConnectionPanel />
        <StatusPanel />
      </MainContainer>
    </AppContainer>
  );
}

export default App;