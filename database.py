import sqlite3

def init_db():
    conn = sqlite3.connect('equipment.db')
    cursor = conn.cursor()
    
    # Таблица автоматов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS circuit_breakers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            rated_current REAL,
            poles INTEGER,
            curve TEXT,
            price REAL,
            vendor TEXT,
            modules INTEGER DEFAULT 1
        )
    ''')
    
    # Добавим стартовые данные
    starters = [
        ('ABB S201 6A', 6, 1, 'C', 450, 'ABB', 1),
        ('ABB S201 10A', 10, 1, 'C', 450, 'ABB', 1),
        ('ABB S201 16A', 16, 1, 'C', 450, 'ABB', 1),
        ('IEK 6A', 6, 1, 'C', 120, 'IEK', 1),
        ('IEK 10A', 10, 1, 'C', 120, 'IEK', 1),
        ('IEK 16A', 16, 1, 'C', 120, 'IEK', 1),
        ('IEK 25A', 25, 1, 'C', 150, 'IEK', 1),
        ('IEK 32A', 32, 1, 'C', 180, 'IEK', 1),
        ('УЗО IEK 25A 30mA', 25, 2, 'AC', 800, 'IEK', 2),
        ('УЗО IEK 40A 30mA', 40, 2, 'AC', 950, 'IEK', 2),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO circuit_breakers 
        (name, rated_current, poles, curve, price, vendor, modules)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', starters)
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("База создана!")