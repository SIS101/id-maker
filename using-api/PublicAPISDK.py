import requests
import json

class StidSDK:
    def __init__(self, auth: str = None):
        self.auth = auth
        self.jsonDecoder = json.decoder.JSONDecoder()
        self.base_url = "https://kihsr.ac.zm/public-api/public/api"
        self.stid_fields = [
            "name",
            "nrc",
            "program",
            "stid",
            "valid_from",
            "valid_to"
        ]
        self.messages = list()
    
    def get_stids(self):
        return self.send_request()
    
    def get_stid(self, id):
        self.messages.clear()
        fields = {"id": id}
        return self.send_request(end_point="/stids/get", payload=fields)
    
    def update_stid(self, data: dict):
        fields = dict()
        self.messages.clear()
        for key, value in data.items():
            if key in self.stid_fields:
                fields[key]=value
            else:
                self.messages.append(f"No column named {key} in the database, this field will be ignored.")
                
        return self.send_request(method="POST", end_point="/stids/update", payload=fields)
    
    def add_stid(self, data: dict):
        fields = dict()
        self.messages.clear()
        for key, value in data.items():
            if key in self.stid_fields:
                fields[key]=value
            else:
                self.messages.append(f"No column named {key} in the database, this field will be ignored.")
                
        return self.send_request(method="POST", end_point="/stids/submit", payload=fields)
    
    def delete_stid(self, id):
        self.messages.clear()
        fields = {"id": id}
        return self.send_request(method="POST", end_point="/stids/delete", payload=fields)
    
    def authenticate(self, email, password):
        form = {
            "email": email,
            "password": password
        }
        res = self.send_request(method="POST", end_point="/login", payload=form)
        if res != None:
            if res["success"]:
                self.auth = res["data"]
            else:
                self.messages.append(res["message"])
        
        return res
    
    def send_request(self, method="GET", end_point="/stids", payload=dict()):
        try:
            if self.auth:
                response = requests.request(method, self.base_url+end_point+"?api_token="+self.auth, data=payload)
            else:
                response = requests.request(method, self.base_url+end_point, data=payload)
        except Exception as e:
            self.messages.append(str(e))
            return None
        else:
            return self.jsonDecoder.decode(response.text)