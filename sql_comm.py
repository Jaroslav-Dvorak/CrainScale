import json
import pyodbc


def is_rpi():
    try:
        with open('/sys/firmware/devicetree/base/model') as model:
            rpi_model = model.read()
    except FileNotFoundError:
        return False
    else:
        return rpi_model


class SqlComm:
    def __init__(self):

        credincials = self.autentification("credincials.json")
        self.settings = {"port": "1433"}
        self.settings.update(credincials)
        if is_rpi():
            self.settings["driver"] = 'FreeTDS'
        else:
            self.settings["driver"] = 'SQL Server'

    def autentification(self, filename):
        credincials = {}
        try:
            with open(filename, "r", encoding='utf8') as f:
                credincials = json.load(f)
        except Exception as e:
            server = input("Server? ")
            user = input("User? ")
            password = input("Password? ")
            credincials = {"server": server,
                           "user": user,
                           "password": password}
            with open(filename, "w", encoding="utf8") as f:
                json.dump(credincials, f, ensure_ascii=False, indent=4)
        finally:
            return credincials

    def get_data_from_db(self, sqlstr):
        try:
            conn = pyodbc.connect(
                f"Driver={self.settings['driver']};"
                f"Server={self.settings['server']};"
                # f"Database={self.settings['database']};"
                f"UID={self.settings['user']};"
                f"PWD={self.settings['password']};"
                f"PORT={self.settings['port']}"
            )
            cursor = conn.cursor()
            cursor.execute(sqlstr)
            newdata = cursor.fetchall()
        except Exception as e:
            print("Error SQL:")
            print(e)
            return None
        else:
            cursor.close()
        return newdata

    def insert_into(self, sqlstr):
        try:
            conn = pyodbc.connect(
                f"Driver={self.settings['driver']};"
                f"Server={self.settings['server']};"
                # f"Database={self.settings['database']};"
                f"UID={self.settings['user']};"
                f"PWD={self.settings['password']};"
                f"PORT={self.settings['port']}"
            )
            cursor = conn.cursor()
            cursor.execute(sqlstr)
            cursor.commit()
        except Exception as e:
            print("Error SQL:")
            print(e)
            return None
        else:
            cursor.close()
        return True


# sql = SqlComm()
# query = "INSERT INTO [HOCK].[dbo].KAY007(HMOTNOST) VALUES (0)"
# t = "01.03.2022 19:09:07"
# query = f"INSERT INTO [HOCK].[dbo].KAY007(DATUM, HMOTNOST) VALUES ('{t}', 0)"
# res = sql.insert_into(query)
# print(res)

# sql = SqlComm(server=r"192.168.60.13\inst1",
#               user="VyrobaStandalone",
#               password="Kmt0203")
# query = "SELECT FirstName, LastName FROM [HOCK].[dbo].SAI_PersonMedium_0048 WHERE ShortCode='9FBB47'"
# res = sql.get_data_from_db(query)
# print(res)
