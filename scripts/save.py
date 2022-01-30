import sqlite3


class Save:
    def __init__(self, database):
        self.con = sqlite3.connect(database)
        self.table = "recordings"
        self.columns = ["level_number", "time", "killed_enemies", "tower_hp", "status"]

    def save(self, level, time, killed_enemies, tower_hp, status):
        cur = self.con.cursor()
        que = f"""INSERT INTO {self.table} VALUES({level}, '{time}', {killed_enemies}, {tower_hp}, '{status}')"""
        cur.execute(que)
        self.con.commit()

    def last_save(self):
        cur = self.con.cursor()
        que = f"""SELECT level_number, status FROM {self.table}"""
        result = cur.execute(que).fetchall()
        if not result:
            return None
        level, status = result[-1]
        if status == "win":
            if level == 3:
                return 1
            return level + 1
        else:
            return level

    def get(self):
        cur = self.con.cursor()
        print(', '.join(self.columns))
        que = f"""SELECT {', '.join(self.columns)} FROM {self.table}"""
        result = cur.execute(que).fetchall()[-1]
        return result
