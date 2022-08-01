import sqlite3


class Database:
    def __init__(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS exercises(id INTEGER PRIMARY KEY, name TEXT, bpm INTEGER, url TEXT)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS topics(id INTEGER PRIMARY KEY, name TEXT, duration INTEGER)")
        self.conn.commit()


    def add_topic(self, name, duration):
        self.cur.execute("INSERT INTO topics VLUES(NULL, ?, ?)",(name, duration))
        self.conn.commit()

    def add_exercise(self, name,bpm,url):
        self.cur.execute("INSERT INTO exercises VALUES(NULL, ?, ?, ?)",(name, bpm, url))
        self.conn.commit()

    def update_exercise(self, _id, name, bpm):
        self.cur.execute("UPDATE exercises SET name=?, bpm=? WHERE id= ?",(name, bpm, _id))
        self.conn.commit()

    def delete_exercise(self, id):
        self.cur.execute("DELETE FROM exercises WHERE id= ?",(id,))
        self.conn.commit()

    def get_exercises(self):
        self.cur.execute("SELECT * FROM exercises")
        rows = self.cur.fetchall()
        return rows

    def __del__(self):
        self.conn.close()


