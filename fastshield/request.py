import json

class BaseRequest(object):
    def __init__(self, id_: int = None, 
                 timestamp: str = None, 
                 origin: str = None, 
                 host: str = None, 
                 request: str = None, 
                 body: str = None, 
                 method: str = None, 
                 headers: dict = None, 
                 threats: dict = None):
        self.id = id_
        self.timestamp = timestamp
        self.origin = origin
        self.host = host       
        self.request = request  
        self.body = body        
        self.method = method   
        self.headers = headers  
        self.threats = threats  

    def to_json(self):
        output = {}
        if self.request is not None and self.request != '':
            output['request'] = self.request
        if self.body is not None and self.body != '':
            output['body'] = self.body
        if self.headers is not None:
            for header, value in self.headers.items():
                output[header] = value
        return json.dumps(output)