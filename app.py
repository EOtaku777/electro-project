from flask import Flask, render_template, request, jsonify
import sqlite3
import json

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('equipment.db')
    conn.row_factory = sqlite3.Row
    return conn

# Расчёт тока
def calc_current(power_kw, voltage=220, cos_fi=0.95):
    return round((power_kw * 1000) / (voltage * cos_fi), 1)

# Выбор автомата
def select_breaker(current_a):
    ratings = [6, 10, 16, 20, 25, 32, 40, 50, 63]
    for r in ratings:
        if r >= current_a:
            return r
    return 63

@app.route('/')
def index():
    return render_template('index.html')

# API: получить всё оборудование
@app.route('/api/equipment')
def get_equipment():
    db = get_db()
    equipment = db.execute('SELECT * FROM equipment ORDER BY vendor, rated_current').fetchall()
    db.close()
    return jsonify([dict(row) for row in equipment])

# API: рассчитать ток и автомат
@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    power = float(data.get('power', 0))
    current = calc_current(power)
    breaker = select_breaker(current)
    return jsonify({
        'power': power,
        'current': current,
        'breaker': breaker,
        'message': f'Для {power} кВт нужен автомат на {breaker} А'
    })

# API: рассчитать щит (суммарная нагрузка, выбор вводного)
@app.route('/api/shield/calculate', methods=['POST'])
def calculate_shield():
    devices = request.json.get('devices', [])
    total_power = sum(d.get('power', 0) for d in devices)
    total_current = sum(calc_current(d.get('power', 0)) for d in devices)
    
    # Коэффициент одновременности
    koef = 1.0 if len(devices) <= 3 else 0.8 if len(devices) <= 6 else 0.7
    
    total_with_koef = round(total_current * koef, 1)
    
    return jsonify({
        'total_power': round(total_power * koef, 1),
        'total_current': total_with_koef,
        'main_breaker': select_breaker(total_with_koef),
        'devices_count': len(devices),
        'koef': koef
    })

# API: сохранить проект
@app.route('/api/save_project', methods=['POST'])
def save_project():
    data = request.json
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            devices TEXT,
            total_price REAL,
            date TEXT
        )
    ''')
    db.execute(
        'INSERT INTO projects (name, devices, total_price, date) VALUES (?, ?, ?, datetime("now"))',
        (data['name'], json.dumps(data['devices']), data['total_price'])
    )
    db.commit()
    db.close()
    return jsonify({'status': 'saved'})

# API: получить все проекты
@app.route('/api/projects')
def get_projects():
    db = get_db()
    projects = db.execute('SELECT id, name, date, total_price FROM projects ORDER BY id DESC').fetchall()
    db.close()
    return jsonify([dict(row) for row in projects])

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)