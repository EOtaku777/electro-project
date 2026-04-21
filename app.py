from flask import Flask, render_template, request, jsonify, session
import sqlite3
import json
from calculations import calc_current, select_circuit_breaker, calculate_group_load

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

def get_db():
    conn = sqlite3.connect('equipment.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    power = float(data.get('power_kw', 0))
    current = calc_current(power)
    breaker = select_circuit_breaker(current)
    
    return jsonify({
        'current_a': current,
        'recommended_breaker': breaker,
        'message': f'Для нагрузки {power} кВт нужен автомат на {breaker}А'
    })

@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM circuit_breakers WHERE rated_current <= 63')
    equipment = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(equipment)

if __name__ == '__main__':
    app.run(debug=True, port=5000)