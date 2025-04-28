from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route('/cleanup_db', methods=['POST'])
def cleanup_db():
    try:
        conn = mysql.connector.connect(
            host='core-mariadb',
            user='homeassistant',
            password='Cap70952058',
            database='homeassistant',
            ssl_disabled=True
        )
        cursor = conn.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cursor.execute("DELETE FROM states WHERE entity_id IS NULL;")
        cursor.execute("OPTIMIZE TABLE states;")
        cursor.execute("OPTIMIZE TABLE state_attributes;")
        cursor.execute("OPTIMIZE TABLE statistics_short_term;")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"cleanup": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
