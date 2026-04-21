import sqlite3

def init_db():
    conn = sqlite3.connect('equipment.db')
    c = conn.cursor()
    
    # Таблица оборудования
    c.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            type TEXT,
            rated_current REAL,
            poles INTEGER,
            price REAL,
            vendor TEXT,
            modules INTEGER
        )
    ''')
    
    # Добавляем оборудование
    equipment = [
        ('ABB S201 6A C', 'MCB', 6, 1, 450, 'ABB', 1),
        ('ABB S201 10A C', 'MCB', 10, 1, 450, 'ABB', 1),
        ('ABB S201 16A C', 'MCB', 16, 1, 450, 'ABB', 1),
        ('ABB S201 20A C', 'MCB', 20, 1, 450, 'ABB', 1),
        ('ABB S201 25A C', 'MCB', 25, 1, 480, 'ABB', 1),
        ('ABB S201 32A C', 'MCB', 32, 1, 500, 'ABB', 1),
        ('IEK 6A C', 'MCB', 6, 1, 120, 'IEK', 1),
        ('IEK 10A C', 'MCB', 10, 1, 120, 'IEK', 1),
        ('IEK 16A C', 'MCB', 16, 1, 120, 'IEK', 1),
        ('IEK 25A C', 'MCB', 25, 1, 150, 'IEK', 1),
        ('IEK 32A C', 'MCB', 32, 1, 180, 'IEK', 1),
        ('УЗО IEK 25A 30mA', 'RCD', 25, 2, 800, 'IEK', 2),
        ('УЗО IEK 40A 30mA', 'RCD', 40, 2, 950, 'IEK', 2),
        ('УЗО ABB FH202 25A', 'RCD', 25, 2, 2500, 'ABB', 2),
        ('Диф ABB DS201 16A', 'RCBO', 16, 2, 3200, 'ABB', 2),
        ('Диф IEK 16A', 'RCBO', 16, 2, 1500, 'IEK', 2),
    ]
    
    c.executemany('INSERT OR IGNORE INTO equipment (name, type, rated_current, poles, price, vendor, modules) VALUES (?,?,?,?,?,?,?)', equipment)
    
    conn.commit()
    conn.close()
    print("✅ База оборудования создана!")

if __name__ == '__main__':
    init_db()