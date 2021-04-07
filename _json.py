import json

class Json:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def get_json(self):
        # return json data
        json_file = open(self.file_path)
        data = json.load(json_file)
        return data
    
    def write_json(self, new_json):
        # Rewrite json settings and change settings variable
        with open(self.file_path, 'w') as json_file:
            json.dump(new_json, json_file)
