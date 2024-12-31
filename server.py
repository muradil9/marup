from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "users.db"

# Получение всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, role FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

# Добавление нового пользователя
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data['username']
    password_hash = data['password_hash']
    role = data['role']
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                       (username, password_hash, role))
        conn.commit()
        return jsonify({"message": "Пользователь добавлен успешно"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"message": "Пользователь уже существует"}), 400
    finally:
        conn.close()

# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
