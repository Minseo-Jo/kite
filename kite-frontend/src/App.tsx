import React from 'react';
import { ConfigProvider, theme } from 'antd';
import koKR from 'antd/locale/ko_KR';
import { MainPage } from './pages/MainPage';
import './App.css';

function App() {
  return (
    <ConfigProvider
      locale={koKR}
      theme={{
        token: {
          colorPrimary: '#ff9a9e',
          colorLink: '#ff6b9d',
          borderRadius: 8,
          fontSize: 14,
        },
        algorithm: theme.defaultAlgorithm,
      }}
    >
      <MainPage />
    </ConfigProvider>
  );
}

export default App;