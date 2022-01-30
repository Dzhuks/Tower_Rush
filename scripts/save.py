import sqlite3


# класс для сохранения прогресса игрока
class Save:
    def __init__(self, database):
        # связываемся с базой данных
        self.con = sqlite3.connect(database)
        self.table = "recordings"
        self.columns = ["level_number", "time", "tower_hp", "status"]

    # сохраняем прогресс
    def save(self, level, time, tower_hp, status):
        cur = self.con.cursor()
        que = f"""INSERT INTO {self.table} VALUES({level}, '{time}', {tower_hp}, '{status}')"""
        cur.execute(que)
        self.con.commit()

    # вернуть последнее сохранение
    def last_save(self):
        cur = self.con.cursor()
        que = f"""SELECT level_number, status FROM {self.table}"""
        result = cur.execute(que).fetchall()

        # если нету ничего, то вернуть None
        if not result:
            return None

        level, status = result[-1]
        # если игрок победил вернуть следующий уровень, иначе уровень где он проиграл
        if status == "win":
            if level == 3:
                return 1
            return level + 1
        else:
            return level

    # функция получения последнего сохранения
    def get(self):
        cur = self.con.cursor()
        que = f"""SELECT {', '.join(self.columns)} FROM {self.table}"""
        result = cur.execute(que).fetchall()[-1]
        return result
