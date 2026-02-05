import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///vpn_users.db')
    VPN_SERVER_HOST = os.environ.get('VPN_SERVER_HOST', 'vpn.example.com')
    VPN_SERVER_PORT = int(os.environ.get('VPN_SERVER_PORT', 51820))
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'