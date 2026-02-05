from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime
import json
import os

# Создание Flask-приложения
app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех маршрутов

# Конфигурация
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# Глобальная переменная для хранения состояния подключения пользователей
user_connections = {}

# HTML-шаблон для Mini App
MINI_APP_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VPN Клиент - Telegram Mini App</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #1a2a6c, #2a4d69, #4b86b4);
            color: white;
            min-height: 100vh;
            box-sizing: border-box;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        h1 {
            text-align: center;
            margin-bottom: 10px;
        }

        .subtitle {
            text-align: center;
            color: #ccc;
            margin-bottom: 30px;
        }

        .status-container {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
        }

        .status-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .status-item:last-child {
            border-bottom: none;
        }

        .status-label {
            font-weight: 600;
            color: #a0aec0;
        }

        .status-value {
            font-weight: 600;
        }

        .button-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin: 20px 0;
        }

        .btn {
            padding: 15px 20px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }

        .btn-connect {
            background: #2ecc71;
            color: white;
        }

        .btn-disconnect {
            background: #e74c3c;
            color: white;
        }

        .btn-refresh {
            background: #3498db;
            color: white;
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .server-selector {
            margin: 20px 0;
        }

        select {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: none;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            font-size: 16px;
            margin-top: 10px;
        }

        option {
            background: #2c3e50;
            color: white;
        }

        .loading {
            text-align: center;
            padding: 20px;
        }

        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 VPN Клиент</h1>
        <p class="subtitle">Безопасное подключение к интернету</p>

        <div class="server-selector">
            <label for="server-select">Выберите сервер:</label>
            <select id="server-select">
                <option value="US-East">US-East (Нью-Йорк) - 25мс</option>
                <option value="US-West">US-West (Лос-Анджелес) - 45мс</option>
                <option value="Europe">Europe (Франкфурт) - 80мс</option>
                <option value="Asia">Asia (Токио) - 120мс</option>
                <option value="Australia">Australia (Сидней) - 180мс</option>
            </select>
        </div>

        <div class="button-group">
            <button id="connect-btn" class="btn btn-connect">🔌 Подключиться</button>
            <button id="disconnect-btn" class="btn btn-disconnect" disabled>🔌 Отключиться</button>
            <button id="refresh-btn" class="btn btn-refresh">🔄 Обновить статус</button>
        </div>

        <div id="status-container" class="status-container">
            <h3>Статус подключения</h3>
            <div id="status-content">
                <div class="status-item">
                    <span class="status-label">Подключен:</span>
                    <span id="connected-status" class="status-value">❌ Нет</span>
                </div>
                <div class="status-item">
                    <span class="status-label">Сервер:</span>
                    <span id="server-status" class="status-value">N/A</span>
                </div>
                <div class="status-item">
                    <span class="status-label">IP-адрес:</span>
                    <span id="ip-status" class="status-value">N/A</span>
                </div>
                <div class="status-item">
                    <span class="status-label">Время подключения:</span>
                    <span id="time-status" class="status-value">N/A</span>
                </div>
            </div>
        </div>

        <div id="loading" class="loading hidden">
            <p>Обработка запроса...</p>
        </div>
    </div>

    <script>
        // Инициализация Telegram Web App
        const tg = window.Telegram.WebApp;

        // Установка цвета темы
        document.body.style.backgroundColor = tg.backgroundColor;

        // Инициализация приложения
        tg.ready();

        // Получение данных пользователя
        const user = tg.initDataUnsafe?.user;
        const userId = user?.id;

        if (!userId) {
            // Если не удается получить userId из Telegram, показываем сообщение
            tg.showAlert('Внимание: Приложение запущено не из Telegram. Некоторые функции могут быть ограничены.');
            console.log('Данные пользователя:', tg.initDataUnsafe);
            // В реальном приложении можно использовать fallback-механизм или запросить данные по-другому
        }

        // Базовый URL бэкенда
        const BACKEND_URL = window.location.origin; // Используем текущий домен

        // DOM элементы
        const connectBtn = document.getElementById('connect-btn');
        const disconnectBtn = document.getElementById('disconnect-btn');
        const refreshBtn = document.getElementById('refresh-btn');
        const serverSelect = document.getElementById('server-select');
        const connectedStatus = document.getElementById('connected-status');
        const serverStatus = document.getElementById('server-status');
        const ipStatus = document.getElementById('ip-status');
        const timeStatus = document.getElementById('time-status');
        const loadingElement = document.getElementById('loading');

        // Функция для показа/скрытия загрузки
        function setLoading(isLoading) {
            if (isLoading) {
                loadingElement.classList.remove('hidden');
                connectBtn.disabled = true;
                disconnectBtn.disabled = true;
                refreshBtn.disabled = true;
            } else {
                loadingElement.classList.add('hidden');
                connectBtn.disabled = false;
                disconnectBtn.disabled = false;
                refreshBtn.disabled = false;
            }
        }

        // Функция для обновления статуса
        async function updateStatus() {
            if (!userId) return;

            setLoading(true);

            try {
                const response = await fetch(`${BACKEND_URL}/api/users/${userId}/status`);
                const data = await response.json();

                if (data.connected) {
                    connectedStatus.textContent = '✅ Да';
                    connectedStatus.style.color = '#2ecc71';
                    serverStatus.textContent = data.server;
                    ipStatus.textContent = data.ip_address;
                    timeStatus.textContent = data.connection_time ? new Date(data.connection_time).toLocaleString() : 'N/A';

                    connectBtn.disabled = true;
                    disconnectBtn.disabled = false;
                } else {
                    connectedStatus.textContent = '❌ Нет';
                    connectedStatus.style.color = '#e74c3c';
                    serverStatus.textContent = 'N/A';
                    ipStatus.textContent = 'N/A';
                    timeStatus.textContent = 'N/A';

                    connectBtn.disabled = false;
                    disconnectBtn.disabled = true;
                }
            } catch (error) {
                console.error('Ошибка при обновлении статуса:', error);
                tg.showAlert('Ошибка при обновлении статуса');
            } finally {
                setLoading(false);
            }
        }

        // Функция для подключения
        async function connect() {
            if (!userId) return;

            const server = serverSelect.value;

            setLoading(true);

            try {
                const response = await fetch(`${BACKEND_URL}/api/users/${userId}/connect`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ server })
                });

                const data = await response.json();

                if (data.success) {
                    tg.showAlert(`Успешно подключено к ${data.server}!`);
                    await updateStatus();
                } else {
                    tg.showAlert('Ошибка при подключении к VPN');
                }
            } catch (error) {
                console.error('Ошибка при подключении:', error);
                tg.showAlert('Ошибка при подключении к VPN');
            } finally {
                setLoading(false);
            }
        }

        // Функция для отключения
        async function disconnect() {
            if (!userId) return;

            setLoading(true);

            try {
                const response = await fetch(`${BACKEND_URL}/api/users/${userId}/disconnect`, {
                    method: 'POST'
                });

                const data = await response.json();

                if (data.success) {
                    tg.showAlert('Успешно отключено от VPN!');
                    await updateStatus();
                } else {
                    tg.showAlert('Ошибка при отключении от VPN');
                }
            } catch (error) {
                console.error('Ошибка при отключении:', error);
                tg.showAlert('Ошибка при отключении от VPN');
            } finally {
                setLoading(false);
            }
        }

        // Обработчики событий
        connectBtn.addEventListener('click', connect);
        disconnectBtn.addEventListener('click', disconnect);
        refreshBtn.addEventListener('click', updateStatus);

        // Инициализация при загрузке
        document.addEventListener('DOMContentLoaded', updateStatus);

        // Обновление статуса каждые 10 секунд
        setInterval(updateStatus, 10000);
    </script>
