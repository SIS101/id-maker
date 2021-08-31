from DB import Database

class StudentsModel(Database):
    def __init__(self):
        Database.__init__(self)
        self.table = "students"
        self.fields = [
            ["uid", "varchar(255) PRIMARY KEY NOT NULL", ""],
            ["name", "varchar(30) NOT NULL", ""],
            ["programme", "varchar(30) NOT NULL", ""],
            ["intake_year", "INT NOT NULL", 0],
            ["stid", "INT", 0]
        ]

s = StudentsModel()
#print(s.down())
#print(s.up())
#print(s.insert({"name": "Shangala", "programme": "PHY"}))
#print(s.all())
print(s.find(uid='eb10521c-88d8-44ee-bb54-6375a8de7caf'))
#print(s.update('c771724d-33e1-4eaf-80b6-7e23ecf5c21a',{"name": "Shangala", "programme": "PHY"}))