import sqlite3

conn = sqlite3.connect("cambio.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cotacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        moeda TEXT,
        valor REAL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def salvar(moeda, valor):
    cursor.execute("INSERT INTO cotacoes (moeda, valor) VALUES (?, ?)", (moeda, valor))
    conn.commit()
