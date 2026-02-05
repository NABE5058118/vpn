from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class BotConfig:
    """Конфигурация бота"""
    token: str = os.getenv('TELEGRAM_BOT_TOKEN', '')
    admin_id: int = int(os.getenv('ADMIN_ID', 0))
    debug: bool = os.getenv('DEBUG', 'False').lower() == 'true'

@dataclass
class BackendConfig:
    """Конфигурация бэкенда"""
    url: str = os.getenv('BACKEND_URL', 'http://localhost:5000')
    api_version: str = os.getenv('API_VERSION', 'v1')

@dataclass
class WebAppConfig:
    """Конфигурация Web App"""
    url: str = os.getenv('MINI_APP_URL', 'http://localhost:5000/miniapp')

# Создание экземпляров конфигурации
bot_config = BotConfig()
backend_config = BackendConfig()
webapp_config = WebAppConfig()