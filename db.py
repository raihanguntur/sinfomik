import sqlite3

DB_PATH = "sinfomik.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS siswa (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nisn INTEGER NOT NULL,
                nama TEXT NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tahun_ajaran (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                th_ajar TEXT NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS semester_pil (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                sm_pil TEXT NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS semester (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                th_ajar_id INTEGER NOT NULL,
                sm_pil_id INTEGER NOT NULL,
                aktif BOOLEAN DEFAULT 0,
                nama TEXT NOT NULL,
                FOREIGN KEY (th_ajar_id) REFERENCES tahun_ajaran(id),
                FOREIGN KEY (sm_pil_id) REFERENCES semester_pil(id)
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY NOT NULL,
                username TEXT NOT NULL, 
                password TEXT NOT NULL, 
                role TEXT NOT NULL DEFAULT admin
            );
        ''')
        cursor.execute("SELECT COUNT(*) FROM user")
        if cursor.fetchone()[0] == 0:
            users = [
                (1, 'admin', 'admin', 'admin'),
                (2, 'siti', 'siti123', 'guru')
            ]
            cursor.executemany("INSERT INTO user (id, username, password, role) VALUES (?, ?, ?, ?)", users)
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kelas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_kelas TEXT NOT NULL,
                tingkat TEXT NOT NULL
            );
        ''')
        cursor.execute("SELECT COUNT(*) FROM kelas")
        if cursor.fetchone()[0] == 0:
            kelas_awal = [
                (1, 'A', '10'),
                (2, 'B', '10'),
                (3, 'C', '10')
            ]
            cursor.executemany("INSERT INTO kelas (id, nama_kelas, tingkat) VALUES (?, ?, ?)", kelas_awal)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mata_pelajaran (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_mapel TEXT NOT NULL,
                kode_mapel TEXT UNIQUE
            );
        ''')
        cursor.execute("SELECT COUNT(*) FROM mata_pelajaran")
        if cursor.fetchone()[0] == 0:
            mapel_awal = [
                (1, 'IPA', 'IPA1'),
                (2, 'IPA', 'IPA2')
            ]
            cursor.executemany("INSERT INTO mata_pelajaran (id, nama_mapel, kode_mapel) VALUES (?, ?, ?)", mapel_awal)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guru_mapel_kelas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mapel_id INTEGER NOT NULL,
                kelas_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES user(id),
                FOREIGN KEY (mapel_id) REFERENCES mata_pelajaran(id),
                FOREIGN KEY (kelas_id) REFERENCES kelas(id),
                UNIQUE(user_id, mapel_id, kelas_id)
            );
        ''')
        cursor.execute("SELECT COUNT(*) FROM guru_mapel_kelas")
        if cursor.fetchone()[0] == 0:
            relasi_awal = [
                (1, 2, 1, 1)
            ]
            cursor.executemany("INSERT INTO guru_mapel_kelas (id, user_id, mapel_id, kelas_id) VALUES (?, ?, ?, ?)", relasi_awal)
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nilai (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                siswa_id INTEGER NOT NULL,
                mapel_id INTEGER NOT NULL,
                jenis_nilai TEXT NOT NULL,  -- 'UTS', 'UAS', 'Harian', dll
                nilai REAL NOT NULL,
                tanggal DATE NOT NULL,
                guru_id INTEGER NOT NULL,
                FOREIGN KEY (siswa_id) REFERENCES siswa(id),
                FOREIGN KEY (mapel_id) REFERENCES mata_pelajaran(id),
                FOREIGN KEY (guru_id) REFERENCES user(id),
                CHECK (nilai >= 0 AND nilai <= 100)
            );
        ''')
        conn.commit()