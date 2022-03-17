from datetime import datetime
from sql_comm import SqlComm


class DB:
    def __init__(self):
        self.local_store = "crain.txt"
        self.sql = SqlComm()

    def write(self, weight):
        sqlstr = f"INSERT INTO [HOCK].[dbo].KAY007(HMOTNOST) VALUES ({weight})"
        if self.sql.insert_into(sqlstr):
            try:
                with open(self.local_store, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            except Exception as e:
                print(e)
                with open(self.local_store, "w", encoding="utf-8") as f:
                    f.write("")
                return

            new_lines = []
            for line in lines:
                record = line.strip().split(";")
                if len(record) == 2:
                    time, weight = record
                    sqlstr = "INSERT INTO [HOCK].[dbo].KAY007(DATUM, HMOTNOST) " \
                             f"VALUES ('{time}', {weight})"
                    if not self.sql.insert_into(sqlstr):
                        new_lines.append(line)

            with open(self.local_store, "w", encoding="utf-8") as f:
                f.write("".join(new_lines))

        else:
            with open(self.local_store, "a", encoding="utf-8") as f:
                curr_time = datetime.now().replace(microsecond=0).strftime("%d.%m.%Y %H:%M:%S")
                f.write(f"{curr_time};{weight}\n")
