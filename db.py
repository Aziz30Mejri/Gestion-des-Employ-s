import sqlite3

class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

        sql ="""
        CREATE TABLE IF NOT EXISTS employees(
        id Integer Primary Key,
        nom text,
        age text,
        emploi text,
        email text,
        genre text,
        mobile text,
        adresse text
        )
        """
        self.cur.execute(sql)
        self.con.commit()

    def insert(self, nom, age, emploi, email, genre, mobile, adresse):
        self.cur.execute("insert into employees values (NULL,?,?,?,?,?,?,?)",
                         (nom, age, emploi, email, genre, mobile, adresse))
        self.con.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM employees")
        rows = self.cur.fetchall()
        return rows

    def remove(self, id):
        self.cur.execute("DELETE FROM employees WHERE id =?", (id,))
        self.con.commit()

    def update(self, id, nom, age, emploi, email, genre, mobile, adresse):
        self.cur.execute("UPDATE employees SET nom=?, age=?, emploi=?, email=?, genre=?, mobile=?, adresse=? WHERE id=?",
                         (nom, age, emploi, email, genre, mobile, adresse, id))
        self.con.commit()