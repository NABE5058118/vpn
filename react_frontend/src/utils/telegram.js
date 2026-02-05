import { useEffect, useState } from 'react';
import Script from 'next/script';

// Заглушка для Telegram WebApp в случае, если скрипт не загрузился
const mockWebApp = {
  initDataUnsafe: {},
  sendData: () => {},
  ready: () => {},
  close: () => {},
  showPopup: (params, callback) => {
    alert(params.message);
    if (callback) callback();
  }
};

// Функция для получения WebApp объекта
export const getWebApp = () => {
  if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
    return window.Telegram.WebApp;
  }
  return mockWebApp;
};

// Компонент для загрузки Telegram WebApp скрипта
export const TelegramWebAppLoader = ({ children }) => {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
      setIsLoaded(true);
    }
  }, []);

  return (
    <>
      <Script
        src="https://telegram.org/js/telegram-web-app.js"
        onLoad={() => setIsLoaded(true)}
      />
      {isLoaded ? children : <div>Загрузка приложения...</div>}
    </>
  );
};

// Хук для работы с WebApp
export const useWebApp = () => {
  const [webApp, setWebApp] = useState(mockWebApp);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      // Ждем, пока скрипт загрузится
      const checkWebApp = () => {
        if (window.Telegram?.WebApp) {
          setWebApp(window.Telegram.WebApp);
        } else {
          setTimeout(checkWebApp, 100);
        }
      };
      checkWebApp();
    }
  }, []);

  return webApp;
};

// Хук для получения данных пользователя
export const useUser = () => {
  const webApp = useWebApp();
  return webApp.initDataUnsafe?.user || null;
};

// Хук для получения ID пользователя
export const useUserId = () => {
  const user = useUser();
  return user?.id || null;
};