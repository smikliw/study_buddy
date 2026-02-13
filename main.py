from flask import Flask, request, jsonify
import hashlib
import hmac
import os
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env

app = Flask(__name__)
BOT_TOKEN = os.getenv('8227957624:AAGwKFJGZdcC3nMwUoeysPLhHrsboPfEDgM')  # Токен бота из @BotFather


def validate_init_data(init_data: str) -> bool:
    """Проверяет подпись данных от Telegram — защита от подделки"""
    parts = sorted([part for part in init_data.split('&') if not part.startswith('hash=')])
    data_check_string = '\n'.join(parts)

    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    hash_hex = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    received_hash = dict(part.split('=') for part in init_data.split('&') if part.startswith('hash='))['hash']
    return hmac.compare_digest(hash_hex, received_hash)


@app.route('/api/save', methods=['POST'])
def save_score():
    data = request.json
    init_data = data.get('initData')  # Данные авторизации от Telegram

    if not validate_init_data(init_data):
        return jsonify({'error': 'Неверная подпись'}), 403

    # Здесь можно сохранить в файл/БД
    user_id = data['userId']
    score = data['score']

    print(f'Пользователь {user_id} набрал {score} очков')

    return jsonify({'success': True, 'message': 'Результат сохранён!'})


@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    # Пример: возвращаем топ-3 игрока
    return jsonify({
        'leaderboard': [
            {'name': 'Анна', 'score': 150},
            {'name': 'Борис', 'score': 120},
            {'name': 'Вика', 'score': 95}
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)