</body>
</html>
'''

# Маршрут для главной страницы
@app.route('/')
def index():
    return '<h1>VPN Сервер работает</h1><p>Для открытия Mini App перейдите по адресу /miniapp</p>'

# Маршрут для Mini App
@app.route('/miniapp')
def mini_app():
    return render_template_string(MINI_APP_TEMPLATE)

# Маршрут для проверки статуса сервера
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# Маршрут для получения статуса подключения пользователя
@app.route('/api/users/<int:user_id>/status', methods=['GET'])
def get_user_status(user_id):
    connection_info = user_connections.get(user_id, {})

    status_data = {
        'connected': connection_info.get('connected', False),
        'server': connection_info.get('server', 'N/A'),
        'connection_time': connection_info.get('connection_time', None),
        'ip_address': connection_info.get('ip_address', 'N/A'),
        'user_id': user_id
    }

    return jsonify(status_data)

# Маршрут для подключения пользователя к VPN
@app.route('/api/users/<int:user_id>/connect', methods=['POST'])
def connect_user(user_id):
    data = request.get_json()
    server = data.get('server', 'US-East')

    # В реальном приложении здесь будет вызов VPN-сервера
    # Для демонстрации используем фиктивные данные
    import random
    assigned_ip = f"10.8.0.{random.randint(2, 254)}"

    # Сохраняем информацию о подключении
    user_connections[user_id] = {
        'connected': True,
        'server': server,
        'connection_time': datetime.now().isoformat(),
        'ip_address': assigned_ip
    }

    return jsonify({
        'success': True,
        'server': server,
        'ip_address': assigned_ip,
        'connection_time': datetime.now().isoformat(),
        'message': 'Успешно подключено к VPN'
    })

# Маршрут для отключения пользователя от VPN
@app.route('/api/users/<int:user_id>/disconnect', methods=['POST'])
def disconnect_user(user_id):
    # Удаляем информацию о подключении
    if user_id in user_connections:
        del user_connections[user_id]

    return jsonify({
        'success': True,
        'message': 'Успешно отключено от VPN'
    })

# Маршрут для получения списка серверов
@app.route('/api/servers', methods=['GET'])
def get_servers():
    servers = [
        {'id': 1, 'name': 'US-East', 'location': 'New York, USA', 'ping': 25, 'status': 'online'},
        {'id': 2, 'name': 'US-West', 'location': 'Los Angeles, USA', 'ping': 45, 'status': 'online'},
        {'id': 3, 'name': 'Europe', 'location': 'Frankfurt, Germany', 'ping': 80, 'status': 'online'},
        {'id': 4, 'name': 'Asia', 'location': 'Tokyo, Japan', 'ping': 120, 'status': 'online'},
        {'id': 5, 'name': 'Australia', 'location': 'Sydney, Australia', 'ping': 180, 'status': 'online'}
    ]

    return jsonify({'servers': servers})

# Запуск сервера
if __name__ == '__main__':
    print("Запуск VPN-сервера...")
    app.run(host='0.0.0.0', port=5000, debug=True)