import sqlite3

DBNAME = "db.sql"

class dbUsers:
    def __init__(self) -> None:
        self.bdName = DBNAME

        conn = sqlite3.connect(self.bdName)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegramId NUMERIC
            )
        """)
        conn.commit()
        conn.close()
    
    def addUser(self, telegramId) -> None:
        conn = sqlite3.connect(self.bdName)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO user(telegramId) VALUES (?);", (telegramId,))

        conn.commit()
        conn.close()

    def checkUser(self, telegramId) -> bool:
        conn = sqlite3.connect(self.bdName)
        cursor = conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM user WHERE telegramId = ?;', (telegramId,))
        numUsers = int(cursor.fetchone()[0])

        conn.close()

        return numUsers > 0

class dbTasks:
    def __init__(self) -> None:
        self.bdName = DBNAME

        conn = sqlite3.connect(self.bdName)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS task(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                complete BOOLEAN DEFAULT FALSE,
                id_user INTEGER,
                FOREIGN KEY (id_user) REFERENCES user (id)
            )
        """)
        conn.commit()
        conn.close()
    
    def addTask(self, telegramId, task) -> None:
        conn = sqlite3.connect(self.bdName)
        cursor = conn.cursor()

        cursor.execute("INSERT INTO task(text, id_user) VALUES (?, (SELECT id FROM user WHERE telegramId = ?))", (task, telegramId))
        
        conn.commit()
        conn.close()

    def getTasks(self, telegramId) -> list:
        conn = sqlite3.connect(self.bdName)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM task WHERE id_user = (SELECT id FROM user WHERE telegramId = ?) AND complete = false;', (telegramId,))
        tasks = cursor.fetchall()

        conn.close()

        return tasks
    
    def getAllTasks(self, telegramId) -> list:
        conn = sqlite3.connect(self.bdName)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM task WHERE id_user = (SELECT id FROM user WHERE telegramId = ?)', (telegramId,))
        tasks = cursor.fetchall()

        conn.close()

        return tasks
    
    def editTask(self, idTask, newTask):
        conn = sqlite3.connect(self.bdName)
        cursor = conn.cursor()

        cursor.execute("UPDATE task SET text = ? WHERE id = ?", (newTask, idTask))
        
        conn.commit()
        conn.close()

    def completeTask(self, idTask) -> None:
        conn = sqlite3.connect(self.bdName)
        cursor = conn.cursor()

        cursor.execute("UPDATE task SET complete = TRUE WHERE id = ?", (idTask,))
        
        conn.commit()
        conn.close()
