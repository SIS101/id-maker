import sqlite3
import uuid

class Database:
    def __init__(self):
        self.conn = None
        self.table = str()
        self.fields = list()
        self.response = {"success": False, "message":"Failed: ", "data": None}

        self.create_connection()

    def create_connection(self, db_name: str = "id-maker.db")->dict:
        response = self.response.copy()
        try:
            self.conn = sqlite3.connect(db_name)
        except Exception as e:
            response["message"] = response["message"]+str(e)
        else:
            response["success"] = True
            response["message"] = "Successful!"
            response["data"] = self.conn
        
        return response
    
    def run_query(self, sql: str)->dict:
        response = self.response.copy()
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
        except Exception as e:
            response["message"] = response["message"]+str(e)
        else:
            response["success"] = True
            response["message"] = "Successful!"
        
        return response

    def run_query_out(self, sql: str)->dict:
        response = self.response.copy()
        try:
            c = self.conn.cursor()
            c.execute(sql)
        except Exception as e:
            response["message"] = response["message"]+str(e)
        else:
            response["success"] = True
            response["message"] = "Successful!"
            response["data"] = c.fetchall()
        
        return response

    def run_query_in(self, sql: str)->dict:
        response = self.response.copy()
        try:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
        except Exception as e:
            response["message"] = response["message"]+str(e)
        else:
            response["success"] = True
            response["message"] = "Successful!"
            response["data"] = c.lastrowid
        
        return response

    def up(self)->dict:
        fillable = str()
        for field in self.fields:
            if len(fillable) > 0:
                fillable += ","+field[0]+" "+field[1]
            else:
                fillable += field[0]+" "+field[1]
        sql = f"""CREATE TABLE IF NOT EXISTS {self.table} 
                    ({fillable});"""

        return self.run_query(sql)

    def down(self)->dict:
        sql = f"DROP TABLE IF EXISTS {self.table};"
        return self.run_query(sql)
    
    def find(self, union: bool = False, **kwargs)->dict:
        response = self.response.copy()
        condition = str()

        if union:
            joiner = "OR"
        else:
            joiner = "AND"

        if kwargs:
            for key, value in kwargs.items():
                if len(condition) > 0:
                    condition += " "+joiner+" "+key+"='"+value+"'"
                else:
                    condition += key+"='"+value+"'"
            
            sql = f"SELECT * FROM {self.table} WHERE {condition};"
            response = self.run_query_out(sql)
        else:
            response["message"] = response["message"]+"No find condition was given"
        
        return response
    
    def insert(self, data: dict)->dict:
        values = str()
        for value in self.fields:
            if len(values) > 0:
                values += ",'"+str(data.get(value[0], value[2]))+"'"
            else:
                values += "'"+str(data.get(value[0], str(uuid.uuid4())))+"'"
                
        fieldlist = str()
        for field in self.fields:
            if len(fieldlist) > 0:
                fieldlist += ','+field[0]
            else:
                fieldlist += field[0]

        sql = f"""INSERT INTO {self.table} ({fieldlist}) 
                    VALUES ({values});"""

        return self.run_query_in(sql)
    
    def update(self, uid: str, data: dict)->dict:
        fieldlist = str()
        for field in self.fields[1:]:
            if len(fieldlist) > 0:
                fieldlist += ','+field[0]+"='"+str(data.get(field[0], field[2]))+"'"
            else:
                fieldlist += field[0]+"='"+str(data.get(field[0], field[2]))+"'"

        sql = f"""UPDATE {self.table} SET {fieldlist}
                    WHERE uid='{uid}';"""

        return self.run_query_in(sql)
    
    def delete(self, uid: str)->dict:
        sql = f"DELETE FROM {self.table} WHERE uid='{uid}';"
        return self.run_query(sql)
    
    def all(self)->dict:
        sql = f"SELECT * FROM {self.table};"
        return self.run_query_out(sql)
