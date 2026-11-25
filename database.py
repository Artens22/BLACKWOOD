import sqlite3


def init_db():
    connection = sqlite3.connect("blackwood.db")
    cursor = connection.cursor()

    # Создаём таблицу записей
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            service TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Проверяем, есть ли колонка status
    columns = [
        row[1] for row in cursor.execute("PRAGMA table_info(appointments)").fetchall()
    ]

    # Если колонки нет — добавляем её
    if "status" not in columns:
        cursor.execute("""
            ALTER TABLE appointments
            ADD COLUMN status TEXT NOT NULL DEFAULT 'new'
        """)

    connection.commit()
    connection.close()
