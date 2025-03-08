







from flask import Flask, jsonify, request
from db_config import get_db_connection

app = Flask(__name__)

from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/docs'
API_URL = '/swagger.yaml'  # Make sure swagger.yaml is in the project folder

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Simple Flask CRUD API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# CREATE a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# READ all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, email FROM users")
        rows = cursor.fetchall()
        users = [{"id": row["id"], "name": row["name"], "email": row["email"]} for row in rows]
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# READ a single user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            user = {"id": row["id"], "name": row["name"], "email": row["email"]}
            return jsonify(user), 200
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# UPDATE a user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET name = ?, email = ? WHERE id = ?", (name, email, user_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "User not found"}), 404
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

# DELETE a user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "User not found"}), 404
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
